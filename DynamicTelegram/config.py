from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

ROOT = Path(__file__).resolve().parent


def _load_env() -> None:
    if load_dotenv is not None:
        env = ROOT / ".env"
        if env.exists():
            load_dotenv(env)


@dataclass
class Config:
    bot_token: str = ""
    api_id: int = 0
    api_hash: str = ""
    db_path: str = "data/users.json"

    @classmethod
    def load(cls) -> Config:
        _load_env()
        try:
            api_id = int(os.getenv("TG_API_ID", "0"))
        except ValueError:
            api_id = 0
        return cls(
            bot_token=os.getenv("BOT_TOKEN", "").strip(),
            api_id=api_id,
            api_hash=os.getenv("TG_API_HASH", "").strip(),
            db_path=os.getenv("DB_PATH", "data/users.json"),
        )

    def validate(self) -> list[str]:
        errs = []
        if not self.bot_token:
            errs.append("BOT_TOKEN не задан")
        if not self.api_id:
            errs.append("TG_API_ID не задан")
        if not self.api_hash:
            errs.append("TG_API_HASH не задан")
        return errs
