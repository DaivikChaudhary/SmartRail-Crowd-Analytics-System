"""
dashboard.py
--------------
SmartRail Analytics Dashboard

Features:
1. Real-time analytics dashboard
2. FastAPI integration
3. Alert monitoring
4. Historical analytics charts
5. Movement analytics
6. Auto-refresh support
"""

import requests
import pandas as pd
import streamlit as st
import plotly.express as px

from streamlit_autorefresh import st_autorefresh


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(

    page_title=(
        "SmartRail Dashboard"
    ),

    page_icon="🚆",

    layout="wide"
)


# -----------------------------------
# AUTO REFRESH
# -----------------------------------

# Refresh every 5 seconds
st_autorefresh(

    interval=5000,

    key="dashboard_refresh"
)


# -----------------------------------
# FASTAPI CONFIG
# -----------------------------------

BASE_URL = "https://smartrail-crowd-analytics-system-production.up.railway.app"


# -----------------------------------
# API REQUEST FUNCTION
# -----------------------------------

def fetch_api_data(endpoint):
    """
    Fetch API data safely.

    Args:
        endpoint:
            API endpoint

    Returns:
        JSON data
    """

    try:

        response = requests.get(
            f"{BASE_URL}{endpoint}",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "FastAPI backend offline."
        )

        return []

    except requests.exceptions.Timeout:

        st.error(
            "API request timeout."
        )

        return []

    except Exception as error:

        st.error(
            f"API Error: {error}"
        )

        return []


# -----------------------------------
# LOAD DATA
# -----------------------------------

analytics_data = fetch_api_data(
    "/analytics"
)

alerts_data = fetch_api_data(
    "/alerts"
)

movement_data = fetch_api_data(
    "/movement"
)

aggression_data = fetch_api_data(
    "/aggression-events"
)

health_data = fetch_api_data(
    "/health"
)


# -----------------------------------
# DASHBOARD HEADER
# -----------------------------------

st.title(
    "🚆 SmartRail Crowd Analytics Dashboard"
)

st.markdown(
    """
    AI-powered railway surveillance
    analytics platform.
    """
)

st.divider()


# -----------------------------------
# SYSTEM STATUS
# -----------------------------------

system_status = (
    health_data.get("status", "OFFLINE")
    if isinstance(health_data, dict)
    else "OFFLINE"
)

status_color = (
    "green"
    if system_status == "OK"
    else "red"
)

st.markdown(

    f"""
    ### System Status:
    :{status_color}[{system_status}]
    """
)


# -----------------------------------
# CONVERT TO DATAFRAMES
# -----------------------------------

analytics_df = pd.DataFrame(
    analytics_data
)

alerts_df = pd.DataFrame(
    alerts_data
)

movement_df = pd.DataFrame(
    movement_data
)

aggression_df = pd.DataFrame(
    aggression_data
)

# -----------------------------------
# LIVE ANALYTICS SECTION
# -----------------------------------

st.subheader(
    "📊 Live Analytics"
)

col1, col2, col3, col4 = st.columns(4)

# Default values
passenger_count = 0
density_level = "N/A"
latest_alert = "No Alerts"
fps_value = "Real-Time"

if not analytics_df.empty:

    latest_data = analytics_df.iloc[0]

    passenger_count = (
        latest_data.get(
            "passenger_count",
            0
        )
    )

    density_level = (
        latest_data.get(
            "density_level",
            "N/A"
        )
    )

    latest_alert = (
        latest_data.get(
            "alert_message",
            "No Alerts"
        )
    )

with col1:

    st.metric(
        "Passengers",
        passenger_count
    )

with col2:

    st.metric(
        "Density Level",
        density_level
    )

with col3:

    st.metric(
        "System FPS",
        fps_value
    )

with col4:

    st.metric(
        "Latest Alert",
        latest_alert
    )


# -----------------------------------
# ALERT PANEL
# -----------------------------------

st.divider()

st.subheader(
    "🚨 Alert Monitoring Panel"
)

if not alerts_df.empty:

    for _, row in alerts_df.head(5).iterrows():

        alert_type = row.get(
            "alert_type",
            "UNKNOWN"
        )

        alert_message = row.get(
            "alert_message",
            ""
        )

        if alert_type == "OVERCROWDING":

            st.warning(
                f"{alert_type}: "
                f"{alert_message}"
            )

        elif alert_type == "AGGRESSION":

            st.error(
                f"{alert_type}: "
                f"{alert_message}"
            )

        else:

            st.info(
                f"{alert_type}: "
                f"{alert_message}"
            )

else:

    st.success(
        "No active alerts."
    )


# -----------------------------------
# CROWD ANALYTICS CHART
# -----------------------------------

st.divider()

st.subheader(
    "📈 Historical Crowd Analytics"
)

if not analytics_df.empty:

    chart = px.line(

        analytics_df,

        x="timestamp",

        y="passenger_count",

        title=(
            "Passenger Count Over Time"
        ),

        markers=True
    )

    st.plotly_chart(
        chart,
        width="stretch"
    )

else:

    st.info(
        "No analytics data available."
    )


# -----------------------------------
# MOVEMENT ANALYTICS
# -----------------------------------

st.divider()

st.subheader(
    "🚶 Movement Analytics"
)

if not movement_df.empty:

    st.dataframe(

        movement_df,

        width="stretch"
    )

else:

    st.info(
        "No movement analytics available."
    )


# -----------------------------------
# AGGRESSION ANALYTICS
# -----------------------------------

st.divider()

st.subheader(
    "⚠️ Aggression Analytics"
)

if not aggression_df.empty:

    aggression_chart = px.bar(

        aggression_df,

        x="timestamp",

        y="aggression_score",

        color="alert_status",

        title=(
            "Aggression Score Timeline"
        )
    )

    st.plotly_chart(

        aggression_chart,

        width="stretch"
    )

    st.dataframe(

        aggression_df,

        width="stretch"
    )

else:

    st.success(
        "No aggression events detected."
    )


# -----------------------------------
# RAW DATABASE TABLES
# -----------------------------------

st.divider()

st.subheader(
    "🗂️ Raw Analytics Tables"
)

tab1, tab2, tab3 = st.tabs([

    "Crowd Logs",

    "Alerts",

    "Movement Logs"
])

with tab1:

    st.dataframe(
        analytics_df,
        width="stretch"
    )

with tab2:

    st.dataframe(
        alerts_df,
        width="stretch"
    )

with tab3:

    st.dataframe(
        movement_df,
        width="stretch"
    )