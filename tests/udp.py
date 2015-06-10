#!/usr/bin/env python
# encoding: utf-8
from . import Base, gen_uuid


class TestClient(Base):
    def testParams(self):
        self.assertEqual(self.client.port, self.port)
        self.assertEqual(self.client.host, self.host)
        self.assertEqual(self.client.ns, self.ns)

    def testSendHeartbeat(self):
        data = self.get_packet()
        self.assertTrue('heartbeat ' in data)

    def testAddMetric(self):
        name = gen_uuid()
        try:
            self.client[name] = int
        except AssertionError:
            pass
        else:
            raise Exception("Client accept unknown metric")

    def testSetNameSpace1(self):
        try:
            self.client.ns = ".a"
        except AssertionError:
            pass

    def testSetNameSpace2(self):
        try:
            self.client.ns = "a."
        except AssertionError:
            pass

    def testSetNameSpace3(self):
        try:
            self.client.ns = "a..b"
        except AssertionError:
            pass

    def testSetNameSpace4(self):
        try:
            self.client.ns = "%%%%.%%%%$!##!"
        except AssertionError:
            pass

    def testSetNameSpace5(self):
        self.client.ns = self.ns

    def testSetHost(self):
        self.assertIsNotNone(self.client.socket)
        self.client.host = "test"
        self.assertIsNone(self.client._UDPClient__socket)

        self.assertIsNotNone(self.client.socket)
        self.client.host = self.host
        self.assertIsNone(self.client._UDPClient__socket)

    def testSetPort1(self):
        try:
            self.client.port = 'a'
        except AssertionError:
            pass

    def testSetPort1(self):
        self.assertIsNotNone(self.client.socket)
        self.client.port = self.port
        self.assertIsNone(self.client._UDPClient__socket)