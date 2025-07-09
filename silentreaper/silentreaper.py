import time
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

# === 設定區 ===
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # 修改為你的 Tesseract 安裝路徑
ACTIVITY_URL = "https://tixcraft.com/activity/detail/25_kai"

# === 啟動瀏覽器 ===
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(ACTIVITY_URL)

# === 點擊『立即購票』進入票種頁 ===
try:
    print("🔍 搜尋『立即購票』連結...")
    buy_now_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/activity/game/25_kai')]"))
    )
    buy_now_link.click()
    print("✅ 成功點擊『立即購票』")
except Exception as e:
    print("❌ 找不到『立即購票』：", e)
    driver.quit()
    exit()

# === 等待頁面載入並點擊 'Find Tickets' ===
try:
    print("🔍 搜尋 'Find Tickets' 按鈕...")
    find_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    ticket_url = find_button.get_attribute("data-href")
    print("✅ 導向票區頁面：", ticket_url)
    driver.get(ticket_url)
except Exception as e:
    print("❌ 找不到 'Find Tickets'：", e)
    driver.quit()
    exit()

# === 點擊第一個可見票區按鈕 ===
try:
    print("⌛ 等待可點選票區...")
    zone_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[style*='opacity: 1']"))
    )
    zone_button.click()
    print("✅ 已點選票區")
except Exception as e:
    print("❌ 沒有可點選的票區：", e)
    driver.quit()
    exit()

# === 處理驗證碼 ===
def solve_captcha(img_url):
    print("📁 下載驗證碼圖片...")
    captcha_img_path = "captcha.png"
    headers = {"Referer": driver.current_url, "User-Agent": "Mozilla/5.0"}
    r = requests.get(img_url, headers=headers)
    with open(captcha_img_path, 'wb') as f:
        f.write(r.content)

    print("✅ 辨識驗證碼...")
    img = Image.open(captcha_img_path).convert("L")
    text = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    os.remove(captcha_img_path)
    return text.strip()

try:
    print("⌛ 等待驗證碼出現...")
    img_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "TicketForm_verifyCode-image"))
    )
    captcha_src = img_element.get_attribute("src")
    full_captcha_url = "https://tixcraft.com" + captcha_src
    code = solve_captcha(full_captcha_url)

    # 勾選同意條款
    driver.find_element(By.ID, "TicketForm_agree").click()

    # 輸入驗證碼
    input_box = driver.find_element(By.ID, "TicketForm_verifyCode")
    input_box.send_keys(code)

    print(f"✅ 已輸入驗證碼：{code}")

    # 提交表單
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    print("✅ 嘗試送出表單...")

except Exception as e:
    print("❌ 驗證碼流程錯誤：", e)
    driver.quit()
    exit()

# === 結尾 ===
print("✨ SilentReaper v1.2.1 任務結束 ☠️")
