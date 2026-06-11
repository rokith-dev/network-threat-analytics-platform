from app.database.packet_repository import PacketRepository


def test_repository_list_recent_is_empty() -> None:
    assert list(PacketRepository().list_recent()) == []
