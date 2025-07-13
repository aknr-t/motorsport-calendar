import requests
from bs4 import BeautifulSoup

url = "https://www.formula1.com/en/racing/2025"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # すべてのリンクを抽出して表示
    for a_tag in soup.find_all('a', href=True):
        print(a_tag['href'])

except requests.exceptions.RequestException as e:
    print(f"Failed to fetch {url}. Error: {e}")
