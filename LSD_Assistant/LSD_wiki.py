from pyrogram import Client
from pyrogram.types import Message
from texts import *
from emoji import *
import wikipedia
import asyncio

async def wiki(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit(LSD_wiki_error1)
        return

    query = " ".join(message.command[1:])
    await message.edit(LSD_wiki.replace("<X>", query))

    try:
        wikipedia.set_lang("ru")
        search_results = wikipedia.search(query, results=1)

        if not search_results:
            await message.edit(LSD_wiki_error2)
            return

        page_title = search_results[0]
        summary = wikipedia.summary(page_title, sentences=3, auto_suggest=False)
        page_url = f"https://ru.wikipedia.org/wiki/{page_title.replace(' ', '_')}"

        result_text = LSD_wiki.replace("<X>", query)
        result_text = result_text.replace("<Заголовок статьи>", page_title)
        result_text = result_text.replace('<a href="https://www.wikipedia.org/">Читать полностью</a>', f'<a href="{page_url}">Читать полностью</a>')

        await message.edit(result_text, disable_web_page_preview=True)

    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n".join([f"[{toch}] {opt}" for opt in e.options[:5]])
        error_text = LSD_wiki_error5.replace("[]", f"{options}")
        await message.edit(error_text)
    except wikipedia.exceptions.PageError:
        await message.edit(LSD_wiki_error3)
    except Exception as e:
        await message.edit(LSD_wiki_error4.replace("[]", f"{str(e)[:200]}"))