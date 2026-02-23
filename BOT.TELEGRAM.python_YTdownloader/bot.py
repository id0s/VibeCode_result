import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim link YouTube untuk didownload.")


def download_video(url, filename="video.mp4"):
    ydl_opts = {
        "outtmpl": filename,
        "format": "best",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "http" not in url:
        await update.message.reply_text("Kirim link yang valid.")
        return

    await update.message.reply_text("⬇️ Downloading...")

    filename = "video.mp4"

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download_video, url, filename)

        await update.message.reply_document(document=open(filename, "rb"))
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


if __name__ == "__main__":
    print("Bot running...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling(close_loop=False)
