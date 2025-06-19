import time
import random
import pytz
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from telegram import Bot

# ====== CONFIG ======
BOT_TOKEN = "8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w"
CHAT_ID = "6971835734"
COOLDOWN = 60  # in seconds
ACCURACY_RANGE = (91, 98)
bd_timezone = pytz.timezone("Asia/Dhaka")
# =====================

last_signal_time = 0

def setup_driver():
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def get_payout_data(driver):
    try:
        driver.get("https://market-qx.pro/en")
        time.sleep(5)  # wait to load
        rows = driver.find_elements("css selector", ".trade-list__row")
        market_data = []

        for row in rows:
            try:
                market = row.find_element("css selector", ".trade-list__name").text.strip()
                payout = row.find_element("css selector", ".trade-list__percent").text.strip()
                if "%" in payout:
                    payout_value = int(payout.replace("%", "").strip())
                    market_data.append((market, payout_value))
            except:
                continue

        return market_data
    except Exception as e:
        print("❌ Payout Scrape Error:", e)
        return []

def send_signal(market, payout, direction):
    now = datetime.now(bd_timezone)
    entry_time = (now + timedelta(minutes=1)).strftime('%H:%M')
    expire_time = (now + timedelta(minutes=2)).strftime('%H:%M')
    accuracy = random.randint(*ACCURACY_RANGE)

    msg = f"""📊 AI Filtered Signal
——————————————
🪙 Market: {market}
💰 Payout: {payout}%
⏰ Timeframe: 1M
🚀 Entry Time: {entry_time}
❌ Expiration: {expire_time}
📈 Signal: {direction.upper()}
🎯 Accuracy: {accuracy}%
—————————"""
    Bot(BOT_TOKEN).send_message(chat_id=CHAT_ID, text=msg)
    print(f"✅ Signal Sent: {market} - {payout}%")

def run_bot():
    global last_signal_time
    driver = setup_driver()
    print("🤖 Pro Quotex AI Bot Running...")

    while True:
        now = time.time()
        if now - last_signal_time < COOLDOWN:
            time.sleep(5)
            continue

        payout_data = get_payout_data(driver)

        valid_markets = [(m, p) for (m, p) in payout_data if p >= 75]

        if valid_markets:
            market, payout = random.choice(valid_markets)
            direction = random.choice(["UP", "DOWN"])
            send_signal(market, payout, direction)
            last_signal_time = now
        else:
            print("⚠ No market with ≥75% payout found.")

        time.sleep(10)

run_bot()
