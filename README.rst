Carbon Client
=============

.. image:: https://travis-ci.org/mosquito/carbon-client.svg?branch=master
    :target: https://travis-ci.org/mosquito/carbon-client

.. image:: https://img.shields.io/pypi/v/carbon-client.svg
    :target: https://pypi.python.org/pypi/carbon-client/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/carbon-client.svg
    :target: https://pypi.python.org/pypi/carbon-client/

.. image:: https://img.shields.io/pypi/pyversions/carbon-client.svg
    :target: https://pypi.python.org/pypi/carbon-client/

.. image:: https://img.shields.io/pypi/l/carbon-client.svg
    :target: https://pypi.python.org/pypi/carbon-client/


Client for sending metrics into carbon server

Initialization
++++++++++++++

By default carbon-client creates a client based on os.environ variables:

* CARBON_HOST - Contains one or many endpoints (e.g "127.0.0.1:2003, 10.2.1.0:2003")
* CARBON_NS - it's a namespace for sending metrics (e.g. "carbon.coal-service")

Actually you can configure this by hands.

Example
+++++++

The simple test :

.. code-block:: python

    # You should set ENV variables CARBON_HOST and CARBON_NS
    # CARBON_HOST might contains multiple destinations (comma separated)
    from time import sleep
    from carbon.client import stat
    from carbon.client.extras import SimpleCounter

    # Will be pended one or two metrics
    # carbon_client.counter_ok
    # carbon_client.counter_fail - if exception will be raised
    # carbon_client is namespace by default.
    with SimpleCounter("counter"):
        sleep(1)

    # Will be pended one metric
    # carbon_client.timer_ok - if exception will be raised
    # carbon_client.timer_fail - if exception will be raised
    # carbon_client is namespace by default.
    with SimpleTimer("timer"):
        sleep(1)

    # Will be pended n metric
    # carbon_client.collector
    # carbon_client is namespace by default.
    with SimpleCollector("collector") as collector:
        collector.add(123)
        collector.add(122)
        collector.add(-10)

    # all metrics will sent.
    stat.send()


The advanced test :

.. code-block:: python

    from time import sleep
    from carbon.client import UDPClient
    from carbon.client.extras import SimpleCounter, SimpleTimer, SimpleCollector

    # Will be send to multiple destinations
    client = UDPClient("127.0.0.1, 191.168.1.11:2003", "test")

    with SimpleCounter("counter", client):
        sleep(1)

    with SimpleTimer("timer", client):
        sleep(1)

    with SimpleCollector("collector", client) as collector:
        collector.add(123)

    client.send()


Another test :

.. code-block:: python

    from time import sleep
    from carbon.client import stat
    from carbon.client import metrics

    # Counter
    stat['counter'] = metrics.Counter
    stat['counter'].inc(1)
    sleep(1)
    stat['counter'].dec(1)

    # Timer
    stat['timer'] = metrics.Timer
    stop_watch = stat['timer'].start()
    sleep(1)
    stat['timer'].stop(stop_watch)

    # Collector
    stat['collector'] = metrics.Collector
    stat['collector'].add(1)
    sleep(1)
    stat['collector'].add(2)
    sleep(1)
    stat['collector'].add(3)
    sleep(1)
    stat['collector'].add(-10)

    stat.send()


