‎import os
‎import yt_dlp
‎from telegram import Update
‎from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
‎
‎TOKEN = "TOKEN_BARU_KAMU"
‎
‎DOWNLOAD_PATH = "downloads"
‎os.makedirs(DOWNLOAD_PATH, exist_ok=True)
‎
‎
‎async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
‎    url = update.message.text
‎
‎    if "youtube.com" not in url and "youtu.be" not in url:
‎        await update.message.reply_text("Kirim link YouTube yang valid.")
‎        return
‎
‎    await update.message.reply_text("Downloading... ⏳")
‎
‎    ydl_opts = {
‎        'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
‎        'format': 'best',
‎    }
‎
‎    try:
‎        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
‎            info = ydl.extract_info(url, download=True)
‎            file_path = ydl.prepare_filename(info)
‎
‎        await update.message.reply_video(video=open(file_path, 'rb'))
‎
‎        os.remove(file_path)
‎
‎    except Exception as e:
‎        await update.message.reply_text(f"Error: {str(e)}")
‎
‎
‎def main():
‎    app = ApplicationBuilder().token(TOKEN).build()
‎    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
‎
‎    print("YT Downloader Bot Running...")
‎    app.run_polling()
‎
‎
‎if __name__ == "__main__":
‎    main()
