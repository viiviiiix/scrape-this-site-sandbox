import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def main():
    url = "https://www.scrapethissite.com/pages/advanced/?gotcha=headers"
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    html = get_html(url, headers=headers)
    print(get_msg(html))


def get_html(url, headers):
    print(f"Scraping: {url}")
    r = requests.get(url, headers=headers)
    html = BeautifulSoup(r.text, "html.parser")
    return html

def get_msg(html):
    msg = html.find("div", class_="row").find("div").text.strip()
    return msg

if __name__ == "__main__":
    main()
