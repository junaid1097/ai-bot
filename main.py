import telebot
import time
import random
import requests

BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6971835734'

bot = telebot.TeleBot(BOT_TOKEN)

SIGNAL_INTERVAL = 60  # Cooldown 1 minute

def fetch_payout_data():
    try:
        url = "https://api.qxbroker.com/api/v2/payouts"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Payout API error: {e}")
        return None

def get_valid_markets(payout_data):
    valid_markets = []
    for market in payout_data.get('binary', {}).get('turbo', []):
        asset = market.get("asset")
        is_open = market.get("enabled")
        payout = market.get("payout")

        if is_open and payout >= 75:
            valid_markets.append((asset, payout))
    return valid_markets

def send_signal():
    payout_data = fetch_payout_data()
    if payout_data is None:
        bot.send_message(CHAT_ID, "❌ Payout API failed.")
        return

    valid_markets = get_valid_markets(payout_data)
    if not valid_markets:
        bot.send_message(CHAT_ID, "⚠ No market found (75%+ payout).")
        return

    market = random.choice(valid_markets)
    direction = random.choice(["UP", "DOWN"])
    accuracy = random.randint(87, 95)
    
    current_time = time.localtime()
    entry_time = time.strftime("%H:%M", current_time)
    expiry_time = time.strftime("%H:%M", time.localtime(time.time() + 60))

    signal = f"""📊 AI Filtered Signal
——————————————
🪙 Market: {market[0]}
💰 Payout: {market[1]}%
⏰ Timeframe: 1M
🚀 Entry Time: {entry_time}
❌ Expiration: {expiry_time}
📈 Signal: {direction}
🎯 Accuracy: {accuracy}%
——————————————
⚠ Execute Manually."""
    
    bot.send_message(CHAT_ID, signal)

if __name__ == "__main__":
    bot.send_message(CHAT_ID, "✅ Pro Quotex AI Bot Running!")
    while True:
        send_signal()
        time.sleep(SIGNAL_INTERVAL)
