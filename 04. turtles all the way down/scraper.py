import asyncio
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import csv
import time

@dataclass
class Turtle:
    name: str
    description: str

async def main():
    url = "https://www.scrapethissite.com/pages/frames/?frame=i"
    semaphore = asyncio.Semaphore(10)
    async with httpx.AsyncClient(timeout=10) as client:
        html = await get_html(url, client, semaphore)
        tasks = [asyncio.create_task(get_html(link, client, semaphore)) for link in get_urls(html)]
        with open("turtles.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Description"])
            for task in asyncio.as_completed(tasks):
                html = await task
                for data in get_data(html):
                    writer.writerow([data.name, data.description])
    print("Scraping complete!\n")

async def get_html(url, client, semaphore):
    async with semaphore:
        print(f"Scraping: {url}")
        r = await client.get(url)
        html = HTMLParser(r.text)
        return html

def get_urls(html):
    family_card = html.css("div.turtle-family-card")
    for elem in family_card:
        yield "https://www.scrapethissite.com" + elem.css_first("a.btn-xs").attributes.get("href")

def get_data(html):
    name = html.css_first("h3.family-name").text().strip()
    desc = html.css_first("p.lead").text().strip()
    yield Turtle(name, desc)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Scraping took {end - start} seconds.")
