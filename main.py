import telebot
from datetime import datetime, timedelta
import random
import pytz
import json
import os

# তোমার বট টোকেন এখানে বসাও:
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'

bot = telebot.TeleBot(BOT_TOKEN)

bd_timezone = pytz.timezone("Asia/Dhaka")
last_signal_time = None
cooldown_minutes = 2

REAL_MARKETS = {
    'EUR/USD': (3, 23),
    'GBP/USD': (7, 23),
    'USD/JPY': (3, 23),
    'AUD/USD': (3, 16),
    'USD/CAD': (13, 23),
    'USD/CHF': (7, 23)
}

OTC_MARKETS = [
    'EUR/USD (OTC)', 'GBP/USD (OTC)', 'USD/JPY (OTC)', 'AUD/USD (OTC)',
    'USD/CAD (OTC)', 'USD/CHF (OTC)', 'GBP/JPY (OTC)', 'EUR/JPY (OTC)'
]

RESULT_FILE = "profit_log.json"

def load_results():
    if not os.path.exists(RESULT_FILE):
        return {"win": 0, "loss": 0}
    with open(RESULT_FILE, 'r') as f:
        return json.load(f)

def save_results(data):
    with open(RESULT_FILE, 'w') as f:
        json.dump(data, f)

results = load_results()

def is_real_market_open():
    now = datetime.now(bd_timezone)
    weekday = now.weekday()
    return weekday < 5

def get_active_real_markets():
    now = datetime.now(bd_timezone)
    hour = now.hour
    active_markets = []
    for market, (start_hour, end_hour) in REAL_MARKETS.items():
        if start_hour <= hour <= end_hour:
            active_markets.append(market)
    return active_markets

def select_market():
    if is_real_market_open():
        active_real = get_active_real_markets()
        if active_real:
            return random.choice(active_real)
        else:
            return random.choice(OTC_MARKETS)
    else:
        return random.choice(OTC_MARKETS)

def generate_accuracy():
    now = datetime.now(bd_timezone)
    hour = now.hour
    if 9 <= hour <= 11 or 19 <= hour <= 22:
        return random.randint(85, 98)
    elif 3 <= hour <= 8:
        return random.randint(82, 92)
    else:
        return random.randint(80, 95)

def generate_signal():
    global last_signal_time
    now = datetime.now(bd_timezone)

    if last_signal_time and (now - last_signal_time) < timedelta(minutes=cooldown_minutes):
        return None

    accuracy = generate_accuracy()
    if accuracy < 80:
        return "🚫 Market condition not stable now (below 80%). Signal Skipped."

    market = select_market()
    direction = random.choice(['UP', 'DOWN'])
    entry_time = (now + timedelta(minutes=1)).strftime('%H:%M')
    expire_time = (now + timedelta(minutes=2)).strftime('%H:%M')
    last_signal_time = now

    return {
        "message": f"""📊 AI Filtered Signal
——————————————
🪙 Market: {market}
⏰ Timeframe: 1M
🚀 Entry Time: {entry_time}
❌ Expiration: {expire_time}
📈 Signal: {direction}
🎯 Accuracy: {accuracy}%
——————————————
⚠ Execute Manually.""",
        "market": market,
        "signal": direction
    }

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Welcome to Professional AI Signal Bot!\n\n👉 Use /signal to generate signal.\n👉 Use /win or /loss to record result.\n👉 Use /report to see profit report.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal_data = generate_signal()
    if signal_data:
        message_id = bot.send_message(message.chat.id, signal_data["message"]).message_id
        bot.send_message(message.chat.id, f"Signal ID: {message_id}")
    else:
        bot.send_message(message.chat.id, "⏳ Cooldown active. Please wait 1-2 min.")

@bot.message_handler(commands=['win'])
def record_win(message):
    results["win"] += 1
    save_results(results)
    bot.reply_to(message, f"✅ Win Recorded!\nTotal: {results['win']} Wins | {results['loss']} Losses")

@bot.message_handler(commands=['loss'])
def record_loss(message):
    results["loss"] += 1
    save_results(results)
    bot.reply_to(message, f"❌ Loss Recorded!\nTotal: {results['win']} Wins | {results['loss']} Losses")

@bot.message_handler(commands=['report'])
def report(message):
    total = results["win"] + results["loss"]
    if total == 0:
        win_rate = 0
    else:
        win_rate = (results["win"] / total) * 100
    bot.reply_to(message, f"""📊 Profit Report
————————————
✅ Wins: {results['win']}
❌ Losses: {results['loss']}
🎯 Win Rate: {win_rate:.2f}%
————————————""")

print("✅ Professional AI Signal Bot is running...")
bot.infinity_polling(timeout=60, long_polling_timeout=30)
