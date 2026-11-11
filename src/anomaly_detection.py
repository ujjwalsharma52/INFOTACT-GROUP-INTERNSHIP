
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("cleaned_sensor_dataset.csv")

# Define demo thresholds
df["high_temperature"] = df["temperature_c"] > 35
df["high_humidity"] = df["humidity_pct"] > 80
df["high_vibration"] = df["vibration_g"] > 3.5

# Identify unusual readings
df["anomaly"] = (
    df["high_temperature"]
    | df["high_humidity"]
    | df["high_vibration"]
)

# Display results
print("Total Sensor Readings:", len(df))
print("High Temperature:", df["high_temperature"].sum())
print("High Humidity:", df["high_humidity"].sum())
print("High Vibration:", df["high_vibration"].sum())
print("Total Anomalies:", df["anomaly"].sum())

# Save anomaly report
df.to_csv("sensor_anomaly_report.csv", index=False)

print("\nAnomaly Detection Completed!")
print("Report saved successfully!")
