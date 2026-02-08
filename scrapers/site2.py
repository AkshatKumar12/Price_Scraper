from utils.logger import logger
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

def scrape_site2(query):
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(3):
        try:
            start = time.time()
            r = requests.get(BASE_URL, headers=headers, timeout=5)
            duration = round(time.time() - start, 2)
            logger.info(f"[BOOKS] URL={BASE_URL} STATUS={r.status_code} TIME={duration}s")

            break
        except Exception:
            if attempt == 2:
                return []

    soup = BeautifulSoup(r.text, "html.parser")

    products = []

    for item in soup.select(".thumbnail"):
        title_tag = item.select_one(".title")
        price_tag = item.select_one(".price")
        rating_container = item.select_one(".ratings")

        if not title_tag or not price_tag:
            continue

        title = title_tag.text.strip()
        price = price_tag.text.replace("$", "").strip()

        # Count stars
        stars = rating_container.select(".glyphicon-star") if rating_container else []
        rating = len(stars)

        products.append({
            "name": title,
            "price": price,
            "rating": rating,
            "url": "https://webscraper.io" + title_tag["href"],
            "source": "webscraper"
        })

    if query:
        products = [
            p for p in products
            if query.lower() in p["name"].lower()
        ]

    return products
