edeposit_amqp_ftp_monitord.py script
====================================

.. automodule:: edeposit_amqp_ftp_managerd

Help
----
::

    $ ./edeposit_amqp_ftp_managerd.py -h
    usage: edeposit_amqp_ftp_managerd.py start/stop/restart [-f] FN

    ProFTPD user manager. This script allows you to add/ remove/change users in
    ProFTPD server over AMQP API.

    positional arguments:
      start/stop/restart  Start/stop/restart the daemon.

    optional arguments:
      -h, --help          show this help message and exit
      -f, --foreground    Run at foreground, not as daemon. If not set, script is
                          will run at background as unix daemon


Example usage::

    ./edeposit_amqp_ftp_managerd.py start
    started with pid 5469

or::

    $ ./edeposit_amqp_ftp_managerd.py start --foreground

In this case, the script runs as normal program, and it is not daemonized.

Stopping::
    
    $ ./edeposit_amqp_ftp_managerd.py stop
    No handlers could be found for logger "pika.adapters.base_connection"

Don't be concerned by warnings when stopping the daemon, it is just something
that out communication library does.