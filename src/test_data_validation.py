
from data_validation import validate_sensor_reading


def test_valid_reading():
    reading = {
        "container_id": "CONT-001",
        "temperature_c": 28.5,
        "humidity_pct": 65,
        "vibration_g": 2.5
    }

    assert validate_sensor_reading(reading) == []


def test_invalid_reading():
    reading = {
        "container_id": "",
        "temperature_c": 75,
        "humidity_pct": 120,
        "vibration_g": 15
    }

    errors = validate_sensor_reading(reading)

    assert len(errors) == 4


def test_missing_container_id():
    reading = {
        "temperature_c": 28,
        "humidity_pct": 60,
        "vibration_g": 2
    }

    errors = validate_sensor_reading(reading)

    assert "Container ID is missing" in errors


if __name__ == "__main__":
    test_valid_reading()
    test_invalid_reading()
    test_missing_container_id()

    print("All 3 validation tests passed successfully!")
