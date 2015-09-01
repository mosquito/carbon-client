#!/usr/bin/env python
# encoding: utf-8
from time import time
from threading import RLock
from .base import MetricTypeBase, Metric


class StopWatch(object):
    def __init__(self):
        self._lock = RLock()
        self._current = None

    def start(self):
        with self._lock:
            self._current = time()

    def stop(self):
        assert self._current, "StopWatch not running"
        with self._lock:
            return time() - self._current


class Timer(MetricTypeBase):
    def __init__(self, cleanup=None):
        MetricTypeBase.__init__(self, cleanup)
        self._current = None

    @classmethod
    def start(cls):
        watch = StopWatch()
        watch.start()
        return watch

    def stop(self, stop_watch):
        assert isinstance(stop_watch, StopWatch)
        self.add(Metric(name=self.name, value=stop_watch.stop()))
