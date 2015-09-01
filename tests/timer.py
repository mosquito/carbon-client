#!/usr/bin/env python
# encoding: utf-8
import random
from . import Base, gen_uuid, client, now
from time import sleep


class TestTimer(Base):
    def testCounter(self):
        name = gen_uuid()
        self.client[name] = client.metrics.Timer

        watch = self.client[name].start()
        sleep(0.01)
        self.client[name].stop(watch)

        data = self.get_packet()
        self.assertTrue(data.split('%s.%s %d %.2f' % (self.ns, name, 0, now)))
