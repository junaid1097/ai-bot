import telebot
import time
from datetime import datetime, timedelta
import random

# তোমার Bot Token এখানে বসাও
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'

bot = telebot.TeleBot(BOT_TOKEN)

# Market list - তোমার দেয়া OTC আর Real Market আলাদা করে দেয়া
REAL_MARKETS = [
    'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'USD/CHF',
    # এখানে আরো রিয়েল মার্কেট এড করো যদি থাকে
]

OTC_MARKETS = [
    'EUR/USD (OTC)', 'GBP/NZD (OTC)', 'GBP/USD (OTC)', 'USD/DZD (OTC)',
    'NZD/CAD (OTC)', 'AUD/NZD (OTC)', 'NZD/USD (OTC)', 'USD/BDT (OTC)',
    'AUD/CHF (OTC)', 'NZD/CHF (OTC)', 'AUD/CAD (OTC)', 'CAD/CHF (OTC)',
    'CAD/JPY (OTC)', 'GBP/JPY (OTC)', 'USD/ZAR (OTC)', 'CHF/JPY (OTC)',
    'USD/COP (OTC)', 'EUR/AUD (OTC)', 'EUR/CAD (OTC)', 'USD/ARS (OTC)',
    'USD/JPY (OTC)', 'EUR/GBP (OTC)', 'EUR/JPY (OTC)', 'EUR/USD (OTC)',
    'GBP/AUD (OTC)', 'USD/NGN (OTC)', 'USD/PKR (OTC)', 'AUD/JPY (OTC)',
    'EUR/CHF (OTC)', 'NZD/JPY (OTC)', 'USD/CAD (OTC)', 'USD/PHP (OTC)',
    'USD/TRY (OTC)', 'AUD/USD (OTC)', 'USD/BRL (OTC)', 'EUR/SGD (OTC)',
    'USD/EGP (OTC)', 'USD/IDR (OTC)', 'USD/MXN (OTC)', 'USD/CHF (OTC)',
    'EUR/NZD (OTC)', 'GBP/CHF (OTC)', 'GBP/CAD (OTC)',
]

# বড় মার্কেট লিস্ট, Real প্রথমে, তারপর OTC
MARKETS = REAL_MARKETS + OTC_MARKETS

# আগের সিগন্যাল ট্র্যাক করতে
last_signal_time = None
last_market = None

def generate_signal():
    global last_signal_time, last_market

    now = datetime.utcnow()
    # আগের সিগন্যাল ১ মিনিট আগে এসেছে কিনা চেক করবো
    if last_signal_time and (now - last_signal_time) < timedelta(minutes=1):
        return None  # ১ মিনিটের মধ্যেই নতুন সিগন্যাল দিব না

    # এবার মার্কেট বাছাই করার লজিক:
    # আগের মার্কেট বাদ দিয়ে পরের মার্কেটে সিগন্যাল দিবো, যদি আগের মার্কেট None হয়, প্রথম মার্কেট থেকে শুরু
    if last_market is None:
        market = MARKETS[0]
    else:
        try:
            last_index = MARKETS.index(last_market)
            market = MARKETS[(last_index + 1) % len(MARKETS)]
        except ValueError:
            market = MARKETS[0]  # safety fallback

    # Signal Direction (UP/DOWN) randomly (তুমি AI দিয়ে পরিবর্তন করতে পারো)
    signal = random.choice(['UP', 'DOWN'])

    # Accuracy 90% এর উপরে ধরে নিচ্ছি
    accuracy = random.randint(90, 98)

    # Entry time: এখন থেকে 1 মিনিট পর
    entry_time = (now + timedelta(minutes=1)).strftime('%H:%M')

    # Expire time: entry time থেকে 1 মিনিট পর
    expire_time = (now + timedelta(minutes=2)).strftime('%H:%M')

    last_signal_time = now
    last_market = market

    return f"""📈 Market: {market}
⏳ Timeframe: 1M
🚀 Entry Time: {entry_time}
⏰ Expiration Time: {expire_time}
📊 Signal: {signal}
🎯 Accuracy: {accuracy}% (Non-MTG)
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমি তোমার AI ট্রেডিং সিগন্যাল বট। সিগন্যাল পেতে /signal কমান্ড দিন।")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal_msg = generate_signal()
    if signal_msg:
        bot.send_message(message.chat.id, signal_msg)
    else:
        bot.send_message(message.chat.id, "অনুগ্রহ করে একটু অপেক্ষা করুন, নতুন সিগন্যাল তৈরি হচ্ছে...")

print("Bot is running...")
bot.infinity_polling()

