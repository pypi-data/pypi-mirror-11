=========================
Deployment - installation
=========================

Watcher Metering Agent
======================

Installation (in production)
----------------------------

In order to install the watcher metering agent, you can install the related
packages using the following command:

.. code-block:: shell

    $ sudo apt-get install watcher-metering-agent

This installation will create the following elements:

- The ``/etc/watcher-metering`` folder, which contains all the configuration
  related to the watcher metering project:

    + The ``/etc/watcher-metering/agent.conf`` contains the agent configuration
      (no driver configuration by default)

- The ``/var/lib/watcher-metering`` folder contains the sources of the project
- The ``/opt/watcher_metering`` contains a virtualenv which isolates the Python
  dependencies of this project from the rest of the system

Please note that all these elements are owned by a created user named
``watcher-metering``.


Configuration
-------------

The agent configuration file (located at ``/etc/watcher-metering/agent.conf``)
contains all the explanations for each of its field. Please refer to these
notes to fully understand the role of each one of them.


Command
-------

To run the agent you can use the following command:

.. code-block:: shell

    $ watcher-metering-agent --config-file=/etc/watcher-metering/agent.conf

Or even:

.. code-block:: shell

    $ watcher-metering-agent --config-dir=/etc/watcher-metering

This alternative will automatically take into account any other file containing
some configuration related to the agent (useful for dynamically including
third-party driver configuration).

But if you want to learn more about all the options this command provides you
can still use the following to access its documentation:

.. code-block:: shell

    $ watcher-metering-agent --help


Watcher Metering Publisher
==========================

Installation (in production)
----------------------------

In order to install the watcher metering publisher, you can install the related
packages using the following command:

.. code-block:: shell

    $ sudo apt-get install watcher-metering-publisher

This installation will create the following elements:

- The ``/etc/watcher-metering`` folder, which contains all the configuration
  related to the watcher metering project:

    + The ``/etc/watcher-metering/publisher.conf`` contains the publisher
      configuration (no driver configuration by default)

- The ``/var/lib/watcher-metering`` folder contains the sources of the project
- The ``/opt/watcher_metering`` contains a virtualenv which isolates the Python
  dependencies of this project from the rest of the system

Please note that all these elements are owned by a created user named
``watcher-metering``.


Configuration
-------------

The publisher configuration file (located at
``/etc/watcher-metering/publisher.conf``) contains all the explanations for
each of its field. Please refer to these notes to fully understand the role
of each one of them.


Command
-------

To run the publisher you can use the following command:

.. code-block:: shell

    $ watcher-metering-publisher \
        --config-file=/etc/watcher-metering/publisher.conf

Or even:

.. code-block:: shell

    $ watcher-metering-publisher --config-dir=/etc/watcher-metering

This alternative will automatically take into account any other file containing
some configuration related to the publisher (useful for dynamically including
third-party driver configuration).

But if you want to learn more about all the options this command provides you
can still use the following to access its documentation:

.. code-block:: shell

    $ watcher-metering-publisher --help
