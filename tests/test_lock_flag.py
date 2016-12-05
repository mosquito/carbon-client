#!/usr/bin/env python
# encoding: utf-8
import unittest

from carbon.client.udp import LockFlag


class LockFlagTest(unittest.TestCase):
    def setUp(self):
        self.lock = LockFlag()

    def tearDown(self):
        self.lock = None

    def testLock(self):
        self.a = 0

        @self.lock
        def foo():
            self.a += 1

        @self.lock
        def bar():
            foo()
            self.a += 1

        bar()

        self.assertIs(self.a, 1)
