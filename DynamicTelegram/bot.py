import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
    BotCommand,
)
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import Config, ROOT
from storage import UserDB
from presets import list_presets, get_preset
import runner

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("bot")

cfg = Config.load()
db = UserDB(cfg.db_path)
bot = Bot(token=cfg.bot_token)
dp = Dispatcher()
router = Router()
dp.include_router(router)


class AuthStates(StatesGroup):
    phone = State()
    code = State()
    password = State()


class CustomStates(StatesGroup):
    text = State()
    frames = State()
    speed = State()


class SettingsStates(StatesGroup):
    prefix = State()
    suffix = State()
    separator = State()
    weather_city = State()


# ── keyboards ──

def kb_main(user_id: int) -> InlineKeyboardMarkup:
    user = db.get(user_id)
    running = runner.is_running(user_id)
    auth = user.get("authorized", False)

    rows = []
    if not auth:
        rows.append([InlineKeyboardButton(text="🔑 войти в аккаунт", callback_data="auth")])
    else:
        if running:
            rows.append([InlineKeyboardButton(text="⏹ остановить", callback_data="stop")])
        else:
            rows.append([InlineKeyboardButton(text="🎬 анимации", callback_data="presets")])
            rows.append([InlineKeyboardButton(text="✏️ свои кадры", callback_data="custom")])

        rows.append([
            InlineKeyboardButton(text="⚙️ настройки", callback_data="settings"),
            InlineKeyboardButton(text="📊 статус", callback_data="status"),
        ])
        rows.append([InlineKeyboardButton(text="🚪 выйти", callback_data="logout")])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_presets() -> InlineKeyboardMarkup:
    rows = []
    items = list_presets()
    for i in range(0, len(items), 2):
        row = []
        for key, name, _ in items[i:i+2]:
            row.append(InlineKeyboardButton(text=name, callback_data=f"preset:{key}"))
        rows.append(row)
    rows.append([InlineKeyboardButton(text="← назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_speed() -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text="⚡ 0.3с", callback_data="speed:0.3"),
            InlineKeyboardButton(text="🔥 0.5с", callback_data="speed:0.5"),
            InlineKeyboardButton(text="⏱ 1.0с", callback_data="speed:1.0"),
        ],
        [
            InlineKeyboardButton(text="🐌 2.0с", callback_data="speed:2.0"),
            InlineKeyboardButton(text="🐢 3.0с", callback_data="speed:3.0"),
        ],
        [InlineKeyboardButton(text="← назад", callback_data="presets")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_settings() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="🕐 время в нике", callback_data="set:time")],
        [InlineKeyboardButton(text="⏰ формат времени", callback_data="set:time_format")],
        [InlineKeyboardButton(text="🕐 эмодзи часов", callback_data="set:emoji_clock")],
        [InlineKeyboardButton(text="📝 префикс", callback_data="set:prefix")],
        [InlineKeyboardButton(text="📝 суффикс", callback_data="set:suffix")],
        [InlineKeyboardButton(text="➖ разделитель", callback_data="set:separator")],
        [InlineKeyboardButton(text="← назад", callback_data="back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← назад", callback_data="back")]
    ])


def kb_confirm_logout() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="да, выйти", callback_data="logout_confirm"),
            InlineKeyboardButton(text="отмена", callback_data="back"),
        ]
    ])


# ── helpers ──

def _status_text(user_id: int) -> str:
    user = db.get(user_id)
    running = runner.is_running(user_id)
    auth = user.get("authorized", False)
    preset = user.get("current_preset", "")
    speed = user.get("speed", 1.0)
    s = user.get("settings", {})

    lines = []
    lines.append(f"авторизация: {'да' if auth else 'нет'}")
    lines.append(f"анимация: {'работает' if running else 'остановлена'}")
    if preset:
        p = get_preset(preset)
        lines.append(f"пресет: {p['name'] if p else preset}")
    lines.append(f"скорость: {speed}с")

    if s.get("prefix"):
        lines.append(f"префикс: {s['prefix']}")
    if s.get("suffix"):
        lines.append(f"суффикс: {s['suffix']}")
    if s.get("show_time"):
        fmt = "12h" if s.get("time_format") == "12h" else "24h"
        lines.append(f"время: вкл ({fmt})")
    if s.get("show_emoji_clock"):
        lines.append("эмодзи часов: вкл")

    return "\n".join(lines)


