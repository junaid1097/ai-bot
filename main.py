import time
import random
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ✅ Telegram Setup
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6365951493'
bot = telegram.Bot(token=BOT_TOKEN)

# ✅ Headless Chrome Setup for Replit
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
service = Service("/usr/bin/chromedriver")

# ✅ Start Browser
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_payouts():
    driver.get("https://market-qx.pro/en")
    time.sleep(5)
    
    try:
        markets = driver.find_elements(By.CLASS_NAME, "trade__list-item")
        signals = []

        for market in markets:
            try:
                name = market.find_element(By.CLASS_NAME, "trade__list-name").text.strip()
                payout_text = market.find_element(By.CLASS_NAME, "trade__list-profit").text.strip()
                payout = int(payout_text.replace("%", "").strip())

                if payout >= 75:
                    direction = random.choice(["⬆️ UP", "⬇️ DOWN"])
                    signal_msg = f"""
📊 Market: {name}
💰 Payout: {payout}%
📈 Signal: {direction}
                    """.strip()
                    signals.append(signal_msg)

            except Exception as e:
                continue
        
        return signals
    except Exception as e:
        return ["❌ Error fetching data"]

def send_signals(signals):
    if signals:
        msg = "✅ Quotex AI Signals:\n\n" + "\n\n".join(signals)
    else:
        msg = "⚠️ No market with payout ≥ 75%."

    bot.send_message(chat_id=CHAT_ID, text=msg)

def main():
    while True:
        signals = get_payouts()
        send_signals(signals)
        time.sleep(60)  # wait 1 minute

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="🤖 Signal Bot is now running!")
    main()
