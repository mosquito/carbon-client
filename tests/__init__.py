#!/usr/bin/env python
# encoding: utf-8
from mock import patch
import socket
import uuid
import random
import unittest


def gen_uuid():
    return str(uuid.uuid4())


def gen_int():
    return random.randint(1, 65535)


now = gen_int()

ENV = {
    'CARBON_HOST': gen_uuid(),
    'CARBON_PORT': gen_int(),
    'CARBON_NS': gen_uuid()
}


with patch('socket.socket', spec=socket.socket) as fake_socket,\
        patch('time.time', new=lambda: now),\
        patch('os.getenv', new=ENV.get):
    from carbon import client


class Base(unittest.TestCase):
    def setUp(self):
        self.port = gen_int()
        self.host = gen_uuid()
        self.ns = gen_uuid()
        self.client = client.UDPClient(hosts="%s:%s" % (self.host, self.port), ns=self.ns)

    def tearDown(self):
        self.client.close()

    def get_packet(self):
        self.client.send()
        data, remote = self.client.socket.sendto.call_args[0]
        host, port = remote
        self.assertEqual(host, self.host)
        self.assertEqual(port, self.port)
        return data
