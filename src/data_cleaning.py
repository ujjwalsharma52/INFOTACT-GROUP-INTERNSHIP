
import pandas as pd

# Load dataset
df = pd.read_csv("atmosync_sensor_dataset.csv")

print("Original Dataset Shape:", df.shape)

# Convert reading_time into datetime
df["reading_time"] = pd.to_datetime(df["reading_time"])

# Remove duplicate records
df = df.drop_duplicates()

# Handle missing numerical values
numeric_columns = [
    "temperature_c",
    "humidity_pct",
    "vibration_g"
]

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# Remove records with invalid sensor values
df = df[
    df["temperature_c"].between(-10, 60)
    & df["humidity_pct"].between(0, 100)
    & df["vibration_g"].between(0, 10)
]

# Save cleaned dataset
df.to_csv("cleaned_sensor_dataset.csv", index=False)

print("Cleaned Dataset Shape:", df.shape)
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate Rows:", df.duplicated().sum())
print("Data Cleaning Completed Successfully!")
