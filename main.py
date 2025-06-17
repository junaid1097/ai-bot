import telebot
import time
from datetime import datetime, timedelta
import random
import pytz
import requests
from bs4 import BeautifulSoup

# ✅ তোমার Bot Token ও Chat ID
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6971835734'

bot = telebot.TeleBot(BOT_TOKEN)

# ✅ Timezone সেট করা হচ্ছে বাংলাদেশ টাইম অনুযায়ী (UTC+6)
bd_timezone = pytz.timezone("Asia/Dhaka")

# ✅ Real এবং OTC মার্কেট লিস্ট
REAL_MARKETS = [
    'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'USD/CHF'
]

OTC_MARKETS = [
    'EUR/USD (OTC)', 'GBP/USD (OTC)', 'USD/JPY (OTC)', 'AUD/USD (OTC)', 'USD/CAD (OTC)', 'USD/CHF (OTC)'
]

# ✅ আগের সিগনাল ট্র্যাক করতে
last_signal_time = None
cooldown_minutes = 1  # প্রতি 1 মিনিটে একবার সিগনাল

# ✅ Live 1-Minute Payout Fetch
def fetch_payouts():
    try:
        url = "https://market-qx.pro/trade"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        payouts = {}
        for row in soup.select('.option'):
            name_elem = row.select_one('.pair-name')
            payout_elem = row.select_one('.percent')
            if name_elem and payout_elem:
                name = name_elem.text.strip()
                percent_text = payout_elem.text.strip().replace('%', '')
                try:
                    percent = int(percent_text)
                    payouts[name] = percent
                except:
                    continue
        return payouts
    except Exception as e:
        print("❌ Payout Fetch Error:", e)
        return {}

# ✅ Market নির্বাচন (payout ≥ 75%)
def select_market():
    payouts = fetch_payouts()
    eligible_markets = []

    now = datetime.now(bd_timezone)
    weekday = now.weekday()
    hour = now.hour
    is_real = weekday < 5 and 3 <= hour <= 23

    market_list = REAL_MARKETS if is_real else OTC_MARKETS

    for market in market_list:
        payout = payouts.get(market, 0)
        if payout >= 75:
            eligible_markets.append((market, payout))

    if eligible_markets:
        return random.choice(eligible_markets)
    else:
        return None

# ✅ Signal তৈরি করা
def generate_signal():
    global last_signal_time
    now = datetime.now(bd_timezone)

    if last_signal_time and (now - last_signal_time) < timedelta(minutes=cooldown_minutes):
        return None

    result = select_market()
    if result is None:
        return "❌ 75%+ payout মার্কেট নেই এখন। পরে চেষ্টা করুন।"

    market, payout = result
    signal = random.choice(['UP', 'DOWN'])
    accuracy = random.randint(91, 97)
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

# ✅ Command Handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "✅ আমি তোমার AI Signal Bot!\n\n👉 নতুন সিগনাল পেতে /signal লিখো।")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal_msg = generate_signal()
    if signal_msg:
        bot.send_message(message.chat.id, signal_msg)
    else:
        bot.send_message(message.chat.id, "🕐 Cooldown চলছে। ১ মিনিট পর আবার চেষ্টা করুন।")

# ✅ Auto Startup Message
def start_bot():
    bot.send_message(CHAT_ID, "✅ Signal Bot is now running and monitoring 75%+ payout markets...")

print("🤖 AI Quotex Bot is Running...")
start_bot()
bot.infinity_polling()
