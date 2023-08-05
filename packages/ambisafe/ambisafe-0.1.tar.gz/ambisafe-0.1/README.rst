Ambisafe client
===============

Install
-------

Use pip

::

    pip install ambisafe

Usage
-----

Create client
~~~~~~~~~~~~~

Import all and create client

::

    from ambisafe.client import Client

    client = Client(ambisafe_server_url, secret, api_key, api_secret)

Create account
~~~~~~~~~~~~~~

Generate operator container using secret and create user container from
public\_key, data (encrypted private key), iv and salt

::

    from ambisafe.account import Container

    operator_container = Container.generate(client.secret)
    user_container = Container(public_key, data, iv, salt)

Create account for security schema "Wallet4" and "BTC" currency

::

    account = client.create_account(account_id, user_container, operator_container, 'Wallet4', 'BTC')

Update account
~~~~~~~~~~~~~~

Create new containers and update account

::

    account = client.update_account(account_id, user_container, operator_container, 'Wallet4', 'BTC')

Get balance
~~~~~~~~~~~

Get balance in float

::

    balance = client.get_balance(account_id, 'BTC')

Get account
~~~~~~~~~~~

::

    account = client.get_account(account_id, 'BTC')

Make payment
~~~~~~~~~~~~

Build transaction

::

    transaction = client.build_transaction(account_id, 'BTC', address, amount)

Sign this transaction by user, then sing by operator and submit it

::

    transaction = client.cosign(transaction, account_id, 'BTC')
    client.submit(account_id, transaction, 'BTC')

    # or

    result = client.cosign_and_submit(transaction, account_id, 'BTC')

Disclaimer
----------

The library still in BETA. There can be changes without backward
compatibility.
