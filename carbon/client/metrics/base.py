#!/usr/bin/env python
# encoding: utf-8
from time import time


class Metric(object):

    def __init__(self, name, value, ts=None):
        if not ts:
            ts = time()

        self.__ts = ts
        self.__name = name
        self.__value = value

    def __str__(self):
        return "%s %s %.6f" % (self.__name, self.__value, self.__ts)

    def __hash__(self):
        return hash(self.__str__())


class MetricTypeBase(object):

    def __init__(self, cleanup=None):
        self.name = None
        self._cleanup = cleanup
        self._values = set([])

    def on_create(self):
        return

    def add(self, metric):
        assert isinstance(metric, Metric), "It's not a Metric"
        self._values.add(metric)

    def on_delete(self):
        if self._cleanup:
            self._cleanup()

    def on_send(self):
        self._values = set([])

    def str(self, ns):
        return "\n".join(map(lambda x: "%s.%s" % (ns, x) if x else '', list(self._values)))
