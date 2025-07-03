import requests
from bs4 import BeautifulSoup

# 設定 MLB 新聞版首頁的 URL
url = "https://www.mlb.com/news"

# 設定 headers，以避免被網站認為是機器人
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

# 發送 GET 請求
response = requests.get(url, headers=headers)

# 檢查請求是否成功
if response.status_code == 200:
    # 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")


    titles = soup.find_all("span", class_="article-navigation__item__meta-headline")

    # 顯示抓取到的文章標題
    if titles:
        print("\nNews Titles:")
        for title in titles:
            print(title.get_text().strip())  # 印出標題
    else:
        print("No titles found.")
else:
    print("Failed to retrieve the page.")
