import time
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ====== তোমার Telegram Bot Token আর Chat ID বসাও নিচে ======
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '5846045357'

bot = telegram.Bot(token=BOT_TOKEN)

# Chrome Headless Setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")

# chromedriver.exe ফাইল যদি একই ফোল্ডারে থাকে, তাহলে path দিতে হবে না
driver = webdriver.Chrome(options=chrome_options)

# Target URL (তোমার দেয়া site)
URL = 'https://market-qx.pro/en'

# Function to check payout and send signal
def check_payout_and_send_signal():
    driver.get(URL)
    time.sleep(5)  # লোডিং এর জন্য অপেক্ষা

    try:
        payout_elements = driver.find_elements(By.XPATH, '//div[contains(text(), "%") and contains(@class, "percent")]')
        for payout in payout_elements:
            payout_text = payout.text.replace("%", "").strip()
            if payout_text.isdigit() and int(payout_text) >= 75:
                message = f"✅ HIGH PAYOUT DETECTED: {payout_text}%\n📈 1-Minute Market (Real or OTC)"
                bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"Signal Sent: {message}")
                break
            else:
                print(f"Payout found but below threshold: {payout_text}%")
    except Exception as e:
        print("❌ Error fetching payout:", e)

# Main Loop with 1 minute cooldown
def main():
    print("🔁 Bot started... Checking every 60 seconds.")
    while True:
        check_payout_and_send_signal()
        time.sleep(60)

if __name__ == "__main__":
    main()
