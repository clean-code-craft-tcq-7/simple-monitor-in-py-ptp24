import unittest
import io
import sys
from unittest.mock import patch
from monitor import (
    vitals_ok, check_vitals, is_temperature_ok, 
    is_pulse_rate_ok, is_spo2_ok, VITAL_LIMITS
)


class MonitorTest(unittest.TestCase):
    def test_temperature_boundary_conditions(self):
        min_temp, max_temp = VITAL_LIMITS["temperature"]
        # Boundary tests
        self.assertTrue(is_temperature_ok(min_temp))  # Lower boundary
        self.assertTrue(is_temperature_ok(max_temp))  # Upper boundary
        self.assertFalse(is_temperature_ok(min_temp - 0.1))  # Below lower boundary
        self.assertFalse(is_temperature_ok(max_temp + 0.1))  # Above upper boundary
        # Common values
        self.assertTrue(is_temperature_ok(98.6))  # Normal body temperature

    def test_pulse_rate_boundary_conditions(self):
        min_rate, max_rate = VITAL_LIMITS["pulse_rate"]
        # Boundary tests
        self.assertTrue(is_pulse_rate_ok(min_rate))  # Lower boundary
        self.assertTrue(is_pulse_rate_ok(max_rate))  # Upper boundary
        self.assertFalse(is_pulse_rate_ok(min_rate - 1))  # Below lower boundary
        self.assertFalse(is_pulse_rate_ok(max_rate + 1))  # Above upper boundary
        # Common values
        self.assertTrue(is_pulse_rate_ok(75))  # Normal pulse rate

    def test_spo2_boundary_conditions(self):
        min_spo2, _ = VITAL_LIMITS["spo2"]
        # Boundary tests
        self.assertTrue(is_spo2_ok(min_spo2))  # Lower boundary
        self.assertTrue(is_spo2_ok(100))  # Upper boundary (max possible value)
        self.assertFalse(is_spo2_ok(min_spo2 - 1))  # Below lower boundary
        # Common values
        self.assertTrue(is_spo2_ok(98))  # Normal SpO2

    def test_check_vitals_function(self):
        # All vitals ok
        result = check_vitals(98.6, 75, 98)
        self.assertTrue(all(result.values()))
        
        # Temperature not ok
        result = check_vitals(103, 75, 98)
        self.assertFalse(result["temperature"])
        self.assertTrue(result["pulse_rate"])
        self.assertTrue(result["spo2"])
        
        # Pulse rate not ok
        result = check_vitals(98.6, 55, 98)
        self.assertTrue(result["temperature"])
        self.assertFalse(result["pulse_rate"])
        self.assertTrue(result["spo2"])
        
        # SpO2 not ok
        result = check_vitals(98.6, 75, 89)
        self.assertTrue(result["temperature"])
        self.assertTrue(result["pulse_rate"])
        self.assertFalse(result["spo2"])
        
        # Multiple vitals not ok
        result = check_vitals(103, 55, 89)
        self.assertFalse(result["temperature"])
        self.assertFalse(result["pulse_rate"])
        self.assertFalse(result["spo2"])

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_vitals_ok_output_and_return(self, mock_stdout):
        # Test when all vitals are ok
        self.assertTrue(vitals_ok(98.6, 75, 98))
        self.assertEqual('', mock_stdout.getvalue())
        
        # Reset mock
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        
        # Test with mocked display_alert to avoid sleep in tests
        with patch('monitor.blink_alert'):
            # Test temperature critical
            self.assertFalse(vitals_ok(103, 75, 98))
            self.assertIn('Temperature critical!', mock_stdout.getvalue())
            
            # Reset mock
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            
            # Test pulse rate out of range
            self.assertFalse(vitals_ok(98.6, 55, 98))
            self.assertIn('Pulse Rate is out of range!', mock_stdout.getvalue())
            
            # Reset mock
            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            
            # Test SpO2 out of range
            self.assertFalse(vitals_ok(98.6, 75, 89))
            self.assertIn('Oxygen Saturation out of range!', mock_stdout.getvalue())

    def test_original_requirements(self):
        # Original tests from the initial implementation
        self.assertFalse(vitals_ok(99, 102, 70))
        self.assertTrue(vitals_ok(98.1, 70, 98))


if __name__ == '__main__':
    unittest.main()
