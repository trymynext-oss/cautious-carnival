import asyncio
import config
from telethon import TelegramClient
from telethon.errors import FloodWaitError

client = TelegramClient(
    config.SESSION_NAME,
    config.API_ID,
    config.API_HASH
)


async def safe_send(bot, text):
    while True:
        try:
            await client.send_message(bot, text)
            return
        except FloodWaitError as e:
            print("FloodWait:", e.seconds)
            await asyncio.sleep(e.seconds)


async def send_start_twice(bot):

    await safe_send(bot, "/start")
    await asyncio.sleep(1)

    await safe_send(bot, "/start")
    await asyncio.sleep(2)


async def wait_and_click(bot, button_text):

    for _ in range(20):

        msg = await client.get_messages(bot, limit=1)

        if msg and msg[0].buttons:

            for row in msg[0].buttons:
                for button in row:

                    if button_text.lower() in button.text.lower():

                        await msg[0].click(text=button.text)
                        return True

        await asyncio.sleep(2)

    return False


async def start_flow(word1, word2, range_text):

    bot = await client.get_entity(config.TARGET_BOT)

    await send_start_twice(bot)

    await safe_send(bot, word1)
    await asyncio.sleep(3)

    await safe_send(bot, word2)
    await asyncio.sleep(4)

    msg = await client.get_messages(bot, limit=1)

    if msg and "not available" in (msg[0].text or "").lower():
        return "country_not_available"

    clicked = await wait_and_click(bot, range_text)

    if not clicked:
        return "numbers_not_available"

    await asyncio.sleep(3)

    msg = await client.get_messages(bot, limit=1)

    if msg and "unallocated number nahi" in (msg[0].text or "").lower():
        return "numbers_not_available"

    await wait_and_click(bot, "Daily")
    await asyncio.sleep(2)

    await wait_and_click(bot, "0")

    await asyncio.sleep(2)

    await safe_send(bot, "50")

    return "success"


async def run_allocate(word1, word2, range_text):

    await client.start()

    result = await start_flow(word1, word2, range_text)

    return result