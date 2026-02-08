# # e-bay

# import requests
# from bs4 import BeautifulSoup

# def scrape_site1(query):
#     headers = {"User-Agent": "Mozilla/5.0"}
#     url = f"https://www.ebay.com/sch/i.html?_nkw={query}"

#     r = requests.get(url, headers=headers, timeout=5)
#     soup = BeautifulSoup(r.text, "html.parser")
#     print(r.status_code)
#     print(r.text[:500])

#     products = []

#     for item in soup.select(".s-item"):
#         title = item.select_one(".s-item__title")
#         price = item.select_one(".s-item__price")
#         link = item.select_one(".s-item__link")

#         if not title or not price or not link:
#             continue

#         # Rating may not exist for all items
#         rating_tag = item.select_one(".x-star-rating span")
#         rating = rating_tag.text if rating_tag else "0"

#         products.append({
#             "name": title.text.strip(),
#             "price": price.text.strip(),
#             "rating": rating,
#             "url": link["href"],
#             "source": "ebay"
#         })

#     return products



import time
from utils.logger import logger
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/catalogue/page-1.html"

def scrape_site1(query):
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

    for item in soup.select(".product_pod"):
        title_tag = item.select_one("h3 a")
        price_tag = item.select_one(".price_color")
        rating_tag = item.select_one("p.star-rating")

        if not title_tag or not price_tag:
            continue

        title = title_tag["title"]
        price = price_tag.text.strip()

        # Convert rating word to number
        rating_class = rating_tag["class"][1] if rating_tag else "Zero"
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        rating = rating_map.get(rating_class, 0)

        products.append({
            "name": title,
            "price": price.replace("£", ""),
            "rating": rating,
            "url": "http://books.toscrape.com/catalogue/" + title_tag["href"],
            "source": "books"
        })

    if query:
        products = [
            p for p in products
            if query.lower() in p["name"].lower()
        ]
    return products
