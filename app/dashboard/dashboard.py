import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from app.detection.port_scan_detector import detect_port_scans

import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px


# ==========================================
# Database Connection
# ==========================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="network_threat_db"
    )


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Network Threat Analytics Platform",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Network Threat Analytics Platform")
st.markdown("### Real-Time Network Traffic Analytics Dashboard")


# ==========================================
# Load Data
# ==========================================

connection = get_connection()

query = """
SELECT *
FROM packets
ORDER BY id DESC
LIMIT 1000
"""

df = pd.read_sql(query, connection)

connection.close()

if df.empty:
    st.warning("No packet data found in the database.")
    st.stop()


# ==========================================
# Threat Detection
# ==========================================

port_scan_df = detect_port_scans(df)


# ==========================================
# Metrics Section
# ==========================================

total_packets = len(df)

tcp_packets = len(df[df["protocol"] == "TCP"])

udp_packets = len(df[df["protocol"] == "UDP"])

icmp_packets = len(df[df["protocol"] == "ICMP"])

unique_ips = df["source_ip"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Packets", total_packets)
col2.metric("TCP Packets", tcp_packets)
col3.metric("UDP Packets", udp_packets)
col4.metric("ICMP Packets", icmp_packets)
col5.metric("Unique Source IPs", unique_ips)


# ==========================================
# Threat Detection Section
# ==========================================

st.divider()

st.subheader("🚨 Threat Detection")

if port_scan_df.empty:
    st.success("No suspicious port scanning detected.")
else:
    st.error("Potential Port Scan Detected!")

    st.dataframe(
        port_scan_df,
        use_container_width=True
    )


# ==========================================
# Protocol Distribution
# ==========================================

st.divider()

protocol_counts = (
    df["protocol"]
    .value_counts()
    .reset_index()
)

protocol_counts.columns = ["Protocol", "Count"]

fig_protocol = px.pie(
    protocol_counts,
    names="Protocol",
    values="Count",
    title="Protocol Distribution"
)

st.plotly_chart(
    fig_protocol,
    use_container_width=True
)


# ==========================================
# Top Source IPs
# ==========================================

st.divider()

top_ips = (
    df["source_ip"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_ips.columns = ["Source IP", "Packets"]

st.subheader("📡 Top Source IP Addresses")

st.dataframe(
    top_ips,
    use_container_width=True
)


# ==========================================
# Top Destination Ports
# ==========================================

st.divider()

top_ports = (
    df["destination_port"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_ports.columns = ["Destination Port", "Packets"]

fig_ports = px.bar(
    top_ports,
    x="Destination Port",
    y="Packets",
    title="Most Active Destination Ports"
)

st.plotly_chart(
    fig_ports,
    use_container_width=True
)


# ==========================================
# Recent Packets
# ==========================================

st.divider()

st.subheader("📄 Recent Packet Activity")

display_columns = [
    "timestamp",
    "source_ip",
    "destination_ip",
    "source_port",
    "destination_port",
    "protocol",
    "packet_size"
]

st.dataframe(
    df[display_columns],
    use_container_width=True,
    height=500
)