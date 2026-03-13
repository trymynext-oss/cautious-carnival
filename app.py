import threading
from flask import Flask

# import your WhatsApp bot start file
import whatsapp

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def start_bot():
    whatsapp.start_bot()

# start bot in background thread
threading.Thread(target=start_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
