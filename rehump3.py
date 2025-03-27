import telebot
import yt_dlp
import os

# 🔹 Replace with your Telegram Bot Token
BOT_TOKEN = "7829114873:AAGw1spPfbWHqK1xpC6eqmWt9rcM0djoCHQ"
bot = telebot.TeleBot(BOT_TOKEN)

def download_audio(youtube_url):
    """Download YouTube audio without FFmpeg"""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'noplaylist': True,  # Prevent downloading playlists
            'quiet': True,  # Reduce console logs
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info)

        # Find the downloaded file (webm or m4a)
        for file in os.listdir():
            if file.startswith("downloaded_audio") and (file.endswith(".webm") or file.endswith(".m4a")):
                return file  # Return filename
        
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "🎵 Send a YouTube link to get audio!")

@bot.message_handler(func=lambda message: "youtube.com" in message.text or "youtu.be" in message.text)
def process_message(message):
    youtube_url = message.text
    bot.send_message(message.chat.id, "⏳ Downloading audio...")

    audio_file = download_audio(youtube_url)
    if audio_file:
        with open(audio_file, "rb") as audio:
            bot.send_audio(message.chat.id, audio, timeout=120)  # Increased timeout
        os.remove(audio_file)  # Delete file after sending
    else:
        bot.send_message(message.chat.id, "❌ Could not fetch audio. Try again later!")

# 🔹 Start the bot with long polling and increased timeout settings
bot.polling(timeout=60, long_polling_timeout=60)