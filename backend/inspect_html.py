import requests
from bs4 import BeautifulSoup

url = "https://www.formula1.com/en/racing/2025"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # pretty-print the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())

except requests.exceptions.RequestException as e:
    print(f"Failed to fetch {url}. Error: {e}")
