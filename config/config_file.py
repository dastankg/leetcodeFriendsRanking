from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_id: list[int]


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_username: str
    db_password: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_id=list(map(int, env('ADMIN_IDS').split(',')))
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_username=env('DB_USERNAME'),
            db_password=env('DB_PASSWORD'),
        )
    )
