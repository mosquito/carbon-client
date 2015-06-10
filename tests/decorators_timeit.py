#!/usr/bin/env python
# encoding: utf-8
from . import Base, gen_int, gen_uuid, client, now


class TestDectoratorTimeit(Base):
    def testTimeit(self):
        name = gen_uuid()
        client.decorators.timeit(name, self.client)(lambda x: x)(gen_int())
        data = self.get_packet()
        self.assertIn('%s.%s %d %.2f' % (self.ns, name, 0, now), data)
