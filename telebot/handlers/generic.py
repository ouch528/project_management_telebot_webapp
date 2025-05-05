from telegram.ext import MessageHandler, filters, ContextTypes
from telegram import Update

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello there! Welcome to the project management bot.")

reply_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, reply)