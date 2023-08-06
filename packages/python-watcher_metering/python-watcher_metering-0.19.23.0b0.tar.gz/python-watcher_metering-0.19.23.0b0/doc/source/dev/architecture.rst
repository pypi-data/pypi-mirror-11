=============================
Watcher metering architecture
=============================

Architecture
============

.. figure:: architecture.png

   Watcher metering overall architecture


Agent
=====

The watcher metering agent registers a given set of metrics drivers which are
collecting the metrics from the host (or elsewhere).

These drivers can be registered via a third party library as long as they
follow a set of constraints as explained in the ``README.md`` file.

The way a metrics driver works is the following:

* It collects one or more metric(s) (or Measurement)
* It notifies the agent of the collected metric
* The agent sends it to the publisher

In order for the agent to be able to connect to the publisher, 2 options can
be used:

- Disable the use of the nanoconfig service and by setting the publisher
  endpoint
- Enable the use of the nanoconfig service by setting the related nanoconfig
  profile name and endpoint


Publisher
=========

The publisher is responsible for gathering metrics from multiple sources/hosts
before channeling them to the right store (with or without some preprocessing).

The publisher workflow is the following:

* It loads the configuration which defines the store to use (Riemann, ...)
* It receives a measurement from a host
* The measurement is pre-processed to match the format the store requires
* The formatted metric is then sent to the store


Nanoconfig server
=================

The nanoconfig server is a separate element that does not belong to this
project although it is advised to use it.

Please refer to the associated documentation in order get more details about
the advantages it offers.
