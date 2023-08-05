===============
199Fix
===============


199Fix provides a logging handler to push exceptions and other errors
to https://199fix.com/. Django 1.4, 1.5 and 1.6 are supported on Python 2.6,
2.7, 3.2 and 3.3.


Installation
============

Installation with ``pip``:
::

    $ pip install 199fix



Settings
========

``level`` (built-in setting)
Change the ``level`` to ``'ERROR'`` to disable logging of 404 error messages.

``api_key`` (required)
    API key provided by the exception handler system.


Contributing
============
* Fork the repository on GitHub and start hacking.
* Run the tests.
* Send a pull request with your changes.
