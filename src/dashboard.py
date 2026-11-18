
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
st.markdown("### Environmental Sensor Monitoring & Analytics")


# Fetch Data
@st.cache_data(ttl=10)
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

        return pd.read_sql_query(query, connection)

    except Exception as error:
        st.error(f"Database Error: {error}")
        return pd.DataFrame()

    finally:
        connection.close()


# Sidebar
st.sidebar.header("Dashboard Controls")

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Load Data
df = load_data()

if not df.empty:

    df["reading_time"] = pd.to_datetime(df["reading_time"])
    df["status"] = df["status"].str.upper()

    # Status counts
    status_counts = df["status"].value_counts()

    normal_count = status_counts.get("NORMAL", 0)
    warning_count = status_counts.get("WARNING", 0)
    critical_count = status_counts.get("CRITICAL", 0)

    # Main KPIs
    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Readings", len(df))
    col2.metric("Avg Temperature", f"{df['temperature_c'].mean():.2f} °C")
    col3.metric("Avg Humidity", f"{df['humidity_pct'].mean():.2f} %")
    col4.metric("Avg Vibration", f"{df['vibration_g'].mean():.2f} g")

    st.divider()

    # Status Monitoring
    st.subheader("🚦 Sensor Status Monitoring")

    col1, col2, col3 = st.columns(3)

    col1.metric("🟢 NORMAL", normal_count)
    col2.metric("🟠 WARNING", warning_count)
    col3.metric("🔴 CRITICAL", critical_count)

    # Status Chart
    status_data = status_counts.reset_index()
    status_data.columns = ["Status", "Count"]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            status_data,
            names="Status",
            values="Count",
            title="Sensor Status Distribution",
            hole=0.4,
            color="Status",
            color_discrete_map={
                "NORMAL": "green",
                "WARNING": "orange",
                "CRITICAL": "red"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Status Summary")

        st.dataframe(
            status_data,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # Commodity Distribution
    st.subheader("🌾 Commodity Distribution")

    commodity_data = df["commodity"].value_counts().reset_index()
    commodity_data.columns = ["Commodity", "Count"]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            commodity_data,
            x="Commodity",
            y="Count",
            title="Commodity Readings",
            text="Count"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            commodity_data,
            names="Commodity",
            values="Count",
            title="Commodity Distribution",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Environmental Sensor Analysis
    st.subheader("📈 Environmental Sensor Analysis")

    sorted_df = df.sort_values("reading_time")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            sorted_df,
            x="reading_time",
            y="temperature_c",
            color="container_id",
            title="Temperature Monitoring",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.line(
            sorted_df,
            x="reading_time",
            y="humidity_pct",
            color="container_id",
            title="Humidity Monitoring",
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        sorted_df,
        x="reading_time",
        y="vibration_g",
        color="container_id",
        title="Container Vibration Analysis",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Reading Filter
    st.subheader("📋 Sensor Readings")

    selected_status = st.sidebar.multiselect(
        "Filter by Sensor Status",
        options=sorted(df["status"].dropna().unique()),
        default=sorted(df["status"].dropna().unique())
    )

    filtered_df = df[df["status"].isin(selected_status)]

    st.write(f"Showing {len(filtered_df)} sensor readings")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning(
        "No sensor data available. "
        "Please insert sensor readings into PostgreSQL."
    )

st.caption("AtmoSync | Smart Cargo Monitoring System")
