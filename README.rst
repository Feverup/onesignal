OneSignal Python SDK
=====================

A Python SDK for OneSignal (https://onesignal.com/). Documentation for OneSignal API is available at
https://documentation.onesignal.com/docs/server-api-overview.

Obtaining User Rest API key and App REST API key
-------------------------------------------------

See details here https://documentation.onesignal.com/docs/server-api-overview

Installing dependencies
------------------------

Create a VirtualEnv and install dependencies from requirements.txt by running (from the root):

::

   > pip install -r requirements.txt

Setup
------

You can install the package by running

::

    > python setup.py install

Once installed, to get started, you can do:

::

   from onesignal import OneSignal
   one_signal =  OneSignal(YOUR_APP_ID, AUTH_TOKEN_HERE)
   one_signal.get_players(your_basic_auth_key)

Tests
------

Tests are located under /tests and these also kind of show some examples on how to use the library.

Running tests
---------------

Go to this directory /tests and then run

::

    > py.test

Contributors
-------------

- Zohaib Ijaz <zohaibijaz.qc@gmail.com>
- Waqas Younas <waqas.younas@gmail.com>

