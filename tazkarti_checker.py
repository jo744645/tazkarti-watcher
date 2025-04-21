import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# إعدادات تليجرام
BOT_TOKEN = '7204967716:AAGJZ5lGRqcn0DNR2zJelfRqCFpZOvGeN8U'
CHAT_ID = '1103230055'

# كلمات البحث
keywords = ["الأهلي", "Al Ahly", "Ahly", "AL-AHLY", "Al Ahly FC"]

# إعداد Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# رابط الموقع
url = 'https://www.tazkarti.com/#/matches'

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print("❌ فشل إرسال رسالة تليجرام:", e)

def check_tickets():
    print("⏳ جاري التحقق من تذاكر الأهلي...")
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(15)
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        if any(word.lower() in soup.text.lower() for word in keywords):
            print("✅ التذاكر متاحة!")
            send_telegram_message("🎟️ فيه تذاكر متاحة لـ Al Ahly FC!\nاحجز من هنا: https://www.tazkarti.com/#/matches")
        else:
            print("❌ مفيش تذاكر دلوقتي.")
    except Exception as e:
        print("🚨 حصل خطأ:", e)

# حلقة التكرار المنتظم
while True:
    start = time.time()
    check_tickets()
    elapsed = time.time() - start
    wait_time = max(0, 60 - elapsed)  # نضمن يكمل الدقيقة
    time.sleep(wait_time)
