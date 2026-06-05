from emoji import *

LSD_start = f"""
<b>[{star}] LSD Assistant
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] Меню</b>

[{toch}] <code>LSD.start</code> — Старт.
[{toch}] <code>LSD.help</code> — Помощь.
[{toch}] <code>LSD.ping</code> — Задержка.
[{toch}] <code>LSD.wiki</code> — Wikipedia.
[{toch}] <code>LSD.rand</code> — Рандом.
[{toch}] <code>LSD.clear</code> — Очищает все сообщения. (Смотреть инструкцию!)
[{toch}] <code>LSD.ch</code> — Отправляет сообщения в канал.
[{toch}] <code>LSD.info</code> — Информация.
[{toch}] <code>LSD.mute</code> — Мут.
"""

LSD_help = f"""
<b>[{star}] Помощь
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] Использование:</b>

[{toch}] <code>LSD.help<команда></code> — Инструкция к <команда>.
"""





LSD_ping = f"""
<b>[{star}] PING
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] <b>[]</b> ms
"""

LSD_wiki = f"""
<b>[{star}] Wikipedia
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Поисковой запрос — <X>

[{toch}] <Заголовок статьи> — <a href="https://www.wikipedia.org/">Читать полностью</a>
"""

LSD_wiki_error1 = f"""
<b>[{star}] Wikipedia
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Ошибка

[{toch}] Укажите поисковой запрос после LSD.wiki
[{skrep}] Пример: <code>LSD.wiki Telegram</code>
"""

SD_wiki_error2 = f"""
<b>[{star}] Wikipedia
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Ошибка

[{toch}] Результатов не найдено
"""

LSD_wiki_error3 = f"""
<b>[{star}] Wikipedia
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Ошибка

[{toch}] Страница не найдена
"""

LSD_wiki_error4 = f"""
<b>[{star}] Wikipedia
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Ошибка

[{toch}] []
"""

LSD_wiki_error5 = f"""
<b>[{star}] Wikipedia
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Ошибка

[{toch}] Уточните запрос: []
"""

LSD_rand = f"""
[{star}] Random
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] Результат

[{toch}] <rand>
"""

LSD_rand_help = f"""
<b>[{star}] Random 
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] LSD.rand</b>

[{toch}] <code>LSD.rand +num +1-100</code>
[{toch}] <code>LSD.rand +word +letter_f +8</code>
[{skrep}] +num — рандомное число. [!]
[{skrep}] +word — рандомное  слово. [!]
[{skrep}] (+num) +1-100 — Задает диапазон рандомного числа. (Тут от 1 до 100)
[{skrep}] (+word) +letter_f — Задает первую букву в рандомном слове (тут f)
[{skrep}] (+word) +8 — Задает количество букв в рандомном слове (тут 8)

[⭐️] [!] Обязательный аргумент.
"""


LSD_clear_me = f"""
[{star}] Clear
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] Ваши сообщения очищены.
"""

LSD_clear_all = f"""
[{star}] Clear
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] Все сообщения очищены.
"""

LSD_clear_wait = f"""
[{star}] Clear
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] Ожидание подтверждения.

[{toch}] Ответьте на это сообщение «LSD.clear.YES» для подтверждения или «LSD.clear.NO» для отмены
"""

LSD_help_wiki = f"""
[{star}] Помощь 
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] LSD.wiki

[{toch}] LSD.wiki X
[{skrep}] X — поисковой запрос
"""

LSD_help_rand = f"""
[{star}] Помощь 
[{code}] Автор: @kwiken | @Unsupported_characters


[{menu}] LSD.rand

[{toch}] LSD.rand +num +1-100
[{toch}] LSD.rand +word +letter_f +8
[{skrep}] +num — рандомное число. [!]
[{skrep}] +word — рандомное  слово. [!]
[{skrep}] (+num) +1-100 — Задает диапазон рандомного числа. (Тут от 1 до 100)
[{skrep}] (+word) +letter_f — Задает первую букву в рандомном слове (тут f)
[{skrep}] (+word) +8 — Задает количество букв в рандомном слове (тут 8)

[{star_two}] [!] Обязательный аргумент.
"""

LSD_ch_success = f"""
<b>[{star}] Channel
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Сообщение отправлено в канал.
"""

LSD_ch_error = f"""
<b>[{star}] Channel
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Ошибка

[{toch}] Укажите текст после LSD.ch
[{skrep}] Пример: <code>LSD.ch Привет, мир!</code>
"""

LSD_ch_error_send = f"""
<b>[{star}] Channel
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Ошибка отправки

[{toch}] []
"""

LSD_online_on = f"""
<b>[{star}] Online
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Постоянный онлайн включен.
"""

LSD_online_off = f"""
<b>[{star}] Online
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Постоянный онлайн выключен.
"""

LSD_online_status = f"""
<b>[{star}] Online
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Статус: []

[{toch}] <code>LSD.online +on</code> — Включить
[{toch}] <code>LSD.online +off</code> — Выключить
"""

LSD_online_already_on = f"""
<b>[{star}] Online
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Постоянный онлайн уже включен.
"""

LSD_online_already_off = f"""
<b>[{star}] Online
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Постоянный онлайн уже выключен.
"""

LSD_online_error = f"""
<b>[{star}] Online
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Ошибка

[{toch}] Используйте <code>+on</code> или <code>+off</code>
"""

LSD_mute_success = f"""
<b>[{star}] Mute
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Пользователь @[] добавлен в мут.

[{toch}] Все сообщения от него будут автоматически удаляться.
"""

LSD_mute_already = f"""
<b>[{star}] Mute
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Пользователь @[] уже в муте.
"""

LSD_mute_list = f"""
<b>[{star}] Mute
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Список замученных пользователей:

[]
"""

LSD_mute_list_empty = f"""
<b>[{star}] Mute
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Список замученных пуст.
"""

LSD_mute_error = f"""
<b>[{star}] Mute
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Использование:

[{toch}] <code>LSD.mute +username</code> — Добавить в мут
[{toch}] <code>LSD.mute -username</code> — Удалить из мута
[{toch}] <code>LSD.mute +list</code> — Список замученных
"""

LSD_mute_removed = f"""
<b>[{star}] Mute
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Пользователь @[] удален из мута.
"""

LSD_mute_not_found = f"""
<b>[{star}] Mute
[{code}] Автор: @kwiken | @Unsupported_characters</b>

[{menu}] Пользователь @[] не найден в муте.
"""