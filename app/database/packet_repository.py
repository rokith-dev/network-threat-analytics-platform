from app.database.db_connection import get_connection


def save_packet(
    timestamp,
    source_ip,
    destination_ip,
    source_port,
    destination_port,
    protocol,
    packet_size
):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO packets
    (
        timestamp,
        source_ip,
        destination_ip,
        source_port,
        destination_port,
        protocol,
        packet_size
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        timestamp,
        source_ip,
        destination_ip,
        source_port,
        destination_port,
        protocol,
        packet_size
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()