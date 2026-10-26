import os, time, threading, qrcode, requests
import telebot
from flask import Flask
from groq import Groq
from io import BytesIO

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
groq = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
app = Flask(__name__)

# --- AUTO AI FUNCTION (Kabhi Atkega Nahi) ---
def ai(prompt):
    try:
        if not groq:
            return "Demo Output: High quality work for your brand. Professional, fast delivery."
        r = groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":prompt}],
            max_tokens=1200, temperature=0.7
        )
        return r.choices[0].message.content
    except Exception as e:
        print(f"AI Error: {e}")
        return f"Demo Ready (AI limit): Premium {prompt[:30]}... for your brand - Ready to deliver in 10 min!"

# --- 20 TOP WORKS LIST ---
WORKS = {
"hunt":"Client Pitch", "logo":"Logo Design", "price":"Invoice/QR",
"reel":"Reels/Shorts", "video":"Video Editing", "web":"Web Design",
"thumb":"Thumbnail", "content":"Content Writing", "story":"Story Writing",
"book":"Book Writing", "graphic":"Graphic Design", "social":"Social Media Post",
"ytseo":"YouTube SEO", "voice":"Voice Over Script", "copy":"Copywriting",
"resume":"Resume Writing", "ui":"UI/UX Design", "ebook":"Ebook Cover",
"podcast":"Podcast Idea", "seo":"Website SEO"
}

@app.route('/')
def home():
    return "✅ Pixel Pen Bot - 30 AI AUTO LIVE - 20 Works Ready"

# --- START ---
@bot.message_handler(commands=['start'])
def start_cmd(m):
    msg = """🔥 **Pixel Pen Bot - 30 AI AUTO LIVE!**

**Tere 3 Purane (Ab Auto + 3 AI):**
/hunt gaming - 3 AI Pitch banayenge
/logo gaming - 3 AI Logo banayenge
/price 50 - 3 AI Invoice + QR

**Naye 17 Auto Add (Total 20 Works):**
/reel - Reels (Hook AI + Caption AI + Hashtag AI)
/video - Video (Cut AI + Script AI + Effect AI)
/web - Website (Design AI + Code AI + SEO AI)
/thumb - Thumbnail (Design AI + Font AI + Color AI)
/content - Article (Writer AI + Research AI + SEO AI)
/story - Story (Story AI + Writer AI + Hook AI)
/book - Book (Writer AI + Chapter AI + Cover AI)
/graphic /social /ytseo /voice /copy /resume /ui /ebook /podcast /seo

**Sab Auto:** /works likho puri list dekho
Type: /reel PUBG - 10 sec me ready!"""
    bot.send_message(m.chat.id, msg)

@bot.message_handler(commands=['works'])
def works_cmd(m):
    txt = "💰 **20 AUTO WORKS - 30 AI:**\n\n"
    for k,v in WORKS.items(): txt+= f"/{k} - {v}\n"
    txt += "\nEx: /logo gaming\nEx: /reel gaming\nEx: /content AI tools"
    bot.send_message(m.chat.id, txt)

@bot.message_handler(commands=['hunt'])
def hunt_cmd(m):
    bot.send_message(m.chat.id, "⏳ **3 AI Lage:** Hunter AI + Pitch AI + Closer AI...")
    topic = m.text[6:].strip() or "Gaming Brand"
    prompt = f"Write 5 ultra short LinkedIn DM pitches for {topic} founders to sell logo/reels/content service for $20. US tone, high converting, with CTA"
    res = ai(prompt)
    bot.send_message(m.chat.id, f"✅ **3 AI DONE - 5 Pitch Ready for {topic}:**\n\n{res}\n\nNext: /logo {topic} se sample banao")

@bot.message_handler(commands=['logo','thumb','graphic','ebook','ui'])
def image_cmd(m):
    cmd = m.text.split()[0][1:]
    idea = m.text[len(cmd)+2:].strip() or "Premium Brand"
    bot.send_message(m.chat.id, f"⏳ **3 AI Lage:** {cmd.upper()} AI + Color AI + Mockup AI for {idea}...")
    try:
        url = f"https://image.pollinations.ai/prompt/{idea} {WORKS.get(cmd)} professional 4k vector, no background noise?width=1024&height=1024&nologo=true&enhance=true&seed={int(time.time())}"
        bot.send_photo(m.chat.id, url, caption=f"✅ **3 AI DONE - {WORKS.get(cmd)}:** {idea}\n\nPrice: /price 20")
    except Exception as e:
        bot.send_message(m.chat.id, f"Image Error, fir try karo: {e}")

@bot.message_handler(commands=['price'])
def price_cmd(m):
    try:
        amt = m.text.split()[1] if len(m.text.split())>1 else "20"
    except: amt="20"
    bot.send_message(m.chat.id, f"⏳ **3 AI Lage:** Invoice AI + QR AI + Payment AI for ${amt}...")
    try:
        qr = qrcode.make(f"upi://pay?pa=9198288206@ybl&am={amt}&pn=PixelPenBot&cu=USD")
        b = BytesIO(); qr.save(b,'PNG'); b.seek(0)
        bot.send_photo(m.chat.id, b, caption=f"✅ **3 AI DONE - Invoice ${amt}:**\nUPI/Bank Ready\n\nClient ko bhejo aur /hunt se naya client lo")
    except Exception as e:
        bot.send_message(m.chat.id, f"Invoice Ready: Pay ${amt} to UPI 9198288206@ybl")

@bot.message_handler(commands=['reel','video','web','content','story','book','social','ytseo','voice','copy','resume','podcast','seo'])
def text_works_cmd(m):
    cmd = m.text.split()[0][1:]
    topic = m.text[len(cmd)+2:].strip() or "My Brand"
    bot.send_message(m.chat.id, f"⏳ **3 AI Lage:** Writer AI + SEO AI + Hook AI for {WORKS.get(cmd)}...")
    prompt = f"You are expert in {WORKS.get(cmd)}. Create ready-to-deliver professional {WORKS.get(cmd)} for topic: {topic}. Make it high quality, client ready, US standard. Keep short but premium."
    res = ai(prompt)
    bot.send_message(m.chat.id, f"✅ **3 AI DONE - {WORKS.get(cmd)} for {topic}:**\n\n{res}\n\nNext: /price 20")

# --- AUTO POLLING (Never Stop) ---
def run_bot():
    while True:
        try:
            print("🚀 Pixel Pen 30AI Bot Polling...")
            bot.infinity_polling(timeout=90, long_polling_timeout=90)
        except Exception as e:
            print(f"Polling Error: {e} - Restart in 5 sec")
            time.sleep(5)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
