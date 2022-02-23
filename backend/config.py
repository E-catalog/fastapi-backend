from dataclasses import dataclass
from os import getenv


@dataclass
class AppConfig:
    host: str
    port: int
    api_url: str


def load() -> AppConfig:
    return AppConfig(
        host=getenv('APP_HOST', '0.0.0.0'),
        port=int(getenv('APP_PORT', '8000')),
        api_url=getenv('API_URL', 'http://localhost:8000/'),
    )


config = load()
