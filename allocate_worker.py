import asyncio
from accounts import accounts
from allocate import run_allocate


async def worker():

    while True:

        if len(accounts) == 0:
            await asyncio.sleep(2)
            continue

        task = accounts.pop(0)

        name = task["name"]
        country = task["country"]
        range_text = task["range"]
        chat = task["chat"]
        client = task["client"]

        print("Starting allocation:", name)

        result = await run_allocate(name, country, range_text)

        if result == "country_not_available":
            reply = "❌ Country not available"

        elif result == "numbers_not_available":
            reply = "❌ Numbers not available"

        else:
            reply = f"✅ Successfully allocated {name}"

        client.send_message(chat, reply)