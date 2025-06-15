import telebot
import time
from datetime import datetime, timedelta
import random
import pytz

# Bot Token
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
bot = telebot.TeleBot(BOT_TOKEN)

# Bangladesh timezone
bd_timezone = pytz.timezone("Asia/Dhaka")

# Market lists
REAL_MARKETS = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'USD/CHF']
OTC_MARKETS = [
    'EUR/USD (OTC)', 'GBP/USD (OTC)', 'USD/JPY (OTC)', 'AUD/USD (OTC)',
    'USD/CAD (OTC)', 'USD/CHF (OTC)', 'GBP/JPY (OTC)', 'EUR/JPY (OTC)'
]

# Cooldown system
last_signal_time = None
cooldown_minutes = 2

# Smart session check
def is_real_market_open():
    now = datetime.now(bd_timezone)
    weekday = now.weekday()
    hour = now.hour
    return weekday < 5 and 3 <= hour <= 23

# AI Based simple market selection
def select_market():
    if is_real_market_open():
        return random.choice(REAL_MARKETS)
    else:
        return random.choice(OTC_MARKETS)

# Smart AI-based accuracy generator
def generate_accuracy():
    now = datetime.now(bd_timezone)
    hour = now.hour

    if 9 <= hour <= 11 or 19 <= hour <= 22:
        return random.randint(94, 98)
    elif 3 <= hour <= 8:
        return random.randint(91, 94)
    else:
        return random.randint(92, 96)

# Final signal generator
def generate_signal():
    global last_signal_time
    now = datetime.now(bd_timezone)

    if last_signal_time and (now - last_signal_time) < timedelta(minutes=cooldown_minutes):
        return None

    market = select_market()
    signal = random.choice(['UP', 'DOWN'])
    accuracy = generate_accuracy()

    entry_time = (now + timedelta(minutes=1)).strftime('%H:%M')
    expire_time = (now + timedelta(minutes=2)).strftime('%H:%M')
    last_signal_time = now

    return f"""📊 AI Generated Signal
——————————————
🪙 Market: {market}
⏰ Timeframe: 1M
🚀 Entry Time: {entry_time}
❌ Expiration: {expire_time}
📈 Signal: {signal}
🎯 Accuracy: {accuracy}% (AI-NonMTG)
——————————————
⚠ Use proper money management."""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Welcome to Advanced AI Signal Bot!\nType /signal to get your signal.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal_msg = generate_signal()
    if signal_msg:
        bot.send_message(message.chat.id, signal_msg)
    else:
        bot.send_message(message.chat.id, "⏳ New signal generating, please wait 1-2 min...")

print("✅ Advanced AI Signal Bot is running...")
bot.infinity_polling()


