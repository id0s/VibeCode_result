import os
import requests
import gdown
from bs4 import BeautifulSoup

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN= os.getenv("BOT_TOKEN")

# ====== DETECT PLATFORM ======
def detect_platform(url):
    if "drive.google.com" in url:
        return "gdrive"
    elif "mediafire.com" in url:
        return "mediafire"
    elif "pixeldrain.com" in url:
        return "pixeldrain"
    else:
        return None


# ====== DOWNLOADERS ======
def download_gdrive(url, filename):
    gdown.download(url, filename, quiet=False)


def download_mediafire(url, filename):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    download_btn = soup.find("a", {"id": "downloadButton"})
    direct_link = download_btn["href"]

    with requests.get(direct_link, stream=True) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)


def download_pixeldrain(url, filename):
    file_id = url.split("/")[-1]
    direct_link = f"https://pixeldrain.com/api/file/{file_id}"

    with requests.get(direct_link, stream=True) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)


# ====== COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Kirim link Google Drive / MediaFire / Pixeldrain."
    )


# ====== HANDLE MESSAGE ======
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    platform = detect_platform(url)

    if not platform:
        await update.message.reply_text("Platform tidak didukung.")
        return

    await update.message.reply_text("🔍 Memproses download...")

    filename = "downloaded_file"

    try:
        if platform == "gdrive":
            download_gdrive(url, filename)
        elif platform == "mediafire":
            download_mediafire(url, filename)
        elif platform == "pixeldrain":
            download_pixeldrain(url, filename)

        await update.message.reply_document(open(filename, "rb"))
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


# ====== MAIN ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("Bot running...")
    app.run_polling()
