import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import csv
import time

@dataclass
class Country:
    country: str
    capital: str
    population: str
    area: str

def main():
    url = "https://www.scrapethissite.com/pages/simple/"
    html = get_html(url)
    with open("country.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Country", "Capital", "Population", "Area (sq km)"])
        for data in get_data(html):
            writer.writerow([data.country, data.capital, data.population, data.area])
    print("Scraping complete!\n")

def get_html(url):
    print(f"Scraping: {url}")
    r = requests.get(url)
    html = BeautifulSoup(r.text, "html.parser")
    return html

def get_data(html):
    for elem in html.find_all("div", class_="country"):
        country = elem.find("h3", class_="country-name").text.strip()
        capital = elem.find("div", class_="country-info").find("span", class_="country-capital").text
        population = elem.find("div", class_="country-info").find("span", class_="country-population").text
        area = elem.find("div", class_="country-info").find("span", class_="country-area").text
        yield Country(country, capital, population, area)

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Scraping took {end - start} seconds.")
