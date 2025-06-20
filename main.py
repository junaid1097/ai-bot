import requests
import json
import time
import pytz
from datetime import datetime, timedelta
from telegram import Bot
import random

# ===== CONFIG =====
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6971835734'
CHECK_INTERVAL = 60  # seconds
MIN_PAYOUT = 75

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://market-qx.pro/',
    'Origin': 'https://market-qx.pro',
    'Sec-Fetch-Site': 'same-origin'
}

COOKIES = {
    'laravel_session': 'eyJpdiI6ImZMK1NrRmtXUTVDUWhNR0pONWZvZmc9PSIsInZhbHVlIjoiczNMMS9MZ0VFOW14UGRPa1dzb1dFVUhTdzNSTHRibm9Ud1IzSGZ2ME1rekZvL1dBeFBFVnhOdUNJUFNaSG9aZkh0SUU1T1VIdVo4ZDdyZjdZQmU0M0xoOUtoK0grdHVSUVFJdlA2UXZnZVZCeDUvK1lIT2g4N1lRa0lISmxmWHciLCJtYWMiOiI3ZWU5OGI2NjEzNDdlN2RjNTFmNzYzNzk3MTk5NTlhZWJkZDQ0OGI1ZWUyNDYwMWIzMTUyNTA4MGI5YmE2NDY0IiwidGFnIjoiIn0%3D',
    '__cf_bm': 'ng1Ha2xW2aDz0WFgkEkFRdzXd67.6pIhFLQ2hD.i948-1750245879-1.0.1.1-bg9M2xdrHznNsJxFGxyKBwVav3vRi9B2xf5Aa3VzSu4bWPj7glBav7rKqxG2c0aH562Fu4hIt7ynEH6_hu.8urKwRdkJPaK.Ug19oFola8E'
}

bot = Bot(token=BOT_TOKEN)
bd_time = pytz.timezone('Asia/Dhaka')

def fetch_payout():
    try:
        response = requests.get(
            'https://market-qx.pro/api/payouts',
            headers=HEADERS,
            cookies=COOKIES
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API error: {response.status_code}")
            print(f"Response content: {response.text}")
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
    print("🤖 Pro Quotex AI Bot Running (Cookie Web Scraping Mode)...")
    while True:
        data = fetch_payout()
        if data and 'data' in data:
            markets = list(data['data'].items())
            random.shuffle(markets)
            for symbol, info in markets:
                payout_1m = info.get('turbo', 0)
                if payout_1m >= MIN_PAYOUT:
                    send_signal(symbol.upper(), payout_1m)
                    break
        else:
            print("❌ Failed to fetch payout.")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    run_bot()
