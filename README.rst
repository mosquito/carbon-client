Carbon Client
=============

Client for sending metrics into carbon server

Example
+++++++

The simple test ::

    # You should set ENV variables CARBON_HOST and CARBON_NS
    # CARBON_HOST might contains multiple destinations (comma separated)
    from time import sleep
    from carbon.client import stat
    from carmon.client.extras import SimpleCounter

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


The advanced test ::

    from time import sleep
    from carbon.client import UDPClient
    from carmon.client.extras import SimpleCounter, SimpleTimer, SimlpeCollector

    # Will be send to multiple destinations
    client = UDPClient("127.0.0.1, 191.168.1.11:2003", "test")

    with SimpleCounter("counter", client):
        sleep(1)

    with SimpleTimer("timer", client):
        sleep(1)

    with SimpleCollector("collector", client) as collector:
        collector.add(123)

    client.send()


Another test ::

    from time import sleep
    from carmon.client import stat
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


