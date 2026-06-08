# ===== Start =====
START_WELCOME = (
    "<b><tg-emoji emoji-id='5404523117114556417'>🎲</tg-emoji> MemDice</b>\n\n"
    "<tg-emoji emoji-id='5402209078929784833'>🎁</tg-emoji> Добро пожаловать! Испытай удачу!\n"
    "<tg-emoji emoji-id='5404799910576914433'>🗂</tg-emoji> Главное Меню:"
)

MAIN_MENU = (
    "<b><tg-emoji emoji-id='5404523117114556417'>🎲</tg-emoji> MemDice</b>\n\n"
    "<tg-emoji emoji-id='5404799910576914433'>🗂</tg-emoji> Главное Меню:"
)

# ===== Profile =====
USER_NOT_FOUND = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Пользователь не найден"

PROFILE_TEXT = (
    "<b><tg-emoji emoji-id='5402386134661595137'>👤</tg-emoji> Профиль</b>\n\n"
    "<tg-emoji emoji-id='5404514819237740545'>👛</tg-emoji> Баланс: <code>{balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n"
    "<tg-emoji emoji-id='5404523117114556417'>🎲</tg-emoji> Сыграно игр: {total_games}\n"
    "<tg-emoji emoji-id='5404547899075854337'>👑</tg-emoji> Побед: {total_wins}\n"
    "<tg-emoji emoji-id='5404618993669505025'>💎</tg-emoji> Коэффициент выигрышей: <code>{ratio}</code>"
)

# ===== Deposit =====
DEPOSIT_PROMPT = (
    "<tg-emoji emoji-id='5402386134661595137'>👤</tg-emoji> <b>Пополнение баланса</b>\n\n"
    "<tg-emoji emoji-id='5404872276480884737'>➡</tg-emoji> Введите сумму в <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT (минимум 1 USDT):\n"
    "<tg-emoji emoji-id='5404334499330785281'>📌</tg-emoji> Пример: <code>5</code> или <code>10.5</code>"
)

INVALID_NUMBER = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Введите корректное число."
MIN_DEPOSIT = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Минимальная сумма пополнения — 1 <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT."
TX_ERROR = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Ошибка создания транзакции."
INVOICE_ERROR = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Ошибка создания счета. Попробуйте позже."

INVOICE_CREATED = (
    "<tg-emoji emoji-id='5404514819237740545'>👛</tg-emoji> <b>Счет создан!</b>\n\n"
    "<tg-emoji emoji-id='5404387559356760065'>⭐</tg-emoji> Сумма: <code>{amount}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n"
    "<tg-emoji emoji-id='5404442457628737537'>⏲</tg-emoji> Статус: ожидает оплаты\n\n"
    "<tg-emoji emoji-id='5404762329613074433'>💎</tg-emoji> <a href='{link}'>Перейти к оплате</a>\n\n"
    "<tg-emoji emoji-id='5402567146058285057'>✔</tg-emoji> После оплаты баланс обновится автоматически."
)

# ===== Withdraw =====
WITHDRAW_ASK_ID = (
    "<tg-emoji emoji-id='5404436612178247681'>👤</tg-emoji> Укажите ваш ID.\n\n"
    "<tg-emoji emoji-id='5404334499330785281'>📌</tg-emoji> Его можно узнать у бота @ChatIDBot\n\n"
    "<tg-emoji emoji-id='5404872276480884737'>➡</tg-emoji> Введите Ваш ID:"
)

INVALID_TARGET_ID = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> ID должен быть числом. Попробуйте снова."

SETID_USAGE = (
    "<tg-emoji emoji-id='5404872276480884737'>➡</tg-emoji> Использование: /setid <ваш ID>\n\n"
    "<tg-emoji emoji-id='5404334499330785281'>📌</tg-emoji> Пример: <code>/setid 123456789</code>"
)

SETID_DONE = "<tg-emoji emoji-id='5402391610744897537'>✅</tg-emoji> ID <code>{cryptopay_id}</code> сохранён."

WITHDRAW_INSUFFICIENT = (
    "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> <b>Недостаточно средств</b>\n\n"
    "<tg-emoji emoji-id='5404514819237740545'>👛</tg-emoji> Ваш баланс: <code>{balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n"
    "<tg-emoji emoji-id='5404387559356760065'>⭐</tg-emoji> Минимальная сумма вывода: <code>15</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT"
)

WITHDRAW_PROMPT = (
    "<tg-emoji emoji-id='5404709733443567617'>⭐</tg-emoji> <b>Вывод средств</b>\n\n"
    "<tg-emoji emoji-id='5404514819237740545'>👛</tg-emoji> Ваш баланс: <code>{balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n"
    "<tg-emoji emoji-id='5404872276480884737'>➡</tg-emoji> Введите сумму для вывода (минимум 15 <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT):"
)

WITHDRAW_MIN = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Минимальная сумма вывода — 15 <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT."

