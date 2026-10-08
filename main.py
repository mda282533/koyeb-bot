import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import io

TOKEN = os.getenv("8815726541:AAHtZCPSqMH7tmxgJmatFMowkSVvvT_nVFc")

# --- Photo Editing Function ---
async def edit_photo(file):
    img_file = io.BytesIO()
    await file.download_to_memory(img_file)
    img = Image.open(img_file).convert("RGB")
    
    # Custom Editing: Brightness + Text
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # Niche ekta kalo box
    draw.rectangle([(0, h-80), (w, h)], fill=(0,0,0))
    draw.text((20, h-55), "Edited by Abdullah Bot ✨", fill=(255,255,255))
    
    output = io.BytesIO()
    output.name = "edited.jpg"
    img.save(output, "JPEG")
    output.seek(0)
    return output

# --- Main Handler ---
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Business ar normal 2 tar jonnoi kaj korbe
    msg = update.business_message or update.message
    if not msg:
        return

    chat_id = msg.chat_id
    biz_id = msg.business_connection_id if hasattr(msg, 'business_connection_id') else None

    # 1. Jodi PHOTO pathay
    if msg.photo:
        await context.bot.send_chat_action(chat_id=chat_id, action="upload_photo", business_connection_id=biz_id)
        photo_file = await msg.photo[-1].get_file()
        edited = await edit_photo(photo_file)
        
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=edited,
            caption="Apnar photo edit kore dilam! 😊\nAro kichu lagle bolun.",
            business_connection_id=biz_id
        )
    # 2. Jodi TEXT pathay (Chat)
    elif msg.text:
        text = msg.text.lower()
        if "hi" in text or "salam" in text or "hello" in text:
            reply = "Walaikum Salam! Kemon achen? Photo pathan, ami edit kore dibo."
        elif "photo" in text or "edit" in text:
            reply = "Ekta photo pathan, ami sundor kore edit kore dicchi!"
        else:
            reply = f"Apni bolechen: {msg.text}\n\nAmi Abdullah er bot. Chat korte pari, photo edit korte pari. Ekta photo diye dekhun!"
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=reply,
            business_connection_id=biz_id
        )

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle))
print("
