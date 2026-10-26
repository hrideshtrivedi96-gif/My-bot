import os, threading
import telebot
from flask import Flask
from groq import Groq

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
groq = Groq(api_key=GROQ_KEY)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🔥 Bot Live! FREE Wala\n\nCommands:\n/hunt - Client Pitch\n/logo gaming - Logo banao\n/price 10 - Invoice")

@bot.message_handler(commands=['hunt'])
def hunt(m):
    bot.send_message(m.chat.id, "⏳ 5 Pitch bana raha hu...")
    prompt = "Write 5 short LinkedIn DMs for US Gaming Founders, each specific compliment + 1 logo mistake + I made free quick fix + US bank $10, 2 lines"
    res = groq.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
    bot.send_message(m.chat.id, res.choices[0].message.content)

@bot.message_handler(commands=['logo'])
def logo(m):
    idea = m.text.replace('/logo','').strip() or "Esports Logo"
    url = f"https://image.pollinations.ai/prompt/{idea} logo vector?width=1024&nologo=true"
    bot.send_photo(m.chat.id, url)

@app.route('/')
def home():
    return "Bot Running FREE - Hridesh"

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()
app.run(host='0.0.0.0', port=10000)
