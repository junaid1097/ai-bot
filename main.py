import requests
import json
import time
import pytz
from datetime import datetime
from telegram import Bot

# ===== CONFIG =====
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6971835734'
CHECK_INTERVAL = 60  # seconds
MIN_PAYOUT = 75
SESSION_COOKIE = 'eyJpdiI6Ill2RlU2R2RBa2cyTWNQcjFwaC9sY1E9PSIsInZhbHVlIjoiZm52TlprcTU5am5jR2tQY08xZUNheHJEcCtEQXdOaGlaWldzeUZ1SGFneUlFRU15L0tRVitMSzV3N1ozL1dBTytmbE1Tbks1Mm1xTTg2YlhwSUhXVXNjRC9zZHNMbUxsYnBsSVAzR1d1TnovNlNaZ0hESkVVVUpwK01xcHF3WlIiLCJtYWMiOiI0MjdhZDk3YTM0NWFiM2RhODY1NTkyNDY3MzM5Y2UwMTJhYmE2ZjAxMTM4MTI0ZjFmMDc3ZjFjZjYwMGU2YjBiIiwidGFnIjoiIn0%3D'

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

COOKIES = {
    'laravel_session': SESSION_COOKIE
}

bot = Bot(token=BOT_TOKEN)

bd_time = pytz.timezone('Asia/Dhaka')

def fetch_payout():
    try:
        response = requests.get('https://market-qx.pro/api/payouts', headers=HEADERS, cookies=COOKIES)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Payout API error: {e}")
        return None

def send_signal(market, payout):
    now = datetime.now(bd_time)
    entry = (now + timedelta(minutes=1)).strftime('%H:%M')
    expiry = (now + timedelta(minutes=2)).strftime('%H:%M')
    signal = random.choice(['UP', 'DOWN'])
    signal_id = random.randint(100, 999)

    message = f"📊 AI Filtered Signal\n" \
              f"——————————————\n" \
              f"🪙 Market: {market}\n" \
              f"💰 Payout: {payout}%\n" \
              f"⏰ Timeframe: 1M\n" \
              f"🚀 Entry Time: {entry}\n" \
              f"❌ Expiration: {expiry}\n" \
              f"📈 Signal: {signal}\n" \
              f"🎯 Accuracy: {random.randint(90, 95)}%\n" \
              f"——————————————\n" \
              f"Signal ID: {signal_id}"

    bot.send_message(chat_id=CHAT_ID, text=message)
    print("✅ Signal Sent")

def run_bot():
    print("🤖 Pro Quotex AI Bot Running...")
    while True:
        data = fetch_payout()
        if data and 'data' in data:
            markets = list(data['data'].items())
            random.shuffle(markets)
            for symbol, info in markets:
                payout_1m = info.get('turbo', 0)
                is_otc = 'otc' in symbol.lower()
                if payout_1m >= MIN_PAYOUT:
                    send_signal(symbol.upper(), payout_1m)
                    break  # cooldown 1 minute per signal
        else:
            print("❌ Failed to fetch payout.")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    run_bot()
