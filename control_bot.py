from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import config
import allocate

async def otp_receiver(update: Update, context):

    text = update.message.text.strip()

    if text.isdigit():

        if allocate.otp_future and not allocate.otp_future.done():

            allocate.otp_future.set_result(text)

            await update.message.reply_text("OTP received")

app = ApplicationBuilder().token(config.CONTROL_BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, otp_receiver))

app.run_polling()