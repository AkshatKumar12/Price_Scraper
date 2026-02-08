from scrapers.site1 import scrape_site1
from scrapers.site2 import scrape_site2

if __name__ == "__main__":
    query = ""

    print("Testing booksToScrape...")
    ebay_results = scrape_site1(query)
    print(f"booksToScrape found: {len(ebay_results)} items")
    print(ebay_results[:3])

    print("\nTesting WebScrapper.io...")
    newegg_results = scrape_site2(query)
    print(f"WebScrapper found: {len(newegg_results)} items")
    print(newegg_results[:3])

