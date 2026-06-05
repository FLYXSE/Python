# Установка бота на ПК

## Требования

- Python 3.10 или выше
- Windows / Linux / macOS

## Шаг 1: Скачайте проект

Склонируйте репозиторий или скачайте архив с кодом.

## Шаг 2: Создайте виртуальное окружение (рекомендуется)

```bash
python -m venv venv
```

## Шаг 3: Активируйте виртуальное окружение

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate
```

**Windows (cmd):**
```bash
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

## Шаг 4: Установите зависимости

```bash
pip install -r requirements.txt
```

## Шаг 5: Настройте переменные окружения

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
BOT_TOKEN=ваш_токен_бота
CHAT_ID=ид_чата_для_получения_сообщений
```

- **BOT_TOKEN** — токен бота от @BotFather в Telegram
- **CHAT_ID** — ID чата, куда будут приходить обращения (можно получить у @userinfobot)

## Шаг 6: Запуск бота

```bash
python bot.py
```

## Структура файлов

```
├── bot.py            # Основной код бота
├── .env              # Токены и настройки (не добавлять в git)
├── requirements.txt  # Зависимости
├── last_message.json # Хранилище времени последних сообщений
└── install.md        # Этот файл
```

## Полезные команды

**Деактивировать виртуальное окружение:**
```bash
deactivate
```

**Перезапуск бота при изменениях (с hot reload):**
```bash
pip install watchdog
python -m watchdog bot.py
```

## Возможные проблемы

- **Ошибка "BOT_TOKEN not set"** — проверьте файл `.env`
- **Бот не отвечает** — убедитесь что токен бота активен
- **Сообщения не приходят в чат** — проверьте CHAT_ID