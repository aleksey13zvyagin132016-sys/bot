import os
import logging
import subprocess
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8674547291:AAF7zIsm1Wv5xUh8BmU9j4cg2H1sB7ExtAo"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пришли ссылку на YouTube")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("Скачиваю...")
    
    try:
        filename = "video.mp4"
        cmd = [
            "yt-dlp",
            "-f", "best[ext=mp4]",
            "-o", filename,
            url
        ]
        
        # Запускаем и получаем вывод ошибки
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            await msg.edit_text(f"Ошибка yt-dlp:\n{result.stderr[:500]}")
            return
        
        # Загружаем на file.io
        with open(filename, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f})
        
        os.remove(filename)
        
        if response.status_code == 200:
            link = response.json().get('link')
            await msg.edit_text(f"Готово: {link}")
        else:
            await msg.edit_text("Ошибка загрузки на file.io")
            
    except Exception as e:
        await msg.edit_text(f"Ошибка: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
