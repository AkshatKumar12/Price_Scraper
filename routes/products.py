from flask import Blueprint, jsonify
from database import SessionLocal
from models import Product

product_bp = Blueprint("products", __name__)

@product_bp.route("/products/<int:product_id>")
def get_product(product_id):
    db = SessionLocal()
    try:
        product = db.query(Product).filter_by(id=product_id).first()

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({
            "id": product.id,
            "name": product.name,
            "normalized_name": product.normalized_name,
            "price": product.price,
            "rating": product.rating,
            "source": product.source,
            "url": product.url,
            "last_updated": product.last_updated.isoformat()
        })
    finally:
        db.close()
