from telegram.ext import Application
from config import TELEBOT_TOKEN
from handlers.naming import naming_handler
from handlers.store_documents import store_documents_handler
from handlers.set_meeting import set_meeting_handler
from handlers.generic import reply_handler
from handlers.add_deadline import add_deadline_handler
import nest_asyncio
import asyncio

async def main():
    application = Application.builder().token(TELEBOT_TOKEN).build()

    application.add_handler(naming_handler)
    application.add_handler(store_documents_handler)
    application.add_handler(set_meeting_handler)
    application.add_handler(reply_handler)
    application.add_handler(add_deadline_handler)

    await application.bot.set_my_commands([
        ("naming", "Name yourselves"),
        ("store_documents", "Store document links"),
        ("set_meeting", "Set a meeting time"),
        ("add_deadline", "Add a task submission deadline in the format: <Task Name>: <Date>."),
    ])

    print("Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())