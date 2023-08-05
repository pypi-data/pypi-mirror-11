======================================
Python Flipkart Marketplace API Client
======================================

.. image:: https://img.shields.io/travis/fulfilio/python-flipkart-api.svg
        :target: https://travis-ci.org/fulfilio/python-flipkart-api

.. image:: https://img.shields.io/pypi/v/python-flipkart.svg
        :target: https://pypi.python.org/pypi/python-flipkart


Python Flipkart Marketplace API Client

* Free software: BSD license
* Documentation: https://python-flipkart.readthedocs.org.

Installing
----------

From PYPI:

.. code-block:: shell

   $ pip install python-flipkart

From source code (advanced users and for development):

.. code-block:: shell

   $ git clone https://github.com/fulfilio/python-flipkart-api.git
   $ cd python-flipkart-api
   $ python setup.py install


Example Usage
-------------

.. code-block:: python

    from flipkart import FlipkartAPI, Authentication

    auth = Authentication('app id', 'app secret', sandbox=True)
    token = auth.get_token_from_client_credentials()

    flipkart = FlipkartAPI(token['access_token'], sandbox=True, debug=True)
    orders = flipkart.search_orders()


Getting Access Token
````````````````````

If you have registered an application with your seller credentials and
would like to access resources in your account, you could use the
application id and secret alone to do so. The authentication helper in the
API gives you a convenient way to get tokens

.. code-block:: python

    from auth import Authentication

    auth = Authentication(
        '<application id>',
        '<application secret>',
        sandbox=True,           # If you are using sandbox
    )
    auth.get_token_from_client_credentials()

Features
--------

* TODO
