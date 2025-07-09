import time
import pytesseract
from PIL import Image
import random
import json
import requests
import os
from datetime import datetime

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# === 設定 Tesseract OCR 路徑（需根據實際安裝位置調整） ===
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# === 載入設定檔 ===
with open("C:/Users/David.Kuo/python/silentreaper/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    ACTIVITIES = config["activities"]
    INTERVAL_RANGE = config["interval_range"]

# === 建立瀏覽器 ===
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options)

# === 驗證碼處理函式 ===
def solve_captcha(img_url):
    print("📥 下載驗證碼...")
    img_path = "captcha.png"
    headers = {"Referer": driver.current_url, "User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(img_url, headers=headers)
        with open(img_path, 'wb') as f:
            f.write(r.content)
        img = Image.open(img_path).convert("L")
        text = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        os.remove(img_path)
        return text.strip()
    except Exception as e:
        print(f"❌ 驗證碼處理失敗：{e}")
        return ""

# === 主流程 ===
for url in ACTIVITIES:
    print(f"\n[{datetime.now()}] 🎯 前往活動頁：{url}")
    driver.get(url)

    # 處理 Cookie 彈窗
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'接受所有 Cookie')]"))
        ).click()
        print("🍪 已接受 Cookie")
    except:
        print("🍪 沒有 Cookie 彈窗")

    # 點『立即購票』
    try:
        link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='buy']/a"))
        )
        href = link.get_attribute("href")
        print(f"✅ 找到購票連結：{href}")
        driver.get(href)
    except Exception as e:
        print(f"❌ 無法取得購票連結：{e}")
        continue

    # 點『Find Tickets』
    try:
        print("🔍 尋找票區按鈕...")
        find_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )
        ticket_url = find_button.get_attribute("data-href")
        print(f"✅ 票區頁面：{ticket_url}")
        driver.get(ticket_url)
    except Exception as e:
        print(f"❌ 找不到票區：{e}")
        continue

    # 點第一個票區
    try:
        print("🧭 等待可點選票區...")
        zone_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[style*='opacity: 1']"))
        )
        zone_button.click()
        print("✅ 點選票區")
    except Exception as e:
        print(f"❌ 沒有票區可選：{e}")
        continue

    # 選擇票數（選第一個 option）
    try:
        print("🎟️ 選擇票數...")
        qty_select = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[name*='TicketForm']"))
        )
        Select(qty_select).select_by_value("1")
        print("✅ 已選擇票數 1 張")
    except Exception as e:
        print(f"❌ 選擇票數失敗：{e}")
        continue

    # 驗證碼與送出
    try:
        img_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "TicketForm_verifyCode-image"))
        )
        captcha_src = img_element.get_attribute("src")
        code = solve_captcha("https://tixcraft.com" + captcha_src)

        driver.find_element(By.ID, "TicketForm_agree").click()
        driver.find_element(By.ID, "TicketForm_verifyCode").send_keys(code)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print(f"✅ 嘗試送出驗證碼：{code}")

    except Exception as e:
        print(f"❌ 驗證碼流程錯誤：{e}")

    delay = random.randint(INTERVAL_RANGE[0], INTERVAL_RANGE[1])
    print(f"⏳ 等待 {delay} 秒後繼續...")
    time.sleep(delay)

print("\n🏁 SilentReaper v1.4 全部完成 ☠️")
driver.quit()
