import random
import time
from datetime import datetime

def generate_sensor_reading(container_id):
    return {
        "container_id": container_id,
        "reading_time": datetime.now(),
        "temperature_c": round(random.uniform(20, 45), 2),
        "humidity_pct": round(random.uniform(30, 80), 2),
        "vibration_g": round(random.uniform(0.1, 5.0), 2)
    }

if __name__ == "__main__":
    for i in range(5):
        reading = generate_sensor_reading(f"CONT-{i+1}")
        print(reading)
        time.sleep(1)
