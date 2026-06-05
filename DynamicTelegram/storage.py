from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any, Optional


_DEFAULT_USER = {
    "phone": "",
    "session": "",
    "authorized": False,
    "animation_running": False,
    "current_preset": "",
    "speed": 1.0,
    "custom_frames": [],
    "settings": {
        "show_time": False,
        "time_format": "24h",
        "show_date": False,
        "show_emoji_clock": False,
        "show_weather": False,
        "weather_city": "",
        "prefix": "",
        "suffix": "",
        "separator": " | ",
    },
}


class UserDB:
    def __init__(self, path: str = "data/users.json") -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._data: dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            try:
                self._data = json.loads(self._path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self._data = {}

    def _save(self) -> None:
        with self._lock:
            self._path.write_text(
                json.dumps(self._data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    def get(self, user_id: int) -> dict:
        key = str(user_id)
        if key not in self._data:
            self._data[key] = json.loads(json.dumps(_DEFAULT_USER))
            self._save()
        return self._data[key]

    def set(self, user_id: int, **kwargs: Any) -> None:
        key = str(user_id)
        if key not in self._data:
            self._data[key] = json.loads(json.dumps(_DEFAULT_USER))
        for k, v in kwargs.items():
            if k == "settings" and isinstance(v, dict):
                self._data[key].setdefault("settings", {}).update(v)
            else:
                self._data[key][k] = v
        self._save()

    def get_setting(self, user_id: int, key: str) -> Any:
        return self.get(user_id).get("settings", {}).get(key)

    def set_setting(self, user_id: int, key: str, value: Any) -> None:
        user = self.get(user_id)
        user.setdefault("settings", {})
        user["settings"][key] = value
        self._save()

    def all_users(self) -> list[int]:
        return [int(k) for k in self._data.keys()]

    def delete(self, user_id: int) -> None:
        key = str(user_id)
        if key in self._data:
            del self._data[key]
            self._save()
