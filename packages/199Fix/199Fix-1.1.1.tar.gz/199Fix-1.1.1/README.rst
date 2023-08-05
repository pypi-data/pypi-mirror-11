===============
199Fix
===============

199Fix provides a logging handler to push exceptions and other errors to https://199fix.com/. 

Installation
============

Installation with ``pip``:
::

    $ pip install 199fix


Get an API Key here https://199fix.com/signup/

Add ``'199fix.handlers.I99FixHandler'`` as a logging handler:
::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            '199fix': {
                'level': 'INFO',
                'class': '199fix.handlers.I99FixHandler',
                'filters': ['require_debug_false'],
                'api_key': '[your-api-key]',
                'env_name': 'production',
            }
        },
        'loggers': {
            'django': {
                'handlers': ['199fix'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    }

Settings
========

``level`` (built-in setting)
    Change the ``level`` to ``'ERROR'`` to disable logging of 404 error messages.

``api_key`` (required)
    API key , Get one here https://199fix.com/.

``env_name`` (required)
    Name of the environment (e.g. production, develop, testing)

Contributing
============
* Fork the repository on GitHub and start hacking.
* Run the tests.
* Send a pull request with your changes.
