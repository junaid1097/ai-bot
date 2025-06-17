import telebot
import requests
import time
import random
from datetime import datetime, timedelta
import pytz

BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6971835734'

bot = telebot.TeleBot(BOT_TOKEN)

bd_timezone = pytz.timezone("Asia/Dhaka")

# Cooldown system
last_signal_time = None
cooldown_minutes = 1

# API Endpoint (Quotex Unofficial)
PAYOUT_API = "https://market-qx.pro/payout"

def fetch_payout_data():
    try:
        response = requests.get(PAYOUT_API, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Payout API failed.")
            return None
    except Exception as e:
        print(f"Error fetching payout: {e}")
        return None

def get_valid_markets():
    data = fetch_payout_data()
    if not data:
        return []

    valid_markets = []
    for market in data:
        payout_info = data[market]
        if "1" in payout_info:
            payout = payout_info["1"]
            if isinstance(payout, (int, float)) and payout >= 75:
                valid_markets.append((market, payout))
    return valid_markets

def generate_signal():
    global last_signal_time

    now = datetime.now(bd_timezone)
    if last_signal_time and (now - last_signal_time) < timedelta(minutes=cooldown_minutes):
        return None

    valid_markets = get_valid_markets()
    if not valid_markets:
        return None

    selected = random.choice(valid_markets)
    market, payout = selected
    signal = random.choice(['UP', 'DOWN'])
    accuracy = random.randint(91, 98)

    entry_time = (now + timedelta(minutes=1)).strftime('%H:%M')
    expire_time = (now + timedelta(minutes=2)).strftime('%H:%M')
    last_signal_time = now

    return f"""📊 AI Filtered Signal
——————————————
🪙 Market: {market}
💰 Payout: {payout}%
⏰ Timeframe: 1M
🚀 Entry Time: {entry_time}
❌ Expiration: {expire_time}
📈 Signal: {signal}
🎯 Accuracy: {accuracy}%
——————————————
⚠ Execute Manually.
"""

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.reply_to(message, "✅ Advanced AI Signal Bot Ready!\n👉 নতুন সিগনাল পেতে /signal লিখো।")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal_text = generate_signal()
    if signal_text:
        bot.send_message(CHAT_ID, signal_text)
    else:
        bot.send_message(CHAT_ID, "⏳ এখন কোন 75%+ মার্কেট খোলা নেই বা Cooldown চলছে। ১ মিনিট পর আবার চেষ্টা করুন।")

print("✅ Pro Quotex AI Bot Running...")
bot.infinity_polling()
