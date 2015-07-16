#!/usr/bin/env python
# encoding: utf-8
from carbon.client.metrics.base import MetricTypeBase, Metric


class Collector(MetricTypeBase):

    def add(self, value):
        self._values.add(Metric(name=self.name, value=value))
