seamless
========

seamless provides an easy way to obtain an https session token via ssh.
It automates creation of user accounts and manages their *authorized_keys* as well as session token creation via forced ssh commands.
The authentication flow is as follows:

* A client connects to `seamless-realm@seamless-host` via ssh and authenticates with a public key.
  The key is restricted to only execute the token creation command of the seamless binary.
  The seamless command returns session token that is signed with a secret specific to `seamless-realm`.

  .. code::

      $ ssh -T seamless-realm@seamless-host
      username.VgfAwA.v-xKIZh3qYawqcm2RRh4q-LPfVE

* The client sends the obtained token in the HTTP *Authorization* header of its requests to `protected-app`.
  The app uses the shared secret to validate the token.

  .. code:: http

     GET / HTTP/1.1
     Host: protected-app
     Authorization: seamless username.VgfAwA.v-xKIZh3qYawqcm2RRh4q-LPfVE


Installation
-------------

From a deb package::

    $ wget https://github.com/emulbreh/seamless/releases/download/v0.1.0/seamless_0.1.0_amd64.deb
    $ sudo dpkg -i seamless_0.1.0_amd64.deb

As Python package::

    $ pip install seamless


Setting up a seamless realm
---------------------------

A seamless realm is a user account on `seamless-host`. The creation and management of *authorized_keys* of these accounts is handled by seamless.

.. code:: bash

    $ sudo seamless init seamless-realm
    $ sudo seamless add seamless-realm /path/to/public/key --user username

A user with this public key is now able to get tokens via ssh:

.. code::

    $ ssh -T seamless-realm@seamless-host
    username.VgfOLQ.EB6NTfXiyv7dWSKUMQJ38JXa5aw

or from Python

.. code:: python

    >>> import seamless
    >>> seamless.get_token('seamless-realm@seamless-host')
    'username.VgfOBA.dRBDY5EUmQvhB8OnqPDWlC1tml4'


Protecting a webservice with WSGI middleware
---------------------------------------------

seamless ships with WSGI middleware that verifies that a valid seamless token is passed via the Authorization header.

.. code:: python

    from seamless.wsgi import SeamlessMiddleware
    
    app = ...

    app = SeamlessMiddleware(app, max_age=60, secret='...')


Requests without a valid *Authorization* header will be rejected with a 401 response.


Making requests to such a protected app is made easy with an auth plugin for `requests`_:

.. code:: python

    import requests
    from seamless.requests import SeamlessAuth
    
    session = requests.Session()
    session.auth = SeamlessAuth('name@seamless-host')

    session.get('http://protected-app/')


The token obtained from `seamless-host` is cached. 
It will be be automatically refreshed when it expires, and the failing request retried.


Caveats
--------

* If token validation is performed on a different host than token creation, clock skew may result in tokens that expire too early or too late.


.. _requests: http://docs.python-requests.org/

