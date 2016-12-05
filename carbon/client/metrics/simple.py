# encoding: utf-8
from carbon.client.metrics.base import Metric, MetricTypeBase


class Counter(MetricTypeBase):

    def __init__(self, cleanup=None):
        MetricTypeBase.__init__(self, cleanup)
        self.value = 0

    def add(self, value):
        self.value += value
        self._values.add(Metric(name=self.name, value=self.value))

    def inc(self, n=1):
        return self.add(n)

    def dec(self, n=1):
        return self.add(-n)
