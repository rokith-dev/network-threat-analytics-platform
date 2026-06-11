"""Application entry point for the network threat analytics platform."""

from app.dashboard.dashboard import Dashboard
from app.monitoring.logger import get_logger


def main() -> None:
    logger = get_logger()
    logger.info("Starting Network Threat Analytics Platform")
    dashboard = Dashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
