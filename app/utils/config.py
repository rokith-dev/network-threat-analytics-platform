"""Centralized configuration values."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_host: str = "localhost"
    database_port: int = 3306
    log_level: str = "INFO"
