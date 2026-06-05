# LSD AI Userbot

Telegram userbot с AI через OmniRoute API. Работает от вашего имени в любом чате.

## Установка

```bash
pip install -r requirements.txt
```

## Настройка

1. Получите API_ID и API_HASH на https://my.telegram.org/apps
2. Создайте `.env` файл:
```
API_ID=ваш_api_id
API_HASH=ваш_api_hash
```

3. Или установите переменные окружения:
```bash
export API_ID="ваш_api_id"
export API_HASH="ваш_api_hash"
```

## Запуск

```bash
python bot.py
```

При первом запуске введите номер телефона и код подтверждения.

## Использование

В любом чате Telegram отправьте от своего имени:
- `.AI вопрос` - задать вопрос AI

Сообщение изменится на "Думаю...", затем на ответ AI.
