import math
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
    def test_nonfinite_inputs(self):
        for parameter in ('customers', 'price', 'price_change', 'churn', 'churn_sensitivity', 'costs'):
            for value in (math.nan, math.inf, -math.inf):
                with self.subTest(parameter=parameter, value=value), self.assertRaises(ValueError):
                    simulate(**{parameter: value})
    def test_customer_count_must_be_integer(self):
        for value in (1.5, True, '100'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                simulate(customers=value)
    def test_extremely_large_customer_count_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'finite numbers'):
            simulate(customers=10 ** 1000)

    def test_full_churn(self):
        self.assertEqual(simulate(churn=1)['monthly_revenue'], 0)

    def test_finite_inputs_that_overflow_intermediate_results(self):
        scenarios = (
            {'price': 1e308, 'price_change': 1e308},
            {'customers': 10000, 'price': 1e308},
            {'price': 1e308, 'costs': 1e308},
            {'churn_sensitivity': 1e308, 'price_change': 1e308},
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario), self.assertRaisesRegex(ValueError, 'numeric range'):
                simulate(**scenario)

if __name__ == '__main__':
    unittest.main()
