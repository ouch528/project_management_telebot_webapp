from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from services.datetime_parser import parse_natural_datetime
from services.firebase import db
from utils.regex_clean import clean_text
from datetime import time

async def add_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_title = update.effective_chat.title
    input_text = clean_text(" ".join(context.args))

    if ":" not in input_text:
        await update.message.reply_text("Please use the format: <Task Name>: <Date>. E.g., `/add_deadline Final Report: next Friday 5pm`")
        return

    task_name, datetime_input = map(str.strip, input_text.split(":", 1))
    parsed_datetime = parse_natural_datetime(datetime_input)

    if parsed_datetime is None:
        await update.message.reply_text(f"Could not understand the deadline date: \"{datetime_input}\". Try a clearer format.")
        return
    
    if parsed_datetime.time() == time(0, 0):
        parsed_datetime = parsed_datetime.replace(hour=23, minute=59)

    deadline_entry = {
        "task_name": task_name,
        "original_input": datetime_input,
        "deadline_datetime": parsed_datetime.isoformat()
    }

    db.collection(chat_title)\
        .document("project_deadlines")\
        .collection("deadlines")\
        .add(deadline_entry)

    await update.message.reply_text(
        f"*{task_name}* deadline set for: _{parsed_datetime.strftime('%A, %d %B %Y at %I:%M %p')}_",
        parse_mode="Markdown"
    )

add_deadline_handler = CommandHandler("add_deadline", add_deadline)