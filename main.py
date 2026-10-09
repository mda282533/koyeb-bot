import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message or update.business_message
    if not msg:
        return
    
    chat_id = msg.chat.id
    text = msg.text or ""
    biz_id = getattr(msg, 'business_connection_id', None)

    if "salam" in text.lower():
        reply = "Walaikum Salam! Kemon achen?"
    elif "photo" in text.lower() or "edit" in text.lower():
        reply = "Ekta photo pathan, ami edit kore dibo."
    else:
        reply = f"Apni bolechen: {msg.text}"

    await context.bot.send_message(
        chat_id=chat_id,
        text=reply,
        business_connection_id=biz_id
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))
print("Bot started!")
app.run_polling()
