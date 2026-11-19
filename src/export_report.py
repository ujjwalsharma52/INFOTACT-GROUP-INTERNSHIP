
import pandas as pd
from database import get_connection


def export_sensor_report():

    connection = get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    try:
        query = """
            SELECT
                id,
                container_id,
                reading_time,
                commodity,
                temperature_c,
                humidity_pct,
                vibration_g,
                status
            FROM sensor_readings
            ORDER BY reading_time DESC
        """

        df = pd.read_sql_query(query, connection)

        if df.empty:
            print("No sensor readings available.")
            return

        report_file = "sensor_readings_report.csv"

        df.to_csv(report_file, index=False)

        print("\nSensor report exported successfully!")
        print("Total records:", len(df))
        print("Report file:", report_file)

    except Exception as error:
        print("Export Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    export_sensor_report()
