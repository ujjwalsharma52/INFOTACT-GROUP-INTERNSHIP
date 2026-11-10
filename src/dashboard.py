
import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

# Page Configuration
st.set_page_config(
    page_title="AtmoSync Dashboard",
    page_icon="🌾",
    layout="wide"
)

# Dashboard Header
st.title("🌾 AtmoSync - Smart Cargo Monitoring")
st.markdown("### Real-Time Environmental Sensor Analytics")

# Fetch Data
def load_data():
    connection = get_connection()

    if connection is None:
        return pd.DataFrame()

    try:
        query = """
            SELECT id, container_id, reading_time,
                   commodity, temperature_c,
                   humidity_pct, vibration_g, status
            FROM sensor_readings
            ORDER BY reading_time DESC
        """

        df = pd.read_sql_query(query, connection)
        return df

    except Exception as error:
        st.error(f"Database Error: {error}")
        return pd.DataFrame()

    finally:
        connection.close()


# Refresh Button
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Load Database Data
df = load_data()

if not df.empty:

    # Convert timestamp
    df["reading_time"] = pd.to_datetime(df["reading_time"])

    # KPI Calculations
    total_readings = len(df)
    avg_temp = df["temperature_c"].mean()
    avg_humidity = df["humidity_pct"].mean()
    avg_vibration = df["vibration_g"].mean()

    # KPI Cards
    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Readings", total_readings)
    col2.metric("Avg Temperature", f"{avg_temp:.2f} °C")
    col3.metric("Avg Humidity", f"{avg_humidity:.2f} %")
    col4.metric("Avg Vibration", f"{avg_vibration:.2f} g")

    st.divider()

    # Commodity Distribution
    st.subheader("🌾 Commodity Distribution")

    col1, col2 = st.columns(2)

    with col1:
        commodity_data = df["commodity"].value_counts().reset_index()
        commodity_data.columns = ["Commodity", "Count"]

        fig = px.pie(
            commodity_data,
            names="Commodity",
            values="Count",
            title="Rice vs Corn Distribution",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            commodity_data,
            x="Commodity",
            y="Count",
            title="Commodity Readings",
            text="Count"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Sensor Graphs
    st.subheader("📈 Environmental Sensor Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            df.sort_values("reading_time"),
            x="reading_time",
            y="temperature_c",
            color="container_id",
            title="Temperature Monitoring",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.line(
            df.sort_values("reading_time"),
            x="reading_time",
            y="humidity_pct",
            color="container_id",
            title="Humidity Monitoring",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

    # Vibration Analysis
    fig = px.bar(
        df,
        x="reading_time",
        y="vibration_g",
        color="container_id",
        title="Container Vibration Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Container Status
    st.subheader("🚢 Container Status Monitoring")

    status_data = df["status"].value_counts().reset_index()
    status_data.columns = ["Status", "Count"]

    st.dataframe(status_data, use_container_width=True)

    # Complete Sensor Records
    st.subheader("📋 Latest Sensor Readings")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning(
        "No sensor data available. "
        "Please insert sensor readings into PostgreSQL."
    )

st.caption("AtmoSync | Smart Cargo Monitoring System")
