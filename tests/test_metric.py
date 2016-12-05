from carbon.client.metrics.base import Metric
from . import Base


class TestMetric(Base):
    def testEqual(self):
        m1 = Metric(name="test", value=10, ts=0)
        m2 = Metric(name="test", value=10, ts=0)

        self.assertEqual(m1, m2)
        self.assertFalse(m1 < m2)
        self.assertFalse(m1 > m2)
        self.assertTrue(m1 == m2)
