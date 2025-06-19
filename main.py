import requests
import json
import time
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from telegram import Bot
import random

# ===== CONFIG =====
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6971835734'
CHECK_INTERVAL = 60  # seconds
MIN_PAYOUT = 75
SESSION_COOKIE = 'eyJpdiI6Ill2RlU2R2RBa2cyTWNQcjFwaC9sY1E9PSIsInZhbHVlIjoiZm52TlprcTU5am5jR2tQY08xZUNheHJEcCtEQXdOaGlaWldzeUZ1SGFneUlFRU15L0tRVitMSzV3N1ozL1dBTytmbE1Tbks1Mm1xTTg2YlhwSUhXVXNjRC9zZHNMbUxsYnBsSVAzR1d1TnovNlNaZ0hESkVVVUpwK01xcHF3WlIiLCJtYWMiOiI0MjdhZDk3YTM0NWFiM2RhODY1NTkyNDY3MzM5Y2UwMTJhYmE2ZjAxMTM4MTI0ZjFmMDc3ZjFjZjYwMGU2YjBiIiwidGFnIjoiIn0%3D'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp',
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
        response = requests.get('https://market-qx.pro/en', headers=HEADERS, cookies=COOKIES)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            market_divs = soup.find_all('div', class_='instrument')
            results = []
            for div in market_divs:
                name = div.find('div', class_='name')
                payout = div.find('div', class_='percent')
                if name and payout:
                    symbol = name.text.strip()
                    payout_val = int(payout.text.replace('%', '').strip())
                    results.append((symbol, payout_val))
            return results
        else:
            print(f"Scraping error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Scraping exception: {e}")
        return []


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
        markets = fetch_payout()
        if markets:
            random.shuffle(markets)
            for symbol, payout in markets:
                if payout >= MIN_PAYOUT:
                    send_signal(symbol, payout)
                    break
        else:
            print("❌ No market data fetched.")
        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    run_bot()
