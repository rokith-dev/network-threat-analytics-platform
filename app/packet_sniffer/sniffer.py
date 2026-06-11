from scapy.all import sniff
from app.packet_sniffer.packet_parser import parse_packet


def start_sniffer():

    print("Starting packet capture...")
    print("Press CTRL + C to stop")

    sniff(
        prn=parse_packet,
        store=False
    )


if __name__ == "__main__":
    start_sniffer()