edeposit.amqp.harvester
=======================

This module is used to collect public metadata about new books published by
selected czech publishers.

.. image:: /_static/relations.png
    :width: 600px

User guide / Uživatelská příručka
---------------------------------

.. toctree::
    :maxdepth: 1

    /uzivatelska_prirucka


Scripts
-------

.. toctree::
    :maxdepth: 1

    /api/harvester.edeposit_autoparser
    /scripts/edeposit_harvester_test

API
---
Whole module is divided into following parts:

Scrappers
+++++++++

:mod:`Scrappers <harvester.scrappers>` are used to download metadata from
publisher's webpages.

.. toctree::
    :maxdepth: 1

    /api/harvester.scrappers.ben_cz
    /api/harvester.scrappers.cpress_cz
    /api/harvester.scrappers.grada_cz
    /api/harvester.scrappers.zonerpress_cz

.. toctree::
    :maxdepth: 1

    /api/harvester.scrappers.utils

Filters
+++++++

:mod:`Filters <harvester.filters>` are then used to filter data from
:mod:`Scrappers <harvester.scrappers>`, before they are returned. This behavior
can be turned off by :attr:`~harvester.settings.USE_DUP_FILTER` and
:attr:`~harvester.settings.USE_ALEPH_FILTER` properties of
:mod:`~harvester.settings` submodule.

.. toctree::
    :maxdepth: 1

    /api/harvester.filters.aleph_filter
    /api/harvester.filters.dup_filter

Other parts
+++++++++++
There are also other, unrelated parts of this module, which are used to set
behavior, or to define representations of the data.

.. toctree::
    :maxdepth: 1

    /api/harvester.settings
    /api/harvester.structures

Autogenerator
^^^^^^^^^^^^^
Last submodule is :mod:`Autoparser <harvester.autoparser>`, which makes creating
new parsers easier.

.. toctree::
    :maxdepth: 1

    /api/harvester.autoparser.conf_reader
    /api/harvester.autoparser.vectors
    /api/harvester.autoparser.path_patterns
    /api/harvester.autoparser.utils
    /api/harvester.autoparser.generator

AMQP connection
---------------
AMQP communication is handled by the
`edeposit.amqp <http://edeposit-amqp.readthedocs.org>`_ module, specifically by
the ``edeposit_amqp_harvester.py`` script.

Source code
-----------
This project is released as opensource (GPL) and source codes can be found at
GitHub:

- https://github.com/edeposit/edeposit.amqp.harvester

Installation
++++++++++++
Module is hosted at `PYPI <https://pypi.python.org/pypi/edeposit.amqp.harvester>`_,
and can be easily installed using
`PIP <http://en.wikipedia.org/wiki/Pip_%28package_manager%29>`_:

::

    sudo pip install edeposit.amqp.harvester

Testing
-------
Almost every feature of the project is tested in unit/integration tests. You
can run this tests using provided ``run_tests.sh`` script, which can be found
in the root of the project.

Requirements
++++++++++++
This script expects that pytest_ is installed. In case you don't have it yet,
it can be easily installed using following command::

    pip install --user pytest

or for all users::

    sudo pip install pytest

.. _pytest: http://pytest.org/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`