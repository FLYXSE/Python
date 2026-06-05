START_TEXT = (
    "<b>🎲 Добропожаловать в MemDice!</b>\n\n"
    "<b>Правила Игры:</b>"
    "\n1. Кидайте кубик 🎲 и зарабатывайте очки."
    "\n2. Смотрите свой баланс командой /balance"
    "\n3. Смотрите Топ 5 игроков командой /top"
    "\n4. Смотрите свою статистику командой /statistics"
)

FAIR_PLAY_TEXT = "🚫 <b>Давай играть честно.</b>"
ANTISPAM_TEXT = "⏱️ Подождите пока предыдущая игра закончится."

RESULTS_TEXT = (
    "🎰 <b>MemDice</b>\n\n"
    "🎲 Выпало: <b>{roll}</b>\n"
    "➕ Начислено: <b>{roll} 🧅</b>\n"
    "💰 В мешке: <b>{balance} 🧅</b>"
)

BALANCE_TEXT = (
    "🎰 <b>MemDice</b>\n\n"
    "💰 В вашем мешке <b>{balance} 🧅</b>"
)

STATISTICS_TEXT = (
    "📊 <b>Статистика игрока @{username}</b>\n"
    " ⌛️ Первый бросок: {first}\n"
    " ⏳ Последний бросок: {last}\n"
    " 💰 В мешке: {balance} 🧅\n"
    " 🎲 Всего бросков: {rolls} раз(-а)"
)

TOP_HEADER = "🏆 <b>Топ 5 игроков</b>\n\n"


PLAYER_NOT_FOUND = "❌ Игрок не найден"
BAN_DONE = "🚫 <b>Игрок забанен</b>"
UNBAN_DONE = "🔓 <b>Игрок разбанен</b>"
UNBAN_NOT_BANNED = "ℹ <b>Игрок не находится в бане</b>"

RESET_CONFIRM = "⚠ <b>Подтвердите сброс баланса</b>"
RESET_DONE = "♻ <b>Баланс сброшен</b>"
RESET_CANCEL = "❌ <b>Отменено</b>"
RESET_DENY = "❌ Не для тебя"

ADMIN_DONE = "✅ Готово"