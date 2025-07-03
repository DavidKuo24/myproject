import requests
import bs4

url="https://www.mlb.com/news"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}


response = requests.get(url, headers=headers)


root=bs4.BeautifulSoup(response.text, "html.parser")
titles = root.find_all("span", class_="article-navigation__item__meta-headline")
if titles:
        print("\nNews Titles:")
        for title in titles:
            print(title.get_text().strip())  
else:
     print ("no titles found")
