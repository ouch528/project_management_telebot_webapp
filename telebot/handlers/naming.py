from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
from services.firebase import db
from utils.hash_util import hash_chat_title

async def naming(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args  # List of words after the command
    user_id = update.effective_user.id
    chat_title = update.effective_chat.title
    hashed_chat_title = hash_chat_title(chat_title)
    if not args:
        await update.message.reply_text("Please provide a name after the command. E.g., /naming Project Phoenix")
    else:
        name = " ".join(args)  # Join the args into a single string
        db.collection(chat_title).document("member_names").set({
            str(user_id): name
        })
        print(f"Added name '{name}' in document 'member_names' in collection '{chat_title}'")

        db.collection(chat_title).document("member_user_id").set({
            name: str(user_id)
        })
        print(f"Added user id '{user_id}' in document 'member_user_id' in collection '{chat_title}'")

        doc_ref = db.collection(chat_title).document("hashed_chat_title")
        doc = doc_ref.get()

        if not doc.exists:
            doc_ref.set({
                chat_title: hashed_chat_title
            })
            print(f"Added hashed chat title '{hashed_chat_title}' in document 'hashed_chat_title' in collection '{chat_title}'")
        else:
            print(f"'hashed_chat' document already exists in collection '{chat_title}'")

        await update.message.reply_text(f"You entered: {name}")

naming_handler = CommandHandler("naming", naming)