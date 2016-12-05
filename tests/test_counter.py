#!/usr/bin/env python
# encoding: utf-8
import random
from six import b
from . import Base, gen_int, gen_uuid, client, now


class TestCounter(Base):
    def testCounters(self):
        attrs = []
        for i in range(random.randint(100, 500)):
            name = gen_uuid()
            val = gen_int()
            attrs.append((name, val))
            self.client[name] = client.metrics.Counter
            self.client[name].add(val)

        data = self.get_packet()
        for name, val in attrs:
            self.assertIn(b('%s.%s %d %.2f' % (self.ns, name, val, now)), data)

    def testCounterInc(self):
        attrs = []
        val = gen_int()
        name = gen_uuid()
        self.client[name] = client.metrics.Counter
        self.client[name].add(val)

        for i in range(random.randint(100, 500)):
            attrs.append((name, val))
            self.client[name].inc()
            val += 1

        data = self.get_packet()
        for name, val in attrs:
            self.assertIn(b('%s.%s %d %.2f' % (self.ns, name, val, now)), data)

    def testCounterDec(self):
        attrs = []
        val = gen_int()
        name = gen_uuid()
        self.client[name] = client.metrics.Counter
        self.client[name].add(val)

        for i in range(random.randint(100, 500)):
            attrs.append((name, val))
            self.client[name].dec()
            val -= 1

        data = self.get_packet()
        for name, val in attrs:
            self.assertIn(b('%s.%s %d %.2f' % (self.ns, name, val, now)), data)

    def testCounterIncN(self):
        attrs = []
        val = gen_int()
        name = gen_uuid()
        self.client[name] = client.metrics.Counter
        self.client[name].add(val)

        for i in range(random.randint(100, 500)):
            attrs.append((name, val))
            delta = gen_int()
            self.client[name].inc(delta)
            val += delta

        data = self.get_packet()
        for name, val in attrs:
            self.assertIn(b('%s.%s %d %.2f' % (self.ns, name, val, now)), data)

    def testCounterDecN(self):
        attrs = []
        val = gen_int()
        name = gen_uuid()
        self.client[name] = client.metrics.Counter
        self.client[name].add(val)

        for i in range(random.randint(100, 500)):
            attrs.append((name, val))
            delta = gen_int()
            self.client[name].dec(delta)
            val -= delta

        data = self.get_packet()
        for name, val in attrs:
            self.assertIn(b('%s.%s %d %.2f' % (self.ns, name, val, now)), data)

    def testCounterMultiple(self):
        attrs = []
        name = gen_uuid()
        self.client[name] = client.metrics.Counter

        base = 0
        for i in range(random.randint(100, 500)):
            val = gen_int()
            self.client[name].add(val)
            attrs.append((name, base + val))
            base += val

        data = self.get_packet()
        for name, val in attrs:
            self.assertIn(b('%s.%s %d %.2f' % (self.ns, name, val, now)), data)
