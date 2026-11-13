
def validate_sensor_reading(reading):
    """Validate sensor reading data."""

    errors = []

    # Validate container ID
    if not reading.get("container_id"):
        errors.append("Container ID is missing")

    # Validate temperature
    temperature = reading.get("temperature_c")

    if temperature is None or not -10 <= temperature <= 60:
        errors.append("Invalid temperature value")

    # Validate humidity
    humidity = reading.get("humidity_pct")

    if humidity is None or not 0 <= humidity <= 100:
        errors.append("Invalid humidity value")

    # Validate vibration
    vibration = reading.get("vibration_g")

    if vibration is None or not 0 <= vibration <= 10:
        errors.append("Invalid vibration value")

    return errors


if __name__ == "__main__":

    sample_reading = {
        "container_id": "CONT-001",
        "temperature_c": 28.5,
        "humidity_pct": 65.0,
        "vibration_g": 2.5
    }

    errors = validate_sensor_reading(sample_reading)

    if errors:
        print("Invalid Sensor Reading:")
        for error in errors:
            print("-", error)
    else:
        print("Sensor Reading is Valid!")
