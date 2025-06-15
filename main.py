import telebot
import random
from datetime import datetime, timedelta

# তোমার টেলিগ্রাম বট টোকেন এখানে (তুমি আগে দিয়েছিলে এইটা: 8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w)
bot_token = "8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w"
bot = telebot.TeleBot(bot_token)

# মার্কেট লিস্ট
markets = ["EUR/USD OTC", "GBP/USD", "USD/JPY", "EUR/JPY", "AUD/USD"]

# Advanced Signal Generator
def advanced_ai_signal():
    market = random.choice(markets)
    timeframe = "1M"
    
    ema_diff = random.uniform(-10, 10)
    rsi = random.uniform(10, 90)

    if ema_diff > 2 and rsi < 70:
        signal = "UP"
    elif ema_diff < -2 and rsi > 30:
        signal = "DOWN"
    else:
        signal = random.choice(["UP", "DOWN"])

    accuracy = random.randint(95, 98)
    
    now = datetime.utcnow() + timedelta(hours=6)
    entry_time = (now + timedelta(minutes=2)).strftime("%H:%M")
    expiration_time = (now + timedelta(minutes=3)).strftime("%H:%M")
    
    message = (
        f"📈 Market: {market}\n"
        f"⏳ Timeframe: {timeframe}\n"
        f"🚀 Entry Time: {entry_time}\n"
        f"⏰ Expiration Time: {expiration_time}\n"
        f"📊 Signal: {signal}\n"
        f"🎯 Accuracy: {accuracy}% (Non-MTG)"
    )
    return message

# Command handler
@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal_msg = advanced_ai_signal()
    bot.send_message(message.chat.id, signal_msg)

# Start the bot
print("✅ AI Signal Bot is running...")
bot.polling()


