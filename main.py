import time
import telegram
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ====== তোমার Bot Token & Chat ID বসাও নিচে ======
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '5846045357'

bot = telegram.Bot(token=BOT_TOKEN)

# Headless Chrome setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# Target URL
URL = 'https://market-qx.pro/en'

# Function to check and send signal
def check_payout_and_send_signal():
    driver.get(URL)
    time.sleep(5)

    try:
        market_blocks = driver.find_elements(By.CLASS_NAME, "item")

        for block in market_blocks:
            try:
                name = block.find_element(By.CLASS_NAME, "pair-name").text.strip()
                payout = block.find_element(By.CLASS_NAME, "percent").text.strip().replace("%", "")
                otc_badge = "OTC" if "otc" in block.get_attribute("class").lower() else "Real"

                if payout.isdigit() and int(payout) >= 75:
                    direction = random.choice(["⬆️ UP", "⬇️ DOWN"])
                    signal = f"""✅ Signal Generated

📊 Market: {name}
🕐 Timeframe: 1-Minute
🌐 Type: {otc_badge}
💰 Payout: {payout}%
📈 Direction: {direction}

⚡ Status: Qualified Signal (≥ 75%)"""
                    bot.send_message(chat_id=CHAT_ID, text=signal)
                    print(f"Signal Sent: {signal}")
                    break
                else:
                    print(f"Skipping {name} | Payout: {payout}%")
            except Exception as e:
                print("⚠️ Block Error:", e)

    except Exception as e:
        print("❌ Scraping Error:", e)

# Main loop
def main():
    print("🤖 Quotex AI Signal Bot is running...")
    while True:
        check_payout_and_send_signal()
        time.sleep(60)  # Cooldown 1 minute

if __name__ == "__main__":
    main()
