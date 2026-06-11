from app.packet_sniffer.sniffer import PacketSniffer


def test_sniffer_returns_empty_iterable() -> None:
    assert list(PacketSniffer().sniff()) == []
