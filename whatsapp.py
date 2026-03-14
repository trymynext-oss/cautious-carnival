import asyncio
import threading

from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv
from neonize.utils import build_jid

from accounts import accounts
from allocate_worker import worker, idle_ping

BOT_NUMBER = "584168808041"

client = NewClient("whatsapp.db")

# create background async loop
loop = asyncio.new_event_loop()


def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()


# start loop thread
threading.Thread(target=start_loop, daemon=True).start()


# start worker and idle ping tasks
asyncio.run_coroutine_threadsafe(worker(), loop)
asyncio.run_coroutine_threadsafe(idle_ping(), loop)


def start_bot():
    print("🚀 Starting WhatsApp Bot")
    client.connect()


@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv):
    print("\n✅ BOT ACTIVE")
    print("--- Waiting for messages ---\n")


@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):

    msg_info = getattr(message, "Info", None)
    msg_content = getattr(message, "Message", None)

    if not msg_info or not msg_content:
        return

    # ignore messages from self
    is_from_me = getattr(msg_info.MessageSource, "IsFromMe", False)
    if is_from_me:
        return

    chat = msg_info.MessageSource.Chat

    text = ""

    if hasattr(msg_content, "conversation") and msg_content.conversation:
        text = msg_content.conversation

    elif hasattr(msg_content, "extendedTextMessage") and msg_content.extendedTextMessage:
        text = getattr(msg_content.extendedTextMessage, "text", "")

    if not text:
        return

    print("DEBUG:", text)

    lower = text.lower()

    # detect add command
    if lower.startswith("add "):

        try:

            command = text[4:].strip()

            parts = command.split(",")

            range_part = parts[0].strip()
            name = parts[1].strip()

            country = range_part.split()[0]

            print("\nADD COMMAND DETECTED")
            print("name:", name)
            print("country:", country)
            print("range:", range_part)

            accounts.append({
                "name": name,
                "country": country,
                "range": range_part,
                "chat": chat,
                "client": client
            })

            client.send_message(chat, "⏳ Allocation request received")

        except Exception as e:

            print("Parsing error:", e)

            client.send_message(chat, "⚠ Invalid command format\nUse:\nAdd Country lx range, Name")


print("🚀 Initializing WhatsApp Listener")
