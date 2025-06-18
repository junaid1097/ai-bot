from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import telegram
import time
import random

# ========================
# তোমার টেলিগ্রাম বট টোকেন আর চ্যাট আইডি এখানে সেট করা হলো
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6971835734'
# ========================

bot = telegram.Bot(token=BOT_TOKEN)

chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"  # Replit বা লিনাক্সে চলার জন্য
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

def get_payout():
    driver.get("https://market-qx.pro/en")
    time.sleep(5)
    # ডেমো হিসেবে র‍্যান্ডম পেআউট দিচ্ছি, তোমার ওয়েবসাইট থেকে scrape করো এখানে
    payout = random.choice([70, 74, 75, 80, 85])
    return payout

def send_signal(signal):
    message = f"🔥 Quotex Signal: {signal} 🔥"
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    cooldown = 60  # 60 সেকেন্ড পর পর সিগনাল যাবে
    last_signal_time = 0

    while True:
        payout = get_payout()
        print(f"Current payout: {payout}%")

        now = time.time()

        if payout >= 75 and now - last_signal_time > cooldown:
            send_signal("UP")
            last_signal_time = now
            print("Signal sent!")
        else:
            print("No signal sent.")

        time.sleep(10)

if __name__ == "__main__":
    try:
        print("Bot started...")
        main()
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    finally:
        driver.quit()
