from base64 import b64encode
import calendar
from datetime import datetime
from functools import partial
import logging
import json
from hashlib import sha512
import hmac
import requests

from .account import Account, Transaction, RecoveryTransaction

logger = logging.getLogger('ambisafe')


class AmbisafeError(Exception):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    def __str__(self):
        return self.message


class ClientError(AmbisafeError):
    def __repr__(self):
        return '<AmbisafeClientError error="{}" message="{}">'.format(self.error, self.message)


class ServerError(AmbisafeError):
    def __repr__(self):
        return '<AmbisafeClientError error="{}" message="{}">'.format(self.error, self.message)


class Client(object):
    def __init__(self, ambisafe_server, secret, api_key, api_secret):
        self.ambisafe_server = ambisafe_server
        self.secret = secret
        self.api_key = api_key
        self.api_secret = api_secret

    def create_account(self, account_id, user_container, operator_container,
                       security_schema='Wallet4', currency='BTC'):
        logger.debug('Creating account for containers: user: {}, operator: {}'
                     .format(user_container, operator_container))
        containers = {
            "USER": user_container.__dict__,
            "OPERATOR": operator_container.__dict__
        }
        return Account.from_server_response(self.make_request('POST', '/accounts', json.dumps({
            'id': account_id,
            'currency': currency,
            'security_schema': security_schema,
            'containers': containers,
        })))

    def update_account(self, account_id, user_container, operator_container,
                       security_schema='Wallet4', currency='BTC', regenerate_server_container=False):
        containers = {
            "USER": user_container.__dict__,
            "OPERATOR": operator_container.__dict__
        }
        return Account.from_server_response(self.make_request('PUT', '/accounts', json.dumps({
            'id': account_id,
            'currency': currency,
            'security_schema': security_schema,
            'containers': containers,
            'regenerate_server_container': regenerate_server_container,
        })))

    def get_balance(self, account_id, currency='BTC'):
        return float(
            self.make_request('GET', '/balances/{currency}/{external_id}'
                              .format(currency=currency, external_id=account_id))['balance']
        )

    def get_account(self, account_id, currency='BTC'):
        return Account.from_server_response(
            self.make_request('GET', '/accounts/{external_id}/{currency}'
                              .format(external_id=account_id, currency=currency))
        )

    def build_transaction(self, account_id, currency, destination, amount):
        body = {
            "destination": destination,
            "amount": amount
        }
        return Transaction(**self.make_request('POST', '/transactions/build/{external_id}/{currency}'
                                               .format(external_id=account_id, currency=currency),
                                               body=json.dumps(body)))

    def submit(self, account_id, transaction, currency):
        return self.make_request('POST', '/transactions/submit/{external_id}/{currency}'
                                 .format(external_id=account_id, currency=currency),
                                 body=transaction.to_json())

    def cosign(self, transaction, account_id, currency='BTC'):
        account = self.get_account(account_id, currency)
        container = account.operator_container
        private_key = container.get_private_key(self.secret)
        sign = partial(container.sign, private_key=private_key)
        transaction.operator_signatures = map(sign, transaction.sighashes)
        return transaction

    def cosign_and_submit(self, transaction, account_id, currency='BTC'):
        transaction = self.cosign(transaction, account_id, currency)
        return self.submit(account_id, transaction, currency)

    def build_recovery_transaction(self, account_id, currency, old_address):
        response = self.make_request(
            'POST',
            '/transactions/build_recovery/{external_id}/{currency}/{address}'
            .format(external_id=account_id, currency=currency, address=old_address)
        )
        logger.debug('response: {}'.format(response))
        return RecoveryTransaction(response['operator'], response['recovery_transaction'])

    def cosign_and_recovery(self, transaction, account_id, currency='BTC'):
        transaction = self.cosign(transaction, account_id, currency)
        return self.submit(account_id, transaction, currency)

    def make_request(self, method, uri, body=None):
        url = self.ambisafe_server + uri
        utctime = datetime.utcnow()
        nonce = int(calendar.timegm(utctime.timetuple()) * 10 ** 3
                    + utctime.microsecond * 10 ** -3)
        message = "{}\n{}\n{}\n".format(nonce, method, url)
        if body:
            message += body
        digest = hmac.new(self.api_secret, msg=message, digestmod=sha512)
        signature = b64encode(digest.digest()).replace('\n', '')
        headers = {
            'API-key': self.api_key,
            'signature': signature,
            'timestamp': nonce,
            'Accept': 'application/json'
        }
        if method in ['POST', 'PUT']:
            headers['Content-Type'] = 'application/json'
        logger.debug('Request to ambisafe KeyServer: method: {}, url: "{}", headers: {}, data: {}'
                     .format(method, url, headers, body))
        response = requests.request(method, url, headers=headers, data=body)
        logger.debug('Response from ambisafe KeyServer: status: {}, text: {}'
                     .format(response.status_code, response.text))
        try:
            response_data = response.json()
        except ValueError, e:
            # ValueError is parent of JSONDecodeError
            raise ServerError(e.message, '')

        if not response.ok:
            if 400 <= response.status_code < 500:
                raise ClientError(response_data['message'], response_data['error'])
            elif 500 <= response.status_code < 600:
                raise ServerError(response_data['message'], response_data['error'])

        return response_data
