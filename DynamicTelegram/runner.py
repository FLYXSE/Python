from __future__ import annotations

import asyncio
import logging
from typing import Optional

from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors import FloodWaitError

from animator import build_frames
from presets import get_preset

log = logging.getLogger("runner")

_active_tasks: dict[int, asyncio.Task] = {}
_clients: dict[int, TelegramClient] = {}


async def authorize(user_id: int, api_id: int, api_hash: str, phone: str, session_dir: str = "sessions") -> TelegramClient:
    import os
    os.makedirs(session_dir, exist_ok=True)
    session_path = f"{session_dir}/{user_id}"
    client = TelegramClient(session_path, api_id, api_hash)
    client.session.set_dc(2, '149.154.167.40', 80)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
    _clients[user_id] = client
    return client


async def submit_code(user_id: int, phone: str, code: str, password: str = "") -> tuple[bool, str]:
    client = _clients.get(user_id)
    if not client:
        return False, "клиент не найден"
    try:
        await client.sign_in(phone=phone, code=code)
        me = await client.get_me()
        return True, f"{me.first_name} (@{me.username or '-'})"
    except Exception as exc:
        err = str(exc).lower()
        if "two-steps" in err or "2fa" in err or "password" in err:
            if password:
                try:
                    await client.sign_in(password=password)
                    me = await client.get_me()
                    return True, f"{me.first_name} (@{me.username or '-'})"
                except Exception as e2:
                    return False, f"ошибка 2FA: {e2}"
            return False, "нужен пароль 2FA"
        return False, str(exc)[:100]


async def start_animation(
    user_id: int,
    text: str,
    preset_key: str,
    speed: float = 1.0,
    custom_frames: list[str] | None = None,
    prefix: str = "",
    suffix: str = "",
    separator: str = " | ",
    show_time: bool = False,
    time_format: str = "24h",
    show_emoji_clock: bool = False,
) -> tuple[bool, str]:
    client = _clients.get(user_id)
    if not client or not client.is_connected():
        return False, "аккаунт не подключён"

    if not await client.is_user_authorized():
        return False, "аккаунт не авторизован"

    stop_animation(user_id)

    preset = get_preset(preset_key)
    if not preset and not custom_frames:
        return False, "пресет не найден"

    if custom_frames:
        frames = custom_frames
        actual_speed = speed
    else:
        builder = preset["builder"]
        actual_speed = speed or preset.get("speed", 0.5)
        frames = build_frames(
            builder=builder,
            text=text,
            frame_count=30,
            prefix=prefix,
            suffix=suffix,
            separator=separator,
            show_time=show_time,
            time_format=time_format,
            show_emoji_clock=show_emoji_clock,
        )

    if not frames:
        return False, "нет кадров"

    task = asyncio.create_task(_animation_loop(user_id, client, frames, actual_speed, text, preset_key))
    _active_tasks[user_id] = task
    return True, f"запущено ({len(frames)} кадров, {actual_speed}с)"


def stop_animation(user_id: int) -> bool:
    task = _active_tasks.pop(user_id, None)
    if task and not task.done():
        task.cancel()
        return True
    return False


def is_running(user_id: int) -> bool:
    task = _active_tasks.get(user_id)
    return task is not None and not task.done()


async def restore_name(user_id: int, original_name: str) -> bool:
    client = _clients.get(user_id)
    if not client:
        return False
    try:
        await client(UpdateProfileRequest(first_name=original_name))
        return True
    except Exception:
        return False


async def disconnect(user_id: int) -> None:
    stop_animation(user_id)
    client = _clients.pop(user_id, None)
    if client and client.is_connected():
        await client.disconnect()


async def get_current_name(user_id: int) -> str:
    client = _clients.get(user_id)
    if not client:
        return ""
    try:
        me = await client.get_me()
        return me.first_name or ""
    except Exception:
        return ""


async def _animation_loop(
    user_id: int,
    client: TelegramClient,
    frames: list[str],
    speed: float,
    text: str,
    preset_key: str,
) -> None:
    log.info("[%d] animation start: preset=%s frames=%d speed=%.1f", user_id, preset_key, len(frames), speed)
    idx = 0
    errors = 0

    try:
        while True:
            frame = frames[idx % len(frames)]

            # для clock/countdown — пересобираем кадры каждый цикл
            if preset_key in ("clock",):
                from animator import build_frames as bf
                preset = get_preset(preset_key)
                if preset:
                    frames = bf(builder=preset["builder"], text=text, frame_count=30)

            try:
                await client(UpdateProfileRequest(first_name=frame))
                errors = 0
            except FloodWaitError as e:
                wait = e.seconds + 5
                log.warning("[%d] flood wait %ds", user_id, wait)
                await asyncio.sleep(wait)
                continue
            except Exception as exc:
                errors += 1
                log.error("[%d] err: %s", user_id, str(exc)[:60])
                if errors >= 10:
                    log.error("[%d] слишком много ошибок, стоп", user_id)
                    break
                await asyncio.sleep(5)
                continue

            idx += 1
            await asyncio.sleep(speed)

    except asyncio.CancelledError:
        log.info("[%d] animation stopped", user_id)
    except Exception as exc:
        log.error("[%d] animation crash: %s", user_id, exc)
    finally:
        _active_tasks.pop(user_id, None)
