from telegram import Update, BotCommand
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import nest_asyncio
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

cred = credentials.Certificate(BASE_DIR / os.getenv("FIREBASE_KEY_PATH"))
firebase_admin.initialize_app(cred)
db = firestore.client()

async def set_commands(application):
    commands = [
        BotCommand(command="naming", description="Name your project"),
    ]
    await application.bot.set_my_commands(commands)

async def naming(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args  # List of words after the command
    user_id = update.effective_user.id
    chat_title = update.effective_chat.title
    if not args:
        await update.message.reply_text("Please provide a name after the command. E.g., /naming Project Phoenix")
    else:
        name = " ".join(args)  # Join the args into a single string
        db.collection(chat_title).document("member_names").set({
            str(user_id): name
        })
        print(f"Added name {name} in document member_names in collection {chat_title}")

        db.collection(chat_title).document("member_user_id").set({
            name: str(user_id)
        })
        print(f"Added user id {user_id} in document member_user_id in collection {chat_title}")

        await update.message.reply_text(f"You entered: {name}")

async def reply(update, context):
    user_id = update.effective_user.id
    message_text = update.message.text

    await update.message.reply_text("Hello there!")

async def main():
    token = os.getenv("TELEBOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("naming", naming))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

    await set_commands(application)
    print("Bot is running...", flush=True)
    await application.run_polling()

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())