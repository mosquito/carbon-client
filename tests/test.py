#!/usr/bin/env python
# encoding: utf-8
import unittest
from .base import TestDefaultClient
from .udp import TestClient
from .counter import TestCounter
from .timer import TestTimer
from .decorators_timeit import TestDectoratorTimeit
from .lock_flag import LockFlagTest
from .simple_extras import TestSimpleCounter, TestSimpleBase, TestSimpleTimer, TestSimpleCollector

if __name__ == '__main__':
    unittest.main()
