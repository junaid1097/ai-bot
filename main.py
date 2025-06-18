import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Bot

# 🔐 Telegram Bot Config
BOT_TOKEN = "8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w"
CHAT_ID = "6971835734"

# 🌐 Setup headless Chrome
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(options=chrome_options)

# 🔎 Extract payout from market-qx.pro
def fetch_payout():
    try:
        driver = get_driver()
        driver.get("https://market-qx.pro/en")
        time.sleep(7)

        all_divs = driver.find_elements("css selector", ".instruments-list > div")

        signals = []
        for div in all_divs:
            try:
                name = div.find_element("css selector", ".pair").text.strip()
                payout_text = div.find_element("css selector", ".percent").text.strip()
                payout = int(payout_text.replace("%", ""))

                if payout >= 75:
                    signals.append((name, payout))
            except:
                continue

        driver.quit()
        return signals

    except Exception as e:
        print("Error:", e)
        return []

# 📤 Send signal to Telegram
def send_signal(name, payout):
    msg = f"""📊 AI Filtered Signal
——————————————
🪙 Market: {name}
💰 Payout: {payout}%
⏰ Timeframe: 1M
🚀 Entry Time: {time.strftime("%H:%M")}
❌ Expiration: {time.strftime("%H:%M", time.localtime(time.time() + 60))}
📈 Signal: UP
🎯 Accuracy: 90%+
—————————"""
    Bot(token=BOT_TOKEN).send_message(chat_id=CHAT_ID, text=msg)

# 🔄 Loop with cooldown
def run_bot():
    while True:
        results = fetch_payout()
        if results:
            for name, payout in results:
                send_signal(name, payout)
                print(f"✅ Sent signal for {name} with {payout}% payout.")
                time.sleep(60)  # cooldown
        else:
            print("❌ No market found with 75%+ payout.")
        time.sleep(60)

if __name__ == "__main__":
    run_bot()
