import requests
import pytesseract
from PIL import Image
from io import BytesIO

# 請改成你自己的 tesseract.exe 路徑
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\David.Kuo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def solve_captcha(driver):
    try:
        # Step 1：找到圖片元素，取得 src
        captcha_img = driver.find_element("id", "TicketForm_verifyCode-image")
        captcha_src = captcha_img.get_attribute("src")

        # Step 2：拼接完整 URL（避免只拿到 /ticket/captcha?v=xxx）
        if captcha_src.startswith("/"):
            captcha_url = "https://tixcraft.com" + captcha_src
        else:
            captcha_url = captcha_src

        print("🔍 驗證碼圖片網址:", captcha_url)

        # Step 3：下載圖片
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(captcha_url, headers=headers)
        img = Image.open(BytesIO(response.content))

        # Step 4：進行 OCR 辨識
        text = pytesseract.image_to_string(img)
        cleaned = text.strip().replace(" ", "").replace("\n", "")
        print("🔎 辨識結果：", cleaned)

        return cleaned
    except Exception as e:
        print("⚠️ 辨識驗證碼失敗：", e)
        return ""
