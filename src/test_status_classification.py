
from status_classification import classify_sensor_status


def test_normal_status():
    reading = {
        "temperature_c": 25,
        "humidity_pct": 60,
        "vibration_g": 2
    }

    assert classify_sensor_status(reading) == "NORMAL"


def test_warning_status():
    reading = {
        "temperature_c": 32,
        "humidity_pct": 60,
        "vibration_g": 2
    }

    assert classify_sensor_status(reading) == "WARNING"


def test_critical_status():
    reading = {
        "temperature_c": 38,
        "humidity_pct": 85,
        "vibration_g": 4.5
    }

    assert classify_sensor_status(reading) == "CRITICAL"


if __name__ == "__main__":
    test_normal_status()
    test_warning_status()
    test_critical_status()

    print("All 3 status classification tests passed!")
