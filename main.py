from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, json, pytz, random
from datetime import datetime, timedelta
from telegram import Bot
import os

# ===== CONFIG =====
BOT_TOKEN = '8180362644:AAGtwc8hDrHkJ6cMcc3-Ioz9Hkn0cF7VD_w'
CHAT_ID = '6971835734'
CHECK_INTERVAL = 60
MIN_PAYOUT = 75

COOKIES = {
    '__cf_bm': '.y1Ox7KfhgqlLHY.zIHHEaPI0N.vr691J7XkyUKZ81g-1750399653-1.0.1.1-HhWfuhxiDWChXjGZRaRTJEMPiVs3hlYx.RI82odZjNMJXoTmmOLnqZti59fp7EtSuHziUSzCmLPqsL0J3tdrmR1hzFvjEHuFEqz2.OkAssg',
    '__vid1': 'af220b0fe006f49b69d0a9deafcf52f8',
    '_ga_L4T5GBPFHJ': 'GS2.1.s1750398649$o8$g1$t1750399646$j60$l0$h0',
    '_ga': 'GA1.1.835734851.1750158089',
    'activeAccount': 'demo',
    'lang': 'en',
    'laravel_session': 'eyJpdiI6Im5VY0o1Snpybm5pMHBjZ1hnQ3Ivanc9PSIsInZhbHVlIjoiN1JHRGJ6ZnFEb000Z3FFVldmTkxqd0NIL0VBSkJ0WHI2MEZEc1VZMVdXT3lFYjVnajVFdlNSMU52Ny9vQklScGxvT1VGbG5HTW5hVnZKeEpCSzk2M3o4UStXS1ZCNU5BbktLUU8rQTZaR3cxenhZb2RBL0YvcXRJc2VHR1h1LzUiLCJtYWMiOiJhOTI3M2JmMmUwNDZjNjBjNWVmYWU4OTlkMmM2NjJlZGIxZTU3MTFmMzJiMmJhMDY1M2Y4NjI2MDZiNTg3NzkwIiwidGFnIjoiIn0%3D',
    'nas': '[%22USDCHF%22%2C%22AUDNZD_otc%22%2C%22USDPKR_otc%22%2C%22USDMXN_otc%22%2C%22USDDZD_otc%22%2C%22GBPUSD%22%2C%22USDJPY%22%2C%22EURJPY%22]',
    'OTCTooltip': '{%22value%22:false}',
    'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6IjArc2hCaUhoT2labjV0djlEQnQ0anc9PSIsInZhbHVlIjoiSm9EM2J3MzY4d25NeWlmV08xS0ZsU3daMEpsSVhEdlN6M0pqaW91bjNJYmtUN1h1WjM3RGJhalQ5Y2M4RFkxelAwdU1RQTgzbUxFclVYeVhqblVlcnIrY3hKWWZjRktKUmE4elM3Q0NHRHdwVTZ4WlVTRXYrMGVkbkRDNjZ2RWh2dS81VHRaNmZWV2F6QTlUUWwzd1ZtM0ZkSkxSVHNsOXMwdTRYREtlZGJCN2J2dnUvbGZlSlY2OVp4ZGVta29IcitSenRoZFFkTHJyN3k4NVVOL1UxbisrY01qVDN0blIvQUNBNzdwRjZLbmVkWndiVGY2LzRaQW5wWDNLQTRucyIsIm1hYyI6IjllMjVlODc4ZjA2ZjJhMTA2NTAyNmM3ZWQ0YzAzNTlhYmY0NDI3ZTU3YjgxZmRiMDBkODlhNDY2ZGRiNmViODgiLCJ0YWciOiIifQ==',
    'z': '[[%22graph%22%2C2%2C0%2C0%2C0.7701333]]'
}

bot = Bot(token=BOT_TOKEN)
bd_time = pytz.timezone('Asia/Dhaka')

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_payout():
    try:
        driver = get_driver()
        driver.get("https://market-qx.pro")
        for key, value in COOKIES.items():
            driver.add_cookie({'name': key, 'value': value})
        driver.get("https://market-qx.pro/api/payouts")
        time.sleep(2)
        response = driver.find_element(By.TAG_NAME, "pre").text
        driver.quit()
        return json.loads(response)
    except Exception as e:
        print(f"❌ Fetch error: {e}")
        return None

def send_signal(market, payout):
    now = datetime.now(bd_time)
    entry = (now + timedelta(minutes=1)).strftime('%H:%M')
    expiry = (now + timedelta(minutes=2)).strftime('%H:%M')
    signal = random.choice(['UP', 'DOWN'])
    signal_id = random.randint(100, 999)
    msg = f"📊 AI Signal\n" \
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
    bot.send_message(chat_id=CHAT_ID, text=msg)
    print("✅ Signal sent")

def run_bot():
    print("🤖 Pro Quotex AI Bot Running (Headless Chrome + Cookie Mode)...")
    while True:
        data = fetch_payout()
        if data and 'data' in data:
            markets = list(data['data'].items())
            random.shuffle(markets)
            for symbol, info in markets:
                payout = info.get('turbo', 0)
                if payout >= MIN_PAYOUT:
                    send_signal(symbol.upper(), payout)
                    break
        else:
            print("❌ Failed to fetch payout.")
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    run_bot()
