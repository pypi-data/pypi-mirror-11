edeposit_amqp_calibredaemon.py script
=====================================

.. automodule:: edeposit_amqp_calibredaemon

Help
----
::

    $ ./edeposit_amqp_calibredaemon.py -h
    usage: edeposit_amqp_calibredaemon.py start/stop/restart [-f] FN

    Calibre daemon, providing AMQP interface for edeposit.amqp.calibre.

    positional arguments:
      start/stop/restart  Start/stop/restart the daemon.

    optional arguments:
      -h, --help          show this help message and exit
      -f, --foreground    Run at foreground, not as daemon. If not set, script is
                          will run at background as unix daemon.


Example usage::

    $ ./edeposit_amqp_calibredaemon.py start 
    started with pid 10005

or::

    $ ./edeposit_amqp_calibredaemon.py start --foreground

In this case, the script runs as normal program, and it is not daemonized.

Stopping::

    $ ./edeposit_amqp_calibredaemon.py stop
    No handlers could be found for logger "pika.adapters.base_connection"

Don't be concerned by warnings when stopping the daemon, it is just something
that out communication library does.