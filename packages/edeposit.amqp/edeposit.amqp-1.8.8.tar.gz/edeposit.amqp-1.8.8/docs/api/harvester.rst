edeposit_amqp_harvester.py script
=================================

.. automodule:: edeposit_amqp_harvester
    :members:
    :undoc-members:
    :show-inheritance:

Help
----
::

    ./edeposit_amqp_harvester.py 
    usage: edeposit_amqp_harvester.py [-h] [-u] [-r]

    This script is used to send data from edeposit.amqp.harvester to AMQP queue.

    optional arguments:
      -h, --help      show this help message and exit
      -u, --unittest  Perform unittest.
      -r, --harvest   Harvest all data and send them to harvester queue.


Example usage::

    $ ./edeposit_amqp_harvester.py start --harvest

Which will harvest all possible sources of publications and send them to
AMQP, or::

    $ ./edeposit_amqp_harvester.py --unittest

Which will perform unittests and send results over AQMP to proper exchange.
