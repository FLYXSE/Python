import telebot
import requests
import threading
import time
import random

BOT_TOKEN     = "2202914218:AAFggBHUpBVeZukJZFJsr9xbiu9w3Bz6Wug/test"
LINK_TTL      = 600
POLL_INTERVAL = 10

bot = telebot.TeleBot(BOT_TOKEN)


def create_token() -> dict | None:
    try:
        r = requests.post(
            "https://webhook.site/token",
            json={"default_status": 200, "default_content": "", "cors": True},
            timeout=10,
        )
        return r.json()
    except Exception as e:
        print(f"[create_token] {e}")
        return None


def get_requests(token_id: str, since: str) -> list[dict]:
    try:
        r = requests.get(
            f"https://webhook.site/token/{token_id}/requests",
            params={"sorting": "newest", "per_page": 10,
                    "date_from": since, "query": "type:web"},
            timeout=10,
        )
        return r.json().get("data", [])
    except Exception as e:
        print(f"[get_requests] {e}")
        return []


def get_ip_info(ip: str) -> tuple[str, str]:
    try:
        d = requests.get(f"http://ip-api.com/json/{ip}?fields=country,city",
                         timeout=5).json()
        return d.get("country", "Unknown"), d.get("city", "Unknown")
    except Exception:
        return "Unknown", "Unknown"


def watch(chat_id: int, msg_id: int, token_id: str, start_str: str):
    deadline = time.time() + LINK_TTL
    seen = set()

    while time.time() < deadline:
        for req in get_requests(token_id, start_str):
            rid = req.get("uuid", "")
            if rid in seen:
                continue
            seen.add(rid)
            ua      = req.get("user_agent") or "Unknown"
            ip      = req.get("ip") or "Unknown"
            country, city = get_ip_info(ip)
            text = f"{ua}\n\n{ip}\nCountry Name: {country}\nCity Name: {city}"
            try:
                bot.send_message(chat_id, text)
            except Exception as e:
                print(f"[send] {e}")
        time.sleep(POLL_INTERVAL)

    try:
        bot.edit_message_text("*link deactivated*",
                              chat_id=chat_id, message_id=msg_id,
                              parse_mode="Markdown")
    except Exception as e:
        print(f"[edit] {e}")


@bot.message_handler(commands=["start"])
def cmd_start(message):
    globe = random.choice(["🌍", "🌎", "🌏"])
    bot.send_message(message.chat.id,
                     f"{globe} *Information about your visit – /q*",
                     parse_mode="Markdown")


@bot.message_handler(commands=["q"])
def cmd_q(message):
    token = create_token()
    if not token or "uuid" not in token:
        bot.send_message(message.chat.id, f"❌ Error: <code>{token}</code>",
                         parse_mode="HTML")
        return

    token_id  = token["uuid"]
    link      = f"https://webhook.site/{token_id}"
    start_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    sent = bot.send_message(
        message.chat.id,
        f"{link}\n\n_the link is active for 10 minutes._",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )

    threading.Thread(
        target=watch,
        args=(message.chat.id, sent.message_id, token_id, start_str),
        daemon=True,
    ).start()


if __name__ == "__main__":
    print("Bot Started.")
    bot.infinity_polling()
