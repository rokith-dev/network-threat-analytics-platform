"""Persistence helpers for packet data."""

from dataclasses import dataclass
from typing import Iterable


@dataclass
class PacketRecord:
    source: str
    destination: str
    protocol: str
    size: int


class PacketRepository:
    def save(self, record: PacketRecord) -> None:
        return None

    def list_recent(self) -> Iterable[PacketRecord]:
        return []
