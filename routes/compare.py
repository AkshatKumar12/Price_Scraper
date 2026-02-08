from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Product

compare_bp = Blueprint("compare", __name__)

@compare_bp.route("/compare")
def compare():
    ids = request.args.get("ids")
    query = request.args.get("q")
    by = request.args.get("by", "price")
    k = int(request.args.get("k", 3))

    if by not in ["price", "rating"]:
        return jsonify({"error": "Invalid metric"}), 400

    db = SessionLocal()
    try:
        if ids:
            id_list = [int(i.strip()) for i in ids.split(",")]
            products = db.query(Product).filter(Product.id.in_(id_list)).all()
        elif query:
            products = db.query(Product).filter(
                Product.normalized_name.contains(query.lower())
            ).all()
            products = sorted(products, key=lambda x: getattr(x, by))[:k]
        else:
            return jsonify({"error": "Provide ids or query"}), 400
    finally:
        db.close()

    if not products:
        return jsonify({"error": "No products found"}), 404

    products_sorted = sorted(products, key=lambda x: getattr(x, by))
    best = products_sorted[0]

    return jsonify({
        "comparison_metric": by,
        "best_product": {
            "id": best.id,
            "name": best.name,
            "price": best.price,
            "rating": best.rating,
            "source": best.source
        },
        "compared_products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "rating": p.rating,
                "source": p.source
            }
            for p in products_sorted
        ]
    })
