from scapy.layers.inet import IP, TCP, UDP

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

        source_port = "N/A"
        destination_port = "N/A"

        if packet.haslayer(TCP):
            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport

        elif packet.haslayer(UDP):
            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport

        print("=" * 60)
        print(f"Source IP        : {source_ip}")
        print(f"Destination IP   : {destination_ip}")
        print(f"Source Port      : {source_port}")
        print(f"Destination Port : {destination_port}")
        print(f"Protocol         : {protocol_name}")
        print(f"Packet Size      : {len(packet)} bytes")