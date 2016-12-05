#!/usr/bin/env python
# encoding: utf-8
from six import b
from . import Base, gen_uuid


class TestClient(Base):
    def testParams(self):
        self.assertEqual(self.client.ns, self.ns)

    def testSendHeartbeat(self):
        data = self.get_packet()
        self.assertTrue(b('heartbeat ') in data)

    def testAddMetric(self):
        name = gen_uuid()
        try:
            self.client[name] = int
        except ValueError:
            pass
        else:
            raise Exception("Client accept unknown metric")

    def testSetNameSpace1(self):
        try:
            self.client.ns = ".a"
        except ValueError:
            pass

    def testSetNameSpace2(self):
        try:
            self.client.ns = "a."
        except ValueError:
            pass

    def testSetNameSpace3(self):
        try:
            self.client.ns = "a..b"
        except ValueError:
            pass

    def testSetNameSpace4(self):
        try:
            self.client.ns = "%%%%.%%%%$!##!"
        except ValueError:
            pass

    def testSetNameSpace5(self):
        self.client.ns = self.ns
