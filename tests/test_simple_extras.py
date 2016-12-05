#!/usr/bin/env python
# encoding: utf-8
from . import Base, gen_uuid, now, gen_int
from time import sleep
from six import b
from carbon.client import extras, stat


class TestSimpleBase(Base):
    def testDefaultClient(self):
        obj = extras.SimpleMetricBase('test')
        self.assertIs(obj._client, stat)


class TestSimpleCounter(Base):
    def testCounterOK(self):
        name = gen_uuid()

        with extras.SimpleCounter(name, self.client):
            sleep(0.4)

        data = self.get_packet()
        self.assertTrue(data.split(b('%s.%s_ok %d %.2f' % (self.ns, name, 1, now))))

    def testCounterFAIL(self):
        name = gen_uuid()

        try:
            with extras.SimpleCounter(name, self.client):
                sleep(0.3)
                raise Exception()
        except:
            pass

        data = self.get_packet()
        self.assertTrue(data.split(b('%s.%s_fail %d %.2f' % (self.ns, name, 1, now))))


class TestSimpleTimer(Base):
    def testTimerOK(self):
        name = gen_uuid()

        with extras.SimpleTimer(name, self.client):
            pass

        data = self.get_packet()
        self.assertTrue(data.split(b('%s.%s_ok %d %.2f' % (self.ns, name, 0, now))))

    def testTimerFail(self):
        name = gen_uuid()

        try:
            with extras.SimpleTimer(name, self.client):
                raise Exception()
        except:
            pass

        data = self.get_packet()
        self.assertTrue(data.split(b('%s.%s_fail %d %.2f' % (self.ns, name, 0, now))))


class TestSimpleCollector(Base):
    def testTimerOK(self):
        name = gen_uuid()
        meas = gen_int()

        with extras.SimpleCollector(name, self.client) as collector:
            collector.add(meas)

        data = self.get_packet()
        self.assertTrue(data.split(b('%s.%s_ok %d %.2f' % (self.ns, name, meas, now))))
