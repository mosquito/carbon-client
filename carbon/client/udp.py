#!/usr/bin/env python
# encoding: utf-8
from functools import wraps
import re
from socket import socket, AF_INET, SOCK_DGRAM

from . import metrics
from carbon.client.metrics.base import MetricTypeBase


class LockFlag(object):

    def __init__(self):
        self.__flag = False

    def __call__(self, func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if self.__flag:
                return

            self.__flag = True
            try:
                func(*args, **kwargs)
            finally:
                self.__flag = False

        return wrap


class UDPClient(object):
    LOCK = LockFlag()
    DEFAULT = metrics.Counter

    def __init__(self, host='127.0.0.1', port=2003, ns='carbonate'):
        assert isinstance(port, (int, long))
        self.__host = host
        self.__port = port
        self.__ns = ns
        self.__socket = None
        self.__sending = False
        self.__metrics = {}
        self.__add_metric(metrics.HeartBeat)

    @property
    def host(self):
        return self.__host

    @host.setter
    @LOCK
    def host(self, host):
        self.socket.close()
        self.__socket = None
        self.__host = host

    @property
    def port(self):
        return self.__port

    @port.setter
    @LOCK
    def port(self, port):
        assert isinstance(port, (int, long))
        self.socket.close()
        self.__socket = None
        self.__port = port

    @property
    def ns(self):
        return self.__ns

    @ns.setter
    def ns(self, ns):
        assert not ns.startswith('.'), "NameSpace mustn't starts with the dot."
        assert not ns.endswith('.'), "NameSpace mustn't ends with the dot."
        assert re.match('^[\w\d\._\-]+$', ns) is not None, "NameSpace must contain special chars (except '_', '-')"
        assert not list(filter(lambda x: not x, ns.split('.'))), "Namespace must contain chars after dots."
        self.__ns = ns

    def __add_metric(self, metric, name=None):
        metric_instance = metric(lambda x: self.__metrics.remove(x))
        metric_instance.name = name
        metric_instance.on_create()
        self.__metrics[name] = metric_instance

    def __contains__(self, item):
        return item in self.__metrics

    @property
    def socket(self):
        if not self.__socket:
            self.__socket = socket(AF_INET, SOCK_DGRAM)
        return self.__socket

    def __getitem__(self, item):
        if item not in self.__metrics:
            self.__add_metric(self.DEFAULT, item)
        return self.__metrics[item]

    def __setitem__(self, key, value):
        assert issubclass(value, MetricTypeBase), "Unknown metric type"
        assert isinstance(key, basestring)
        self.__add_metric(value, key)

    @LOCK
    def send(self):
        metric_set = list(self.__metrics.values())
        self.socket.sendto("\n".join(
            filter(lambda x: x, map(lambda x: x.str(self.__ns), metric_set))),
            (self.__host, self.__port)
        )

        map(lambda m: m.on_send(), metric_set)

    def close(self):
        self.socket.close()
