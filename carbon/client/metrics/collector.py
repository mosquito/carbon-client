# encoding: utf-8
from carbon.client.metrics.base import MeasurerBase, Metric


class Collector(MeasurerBase):

    def add(self, value):
        self._values.add(Metric(name=self.name, value=value))
