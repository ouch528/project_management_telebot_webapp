from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from services.datetime_parser import parse_natural_datetime
from services.firebase import db
from utils.regex_clean import clean_text
from datetime import datetime

async def set_meeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    chat_title = update.effective_chat.title

    if not args:
        await update.message.reply_text("Please provide a meeting time. E.g., /set_meeting next Tuesday at 3pm")
        return

    datetime_input = clean_text(" ".join(args))
    parsed_datetime = parse_natural_datetime(datetime_input)

    if parsed_datetime is None:
        await update.message.reply_text(f"Could not understand the time: \"{datetime_input}\". Try a clearer format.")
        return

    # Prepare the meeting entry
    meeting_entry = {
        "original_input": datetime_input,
        "meeting_datetime": parsed_datetime.isoformat(),
        "minutes": "",
    }

    # Store in subcollection: chat_title > meeting_details > meetings > auto-id
    db.collection(chat_title)\
        .document("meeting_details")\
        .collection("meetings")\
        .add(meeting_entry)

    await update.message.reply_text(
        f"Meeting time set for: {parsed_datetime.strftime('%A, %d %B %Y at %I:%M %p')}"
    )

set_meeting_handler = CommandHandler("set_meeting", set_meeting)