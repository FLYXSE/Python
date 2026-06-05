from pyrogram import Client
from pyrogram.types import Message
from texts import *
from emoji import *
import random
import string


async def rand(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit(LSD_rand_help)
        return

    args = message.command[1:]

    mode = None
    min_val = 1
    max_val = 100
    first_letter = None
    length = 8

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "+num":
            mode = "num"
        elif arg == "+word":
            mode = "word"
        elif arg.startswith("+1-") and mode == "num":
            try:
                parts = arg[3:].split("-")
                if len(parts) == 2:
                    min_val = int(parts[1])
                    max_val = int(parts[3:-1])
            except:
                pass
        elif arg.startswith("+letter_") and mode == "word":
            first_letter = arg[8:].lower()
        elif arg.isdigit() and mode == "word":
            try:
                length = int(arg)
                if length < 1:
                    length = 1
                if length > 50:
                    length = 50
            except:
                pass
        i += 1

    if mode is None:
        await message.edit("Error")
        return

    if mode == "num":
        result = str(random.randint(min_val, max_val))
    else:
        if first_letter and first_letter.isalpha():
            first = first_letter
        else:
            first = random.choice(string.ascii_lowercase)

        remaining_length = length - 1 if length > 0 else 0
        if remaining_length > 0:
            rest = "".join(random.choice(string.ascii_lowercase) for _ in range(remaining_length))
            result = first + rest
        else:
            result = first

    result_text = LSD_rand.replace("<rand>", result)
    await message.edit(result_text)