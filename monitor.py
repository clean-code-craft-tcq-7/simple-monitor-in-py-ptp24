
from time import sleep
import sys
from typing import Dict, Tuple, Callable, List


# Define vital sign limits as constants for easy modification
VITAL_LIMITS = {
    "temperature": (95, 102),  # (min, max)
    "pulse_rate": (60, 100),
    "spo2": (90, 100)
}


def is_temperature_ok(temperature: float) -> bool:
    """Check if temperature is within normal range."""
    min_temp, max_temp = VITAL_LIMITS["temperature"]
    return min_temp <= temperature <= max_temp


def is_pulse_rate_ok(pulse_rate: int) -> bool:
    """Check if pulse rate is within normal range."""
    min_rate, max_rate = VITAL_LIMITS["pulse_rate"]
    return min_rate <= pulse_rate <= max_rate


def is_spo2_ok(spo2: int) -> bool:
    """Check if oxygen saturation is within normal range."""
    min_spo2, _ = VITAL_LIMITS["spo2"]
    return spo2 >= min_spo2


def get_vital_status() -> Dict[str, Callable]:
    """
    Return a dictionary mapping vital names to their status check functions.
    This makes it easy to add new vital signs in the future.
    """
    return {
        "temperature": is_temperature_ok,
        "pulse_rate": is_pulse_rate_ok,
        "spo2": is_spo2_ok
    }


def check_vitals(temperature: float, pulse_rate: int, spo2: int) -> Dict[str, bool]:
    """
    Pure function to check all vitals and return their status.
    Returns a dictionary with vital name as key and status (True if ok, False if not) as value.
    """
    vital_checkers = get_vital_status()
    return {
        "temperature": vital_checkers["temperature"](temperature),
        "pulse_rate": vital_checkers["pulse_rate"](pulse_rate),
        "spo2": vital_checkers["spo2"](spo2)
    }


def display_alert(vital_name: str) -> None:
    """Display an alert for a critical vital sign."""
    messages = {
        "temperature": "Temperature critical!",
        "pulse_rate": "Pulse Rate is out of range!",
        "spo2": "Oxygen Saturation out of range!"
    }
    print(messages.get(vital_name, f"{vital_name} out of range!"))
    
    # Blink alert pattern
    blink_alert()


def blink_alert() -> None:
    """Display a blinking alert pattern."""
    for i in range(6):
        print('\r* ', end='')
        sys.stdout.flush()
        sleep(1)
        print('\r *', end='')
        sys.stdout.flush()
        sleep(1)


def vitals_ok(temperature: float, pulse_rate: int, spo2: int) -> bool:
    """
    Check if all vitals are ok and display alerts if not.
    This function separates the I/O (alerts) from the pure checking logic.
    """
    vital_status = check_vitals(temperature, pulse_rate, spo2)
    
    # Process any critical vitals
    for vital, is_ok in vital_status.items():
        if not is_ok:
            display_alert(vital)
            return False
    
    return True
