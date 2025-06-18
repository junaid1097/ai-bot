import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot
import logging

# ====== CONFIGURATION ======

# তোমার Telegram Bot Token এবং Chat ID এখানে বসাও:
TELEGRAM_BOT_TOKEN = "8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w"
TELEGRAM_CHAT_ID = "5330568384"

# Minimum payout threshold for signal
MIN_PAYOUT = 75

# URL to check
MARKET_URL = "https://market-qx.pro/en"

# Cooldown between checks (seconds)
COOLDOWN = 60

# ====== SETUP TELEGRAM BOT ======
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ====== SETUP SELENIUM CHROME ======
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Adjust chromedriver path as per your setup
CHROMEDRIVER_PATH = "./chromedriver.exe"

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"Sent signal: {message}")
    except Exception as e:
        print(f"Telegram send error: {e}")

def fetch_payouts(driver):
    driver.get(MARKET_URL)
    time.sleep(7)  # Wait for page to load properly

    payouts = {}

    try:
        # Real Market Payout
        real_xpath = "//div[contains(text(),'Real')]/following-sibling::div[contains(@class,'payout')]"
        real_elem = driver.find_element(By.XPATH, real_xpath)
        real_payout_text = real_elem.text.strip().replace('%', '')
        real_payout = float(real_payout_text)
        payouts['Real'] = real_payout
    except Exception as e:
        print(f"Error fetching Real payout: {e}")

    try:
        # OTC Market Payout
        otc_xpath = "//div[contains(text(),'OTC')]/following-sibling::div[contains(@class,'payout')]"
        otc_elem = driver.find_element(By.XPATH, otc_xpath)
        otc_payout_text = otc_elem.text.strip().replace('%', '')
        otc_payout = float(otc_payout_text)
        payouts['OTC'] = otc_payout
    except Exception as e:
        print(f"Error fetching OTC payout: {e}")

    return payouts

def main():
    print("Bot started...")

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

    last_signal_time = 0

    while True:
        try:
            payouts = fetch_payouts(driver)
            print(f"Payouts fetched: {payouts}")

            # Check payouts and send signal if payout >= MIN_PAYOUT
            for market, payout in payouts.items():
                if payout >= MIN_PAYOUT:
                    now = time.time()
                    if now - last_signal_time > COOLDOWN:
                        message = f"🔥 {market} Market payout is {payout}% — Signal is ON! ✅"
                        send_telegram_message(message)
                        last_signal_time = now
                    else:
                        print("Cooldown active, skipping signal.")
                else:
                    print(f"{market} payout {payout}% below threshold.")

        except Exception as e:
            print(f"Error in main loop: {e}")

        time.sleep(COOLDOWN)

if __name__ == "__main__":
    main()

