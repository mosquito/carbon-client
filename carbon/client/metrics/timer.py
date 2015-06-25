#!/usr/bin/env python
# encoding: utf-8
from time import time
from threading import RLock

from carbon.client.metrics.base import MetricTypeBase, Metric


class Timer(MetricTypeBase):

    def __init__(self, cleanup=None):
        MetricTypeBase.__init__(self, cleanup)
        self._current = None
        self._lock = RLock()

    def __enter__(self):
        self.start(False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self, restart=True):
        with self._lock:
            if not restart and self._current:
                raise RuntimeError('StopWatch are running')
            self._current = time()

    def stop(self):
        if self._current is None:
            return

        with self._lock:
            delta = time() - self._current
            self.add(Metric(name=self.name, value=delta))
            self._current = None
