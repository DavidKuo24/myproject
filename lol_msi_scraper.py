import requests
from bs4 import BeautifulSoup
import sys

def get_msi_player_stats():
    """
    從 Leaguepedia 爬取並顯示 MSI 選手的 K/D/A 數據。
    """
    # 使用 Session 物件來保持連線狀態並處理 cookies
    session = requests.Session()
    
    # 設定更完整的 headers 來模擬真實瀏覽器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1', # Do Not Track
    }
    session.headers.update(headers)

    # **注意**: 這是 2025 MSI 頁面的預測網址，屆時可能需要更新。
    # 我們先連到主賽事頁面，然後從中找到選手數據頁面的連結。
    base_url = "https://lol.fandom.com"
    main_event_url = f"{base_url}/wiki/2024_Mid-Season_Invitational"
    
    print(f"正在從主賽事頁面 {main_event_url} 尋找選手數據連結...")

    try:
        # 關閉 SSL 驗證 (verify=False)，並抑制因此產生的警告。
        # 這在某些公司或受限網路中是必要的，但會降低安全性。
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = session.get(main_event_url, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"錯誤：無法取得主賽事頁面內容。請檢查網路連線或網址是否正確。")
        print(f"詳細錯誤訊息: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 尋找指向 "Player Statistics" 的連結
    # 連結的 href 通常是 /wiki/YYYY_Mid-Season_Invitational/Player_Stats
    player_stats_link = soup.find('a', href="/wiki/2024_Mid-Season_Invitational/Player_Stats")
    
    if not player_stats_link:
        print("錯誤：在主賽事頁面上找不到預期的 'Player Stats' 連結。")
        print("--- 以下是頁面上找到的所有連結 (<a> 標籤)，請從中尋找正確的連結：---")
        all_links = soup.find_all('a', href=True) # 只找有 href 屬性的 a 標籤
        for link in all_links:
            # 印出連結文字和它的 href 屬性
            link_text = link.text.strip()
            link_href = link['href']
            print(f"文字: '{link_text}', 連結: '{link_href}'")
        print("---------------------------------------------------------------------")
        print("請根據上面的列表，找到包含選手數據的正確連結，並更新程式碼中的 `player_stats_link` 搜尋條件。")
        sys.exit(1)
        
    # 組合完整的選手數據頁面網址
    player_stats_url = base_url + player_stats_link['href']
    print(f"找到選手數據頁面: {player_stats_url}")
    print("正在抓取選手數據...")

    try:
        response = session.get(player_stats_url, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"錯誤：無法取得選手數據頁面內容。")
        print(f"詳細錯誤訊息: {e}")
        sys.exit(1)
        
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到 "Player Statistics" 標題，然後找到緊鄰的表格
    stats_header = soup.find('span', id='Player_Statistics')
    if not stats_header:
        print("錯誤：在頁面上找不到 'Player_Statistics' 的區塊。")
        print("可能是網頁結構已變更，或是今年的賽事頁面未使用此標題。")
        sys.exit(1)

    stats_table = stats_header.find_next('table', class_='wikitable')
    if not stats_table:
        print("錯誤：在 'Player_Statistics' 區塊後找不到選手數據表格。")
        print("可能是網頁結構已變更。")
        sys.exit(1)

    # --- 動態尋找欄位索引 ---
    header_row = stats_table.find('tr')
    headers = [th.text.strip() for th in header_row.find_all('th')]
    
    try:
        # 建立一個字典來儲存我們需要的欄位名稱和它們的索引
        col_indices = {
            'Player': headers.index('Player'),
            'K': headers.index('K'),
            'D': headers.index('D'),
            'A': headers.index('A')
        }
    except ValueError as e:
        print(f"錯誤：無法在表格標頭中找到必要的欄位: {e}")
        print(f"偵測到的標頭為: {headers}")
        print("請確認網頁表格是否包含 'Player', 'K', 'D', 'A' 欄位。")
        sys.exit(1)

    # --- 提取數據 ---
    player_stats = []
    # 忽略標題行，從資料行開始遍歷
    for row in stats_table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if not cells:
            continue

        try:
            player_name = cells[col_indices['Player']].text.strip()
            kills = cells[col_indices['K']].text.strip()
            deaths = cells[col_indices['D']].text.strip()
            assists = cells[col_indices['A']].text.strip()
            player_stats.append((player_name, kills, deaths, assists))
        except IndexError:
            # 如果某一行資料不完整，跳過此行
            continue

    # --- 顯示結果 ---
    if not player_stats:
        print("成功連線並找到表格，但未能抓取到任何選手數據。")
        return

    print("\n--- 2025 MSI 選手 KDA 統計 (資料來源: Leaguepedia) ---\n")
    # 格式化輸出，讓欄位對齊
    print(f"{'選手 (Player)':<20} {'擊殺 (K)':<10} {'死亡 (D)':<10} {'助攻 (A)':<10}")
    print("-" * 55)
    for stat in player_stats:
        print(f"{stat[0]:<20} {stat[1]:<10} {stat[2]:<10} {stat[3]:<10}")

if __name__ == "__main__":
    get_msi_player_stats()
