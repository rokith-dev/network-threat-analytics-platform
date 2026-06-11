from app.detection.port_scan_detector import detect_port_scan


def test_port_scan_detector_defaults_to_false() -> None:
    assert detect_port_scan([]) is False
