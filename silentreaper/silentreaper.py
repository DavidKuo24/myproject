import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from captcha_solver import solve_captcha

TIX_URL = "https://tixcraft.com/activity/detail/25_kai"

def main():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)
    driver.get(TIX_URL)

    wait = WebDriverWait(driver, 10)

    # 點擊『立即購票』
    try:
        buy_now_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "立即購票")))
        buy_now_btn.click()
        print("✅ 點擊立即購票成功")
    except Exception as e:
        print("❌ 點擊『立即購票』失敗：", e)
        return

    # 等待區域出現，然後隨機選可點的票區
    try:
        time.sleep(2)
        area_links = driver.find_elements(By.CSS_SELECTOR, 'a[style*="opacity: 1"]')
        if area_links:
            random.choice(area_links).click()
            print("✅ 隨機選擇票區成功")
        else:
            print("❌ 沒有可點選的票區")
            return
    except Exception as e:
        print("❌ 點選票區失敗：", e)
        return

    # 等待驗證碼與條款 checkbox 出現
    try:
        time.sleep(2)
        checkbox = driver.find_element(By.ID, "TicketForm_agree")
        checkbox.click()
        print("✅ 勾選條款成功")

        captcha_code = solve_captcha(driver)
        print("🧠 OCR 辨識結果：", captcha_code)

        code_input = driver.find_element(By.ID, "TicketForm_verifyCode")
        code_input.clear()
        code_input.send_keys(captcha_code)

        # 送出表單
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        print("✅ 表單已送出")
    except Exception as e:
        print("❌ 驗證碼或送出表單錯誤：", e)

    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
