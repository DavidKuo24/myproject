import time
import pytesseract
import requests
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By

# Tesseract 安裝路徑（請依你本機安裝位置調整）
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\David.Kuo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def solve_captcha(driver):
    # 找到驗證碼圖片並點一下讓它刷新
    img_element = driver.find_element(By.ID, "TicketForm_verifyCode-image")
    img_element.click()
    time.sleep(0.8)  # 等一下刷新完

    # 抓圖片 src，補上網域
    src = img_element.get_attribute("src")
    if src.startswith("/"):
        src = "https://tixcraft.com" + src

    # 下載圖片
    response = requests.get(src, headers={
        "User-Agent": "Mozilla/5.0"
    })

    # 用 PIL 開啟圖片
    img = Image.open(BytesIO(response.content))

    # OCR 辨識
    text = pytesseract.image_to_string(img).strip()
    return text
