import os
import openai
import telebot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши мне что-нибудь, и я спрошу у OpenAI 🤖")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content.strip())
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

print("Бот запущен...")
bot.polling()
