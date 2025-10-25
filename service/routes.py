from flask import Blueprint, abort, jsonify, request

from app import db
from app.models import Product
from app.schema import product_schema, products_schema

bp = Blueprint("service_api", __name__)


@bp.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        abort(404, description="Product not found")
    return jsonify(product_schema.dump(product)), 200


@bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        abort(404, description="Product not found")

    json_data = request.get_json(silent=True) or {}
    try:
        data = product_schema.load(json_data, partial=True)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    for field, value in data.items():
        setattr(product, field, value)
    db.session.commit()
    return jsonify(product_schema.dump(product)), 200


@bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int):
    product = Product.query.get(product_id)
    if not product:
        abort(404, description="Product not found")
    db.session.delete(product)
    db.session.commit()
    return "", 204


@bp.route("/products", methods=["GET"])
def list_products():
    category = request.args.get("category")
    available = request.args.get("available")
    name = request.args.get("name")

    query = Product.query

    if category:
        query = query.filter(Product.category == category)

    if available is not None:
        aval = available.lower()
        if aval in ("true", "1", "yes"):
            query = query.filter(Product.available.is_(True))
        elif aval in ("false", "0", "no"):
            query = query.filter(Product.available.is_(False))
        else:
            return jsonify({"error": "available must be true/false"}), 400

    if name:
        like = f"%{name}%"
        query = query.filter(Product.name.ilike(like))

    products = query.order_by(Product.id.asc()).all()
    return jsonify(products_schema.dump(products)), 200
