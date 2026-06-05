from __future__ import annotations

PRESETS: dict[str, dict] = {
    "typing": {
        "name": "Печатает...",
        "desc": "Имя появляется по буквам",
        "speed": 0.4,
        "builder": "typing",
    },
    "wave": {
        "name": "Волна",
        "desc": "Буквы поднимаются волной",
        "speed": 0.5,
        "builder": "wave",
    },
    "glitch": {
        "name": "Глитч",
        "desc": "Случайные символы заменяют буквы",
        "speed": 0.3,
        "builder": "glitch",
    },
    "bounce": {
        "name": "Прыжки",
        "desc": "Буквы прыгают вверх-вниз",
        "speed": 0.4,
        "builder": "bounce",
    },
    "snake": {
        "name": "Змейка",
        "desc": "Текст ползёт как змейка",
        "speed": 0.5,
        "builder": "snake",
    },
    "fade": {
        "name": "Затухание",
        "desc": "Буквы появляются и исчезают",
        "speed": 0.6,
        "builder": "fade",
    },
    "rotate": {
        "name": "Ротация",
        "desc": "Текст сдвигается по кругу",
        "speed": 0.5,
        "builder": "rotate",
    },
    "sparkle": {
        "name": "Искры",
        "desc": "Эмодзи-искры вокруг текста",
        "speed": 0.6,
        "builder": "sparkle",
    },
    "matrix": {
        "name": "Матрица",
        "desc": "Символы как в Matrix",
        "speed": 0.2,
        "builder": "matrix",
    },
    "heartbeat": {
        "name": "Сердцебиение",
        "desc": "Пульсация сердечками",
        "speed": 0.7,
        "builder": "heartbeat",
    },
    "clock": {
        "name": "Часы",
        "desc": "Текущее время в нике",
        "speed": 1.0,
        "builder": "clock",
    },
    "countdown": {
        "name": "Обратный отсчёт",
        "desc": "Отсчёт до нуля",
        "speed": 1.0,
        "builder": "countdown",
    },
}


def list_presets() -> list[tuple[str, str, str]]:
    return [(k, v["name"], v["desc"]) for k, v in PRESETS.items()]


def get_preset(key: str) -> dict | None:
    return PRESETS.get(key)
