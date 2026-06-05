WELCOME = (
    "<tg-emoji emoji-id='5458771298547138561'>🎲</tg-emoji> <b>Добро пожаловать в MemDice!</b>\n\n"
    "Используйте кнопки меню <tg-emoji emoji-id='5195136499292569601'>👇</tg-emoji>"
)

SUBSCRIBE_PROMPT = (
    "<tg-emoji emoji-id='5197233456945299457'>🚫</tg-emoji> <b>Для использования бота необходимо подписаться на каналы:</b>\n\n"
    "<tg-emoji emoji-id='5194998910015242241'>🕔</tg-emoji> После подписки нажмите /start снова."
)

PROFILE_TEMPLATE = (
    "<tg-emoji emoji-id='5195154344881684481'>👤</tg-emoji> <b>Профиль игрока</b> @{username}\n\n"
    "<tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji> <b>Баланс:</b> {balance:,}\n"
    "<tg-emoji emoji-id='5195077439197282305'>📊</tg-emoji> <b>Всего игр:</b> {games}"
)

ABOUT = (
    "<tg-emoji emoji-id='5458771298547138561'>🎲</tg-emoji> <b>MemDice</b> - игровой бот основанный  на Dice.\n\n"
    "<tg-emoji emoji-id='5195078689032765441'>▶️</tg-emoji> Оплачивай бросок.\n"
    "<tg-emoji emoji-id='5195078689032765441'>▶️</tg-emoji> Получай выигрыш.\n"
    "<tg-emoji emoji-id='5195078689032765441'>▶️</tg-emoji> Хвастайся друзьям своими победами.\n\n\n"
    "<tg-emoji emoji-id='5197427825690279937'>❤️</tg-emoji> Owner - @kwiken\n"
    "<tg-emoji emoji-id='5197427825690279937'>❤️</tg-emoji> MemDice News - @MemDice\n"
    "<tg-emoji emoji-id='5197427825690279937'>❤️</tg-emoji> Onion [LSD] - @Onion_vf"
)

GAME_RESULT = (
    "<tg-emoji emoji-id='5195336932531372033'>💡</tg-emoji> <b>Бросок @{username}'а</b>\n\n"
    "<tg-emoji emoji-id='5458771298547138561'>🎲</tg-emoji> <b>Выпало:</b> {n}\n"
    "<tg-emoji emoji-id='5197470792543109121'>➕</tg-emoji> <b>Начислено:</b> {win:,} <tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji>"
)

GAME_IN_PROGRESS = "<tg-emoji emoji-id='5197662631552352258'>👁</tg-emoji> У вас уже есть неоплаченый счет выше."

INSUFFICIENT_BALANCE = (
    "<tg-emoji emoji-id='5197233456945299457'>🚫</tg-emoji> <b>Недостаточно средств.</b>\n"
    "<tg-emoji emoji-id='5197578639171911681'>🌬</tg-emoji> Минимальный баланс: <b>2500</b> <tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji> (1 Premium <tg-emoji emoji-id='5465526891261722625'>⭐</tg-emoji> на 6 месяцев)."
)
ASK_WITHDRAW_COUNT = (
    "<tg-emoji emoji-id='5197524763102150658'>✈️</tg-emoji> <b>Вывод Telegram Premium</b>\n\n"
    "<tg-emoji emoji-id='5197470332981608449'>🌬</tg-emoji> Каждая подписка на 6 месяцев стоит <b>2500</b> <tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji>.\n"
    "<tg-emoji emoji-id='5197167073930772481'>🌬</tg-emoji> Введите количество подписок, которые хотите получить (целое число ≥1):"
)
INVALID_WITHDRAW_COUNT = "<tg-emoji emoji-id='5197233456945299457'>🚫</tg-emoji> Неверный ввод. Введите целое положительное число."
INSUFFICIENT_FOR_COUNT = (
    "<tg-emoji emoji-id='5197233456945299457'>🚫</tg-emoji> Недостаточно баланса.\n"
    "<tg-emoji emoji-id='5197578639171911681'>🌬</tg-emoji> Для {count} подписок нужно {cost:,} <tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji>, у вас {balance:,} <tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji>."
)
SUCCESS_WITHDRAW = (
    "<tg-emoji emoji-id='5195121694540300289'>✅</tg-emoji> Успешно отправлено <b>{success_count}</b> подписок Telegram Premium <tg-emoji emoji-id='5465526891261722625'>⭐</tg-emoji> на 6 месяцев каждая!\n"
    "<tg-emoji emoji-id='5195445505009647617'>🌬</tg-emoji> С вашего баланса списано <b>{cost:,} <tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji></b>.\n"
)
PARTIAL_WITHDRAW = (
    "<tg-emoji emoji-id='5197454626286206977'>⚠️</tg-emoji> Частичный успех: отправлено <b>{success_count}</b> из {requested} подписок.\n"
    "<tg-emoji emoji-id='5195445505009647617'>🌬</tg-emoji> Списано <b>{cost:,} <tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji></b>.\n"
    "<tg-emoji emoji-id='5195207340483149825'>🌬</tg-emoji>Остаток баланса: <b>{new_balance:,} <tg-emoji emoji-id='5463040341420539905'>⭐</tg-emoji></b>\n"
    "<tg-emoji emoji-id='5197578639171911681'>🌬</tg-emoji> Попробуйте позже для остальных."
)
ERROR_WITHDRAW = "<tg-emoji emoji-id='5197233456945299457'>🚫</tg-emoji> Ошибка при отправке подписок. Попробуйте позже или обратитесь в поддержку."