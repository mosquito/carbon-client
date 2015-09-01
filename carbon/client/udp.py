#!/usr/bin/env python
# encoding: utf-8
import re
import logging

from functools import wraps
from socket import socket, AF_INET, SOCK_DGRAM

from . import metrics
from .metrics.base import MetricTypeBase


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

    def __init__(self, hosts='127.0.0.1', ns='carbon.client'):
        self.__host = hosts
        self.__ns = ns
        self.__socket = None
        self.__endpoints = map(
            lambda x: x if len(x) > 1 else [x[0], 2003],
            map(
                lambda x: [int(i) if i.isdigit() else i for i in x.strip(" ").split(":")],
                hosts.split(",")
            )
        )

        self.__sending = False
        self.__metrics = {}
        self.__add_metric(metrics.HeartBeat)

    @property
    def hosts(self):
        return self.__endpoints

    @hosts.setter
    @LOCK
    def hosts(self, hosts):
        self.__endpoints = map(
            lambda x: x if len(x) > 1 else [x[0], 2003],
            map(
                lambda x: [int(i) if i.isdigit() else i for i in x.strip(" ").split(":")],
                hosts.split(",")
            )
        )

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

    def __setitem__(self, name, metric_type):
        assert issubclass(metric_type, MetricTypeBase), "Unknown metric type"
        assert isinstance(name, basestring)

        if name not in self or self.__metrics.get(name) is not metric_type:
            self.__add_metric(metric_type, name)

    @LOCK
    def send(self):
        metric_set = list(self.__metrics.values())

        packet = "\n".join(
            filter(lambda x: x, map(lambda x: x.str(self.__ns), metric_set))
        )

        for host, port in self.__endpoints:
            self.socket.sendto(
                packet,
                (host, port)
            )

        map(lambda m: m.on_send(), metric_set)

    def close(self):
        self.socket.close()
