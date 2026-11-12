
import random
import time
from datetime import datetime

from database import get_connection


def generate_sensor_data():
    return {
        "container_id": "CONTAINER_001",
        "reading_time": datetime.now(),
        "commodity": random.choice(
            ["Wheat", "Rice", "Corn", "Soybean"]
        ),
        "temperature_c": round(random.uniform(15, 40), 2),
        "humidity_pct": round(random.uniform(30, 90), 2),
        "vibration_g": round(random.uniform(0.1, 5.0), 2),
        "status": "NORMAL"
    }


def insert_sensor_data(data):
    connection = get_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO sensor_readings
        (container_id, reading_time, commodity,
         temperature_c, humidity_pct, vibration_g, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["container_id"],
            data["reading_time"],
            data["commodity"],
            data["temperature_c"],
            data["humidity_pct"],
            data["vibration_g"],
            data["status"]
        ))

        connection.commit()
        print("Sensor reading inserted:", data)

        cursor.close()

    except Exception as error:
        connection.rollback()
        print("Insertion error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    for i in range(5):
        sensor_data = generate_sensor_data()
        insert_sensor_data(sensor_data)
        time.sleep(2)
