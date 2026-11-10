
import pandas as pd
from database import get_connection


def analyze_sensor_data():

    connection = get_connection()

    if connection is None:
        return

    try:
        query = """
        SELECT
            container_id,
            commodity,
            temperature_c,
            humidity_pct,
            vibration_g,
            status,
            reading_time
        FROM sensor_readings
        """

        df = pd.read_sql_query(query, connection)

        print("\n========== ATMOSYNC ANALYTICS ==========\n")

        print("Total Sensor Readings:", len(df))

        print("\nAverage Temperature:")
        print(df["temperature_c"].mean())

        print("\nAverage Humidity:")
        print(df["humidity_pct"].mean())

        print("\nAverage Vibration:")
        print(df["vibration_g"].mean())

        print("\nCommodity Distribution:")
        print(df["commodity"].value_counts())

        print("\nComplete Sensor Data:")
        print(df.to_string(index=False))

    except Exception as error:
        print("Analytics Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    analyze_sensor_data()
