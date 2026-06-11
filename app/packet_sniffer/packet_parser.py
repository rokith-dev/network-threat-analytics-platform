from scapy.layers.inet import IP, TCP, UDP
from datetime import datetime
from app.database.packet_repository import save_packet

PROTOCOLS = {
    1: "ICMP",
    6: "TCP",
    17: "UDP"
}

def parse_packet(packet):

    if packet.haslayer(IP):

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        protocol_number = packet[IP].proto
        protocol_name = PROTOCOLS.get(protocol_number, str(protocol_number))

        source_port = 0
        destination_port = 0

        if packet.haslayer(TCP):
            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport

        elif packet.haslayer(UDP):
            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport

        timestamp = datetime.now()

        save_packet(
            timestamp,
            source_ip,
            destination_ip,
            source_port,
            destination_port,
            protocol_name,
            len(packet)
        )

        print("=" * 60)
        print(f"Source IP        : {source_ip}")
        print(f"Destination IP   : {destination_ip}")
        print(f"Source Port      : {source_port}")
        print(f"Destination Port : {destination_port}")
        print(f"Protocol         : {protocol_name}")
        print(f"Packet Size      : {len(packet)} bytes")