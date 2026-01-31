import asyncio
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import csv
import time

@dataclass
class Hockey:
    team_name: str
    year: str
    wins: str
    losses: str
    ot_losses: str
    win_percent: str
    goals_for: str
    goals_against: str
    diff: str

async def main():
    urls = [f"https://www.scrapethissite.com/pages/forms/?page_num={i}&per_page=25" for i in range(1, 25)]
    semaphore = asyncio.Semaphore(10)
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [asyncio.create_task(get_response(url, client, semaphore)) for url in urls]
        with open("hockey.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Team", "Year", "Wins", "Losses", "OT Losses", "Win %", "Goals For", "Goals Against", "+/-"])
            for task in asyncio.as_completed(tasks):
                resp = await task
                for data in get_data(resp):
                    writer.writerow([data.team_name, data.year, data.wins, data.losses, data.ot_losses, data.win_percent, data.goals_for, data.goals_against, data.diff])
    print("Scraping complete!\n")

async def get_response(url, client, semaphore):
   async with semaphore:
       print(f"Scraping: {url}")
       resp = await client.get(url)
       return resp.text

def get_data(resp):
    html = HTMLParser(resp)
    team = html.css("tr.team")
    for elem in team:
        team_name = elem.css_first("td.name").text(strip=True)
        year = elem.css_first("td.year").text(strip=True)
        wins = elem.css_first("td.wins").text(strip=True)
        losses = elem.css_first("td.losses").text(strip=True)
        ot_losses = elem.css_first("td.ot-losses").text(strip=True)
        win_percent = elem.css_first("td.pct").text(strip=True)
        goals_for = elem.css_first("td.gf").text(strip=True)
        goals_against = elem.css_first("td.ga").text(strip=True)
        diff = elem.css_first("td.diff").text(strip=True)
        yield Hockey(team_name, year, wins, losses, ot_losses, win_percent, goals_for, goals_against, diff)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Scraping took {end - start} seconds.")
