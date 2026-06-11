"""Packet capture orchestration."""

from dataclasses import dataclass
from typing import Iterable


@dataclass
class CapturedPacket:
    source: str
    destination: str
    protocol: str
    size: int


class PacketSniffer:
    def sniff(self) -> Iterable[CapturedPacket]:
        return []
