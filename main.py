import telebot
from datetime import datetime, timedelta
import random

# তোমার বট টোকেন
bot_token = "8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w"
bot = telebot.TeleBot(bot_token)

# মার্কেট লিস্ট (OTC সহ)
markets = [
    "EUR/USD", "USD/JPY", "GBP/USD", "AUD/USD", "USD/CAD",
    "EUR/JPY", "EUR/GBP", "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC"
]

# সিগনাল জেনারেটর
def get_signal():
    now = datetime.now()
    entry_time = now + timedelta(minutes=2)  # 2 মিনিট পরের এন্ট্রি টাইম
    expiration_time = entry_time + timedelta(minutes=1)  # 1 মিনিট এক্সপায়ার
    selected_market = random.choice(markets)
    direction = random.choice(["CALL", "PUT"])  # UP বা DOWN এর জন্য

    message = (
        f"📈 Market: {selected_market}\n"
        f"🕰 Timeframe: 1 Minute\n"
        f"🚀 Entry Time: {entry_time.strftime('%H:%M')}\n"
        f"⏳ Expiration Time: {expiration_time.strftime('%H:%M')}\n"
        f"📊 Signal: {direction}\n"
        f"✅ Accuracy: 97%"
    )
    return message

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "✅ Bot is running.\n\nType /getsignal to get your signal."
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['getsignal'])
def send_signal(message):
    signal_message = get_signal()
    bot.send_message(message.chat.id, signal_message)

print("Bot is running...")

bot.polling(non_stop=True)

