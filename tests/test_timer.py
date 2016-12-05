#!/usr/bin/env python
# encoding: utf-8
from . import Base, gen_uuid, client, now
from time import sleep
from six import b


class TestTimer(Base):
    def testCounter(self):
        name = gen_uuid()
        self.client[name] = client.metrics.Timer

        watch = self.client[name].start()
        sleep(0.01)
        self.client[name].stop(watch)

        data = self.get_packet()
        self.assertTrue(data.split(b('%s.%s %d %.2f' % (self.ns, name, 0, now))))
