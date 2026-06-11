import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="mysql-db",
        user="root",
        password="root123",
        database="network_threat_db"
    )