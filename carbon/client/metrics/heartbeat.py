# encoding: utf-8
from carbon.client.metrics.base import Metric, MeasurerBase


class HeartBeat(MeasurerBase):
    __slots__ = 'value',

    def __init__(self, cleanup=None):
        super(HeartBeat, self).__init__(cleanup)
        self.value = 0
        self.add(Metric(name='heartbeat', value=self.value))

    def on_send(self):
        self.value += 1
        self._values.clear()
        self.add(Metric(name='heartbeat', value=self.value))
