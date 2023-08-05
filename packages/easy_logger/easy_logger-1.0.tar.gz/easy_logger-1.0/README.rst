Easy Logger
===========

A python package for logging easily.

Installation
------------

::

    $ pip install easy_logger

Usage
-----

.. code:: python

    from easy_logger import Logger

    logger = Logger().get_logger(__name__)
    logger.info('logger')

API
---

.. code:: python

    class Logger(object):

        def get_logger(name):
            """The same as get_stream_logger."""
            pass

        def get_stream_logger(name):
            """Get logger which has add streamHandler. Output log message to stream.

            :param str name: logger name
            """
            pass

        def get_file_logger(name, filepath):
            """Get logger which has add fileHandler. Output log message to specify file.

            :param str name: logger name
            :param str filepath: the log file path
            """
            pass

        def get_both_logger(name, filepath):
            """Get logger which has both add streamHandler and fileHandler.
            Output log message to stream and specify file.

            :param str name: logger name
            :param str filepath: the log file path
            """
            pass


Better
------

If you feel anything wrong, feedbacks or pull requests are welcomed.
