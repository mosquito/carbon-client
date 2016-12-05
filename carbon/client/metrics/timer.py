# encoding: utf-8
from time import time
from threading import RLock
from carbon.client.metrics.base import MeasurerBase, Metric


class StopWatch(object):
    __slots__ = '_lock', '_current'

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


class Timer(MeasurerBase):
    __slots__ = '_current',

    def __init__(self, cleanup=None):
        MeasurerBase.__init__(self, cleanup)
        self._current = None

    @classmethod
    def start(cls):
        watch = StopWatch()
        watch.start()
        return watch

    def stop(self, stop_watch):
        assert isinstance(stop_watch, StopWatch)
        self.add(Metric(name=self.name, value=stop_watch.stop()))
