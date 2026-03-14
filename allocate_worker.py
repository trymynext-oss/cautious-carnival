import asyncio
from accounts import accounts
from allocate import run_allocate
import config
from telethon import TelegramClient

client = TelegramClient(
    config.SESSION_NAME,
    config.API_ID,
    config.API_HASH
)

last_command_time = asyncio.get_event_loop().time()


async def idle_ping():

    await client.start()

    bot = await client.get_entity(config.TARGET_BOT)

    global last_command_time

    while True:

        await asyncio.sleep(120)

        now = asyncio.get_event_loop().time()

        if now - last_command_time >= 120:

            print("Idle detected → sending /start twice")

            await client.send_message(bot, "/start")
            await asyncio.sleep(1)
            await client.send_message(bot, "/start")


async def worker():

    global last_command_time

    while True:

        if len(accounts) == 0:
            await asyncio.sleep(2)
            continue

        task = accounts.pop(0)

        last_command_time = asyncio.get_event_loop().time()

        name = task["name"]
        country = task["country"]
        range_text = task["range"]
        chat = task["chat"]
        client_wa = task["client"]

        print("Starting allocation:", name)

        result = await run_allocate(name, country, range_text)

        if result == "country_not_available":
            reply = "❌ Country not available"

        elif result == "numbers_not_available":
            reply = "❌ Numbers not available"

        else:
            reply = f"✅ Successfully allocated {name}"

        client_wa.send_message(chat, reply)
