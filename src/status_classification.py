
def classify_sensor_status(reading):
    """
    Classify sensor readings as NORMAL, WARNING or CRITICAL.

    These are illustrative project thresholds,
    not certified cargo safety limits.
    """

    temperature = reading["temperature_c"]
    humidity = reading["humidity_pct"]
    vibration = reading["vibration_g"]

    # Critical conditions
    if (
        temperature >= 35
        or humidity >= 80
        or vibration >= 4
    ):
        return "CRITICAL"

    # Warning conditions
    elif (
        temperature >= 30
        or humidity >= 70
        or vibration >= 3
    ):
        return "WARNING"

    # Normal conditions
    return "NORMAL"
