#!/usr/bin/env python
# encoding: utf-8
import random
from . import Base, gen_uuid, client, now


class TestTimer(Base):
    def testCounter(self):
        name = gen_uuid()
        self.client[name] = client.metrics.Timer

        with self.client[name]:
            pass

        data = self.get_packet()
        self.assertTrue(data.split('%s.%s %d %.2f' % (self.ns, name, 0, now)))

    def testCounters(self):
        name = gen_uuid()
        self.client[name] = client.metrics.Timer
        count = random.randint(100, 200)

        with self.client[name] as timer:
            for i in range(count):
                timer.start()
                timer.stop()

        data = self.get_packet()
        self.assertTrue(len(data.split('%s.%s %d %.2f' % (self.ns, name, 0, now))) == (count + 1))
