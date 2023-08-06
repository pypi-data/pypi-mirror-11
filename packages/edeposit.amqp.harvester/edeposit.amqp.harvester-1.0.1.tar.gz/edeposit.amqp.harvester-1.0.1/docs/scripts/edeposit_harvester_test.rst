edeposit_harvester_test.py
==========================

Test script used to show output of all downloaded data.

Help::

    $ ./edeposit_harvester_test.py -h
    usage: edeposit_harvester_test.py [-h] [-u] [-r] [-d]

    This script is used to read data from edeposit.amqp.harvester and print it to
    stdout.

    optional arguments:
      -h, --help        show this help message and exit
      -u, --unittest    Perform unittest.
      -r, --harvest     Harvest all data and send them to harvester queue.
      -d, --dup-filter  Filter duplicate results. Default False.


API
---

.. automodule:: edeposit_harvester_test
    :members:
    :undoc-members:
    :private-members:
