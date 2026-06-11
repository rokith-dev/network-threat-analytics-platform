import streamlit as st
import pandas as pd
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="network_threat_db"
    )


st.set_page_config(
    page_title="Network Threat Analytics Platform",
    layout="wide"
)

st.title("🌐 Network Threat Analytics Platform")

connection = get_connection()

query = """
SELECT *
FROM packets
ORDER BY id DESC
LIMIT 100
"""

df = pd.read_sql(query, connection)

st.subheader("Recent Packets")

st.dataframe(df)

connection.close()