WITHDRAW_NO_FUNDS = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Недостаточно средств. Баланс: <code>{balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT"

WITHDRAW_NO_CRYPTOPAY_ID = (
    "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> <b>CryptoPay ID не найден</b>\n\n"
    "<tg-emoji emoji-id='5404334499330785281'>📌</tg-emoji> Совершите хотя бы одно пополнение через депозит,\n"
    "<tg-emoji emoji-id='5404334499330785281'>📌</tg-emoji> чтобы бот запомнил ваш ID."
)

WITHDRAW_CONFIRM = (
    "<tg-emoji emoji-id='5404387559356760065'>⭐</tg-emoji> Сумма: <code>{amount}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n\n"
    "<tg-emoji emoji-id='5402209839138996225'>👤</tg-emoji>Вывод будет выполнен на ваш ID."
)

WITHDRAW_NO_FUNDS_SHORT = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Недостаточно средств."
WITHDRAW_ERROR = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Ошибка вывода. Попробуйте позже."

WITHDRAW_SUCCESS = (
    "<tg-emoji emoji-id='5402391610744897537'>✅</tg-emoji> <b>Вывод выполнен!</b>\n\n"
    "<tg-emoji emoji-id='5404387559356760065'>⭐</tg-emoji> Сумма: <code>{amount}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n"
    "<tg-emoji emoji-id='5404514819237740545'>👛</tg-emoji> Новый баланс: <code>{new_balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT"
)

# ===== Game rules =====
GAME_RULES = (
    "<b><tg-emoji emoji-id='5404523117114556417'>🎲</tg-emoji> Правила игры в Dice</b>\n\n"
    "Бот кидает кубик (1-6). Результаты:\n\n"
    "<tg-emoji emoji-id='5404769944590090241'>1⃣</tg-emoji> — Проигрыш (ставка сгорает)\n"
    "<tg-emoji emoji-id='5404402544497655809'>2⃣</tg-emoji> — Проигрыш (ставка сгорает)\n"
    "<tg-emoji emoji-id='5402402691760521217'>3⃣</tg-emoji> — Возврат ставки (1x)\n"
    "<tg-emoji emoji-id='5404697943758340097'>4⃣</tg-emoji> — Выигрыш 1.5x\n"
    "<tg-emoji emoji-id='5404577925192220673'>5⃣</tg-emoji> — Выигрыш 2x\n"
    "<tg-emoji emoji-id='5404407299026452481'>6⃣</tg-emoji> — ДЖЕКПОТ 4x\n\n"
    "<tg-emoji emoji-id='5402347462776061953'>🎞</tg-emoji> Нажми <b>«Начать»</b> чтобы сыграть!"
)

GAME_NO_BALANCE = (
    "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> <b>Недостаточно средств!</b>\n\n"
    "<tg-emoji emoji-id='5404514819237740545'>👛</tg-emoji> Ваш баланс: <code>{balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n"
    "<tg-emoji emoji-id='5404334499330785281'>📌</tg-emoji> Пополните баланс в <b>Профиле</b>."
)

GAME_BET_PROMPT = (
    "<tg-emoji emoji-id='5404514819237740545'>👛</tg-emoji> Ваш баланс: <code>{balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n\n"
    "<tg-emoji emoji-id='5404872276480884737'>➡</tg-emoji> Введите сумму ставки:"
)

GAME_BET_ZERO = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Ставка должна быть больше 0."

GAME_NO_BALANCE_SHORT = "<tg-emoji emoji-id='5402156585839493121'>❌</tg-emoji> Недостаточно средств. Баланс: <code>{balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT"

GAME_RESULT_TEMPLATE = (
    "<tg-emoji emoji-id='5404523117114556417'>🎲</tg-emoji> <b>Результат:</b>\n\n"
    "{result_line}\n\n"
    "<tg-emoji emoji-id='5404619844073029633'>⚡</tg-emoji> Ставка: <code>{bet}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n"
    "<tg-emoji emoji-id='5404820603729346561'>📈</tg-emoji> Множитель: <code>{multiplier}x</code>\n"
    "{win_line}"
    "<tg-emoji emoji-id='5404514819237740545'>👛</tg-emoji> Баланс: <code>{balance}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT"
)

ROLL_RESULTS = {
    1: "<b><tg-emoji emoji-id='5404769944590090241'>1⃣</tg-emoji></b> — Проигрыш!",
    2: "<b><tg-emoji emoji-id='5404402544497655809'>2⃣</tg-emoji></b> — Проигрыш!",
    3: "<b><tg-emoji emoji-id='5402402691760521217'>3⃣</tg-emoji></b> — Возврат ставки.",
    4: "<b><tg-emoji emoji-id='5404697943758340097'>4⃣</tg-emoji></b> — Выигрыш <b>1.5x</b>!",
    5: "<b><tg-emoji emoji-id='5404577925192220673'>5⃣</tg-emoji></b> — Выигрыш <b>2x</b>!",
    6: "<b><tg-emoji emoji-id='5404407299026452481'>6⃣</tg-emoji></b> — ДЖЕКПОТ <b>4x</b>!",
}

MULTIPLIERS = {1: 0, 2: 0, 3: 1, 4: 1.5, 5: 2, 6: 4}

# ===== Invoice checker =====
DEPOSIT_CONFIRMED = (
    "<tg-emoji emoji-id='5402391610744897537'>✅</tg-emoji> <b>Пополнение подтверждено!</b>\n\n"
    "<tg-emoji emoji-id='5404387559356760065'>⭐</tg-emoji> Сумма: <code>{amount}</code> <tg-emoji emoji-id='5226943850265706497'>💲</tg-emoji> USDT\n"
)
