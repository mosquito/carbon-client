# encoding: utf-8
from time import time
from abc import abstractmethod


class Metric(object):
    __slots__ = '__value', '__ts', '__name'

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


class MeasurerAbstract(object):
    @abstractmethod
    def __init__(self, cleanup=None):
        raise NotImplementedError

    @abstractmethod
    def on_create(self):
        raise NotImplementedError

    @abstractmethod
    def add(self, metric):
        raise NotImplementedError

    @abstractmethod
    def on_delete(self):
        raise NotImplementedError

    @abstractmethod
    def on_send(self):
        raise NotImplementedError

    @abstractmethod
    def str(self, ns):
        raise NotImplementedError


class MeasurerBase(MeasurerAbstract):
    __slots__ = '_value', '_cleanup', '_values', 'name'

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


MetricTypeBase = MeasurerBase
