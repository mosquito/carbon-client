# encoding: utf-8
import unittest
from . import client, ENV


class TestDefaultClient(unittest.TestCase):
    def testHost(self):
        self.assertEqual(client.stat.ns, ENV['CARBON_NS'])
