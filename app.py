import streamlit as st
import pandas as pd

st.set_page_config(page_title="ICU Alert Dashboard", layout="wide")

st.title("🧠 Dehumanized ICU Critical Alert Triage")
st.markdown("This demo simulates smart filtering of critical values using vital signs and WBC data.")

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv("sparse_icu_alert_data.csv", parse_dates=["Timestamp"])

df = load_data()

# Define critical value rules
def is_critical(row):
    alerts = []
    if row["HeartRate"] > 130 or row["HeartRate"] < 40:
        alerts.append("Heart Rate")
    if row["RespiratoryRate"] > 30 or row["RespiratoryRate"] < 8:
        alerts.append("Resp Rate")
    if row["Temperature"] > 39.5 or row["Temperature"] < 35:
        alerts.append("Temp")
    if pd.notna(row["WBCCount"]):
        if row["WBCCount"] > 20 or row["WBCCount"] < 1.5:
            alerts.append("WBC")
    return alerts

df["CriticalParams"] = df.apply(is_critical, axis=1)
df["AlertSuppressed"] = df.apply(lambda x: 1 if x["PriorAlert"] == 1 else 0)

# Filter only current alerts that are not suppressed
active_alerts = df[(df["CriticalParams"].apply(len) > 0) & (df["AlertSuppressed"] == 0)]

# Display dashboard
st.subheader("⚠️ Current Unacknowledged Critical Alerts")
st.dataframe(active_alerts[["PatientID", "Timestamp", "CriticalParams"]], height=400)

st.subheader("🗂️ Full Alert History")
st.dataframe(df[["PatientID", "Timestamp", "CriticalParams", "AlertSuppressed"]], height=300)
