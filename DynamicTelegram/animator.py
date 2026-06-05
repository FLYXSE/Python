from __future__ import annotations

import random
import string
from datetime import datetime, timedelta
from typing import Optional


_WAVE_UP = "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ qʳˢᵗᵘᵛʷˣʸᶻ"
_WAVE_CHARS = {chr(c): _WAVE_UP[i] if i < len(_WAVE_UP) else chr(c)
               for i, c in enumerate(range(ord('a'), ord('z') + 1))}

_GLITCH_CHARS = "█▓▒░╳╲╱┃┣┫▐▌◤◥◣◢"
_MATRIX_CHARS = "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ012345789"
_SPARKLE_EMOJI = ["✨", "⚡", "💫", "🌟", "⭐", "🔥", "💥", "🌸", "❄️", "🎯"]
_HEARTS = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "💖", "💗"]
_CLOCK_EMOJI = ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"]
_FADE_CHARS = ["░", "▒", "▓", "█"]


def build_frames(
    builder: str,
    text: str,
    frame_count: int = 30,
    prefix: str = "",
    suffix: str = "",
    separator: str = " | ",
    show_time: bool = False,
    time_format: str = "24h",
    show_emoji_clock: bool = False,
) -> list[str]:
    raw = _BUILDERS.get(builder, _build_typing)(text, frame_count)

    frames = []
    for frame in raw:
        parts = []
        if prefix:
            parts.append(prefix)

        if show_time:
            now = datetime.now()
            if time_format == "12h":
                t = now.strftime("%I:%M %p")
            else:
                t = now.strftime("%H:%M")
            if show_emoji_clock:
                h = now.hour % 12
                t = f"{_CLOCK_EMOJI[h]} {t}"
            parts.append(t)

        parts.append(frame)

        if suffix:
            parts.append(suffix)

        full = separator.join(parts) if len(parts) > 1 else parts[0]

        if len(full) > 64:
            full = full[:64]
        if len(full) < 1:
            full = text

        frames.append(full)

    return frames


def _build_typing(text: str, count: int) -> list[str]:
    frames = []
    for i in range(len(text) + 1):
        frames.append(text[:i] + "▌")
    frames.append(text)
    for _ in range(3):
        frames.append(text + "▌")
        frames.append(text)
    return frames


def _build_wave(text: str, count: int) -> list[str]:
    frames = []
    for offset in range(len(text) + 3):
        chars = []
        for i, ch in enumerate(text):
            if i == offset or i == offset - 1:
                upper = ch.upper()
                chars.append(upper)
            else:
                chars.append(ch.lower())
        frames.append("".join(chars))
    return frames


def _build_glitch(text: str, count: int) -> list[str]:
    frames = [text]
    for _ in range(count):
        chars = list(text)
        num_glitch = random.randint(1, max(1, len(text) // 3))
        positions = random.sample(range(len(text)), min(num_glitch, len(text)))
        for p in positions:
            chars[p] = random.choice(_GLITCH_CHARS)
        frames.append("".join(chars))
        frames.append(text)
    return frames


def _build_bounce(text: str, count: int) -> list[str]:
    frames = []
    for offset in range(len(text)):
        chars = []
        for i, ch in enumerate(text):
            if i == offset:
                chars.append(ch.upper())
            else:
                chars.append(ch.lower())
        frames.append("".join(chars))
    for offset in range(len(text) - 2, 0, -1):
        chars = []
        for i, ch in enumerate(text):
            if i == offset:
                chars.append(ch.upper())
            else:
                chars.append(ch.lower())
        frames.append("".join(chars))
    return frames


def _build_snake(text: str, count: int) -> list[str]:
    padded = "   " + text + "   "
    frames = []
    for i in range(len(padded)):
        start = i % len(padded)
        frame = (padded + padded)[start:start + len(text)]
        frames.append(frame.strip() or text)
    return frames


def _build_fade(text: str, count: int) -> list[str]:
    frames = []
    for i in range(len(text) + 1):
        visible = text[:i]
        hidden = "".join(random.choice(_FADE_CHARS) for _ in range(len(text) - i))
        frames.append(visible + hidden)
    frames.append(text)
    for i in range(len(text) + 1):
        visible = text[:len(text) - i]
        hidden = "".join(random.choice(_FADE_CHARS) for _ in range(i))
        frames.append(visible + hidden)
    return frames


def _build_rotate(text: str, count: int) -> list[str]:
    frames = []
    for i in range(len(text)):
        rotated = text[i:] + text[:i]
        frames.append(rotated)
    return frames


def _build_sparkle(text: str, count: int) -> list[str]:
    frames = []
    for _ in range(count):
        left = random.choice(_SPARKLE_EMOJI)
        right = random.choice(_SPARKLE_EMOJI)
        frames.append(f"{left} {text} {right}")
    return frames


def _build_matrix(text: str, count: int) -> list[str]:
    frames = []
    for step in range(count):
        chars = []
        for i, ch in enumerate(text):
            if random.random() < 0.3:
                chars.append(random.choice(_MATRIX_CHARS))
            else:
                chars.append(ch)
        frames.append("".join(chars))
    frames.append(text)
    return frames


def _build_heartbeat(text: str, count: int) -> list[str]:
    frames = []
    for i in range(count):
        h = _HEARTS[i % len(_HEARTS)]
        if i % 4 == 0:
            frames.append(f"{h} {text}")
        elif i % 4 == 1:
            frames.append(f"{h} {text} {h}")
        elif i % 4 == 2:
            frames.append(f"{text} {h}")
        else:
            frames.append(text)
    return frames


def _build_clock(text: str, count: int) -> list[str]:
    frames = []
    now = datetime.now()
    for i in range(60):
        t = (now + timedelta(seconds=i)).strftime("%H:%M:%S")
        h = (now + timedelta(seconds=i)).hour % 12
        frames.append(f"{_CLOCK_EMOJI[h]} {t} | {text}")
    return frames


def _build_countdown(text: str, count: int) -> list[str]:
    frames = []
    for i in range(count, 0, -1):
        frames.append(f"⏳ {i} | {text}")
    frames.append(f"🎉 {text}")
    return frames


_BUILDERS = {
    "typing": _build_typing,
    "wave": _build_wave,
    "glitch": _build_glitch,
    "bounce": _build_bounce,
    "snake": _build_snake,
    "fade": _build_fade,
    "rotate": _build_rotate,
    "sparkle": _build_sparkle,
    "matrix": _build_matrix,
    "heartbeat": _build_heartbeat,
    "clock": _build_clock,
    "countdown": _build_countdown,
}
