import requests
from bs4 import BeautifulSoup

url = "https://www.mlb.com/news"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}


response = requests.get(url, headers=headers)


if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, "html.parser")


    titles = soup.find_all("span", class_="article-navigation__item__meta-headline")

    
    if titles:
        print("\nNews Titles:")
        for title in titles:
            print(title.get_text().strip()) 
    else:
        print("No titles found.")
else:
    print("Failed to retrieve the page.")
