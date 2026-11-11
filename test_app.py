import unittest
from app import simulate

class SimulationTests(unittest.TestCase):
    def test_baseline(self):
        self.assertEqual(simulate()['monthly_revenue'], 190000)
    def test_price_increase(self):
        self.assertEqual(simulate(price_change=0.1)['retained_customers'], 9100)
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            simulate(customers=-1)
    def test_full_churn(self):
        self.assertEqual(simulate(churn=1)['monthly_revenue'], 0)

if __name__ == '__main__':
    unittest.main()
