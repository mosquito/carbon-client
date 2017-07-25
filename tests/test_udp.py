#!/usr/bin/env python
# encoding: utf-8
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from six import b

from carbon.client import UDPClient
from carbon.client.extras import SimpleCounter
from tests import Base, gen_uuid


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

    def testChackMetricsWhenCarbonUnavailable(self):
        name = gen_uuid()
        ok_label = "{}_ok".format(name)
        fail_label = "{}_fail".format(name)

        client = UDPClient()
        client._UDPClient__socket = Mock()
        client._UDPClient__socket.sendto = Mock(return_value=Exception)

        with SimpleCounter(name, client):
            pass
        try:
            with SimpleCounter(name, client):
                raise Exception("error")
        except:
            pass

        self.assertTrue(client[ok_label]._values)
        self.assertTrue(client[fail_label]._values)
        client.send()
        self.assertFalse(client[ok_label]._values)
        self.assertFalse(client[fail_label]._values)

    def testGaiError(self):
        # socket.gaierror: [Errno -2] Name or service not known
        name = gen_uuid()
        ok_label = "{}_ok".format(name)
        fail_label = "{}_fail".format(name)

        client = UDPClient(hosts="{}.com".format(name))
        with SimpleCounter(name, client):
            pass
        try:
            with SimpleCounter(name, client):
                raise Exception("error")
        except:
            pass
        self.assertTrue(client[ok_label]._values)
        self.assertTrue(client[fail_label]._values)
        client.send()
        self.assertFalse(client[ok_label]._values)
        self.assertFalse(client[fail_label]._values)
