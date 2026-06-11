"""Packet parsing helpers."""

from app.packet_sniffer.sniffer import CapturedPacket


def parse_packet(raw_packet: object) -> CapturedPacket:
    return CapturedPacket(source="unknown", destination="unknown", protocol="unknown", size=0)
