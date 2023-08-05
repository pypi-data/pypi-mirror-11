Easy Logger
===========

A python package for using logger easily.

Installation
------------

TODO

Usage
-----

.. code:: python

    from elogger import Logger

    logger = Logger.get_stream_logger()
    logger.info('logger')

API
---

.. code:: python

    class Logger(object):

        def init_config(self, level=logging.INFO):
            """Init logging baseConfig

            :param int level: logging level
            """
            pass

        def get_stream_logger(name):
            """Get logger which has add streamHandler. Output log message to stream.

            :param str name: logger name
            """
            pass

        def get_file_logger(name, filepath):
            """Get logger which has add fileHandler. Output log message to specify file.

            :param str name: logger name
            """
            pass

        def get_both_logger(name, filepath):
            """Get logger which has both add streamHandler and fileHandler.
            Output log message to stream and specify file.

            :param str name: logger name
            """
            pass


Better
------

If you feel anything wrong, feedbacks or pull requests are welcomed.
