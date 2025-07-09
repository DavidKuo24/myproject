import requests
import time
from datetime import datetime
import random

# === 設定區 ===
TICKET_URL = "https://tixcraft.com/"  # 目標票務網站的網址（請替換成實際網址）
REQUEST_INTERVAL = 0.5  # 每次發送請求的間隔秒數
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}  # 模擬瀏覽器的 headers，避免被當作機器人擋掉

# === 檢查是否有票的函式 ===
def is_ticket_available(html_text):
    """
    根據網頁內容判斷是否有票
    可以依照實際網站的文字做判斷邏輯調整
    """
    # 範例：如果沒有看到 "Sold Out" 就代表可能還有票
    return "Sold Out" not in html_text and "sold out" not in html_text

# === 嘗試購票的函式 ===
def attempt_purchase():
    """
    發送購票請求
    這裡的欄位名稱要根據實際網站的表單欄位做調整
    """
    purchase_data = {
        "ticket_id": "123456",   # 假設的欄位，可自行替換
        "quantity": 1            # 購買數量
    }
    try:
        response = requests.post(TICKET_URL, headers=HEADERS, data=purchase_data)
        if response.status_code == 200:
            print(f"[{datetime.now()}] 成功送出購票請求！")
        else:
            print(f"[{datetime.now()}] 購票請求失敗：HTTP 狀態碼 {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] 發送購票請求時發生錯誤：{e}")

# === 機器人主邏輯 ===
def ticket_bot():
    print("🎟 搶票機器人啟動中...")
    while True:
        try:
            response = requests.get(TICKET_URL, headers=HEADERS)
            if response.status_code == 200:
                if is_ticket_available(response.text):
                    print(f"[{datetime.now()}] 偵測到票券！嘗試購票中...")
                    attempt_purchase()
                    break  # 購票完後就停止程式
                else:
                    print(f"[{datetime.now()}] 尚未開放購票，繼續監控中...")
            else:
                print(f"[{datetime.now()}] 網頁載入失敗：HTTP 狀態碼 {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now()}] 請求發生錯誤：{e}")

        delay = random.uniform(0.4, 1.2)  # 模擬人類隨機等待秒數
        print(f"[{datetime.now()}] 模擬人類等待中... 暫停 {round(delay, 2)} 秒")
        time.sleep(delay

if __name__ == "__main__":
    ticket_bot()
