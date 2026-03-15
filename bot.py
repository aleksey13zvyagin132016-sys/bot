import os
import logging
import subprocess
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Твой токен
TOKEN = "8674547291:AAF7zIsm1Wv5xUh8BmU9j4cg2H1sB7ExtAo"

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пришли ссылку на YouTube — скачаю видео и дам ссылку на file.io")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("Скачиваю...")
    
    try:
        # Скачиваем видео
        filename = "video.mp4"
        subprocess.run([
            "yt-dlp",
            "-f", "best[ext=mp4]",
            "-o", filename,
            url
        ], check=True, timeout=300)
        
        # Загружаем на file.io
        with open(filename, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f})
        
        os.remove(filename)  # удаляем видео после загрузки
        
        if response.status_code == 200:
            link = response.json().get('link')
            await msg.edit_text(f"Готово: {link}\n(Ссылка действует 14 дней)")
        else:
            await msg.edit_text("Ошибка при загрузке на file.io")
            
    except Exception as e:
        await msg.edit_text(f"Ошибка: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
