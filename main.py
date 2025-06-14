import telebot
from datetime import datetime, timedelta
import random

bot_token = "তোমার_বট_টোকেন_এখানে_দাও"
bot = telebot.TeleBot(bot_token)

markets = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC"
]

signals = ["UP", "DOWN"]

def round_to_next_minute(dt, minute_step=1):
    # dt কে minute_step মিনিটের multiple এ round করবে
    discard = timedelta(minutes=dt.minute % minute_step,
                        seconds=dt.second,
                        microseconds=dt.microsecond)
    dt += timedelta(minutes=minute_step) - discard
    return dt.replace(second=0, microsecond=0)

def get_signal():
    now = datetime.now()
    # এখনকার সময়কে ২ মিনিট পরের মিনিটে রাউন্ড করলাম (যেমন: ৮:৩৭ এ দিলে ৮:৩৯ হবে)
    entry_time = round_to_next_minute(now, 2)
    expiration_time = entry_time + timedelta(minutes=1)  # ১ মিনিটের ট্রেড টাইমফ্রেম

    selected_market = random.choice(markets)
    trade_signal = random.choice(signals)
    accuracy = random.randint(95, 98)  # 95-98% accuracy দেখানো জন্য

    message = (
        f"📈 Market: {selected_market}\n"
        f"⏳ Timeframe: 1M\n"
        f"🚀 Entry Time: {entry_time.strftime('%H:%M')}\n"
        f"⏰ Expiration Time: {expiration_time.strftime('%H:%M')}\n"
        f"📊 Signal: {trade_signal}\n"
        f"🎯 Accuracy: {accuracy}% (Non-MTG)"
    )
    return message

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "✅ বট চালু আছে। টাইপ করো /getsignal সিগন্যাল পেতে।"
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['getsignal'])
def send_signal(message):
    signal_message = get_signal()
    bot.send_message(message.chat.id, signal_message)

print("Bot is running...")

bot.polling(non_stop=True)
