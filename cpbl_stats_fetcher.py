import requests
from bs4 import BeautifulSoup
import sys

def get_cpbl_player_stats(player_name):
    """
    從中華職棒官網 (cpbl.com.tw) 爬取指定球員的生涯成績。
    """
    # CPBL 官網的球員搜尋頁面
    search_url = f"https://www.cpbl.com.tw/player/search"
    base_url = "https://www.cpbl.com.tw"

    # 使用 Session 物件來保持連線狀態，並設定更完整的 headers 模擬瀏覽器
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.cpbl.com.tw/", # 告訴伺服器我們是從官網首頁來的
    }
    session.headers.update(headers)

    print(f"正在搜尋球員：{player_name}...")

    try:
        # --- 模擬真實使用者瀏覽的兩步驟流程 ---

        # 第一步：先用 GET 請求訪問搜尋頁面，以取得必要的 session cookies
        print("正在訪問搜尋頁面以建立連線...")
        initial_response = session.get(search_url)
        initial_response.raise_for_status() # 確保第一步請求成功
        print("連線建立成功，正在提交搜尋...")

        # 第二步：在同一個 session 中，使用 POST 請求提交搜尋表單
        search_payload = {
            'name': player_name,
            'order': '1'
        }
        response = session.post(search_url, data=search_payload)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尋找搜尋結果中的球員連結 (根據經驗，class name 可能是 PlayerListBlock)
        player_link_element = soup.find('div', class_='PlayerListBlock')
        if not player_link_element or not player_link_element.find('a'):
            print(f"錯誤：找不到名為 '{player_name}' 的球員。請檢查姓名是否正確或網站結構已變更。")
            print("--- 以下為回傳的 HTML，以供除錯 ---")
            print(soup.prettify())
            sys.exit(1)
        
        player_page_url = base_url + player_link_element.find('a')['href']
        print(f"找到球員頁面：{player_page_url}")

        # 第二步：訪問球員個人頁面，抓取數據
        response = requests.get(player_page_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 判斷是打者還是投手 (以第一個數據表格的標題為準)
        record_title_element = soup.find('div', class_='RecordTitle')
        is_hitter = 'Hitter' in record_title_element.text

        # 找到生涯成績表格
        # 官網的結構是 RecordBox class 裡面有好幾個 table
        # 生涯成績通常是最後一個 table
        all_tables = soup.find_all('table', class_='RecordTable')
        if not all_tables:
            print("錯誤：在此頁面找不到任何成績表格。")
            sys.exit(1)

        career_table = all_tables[-1] # 生涯成績是最後一個表格

        # 提取表頭 (headers)
        header_row = career_table.find('thead').find('tr')
        headers = [th.text.strip() for th in header_row.find_all('th')]

        # 提取生涯總計數據 (通常是 tbody 的最後一列 tr)
        career_row = career_table.find('tbody').find_all('tr')[-1]
        stats = [td.text.strip() for td in career_row.find_all('td')]

        # --- 顯示結果 ---
        print(f"\n--- {player_name} 生涯總計成績 (資料來源: CPBL官網) ---")
        if is_hitter:
            print("成績類型：打者")
        else:
            print("成績類型：投手")
        print("-" * 50)

        # 將表頭和數據配對印出
        for header, stat in zip(headers, stats):
            print(f"{header:<10}: {stat}")
        
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"錯誤：網路連線或請求失敗。")
        print(f"詳細錯誤訊息: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 我們以「張志豪」作為目標
    get_cpbl_player_stats("張志豪")