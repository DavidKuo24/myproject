import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# 打開瀏覽器（使用 undetected_chromedriver 防偵測）
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.headless = False  # 測試時先打開瀏覽器畫面方便觀察

driver = uc.Chrome(options=options)

# 進入活動頁面
activity_url = "https://tixcraft.com/activity/detail/24_NewYearConcert"
print(f"[{datetime.now()}] 前往活動頁：{activity_url}")
driver.get(activity_url)

try:
    # 等待「立即訂購」按鈕出現，最多等10秒
    order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'立即訂購')]"))
    )
    print(f"[{datetime.now()}] 找到『立即訂購』按鈕，即將點擊...")
    order_button.click()

except Exception as e:
    print(f"[{datetime.now()}] ❌ 無法找到按鈕或點擊失敗：{e}")

# 暫停5秒觀察點擊後結果
import time
time.sleep(5)
driver.quit()
