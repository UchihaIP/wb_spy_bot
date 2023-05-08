from typing import Any
from pydantic import BaseSettings


class Setting(BaseSettings):
    BOT_TOKEN: str

    ADMIN_IDS: list[int]
    SELLER_ID: int
    CLIENT_ID: int

    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            return [int(x) for x in raw_val.split(',')]


settings = Setting()
