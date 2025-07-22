from time import sleep
import sys


def display_alert(message):
  for _ in range(6):
    print('\r* ', end='')
    sys.stdout.flush()
    sleep(1)
  print(message)


def is_temperature_ok(temperature):
  if temperature > 102 or temperature < 95:
    display_alert('Temperature critical!')
    return False
  return True


def is_pulse_rate_ok(pulse_rate):
  if pulse_rate < 60 or pulse_rate > 100:
    display_alert('Pulse Rate is out of range!')
    return False
  return True


def is_spo2_ok(spo2):
  if spo2 < 90:
    display_alert('Oxygen Saturation out of range!')
    return False
  return True


def vitals_ok(temperature, pulse_rate, spo2):
  return is_temperature_ok(temperature) and is_pulse_rate_ok(pulse_rate) and is_spo2_ok(spo2)
