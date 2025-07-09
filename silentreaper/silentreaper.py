import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from captcha_solver import solve_captcha_full

# === 讀取設定 ===
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

ACTIVITIES = config["activities"]
INTERVAL_MIN, INTERVAL_MAX = config["interval_range"]

# === 啟動瀏覽器 ===
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def random_wait():
    t = random.uniform(INTERVAL_MIN, INTERVAL_MAX)
    time.sleep(t)

def process_activity(activity_url):
    print(f"\n🚀 開始處理活動：{activity_url}")
    driver.get(activity_url)

    # 接受 Cookie 條款
    try:
        cookie_btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cookie-popup-accept-all"))
        )
        cookie_btn.click()
        print("🍪 已點選 Cookie")
    except:
        print("🍪 無 Cookie 彈窗")

    # 點『立即購票』
    try:
        print("➡️ 搜尋『立即購票』...")
        buy_now = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/activity/game/') and contains(., '立即購票')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", buy_now)
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable(buy_now)).click()
        print("✅ 進入票種頁面")
    except Exception as e:
        print("❌ 找不到『立即購票』：", e)
        return

    # 點『Find Tickets』
    try:
        find_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )
        ticket_url = find_btn.get_attribute("data-href")
        print("🎯 導向票區頁面：", ticket_url)
        driver.get(ticket_url)
    except Exception as e:
        print("❌ 找不到『Find Tickets』：", e)
        return

    # 點票區
    try:
        print("🧭 搜尋可選票區...")
        zone = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[style*='opacity: 1']"))
        )
        zone.click()
        print("✅ 成功點票區")
    except Exception as e:
        print("❌ 沒有可選票區：", e)
        return

    # 處理驗證碼 + 條款 + 送出
    try:
        img = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "TicketForm_verifyCode-image"))
        )
        src = img.get_attribute("src")
        full_url = "https://tixcraft.com" + src

        code = solve_captcha_full(full_url)
        driver.find_element(By.ID, "TicketForm_agree").click()
        driver.find_element(By.ID, "TicketForm_verifyCode").send_keys(code)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("✅ 已送出驗證碼與表單！")
    except Exception as e:
        print("❌ 表單送出錯誤：", e)

# === 主流程 ===
while True:
    for url in ACTIVITIES:
        process_activity(url)
        random_wait()
