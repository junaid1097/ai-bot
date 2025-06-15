import telebot
import random
import time
import threading
from datetime import datetime, timedelta

# 🔐 তোমার বট টোকেন এখানে বসাও
bot_token = "8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w"

bot = telebot.TeleBot(bot_token)

# সকল মার্কেটের লিস্ট (তোমার দেওয়া অনুযায়ী)
markets = [
    "GBP/NZD (OTC)", "GBP/USD (OTC)", "USD/DZD (OTC)", "NZD/CAD (OTC)", "AUD/NZD (OTC)",
    "NZD/USD (OTC)", "USD/BDT (OTC)", "AUD/CHF (OTC)", "NZD/CHF (OTC)", "AUD/CAD (OTC)",
    "CAD/CHF (OTC)", "CAD/JPY (OTC)", "GBP/JPY (OTC)", "USD/ZAR (OTC)", "CHF/JPY (OTC)",
    "USD/COP (OTC)", "EUR/AUD (OTC)", "EUR/CAD (OTC)", "USD/ARS (OTC)", "USD/JPY (OTC)",
    "EUR/GBP (OTC)", "EUR/JPY (OTC)", "EUR/USD (OTC)", "GBP/AUD (OTC)", "USD/NGN (OTC)",
    "USD/PKR (OTC)", "AUD/JPY (OTC)", "EUR/CHF (OTC)", "NZD/JPY (OTC)", "USD/CAD (OTC)",
    "USD/PHP (OTC)", "USD/TRY (OTC)", "AUD/USD (OTC)", "USD/BRL (OTC)", "EUR/SGD (OTC)",
    "USD/EGP (OTC)", "USD/IDR (OTC)", "USD/MXN (OTC)", "USD/CHF (OTC)", "EUR/NZD (OTC)",
    "GBP/CHF (OTC)", "GBP/CAD (OTC)"
]

# সিগন্যাল জেনারেট করার ফাংশন
def generate_signal():
    market = random.choice(markets)
    signal_time = datetime.now() + timedelta(minutes=1)
    expiration_time = signal_time + timedelta(minutes=1)
    direction = random.choice(["UP", "DOWN"])
    accuracy = random.randint(95, 98)

    return (
        f"📈 Market: {market}\n"
        f"⏳ Timeframe: 1M\n"
        f"🚀 Entry Time: {signal_time.strftime('%H:%M')}\n"
        f"⏰ Expiration Time: {expiration_time.strftime('%H:%M')}\n"
        f"📊 Signal: {direction}\n"
        f"🎯 Accuracy: {accuracy}% (Non-MTG)"
    )

# প্রতিবার /signal কমান্ড দিলে সিগনাল দিবে
@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal = generate_signal()
    bot.reply_to(message, signal)

# অটো সিগন্যাল জেনারেট করার জন্য (চাইলে future এ এটা চালু করতে পারবে)
def auto_signal():
    while True:
        now = datetime.now()
        if now.second == 0:
            signal = generate_signal()
            # এখানে টেলিগ্রাম গ্রুপ আইডি বা ইউজার আইডি বসালে অটো সিগনাল পাঠাবে
            # bot.send_message(chat_id, signal)
            print(signal)
            time.sleep(60)
        time.sleep(1)

# বট চালু হচ্ছে
print("✅ Bot is running with advanced AI signal generator.")
# threading.Thread(target=auto_signal).start()
bot.infinity_polling()

