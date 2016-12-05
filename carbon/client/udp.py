# encoding: utf-8
import re
import logging

from functools import wraps
from socket import socket, AF_INET, SOCK_DGRAM

from . import metrics
from .metrics.base import MeasurerBase


log = logging.getLogger('carbon.client.udp')


try:
    basestring
except NameError:
    basestring = str


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

    __slots__ = '__host', '__ns', '__socket', '__endpoints', '__sending', '__metrics'

    def __init__(self, hosts='127.0.0.1', ns='carbon.client'):
        self.__host = hosts
        self.__ns = ns
        self.__socket = None

        self.__sending = False
        self.__metrics = {}
        self.__endpoints = self._parse_hosts(hosts)
        self.__add_metric(metrics.HeartBeat)

    @staticmethod
    def _parse_hosts(hosts):
        endpoints = list()

        for host_str in hosts.split(","):
            if ":" in host_str:
                host, port = host_str.split(":", 1)
                port = int(port)
            else:
                host, port = host_str, 2003

            endpoints.append((host, port))

        return frozenset(endpoints)

    @property
    def hosts(self):
        return self.__endpoints

    @hosts.setter
    @LOCK
    def hosts(self, hosts):
        self.__endpoints = self._parse_hosts(hosts)

    @property
    def ns(self):
        return self.__ns

    @ns.setter
    def ns(self, ns):
        if ns.startswith('.'):
            raise ValueError("NameSpace mustn't starts with the dot.")

        if ns.endswith('.'):
            raise ValueError("NameSpace mustn't ends with the dot.")

        if re.match('^[\w\d\._\-]+$', ns) is None:
            raise ValueError("NameSpace mustn't contain special chars (except '_', '-')")

        if bool(list(filter(lambda x: not x, ns.split('.')))):
            raise ValueError("Namespace must contain chars after dots.")

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

    def __setitem__(self, name, metric_type):
        assert issubclass(metric_type, MeasurerBase), "Unknown metric type"
        assert isinstance(name, basestring)

        if name not in self or self.__metrics.get(name) is not metric_type:
            self.__add_metric(metric_type, name)

    @LOCK
    def send(self):
        metric_set = list(self.__metrics.values())

        packet = "\n".join(filter(lambda x: x, map(lambda x: x.str(self.__ns), metric_set)))

        for host, port in self.__endpoints:
            self.socket.sendto(packet, (host, port))

        for m in metric_set:
            m.on_send()

    def close(self):
        self.socket.close()
