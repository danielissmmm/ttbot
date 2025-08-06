from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import os
from keep_alive import keep_alive

# Keep the bot alive (for Render / Replit)
keep_alive()

# Get bot token from environment variables
BOT_TOKEN = os.environ["BOT_TOKEN"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "tiktok.com" not in text:
        await update.message.reply_text("Please send a valid TikTok link.")
        return

    await update.message.reply_text("Downloading your video...")

    try:
        # Follow redirect for shortened links
        response = requests.get(text, allow_redirects=True)
        real_url = response.url

        # TikWM API call
        api_url = f"https://tikwm.com/api/?url={real_url}"
        api_response = requests.get(api_url).json()

        if api_response.get("data") and api_response["data"].get("play"):
            video_url = api_response["data"]["play"]
            video_data = requests.get(video_url).content
            await update.message.reply_video(video=video_data)
        else:
            await update.message.reply_text("⚠️ Failed to download the video.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# Setup the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Bot is running...")
app.run_polling()