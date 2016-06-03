OneSignal Python SDK
=====================

A Python SDK for OneSignal (https://onesignal.com/). Documentation for OneSignal API is available at
https://documentation.onesignal.com/docs/server-api-overview.

Obtaining User Rest API key and App REST API key
-------------------------------------------------

See details here https://documentation.onesignal.com/docs/server-api-overview

Install from pip
------------------------

   > pip install onesignal 

Setup for develop
------

You can install the package by running

::

    > python setup.py install

Once installed, to get started, you can do:

::

   from onesignal import OneSignal
   one_signal =  OneSignal(USER_AUTH_KEY, YOUR_APP_ID)
   one_signal.get_players(REST_API_KEY)
   
   
USER_AUTH_KEY: Your e-mail -> Api Keys -> User Auth Key

YOUR_APP_ID: Your App -> App settings -> Keys and Id

REST_API_KEY: Your App -> App settings -> Keys and Id

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

