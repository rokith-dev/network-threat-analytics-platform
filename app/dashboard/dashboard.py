import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from app.detection.port_scan_detector import detect_port_scans
from app.detection.dos_detector import detect_dos

import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ==========================================

# Database Connection

# ==========================================


def get_connection():
	return mysql.connector.connect(
		host="mysql-db",
		user="root",
		password="root123",
		database="network_threat_db",
	)


# ==========================================

# Page Configuration

# ==========================================

st.set_page_config(
	page_title="Network Threat Analytics Platform",
	page_icon="🌐",
	layout="wide",
)

st.title("🌐 Network Threat Analytics Platform")
st.markdown("### Real-Time Network Traffic Analytics Dashboard")
st.caption("🔄 Refresh browser to see latest traffic")
st.success("🟢 Network Monitoring Active")

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

try:
	df = pd.read_sql(query, connection)
finally:
	connection.close()

if df.empty:
	st.warning("No packet data found in the database.")
	st.stop()

# ==========================================

# Threat Detection

# ==========================================

port_scan_df = detect_port_scans(df)
dos_df = detect_dos(df)

port_scan_count = len(port_scan_df)
dos_count = len(dos_df)

high_risk_ips = set()

if not port_scan_df.empty:
	high_risk_ips.update(port_scan_df["source_ip"])

if not dos_df.empty:
	high_risk_ips.update(dos_df["source_ip"])

# ==========================================

# Metrics Section

# ==========================================

total_packets = len(df)
tcp_packets = len(df[df["protocol"] == "TCP"])
udp_packets = len(df[df["protocol"] == "UDP"])
icmp_packets = len(df[df["protocol"] == "ICMP"])
unique_ips = df["source_ip"].nunique()

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

col1.metric("Total Packets", total_packets)
col2.metric("TCP Packets", tcp_packets)
col3.metric("UDP Packets", udp_packets)
col4.metric("ICMP Packets", icmp_packets)
col5.metric("Unique Source IPs", unique_ips)
col6.metric("Port Scan Alerts", port_scan_count)
col7.metric("DoS Alerts", dos_count)

st.divider()

st.subheader("🛡️ Security Overview")

sec1, sec2, sec3 = st.columns(3)

sec1.metric(
	"Port Scan Threats",
	port_scan_count,
)

sec2.metric(
	"DoS Threats",
	dos_count,
)

sec3.metric(
	"High Risk IPs",
	len(high_risk_ips),
)

# ==========================================

# Threat Detection

# ==========================================

st.divider()

st.subheader("🚨 Threat Detection")

if port_scan_df.empty:
	st.success("No suspicious port scanning detected.")
else:
	st.error("Potential Port Scan Detected!")
	st.dataframe(port_scan_df, use_container_width=True)

st.subheader("⚠️ DoS Detection")

if dos_df.empty:
	st.success("No DoS activity detected.")
else:
	st.error("Potential DoS Activity Detected!")
	st.dataframe(dos_df, use_container_width=True)

# ==========================================

# High Risk IPs

# ==========================================

st.divider()

st.subheader("🔥 High Risk IPs")

if len(high_risk_ips) == 0:
	st.success("No high-risk IPs detected.")
else:
	st.dataframe(
		pd.DataFrame(
			{"High Risk IP": list(high_risk_ips)}
		),
		use_container_width=True,
	)

# ==========================================

# Suspicious IP Ranking

# ==========================================

st.divider()

st.subheader("🚨 Suspicious IP Ranking")

suspicious_ips = (
	df["source_ip"]
	.value_counts()
	.head(10)
	.reset_index()
)

suspicious_ips.columns = [
	"IP Address",
	"Traffic Count",
]

st.dataframe(
	suspicious_ips,
	use_container_width=True,
)

# ==========================================

# Traffic Timeline

# ==========================================

st.divider()

st.subheader("📈 Traffic Timeline")

timeline_df = df.copy()

timeline_df["timestamp"] = pd.to_datetime(timeline_df["timestamp"])

timeline_df["minute"] = timeline_df["timestamp"].dt.strftime("%H:%M")

traffic_timeline = (
	timeline_df.groupby("minute")
	.size()
	.reset_index(name="Packets")
)

fig_timeline = px.line(
	traffic_timeline,
	x="minute",
	y="Packets",
	title="Packets Per Minute",
)

st.plotly_chart(
	fig_timeline,
	use_container_width=True,
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
	title="Protocol Distribution",
)

st.plotly_chart(
	fig_protocol,
	use_container_width=True,
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
	use_container_width=True,
)

# ==========================================

# Top Destination IPs

# ==========================================

st.divider()

top_dest_ips = (
	df["destination_ip"]
	.value_counts()
	.head(10)
	.reset_index()
)

top_dest_ips.columns = [
	"Destination IP",
	"Packets",
]

st.subheader("🎯 Top Destination IP Addresses")

st.dataframe(
	top_dest_ips,
	use_container_width=True,
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
	title="Most Active Destination Ports",
)

st.plotly_chart(
	fig_ports,
	use_container_width=True,
)

# ==========================================

# Top Source Ports

# ==========================================

st.divider()

top_source_ports = (
	df["source_port"]
	.value_counts()
	.head(10)
	.reset_index()
)

top_source_ports.columns = [
	"Source Port",
	"Packets",
]

fig_source_ports = px.bar(
	top_source_ports,
	x="Source Port",
	y="Packets",
	title="Most Active Source Ports",
)

st.plotly_chart(
	fig_source_ports,
	use_container_width=True,
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
	"packet_size",
]

st.dataframe(
	df[display_columns],
	use_container_width=True,
	height=500,
)
