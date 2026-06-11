import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="root123",
        database="network_threat_db"
    )