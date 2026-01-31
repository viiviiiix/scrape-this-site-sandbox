import asyncio
import httpx
from dataclasses import dataclass
import csv
import time

@dataclass
class Movie:
    title: str
    year: str
    awards: str
    nominations: str
    best_picture: str

async def main():
    urls = [f"https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year={i}" for i in range(2010, 2016)]
    semaphore = asyncio.Semaphore(6)
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [asyncio.create_task(get_json(url, client, semaphore)) for url in urls]
        with open("movies.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Year", "Awards", "Nominations", "Best Picture"])
            for task in asyncio.as_completed(tasks):
                js = await task
                for data in get_data(js):
                    writer.writerow([data.title, data.year, data.awards, data.nominations, data.best_picture])
    print("Scraping complete!\n")

async def get_json(url, client, semaphore):
    async with semaphore:
        print(f"Scraping: {url}")
        s = await client.get(url)
        return s.json()

def get_data(js):
    for elem in js:
        title = elem["title"].strip()
        year = elem["year"]
        awards = elem["awards"]
        nominations = elem["nominations"]
        best_picture = elem.get("best_picture", False)
        yield Movie(title, year, awards, nominations, best_picture)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Scraping took {end - start} seconds.")
