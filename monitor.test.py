import unittest
from unittest.mock import patch
from monitor import *

class TestMonitor(unittest.TestCase):

    @patch('builtins.print')
    def test_temperature_ok(self, mock_print):
        self.assertTrue(is_temperature_ok(98.6))  # Normal temp
        self.assertFalse(is_temperature_ok(103))  # High temp
        self.assertFalse(is_temperature_ok(94))   # Low temp
        mock_print.assert_called_with('Temperature critical!')

    @patch('builtins.print')
    def test_pulse_rate_ok(self, mock_print):
        self.assertTrue(is_pulse_rate_ok(75))     # Normal pulse
        self.assertFalse(is_pulse_rate_ok(50))    # Low pulse
        self.assertFalse(is_pulse_rate_ok(110))   # High pulse
        mock_print.assert_called_with('Pulse Rate is out of range!')

    @patch('builtins.print')
    def test_spo2_ok(self, mock_print):
        self.assertTrue(is_spo2_ok(95))           # Normal SpO2
        self.assertFalse(is_spo2_ok(85))         # Low SpO2
        mock_print.assert_called_with('Oxygen Saturation out of range!')

    @patch('builtins.print')
    def test_vitals_ok(self, mock_print):
        self.assertTrue(vitals_ok(98.6, 75, 95))  # All normal
        self.assertFalse(vitals_ok(103, 75, 95))  # Bad temp
        self.assertFalse(vitals_ok(98.6, 50, 95)) # Bad pulse
        self.assertFalse(vitals_ok(98.6, 75, 85)) # Bad SpO2

if __name__ == '__main__':
    unittest.main()