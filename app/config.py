import typing
from dataclasses import asdict, dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class BotConfig:
    token: str


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "own_game"

    def url(self):
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **asdict(self)
        )


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig
    bot: BotConfig
    database: DatabaseConfig


def load_config(config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
    return Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
        ),
        bot=BotConfig(
            token=raw_config["bot"]["token"],
        ),
        database=DatabaseConfig(**raw_config["database"]),
    )


def setup_config(app: "Application", config_path: str):
    app.config = load_config(config_path)