# ── handlers ──

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    user = db.get(message.from_user.id)

    text = (
        "анимированный ник в телеграме\n\n"
        "меняет имя аккаунта с анимацией\n"
        "12 пресетов + свои кадры\n\n"
        "⚠️ используй на втором аккаунте"
    )
    await message.answer(text, reply_markup=kb_main(message.from_user.id))


# ── auth ──

@router.callback_query(F.data == "auth")
async def cb_auth(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AuthStates.phone)
    await cb.message.edit_text(
        "введи номер телефона второго аккаунта\n"
        "формат: +79991234567\n\n"
        "⚠️ не используй основной аккаунт",
        reply_markup=kb_back(),
    )
    await cb.answer()


@router.message(AuthStates.phone)
async def auth_phone(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()
    if not phone.startswith("+") or len(phone) < 10:
        await message.answer("неверный формат, нужно: +79991234567")
        return

    await state.update_data(phone=phone)

    try:
        await runner.authorize(message.from_user.id, cfg.api_id, cfg.api_hash, phone)
        await state.set_state(AuthStates.code)
        await message.answer(
            f"код отправлен на {phone}\nвведи его:",
            reply_markup=kb_back(),
        )
    except Exception as exc:
        await message.answer(f"ошибка: {str(exc)[:100]}", reply_markup=kb_back())
        await state.clear()


@router.message(AuthStates.code)
async def auth_code(message: Message, state: FSMContext) -> None:
    code = message.text.strip().replace(" ", "").replace("-", "")
    data = await state.get_data()
    phone = data.get("phone", "")

    ok, info = await runner.submit_code(message.from_user.id, phone, code)
    if ok:
        db.set(message.from_user.id, phone=phone, authorized=True, session=f"sessions/{message.from_user.id}")
        await message.answer(
            f"авторизован: {info}\n\n⚠️ это второй аккаунт, верно?",
            reply_markup=kb_main(message.from_user.id),
        )
        await state.clear()
    elif "2FA" in info or "пароль" in info:
        await state.set_state(AuthStates.password)
        await state.update_data(code=code)
        await message.answer("введи пароль 2FA:", reply_markup=kb_back())
    else:
        await message.answer(f"ошибка: {info}\nпопробуй ещё раз:")


@router.message(AuthStates.password)
async def auth_password(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    phone = data.get("phone", "")
    code = data.get("code", "")
    password = message.text.strip()

    ok, info = await runner.submit_code(message.from_user.id, phone, code, password)
    if ok:
        db.set(message.from_user.id, phone=phone, authorized=True, session=f"sessions/{message.from_user.id}")
        await message.answer(f"авторизован: {info}", reply_markup=kb_main(message.from_user.id))
        await state.clear()
    else:
        await message.answer(f"ошибка: {info}", reply_markup=kb_back())
        await state.clear()


# ── presets ──

@router.callback_query(F.data == "presets")
async def cb_presets(cb: CallbackQuery) -> None:
    items = list_presets()
    lines = ["выбери анимацию:\n"]
    for key, name, desc in items:
        lines.append(f"{name} — {desc}")
    await cb.message.edit_text("\n".join(lines), reply_markup=kb_presets())
    await cb.answer()


@router.callback_query(F.data.startswith("preset:"))
async def cb_preset_select(cb: CallbackQuery, state: FSMContext) -> None:
    key = cb.data.split(":", 1)[1]
    preset = get_preset(key)
    if not preset:
        await cb.answer("не найден")
        return

    await state.update_data(preset_key=key)
    db.set(cb.from_user.id, current_preset=key)

    await cb.message.edit_text(
        f"пресет: {preset['name']}\n{preset['desc']}\n\nвыбери скорость:",
        reply_markup=kb_speed(),
    )
    await cb.answer()


@router.callback_query(F.data.startswith("speed:"))
async def cb_speed_select(cb: CallbackQuery, state: FSMContext) -> None:
    speed = float(cb.data.split(":", 1)[1])
    data = await state.get_data()
    preset_key = data.get("preset_key", db.get(cb.from_user.id).get("current_preset", ""))
    user = db.get(cb.from_user.id)

    if not preset_key:
        await cb.answer("сначала выбери пресет")
        return

    db.set(cb.from_user.id, speed=speed)

    name = await runner.get_current_name(cb.from_user.id)
    if not name:
        name = "User"

    s = user.get("settings", {})

    ok, info = await runner.start_animation(
        user_id=cb.from_user.id,
        text=name,
        preset_key=preset_key,
        speed=speed,
        prefix=s.get("prefix", ""),
        suffix=s.get("suffix", ""),
        separator=s.get("separator", " | "),
        show_time=s.get("show_time", False),
        time_format=s.get("time_format", "24h"),
        show_emoji_clock=s.get("show_emoji_clock", False),
    )

    db.set(cb.from_user.id, animation_running=ok)

    if ok:
        await cb.message.edit_text(
            f"запущено\n{info}",
            reply_markup=kb_main(cb.from_user.id),
        )
    else:
        await cb.message.edit_text(f"ошибка: {info}", reply_markup=kb_main(cb.from_user.id))
    await cb.answer()


# ── custom frames ──

@router.callback_query(F.data == "custom")
async def cb_custom(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(CustomStates.frames)
    await cb.message.edit_text(
        "отправь кадры анимации\n"
        "каждая строка = один кадр\n\n"
        "пример:\n"
        "привет\n"
        "п р и в е т\n"
        "ПРИВЕТ\n"
        "✨привет✨",
        reply_markup=kb_back(),
    )
    await cb.answer()


@router.message(CustomStates.frames)
async def custom_frames(message: Message, state: FSMContext) -> None:
    lines = [ln.strip() for ln in message.text.strip().splitlines() if ln.strip()]
    if len(lines) < 2:
        await message.answer("нужно минимум 2 кадра")
        return
    if len(lines) > 100:
        lines = lines[:100]

    await state.update_data(custom_frames=lines)
    await state.set_state(CustomStates.speed)
    await message.answer(
        f"получено {len(lines)} кадров\n\n"
        "введи скорость (секунды между кадрами)\n"
        "например: 0.5",
    )


@router.message(CustomStates.speed)
async def custom_speed(message: Message, state: FSMContext) -> None:
    try:
        speed = float(message.text.strip())
        if speed < 0.1:
            speed = 0.1
        if speed > 10:
            speed = 10
    except ValueError:
        await message.answer("введи число, например 0.5")
        return

    data = await state.get_data()
    frames = data.get("custom_frames", [])

    db.set(message.from_user.id, custom_frames=frames, speed=speed, current_preset="custom")

    ok, info = await runner.start_animation(
        user_id=message.from_user.id,
        text="",
        preset_key="custom",
        speed=speed,
        custom_frames=frames,
    )

    db.set(message.from_user.id, animation_running=ok)
    await state.clear()

    if ok:
        await message.answer(f"запущено\n{info}", reply_markup=kb_main(message.from_user.id))
    else:
        await message.answer(f"ошибка: {info}", reply_markup=kb_main(message.from_user.id))


# ── stop ──

@router.callback_query(F.data == "stop")
async def cb_stop(cb: CallbackQuery) -> None:
    was_running = runner.stop_animation(cb.from_user.id)

    name = await runner.get_current_name(cb.from_user.id)
    if name:
        await runner.restore_name(cb.from_user.id, name.split("|")[0].strip() if "|" in name else name)

    db.set(cb.from_user.id, animation_running=False)
    await cb.message.edit_text(
        "анимация остановлена" if was_running else "анимация не запущена",
        reply_markup=kb_main(cb.from_user.id),
    )
    await cb.answer()


# ── settings ──

@router.callback_query(F.data == "settings")
async def cb_settings(cb: CallbackQuery) -> None:
    user = db.get(cb.from_user.id)
    s = user.get("settings", {})

    lines = [
        "настройки:\n",
        f"время: {'вкл' if s.get('show_time') else 'выкл'}",
        f"формат: {s.get('time_format', '24h')}",
        f"эмодзи часов: {'вкл' if s.get('show_emoji_clock') else 'выкл'}",
        f"префикс: {s.get('prefix') or '—'}",
        f"суффикс: {s.get('suffix') or '—'}",
        f"разделитель: {s.get('separator', ' | ')}",
    ]

    await cb.message.edit_text("\n".join(lines), reply_markup=kb_settings())
    await cb.answer()


@router.callback_query(F.data == "set:time")
async def cb_set_time(cb: CallbackQuery) -> None:
    current = db.get_setting(cb.from_user.id, "show_time") or False
    db.set_setting(cb.from_user.id, "show_time", not current)
    await cb.answer(f"время: {'вкл' if not current else 'выкл'}")
    await cb_settings(cb)


@router.callback_query(F.data == "set:time_format")
async def cb_set_time_format(cb: CallbackQuery) -> None:
    current = db.get_setting(cb.from_user.id, "time_format") or "24h"
    new = "12h" if current == "24h" else "24h"
    db.set_setting(cb.from_user.id, "time_format", new)
    await cb.answer(f"формат: {new}")
    await cb_settings(cb)


@router.callback_query(F.data == "set:emoji_clock")
async def cb_set_emoji_clock(cb: CallbackQuery) -> None:
    current = db.get_setting(cb.from_user.id, "show_emoji_clock") or False
    db.set_setting(cb.from_user.id, "show_emoji_clock", not current)
    await cb.answer(f"эмодзи: {'вкл' if not current else 'выкл'}")
    await cb_settings(cb)


@router.callback_query(F.data == "set:prefix")
async def cb_set_prefix(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingsStates.prefix)
    await cb.message.edit_text("введи префикс (текст перед ником)\nили отправь - чтобы убрать:", reply_markup=kb_back())
    await cb.answer()


@router.message(SettingsStates.prefix)
async def set_prefix(message: Message, state: FSMContext) -> None:
    val = "" if message.text.strip() == "-" else message.text.strip()[:20]
    db.set_setting(message.from_user.id, "prefix", val)
    await state.clear()
    await message.answer(f"префикс: {val or 'убран'}", reply_markup=kb_main(message.from_user.id))


@router.callback_query(F.data == "set:suffix")
async def cb_set_suffix(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingsStates.suffix)
    await cb.message.edit_text("введи суффикс (текст после ника)\nили отправь - чтобы убрать:", reply_markup=kb_back())
    await cb.answer()


@router.message(SettingsStates.suffix)
async def set_suffix(message: Message, state: FSMContext) -> None:
    val = "" if message.text.strip() == "-" else message.text.strip()[:20]
    db.set_setting(message.from_user.id, "suffix", val)
    await state.clear()
    await message.answer(f"суффикс: {val or 'убран'}", reply_markup=kb_main(message.from_user.id))


@router.callback_query(F.data == "set:separator")
async def cb_set_separator(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SettingsStates.separator)
    await cb.message.edit_text("введи разделитель между элементами\nпо умолчанию: ' | '", reply_markup=kb_back())
    await cb.answer()


@router.message(SettingsStates.separator)
async def set_separator(message: Message, state: FSMContext) -> None:
    val = message.text.strip()[:10]
    db.set_setting(message.from_user.id, "separator", val)
    await state.clear()
    await message.answer(f"разделитель: '{val}'", reply_markup=kb_main(message.from_user.id))


# ── status ──

@router.callback_query(F.data == "status")
async def cb_status(cb: CallbackQuery) -> None:
    text = _status_text(cb.from_user.id)
    await cb.message.edit_text(text, reply_markup=kb_back())
    await cb.answer()


# ── logout ──

@router.callback_query(F.data == "logout")
async def cb_logout(cb: CallbackQuery) -> None:
    await cb.message.edit_text("точно выйти из аккаунта?", reply_markup=kb_confirm_logout())
    await cb.answer()


@router.callback_query(F.data == "logout_confirm")
async def cb_logout_confirm(cb: CallbackQuery) -> None:
    await runner.disconnect(cb.from_user.id)
    db.set(cb.from_user.id, authorized=False, animation_running=False, phone="", current_preset="")
    await cb.message.edit_text("вышел из аккаунта", reply_markup=kb_main(cb.from_user.id))
    await cb.answer()


# ── back ──

@router.callback_query(F.data == "back")
async def cb_back(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.message.edit_text(
        "анимированный ник в телеграме\n\n⚠️ используй на втором аккаунте",
        reply_markup=kb_main(cb.from_user.id),
    )
    await cb.answer()


# ── main ──

async def main() -> None:
    errors = cfg.validate()
    if errors:
        for e in errors:
            log.error("config: %s", e)
        print("\nзаполни .env:")
        print("  BOT_TOKEN=...")
        print("  TG_API_ID=...")
        print("  TG_API_HASH=...")
        sys.exit(1)

    print("=" * 45)
    print("  animated nick bot")
    print("  funpay/klumik")
    print("=" * 45)
    print()
    print("  ⚠️  предупреждение:")
    print("  используйте только на вторых аккаунтах")
    print("  telegram может ограничить аккаунт")
    print("  за частую смену имени")
    print()
    print("=" * 45)

    await bot.set_my_commands([
        BotCommand(command="start", description="главное меню"),
    ])

    log.info("бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("остановлен")
