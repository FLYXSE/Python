import asyncio
from aiogram import Bot
from services import cryptopay
import database
from utils import log_deposit, logger
import texts


async def check_pending_invoices(bot: Bot):
    while True:
        try:
            pending = database.get_pending_deposits()
            for tx in pending:
                invoice_id = tx["invoice_id"]
                if not invoice_id:
                    continue
                invoice_data = await cryptopay.get_invoice(invoice_id)
                if invoice_data and invoice_data.get("status") == "paid":
                    amount = float(invoice_data.get("amount", tx["amount"]))
                    database.complete_deposit(tx["id"], tx["telegram_id"], amount)

                    paid_by = invoice_data.get("paid_by")
                    if paid_by is not None:
                        database.save_cryptopay_id(tx["telegram_id"], int(paid_by))

                    log_deposit(tx["telegram_id"], amount, invoice_id, "paid")
                    try:
                        await bot.send_message(
                            tx["telegram_id"],
                            texts.DEPOSIT_CONFIRMED.format(amount=f"{amount:.2f}"),
                        )
                    except Exception as e:
                        logger.error(f"Failed to notify user {tx['telegram_id']}: {e}")
        except Exception as e:
            logger.error(f"Invoice checker error: {e}")
        await asyncio.sleep(10)
