import requests
from bs4 import BeautifulSoup

def scrape(url):
    if not url:
        return ""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return f"[Error scraping URL: {e}]"
