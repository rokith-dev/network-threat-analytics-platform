"""Database connection helpers."""

from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 3306
    database: str = "nta_platform"
    user: str = "nta_user"
    password: str = "nta_password"


def get_connection() -> object:
    return None
