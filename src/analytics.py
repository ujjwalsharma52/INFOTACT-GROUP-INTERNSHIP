
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
        ORDER BY reading_time DESC
        """

        df = pd.read_sql_query(query, connection)

        if df.empty:
            print("No sensor data available.")
            return

        print("\n========== ATMOSYNC ANALYTICS ==========\n")

        # Total readings
        print("Total Sensor Readings:", len(df))

        # Average sensor values
        print("\nAverage Temperature:",
              round(df["temperature_c"].mean(), 2), "°C")

        print("Average Humidity:",
              round(df["humidity_pct"].mean(), 2), "%")

        print("Average Vibration:",
              round(df["vibration_g"].mean(), 2), "g")

        # Maximum and minimum temperature
        print("\nTemperature Analysis:")
        print("Maximum Temperature:",
              df["temperature_c"].max(), "°C")

        print("Minimum Temperature:",
              df["temperature_c"].min(), "°C")

        # Commodity distribution
        print("\nCommodity Distribution:")
        print(df["commodity"].value_counts())

        # Container-wise analysis
        print("\nContainer-wise Analytics:")
        container_summary = df.groupby("container_id").agg(
            total_readings=("container_id", "count"),
            avg_temperature=("temperature_c", "mean"),
            avg_humidity=("humidity_pct", "mean"),
            avg_vibration=("vibration_g", "mean")
        ).round(2)

        print(container_summary)

        # Sensor status summary
        print("\nSensor Status Summary:")
        print(df["status"].value_counts())

        # Latest sensor readings
        print("\nLatest 5 Sensor Readings:")
        print(df.head(5).to_string(index=False))

    except Exception as error:
        print("Analytics Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    analyze_sensor_data()
