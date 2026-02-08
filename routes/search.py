from flask import Blueprint, request, jsonify
from scrapers.site1 import scrape_site1
from scrapers.site2 import scrape_site2
from utils.normalize import normalize_price, normalize_title
from utils.dedup import deduplicate
from utils.cache import get_cache, set_cache
from utils.rate_limit import check_rate_limit
from concurrent.futures import ThreadPoolExecutor
from database import SessionLocal
from models import Product
from datetime import datetime


search_bp = Blueprint("search", __name__)

@search_bp.route("/search")
def search():
    query = request.args.get("q")

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    sort_by = request.args.get("sort", "price")
    order = request.args.get("order", "asc")

    ip = request.remote_addr
    if not check_rate_limit(ip):
        return jsonify({"error": "Rate limit exceeded"}), 429

    cache_key = f"{query}_{sort_by}_{order}_{page}_{per_page}"
    cached = get_cache(cache_key)

    if cached:
        return jsonify(cached)

    # Concurrent scraping
    with ThreadPoolExecutor(max_workers=5) as executor:
        future1 = executor.submit(scrape_site1, query)
        future2 = executor.submit(scrape_site2, query)

        results1 = future1.result()
        results2 = future2.result()

    products = results1 + results2

    # Normalize
    for p in products:
        p["price"] = normalize_price(str(p["price"]))
        p["normalized_name"] = normalize_title(p["name"])

    # Deduplicate
    products = deduplicate(products)
    db = SessionLocal()

    try:
        for p in products:
            existing = db.query(Product).filter_by(url=p["url"]).first()

            if existing:
                existing.price = p["price"]
                existing.rating = p["rating"]
                existing.last_updated = datetime.utcnow()
            else:
                new_product = Product(
                    name=p["name"],
                    normalized_name=p["normalized_name"],
                    price=p["price"],
                    rating=p["rating"],
                    source=p["source"],
                    url=p["url"],
                )
                db.add(new_product)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


    # Sorting
    reverse = True if order == "desc" else False
    if sort_by in ["price", "rating"]:
        products = sorted(products, key=lambda x: x.get(sort_by, 0), reverse=reverse)

    # Pagination
    total = len(products)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = products[start:end]

    response = {
        "page": page,
        "per_page": per_page,
        "total": total,
        "has_next": end < total,
        "results": paginated
    }

    set_cache(cache_key, response)

    return jsonify(response)
