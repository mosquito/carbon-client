#!/usr/bin/env python
# encoding: utf-8
import unittest
from . import client, ENV


class TestDefaultClient(unittest.TestCase):
    def testHost(self):
        self.assertEqual(client.stat.host, ENV['CARBON_HOST'])
        self.assertEqual(client.stat.port, ENV['CARBON_PORT'])
        self.assertEqual(client.stat.ns, ENV['CARBON_NS'])
