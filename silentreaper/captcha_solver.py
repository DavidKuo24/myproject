import requests
import pytesseract
from PIL import Image
import os
import random
import string

def download_captcha(url, save_path="captcha.png"):
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://tixcraft.com"}
    response = requests.get(url, headers=headers)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    return save_path

def solve_with_ocr(image_path):
    img = Image.open(image_path).convert("L")
    text = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return text.strip()

def is_valid_code(code):
    return code.isalpha() and 4 <= len(code) <= 6

def solve_captcha_full(url):
    image_path = download_captcha(url)
    code = solve_with_ocr(image_path)
    os.remove(image_path)
    print(f"🧠 OCR 辨識結果：{code}")

    if not is_valid_code(code):
        code = input("✍️ 請手動輸入驗證碼：").strip()
    return code
