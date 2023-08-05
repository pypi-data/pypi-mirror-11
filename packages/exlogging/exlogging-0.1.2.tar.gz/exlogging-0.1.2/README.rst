.. image:: https://travis-ci.org/narusemotoki/exlogging.svg?branch=master
    :target: https://travis-ci.org/narusemotoki/exlogging


exlogging
#########

Supports to setup python standard logging package.

How to use
==========

The way to use exlogging almost same with Python standard logging. First, you can call init function with config dict. After that, completely same with logging.

.. code-block:: python

    import exlogging

    config = {
        'file': {
            'level': 'debug',
            'filename': '/path/to/logfile'
        }
        # You can conbinate with other handlers.
    }

    # If you call init function without second parameter(name), exlogging setup root logger.
    exlogging.init(config)

    bloging.debug("Hello exlogging!")

    # If you want to use named logger, you can call init function with config and name
    exlogging.init(config, 'example')

    # You can access named logger via getLogger function
    example_logger = exlogging.getLogger('example')
    example_logger.info('You named logger')

exlogging or getLogger response object has `debug`, `info`, `warning`, `error`, `exception` and `critical` functions. If you pass  'warning` as `level` in config dict to init function, when you call `warning`, `error`, `critical` or `critical`, it will be logged, but when you call `info` or `debug` function, it is not logged.

Logger is common in your application, so you can setup logger via exlogging at your application entry point, you can use the logger anywhere.

Handlers
========

Common settings
---------------

All handlers have level and format.

Levels
++++++

   * critical
   * error
   * warning
   * info
   * debug
   * notset

Format
++++++

If you don't pass log_format here, exlogging uses this format: %(levelname)s %(name)s - %(asctime)s - File: %(pathname)s - Line: %(lineno)d - Func: %(funcName)s Message: %(message)s

See https://docs.python.org/3.5/library/logging.html#logrecord-attributes

FileHandler
-----------

When you call logger function, record the message in file at filename.

.. code-block:: python

    'file': {
        'level': str, # requirement
        'format': str, # optional
        'filename': str # requirement
    }

RotatingFileHandler
-------------------

When you call logger function, record the message in file at filename.

.. code-block:: python

    'file': {
        'level': str, # requirement
        'format': str, # optional
        'filename': str, # requirement
        'max_bytes': int, # optional
        'backup_count': int # optional
    }

EmailHandler
------------

When you call logger function, send an email with the message.

.. code-block:: python

    'email': {
        'level': str, # requirement
        'format': str, # optional
        'smtp_host': str, # requirement
        'smtp_port': int, # requirement
        'email_from': str, # requirement
        'email_to': str, # requirement
        'email_subject': str, # requirement
        'smtp_username': str, # requirement
        'smtp_password': str # requirement
    }
