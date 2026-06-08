from typing import Optional, Any
import aiohttp
import config

HEADERS = {"Crypto-Pay-Api-Token": config.CRYPTOPAY_TOKEN}
BASE_URL = config.CRYPTOPAY_URL.rstrip("/")


async def api_request(method: str, endpoint: str, json_data: dict = None) -> Optional[Any]:
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.request(method, url, json=json_data, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                data = await resp.json()
                if data.get("ok"):
                    return data.get("result")
                print(f"[CryptoPay] Error on {endpoint}: {data}")
                return None
    except Exception as e:
        print(f"[CryptoPay] Exception on {endpoint}: {e}")
        return None


async def get_me() -> Optional[dict]:
    return await api_request("GET", "me")


async def create_invoice(amount: float, payload: str, description: str = "Пополнение баланса") -> Optional[dict]:
    result = await api_request("POST", "createInvoice", {
        "currency": "USDT",
        "amount": amount,
        "description": description,
        "payload": payload,
    })
    if isinstance(result, dict):
        return {
            "invoice_id": result.get("invoice_id", ""),
            "link": result.get("bot_invoice_url") or result.get("mini_app_invoice_url") or "",
            "amount": float(result.get("amount", 0)),
            "status": result.get("status", ""),
            "payload": result.get("payload", ""),
        }
    return result


async def get_invoice(invoice_id: str) -> Optional[dict]:
    result = await api_request("GET", f"getInvoice?invoice_id={invoice_id}")
    if isinstance(result, dict):
        return {
            "invoice_id": result.get("invoice_id", ""),
            "status": result.get("status", ""),
            "amount": float(result.get("amount", 0)),
            "payload": result.get("payload", ""),
            "paid_by": result.get("paid_by"),
        }
    return result


async def get_invoices(status: str = "active") -> Optional[list]:
    result = await api_request("GET", f"getInvoices?status={status}")
    if isinstance(result, dict):
        items = result.get("items", [])
        return [{
            "invoice_id": inv.get("invoice_id", ""),
            "status": inv.get("status", ""),
            "amount": float(inv.get("amount", 0)),
            "payload": inv.get("payload", ""),
        } for inv in items]
    return []


async def transfer(user_id: int, amount: float, currency: str = "USDT") -> Optional[dict]:
    result = await api_request("POST", "transfer", {
        "user_id": user_id,
        "currency": currency,
        "amount": amount,
    })
    return result


async def get_balance() -> Optional[list]:
    result = await api_request("GET", "getBalance")
    return result
