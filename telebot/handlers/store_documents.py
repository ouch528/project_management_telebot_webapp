from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
from services.firebase import db

async def store_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args  # List of words after the command
    chat_title = update.effective_chat.title

    if not args:
        await update.message.reply_text("Please provide a document link. E.g., /store_docs https://...")
        return

    doc_link = args[0]  # Just the first word after the command
    user_id = update.effective_user.id

    doc_ref = db.collection(chat_title).document("stored_docs")
    doc = doc_ref.get()

    # Append to existing list if present
    if doc.exists:
        existing_links = doc.to_dict().get("links", [])
        if doc_link in existing_links:
            await update.message.reply_text("This link is already stored.")
        else:
            existing_links.append(doc_link)
            doc_ref.set({"links": existing_links}, merge=True)
            await update.message.reply_text("Document link stored successfully.")
    else:
        doc_ref.set({"links": [doc_link]})
        await update.message.reply_text("Document link stored successfully.")

    print(f"User {user_id} stored doc link: {doc_link} in chat '{chat_title}'")

store_documents_handler = CommandHandler("store_documents", store_docs)