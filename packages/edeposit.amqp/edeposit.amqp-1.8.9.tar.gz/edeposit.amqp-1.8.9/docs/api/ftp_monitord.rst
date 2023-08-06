edeposit_amqp_ftp_monitord.py script
====================================

.. automodule:: edeposit_amqp_ftp_monitord
    :members:
    :undoc-members:
    :show-inheritance:

Help
----
::

    ./edeposit_amqp_ftp_monitord.py -h
    usage: edeposit_amqp_ftp_monitord.py start/stop/restart [-f] FN

    ProFTPD log monitor. This script reacts to preprogrammed events from FTP
    server.

    positional arguments:
      start/stop/restart    Start/stop/restart the daemon.

    optional arguments:
      -h, --help            show this help message and exit
      -f, --foreground      Run at foreground, not as daemon. If not set, script
                            is will run at background as unix daemon.
      -n FILENAME, --filename FILENAME
                            Path to the log file (usually
                            /var/log/proftpd/extended.log).


Example usage::

    $ ./edeposit_amqp_ftp_monitord.py start --filename /var/log/proftpd/extended.log 
    Monitoring file '/var/log/proftpd/extended.log'.
    started with pid 1633

or::

    $ ./edeposit_amqp_ftp_monitord.py start --filename /var/log/proftpd/extended.log --foreground
    Monitoring file '/var/log/proftpd/extended.log'.

In this case, the script runs as normal program, and it is not daemonized.

Stopping::
    
    $ ./edeposit_amqp_ftp_monitord.py stop
    WARNING:pika.adapters.base_connection:Unknown state on disconnect: 0
    WARNING:pika.adapters.base_connection:Unknown state on disconnect: 0

Don't be concerned by warnings when stopping the daemon, it is just something
that out communication library does.