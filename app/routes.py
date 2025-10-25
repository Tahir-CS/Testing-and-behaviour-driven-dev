from flask import Blueprint, jsonify, request, abort
from . import db
from .models import Product
from .schema import product_schema, products_schema

bp = Blueprint("api", __name__)


@bp.route("/health", methods=["GET"])  # simple health check
def health():
    return jsonify({"status": "ok"}), 200


@bp.route("/products", methods=["POST"])
def create_product():
    json_data = request.get_json(silent=True) or {}
    try:
        data = product_schema.load(json_data)
    except Exception as exc:  # Marshmallow ValidationError
        return jsonify({"error": str(exc)}), 400

    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product_schema.dump(product)), 201


@bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
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
        # Partial update allowed: validate only provided fields by loading then merging
        # We validate using schema with partial=True to allow missing required fields
        data = product_schema.load(json_data, partial=True)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    product.update_from_dict(data)
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
    # Filters: category, available, name (substring match, case-insensitive)
    category = request.args.get("category")
    available = request.args.get("available")
    name = request.args.get("name")

    query = Product.query

    if category:
        query = query.filter(Product.category == category)

    if available is not None:
        if available.lower() in ("true", "1", "yes"):  # type: ignore[union-attr]
            query = query.filter(Product.available.is_(True))
        elif available.lower() in ("false", "0", "no"):  # type: ignore[union-attr]
            query = query.filter(Product.available.is_(False))
        else:
            return jsonify({"error": "available must be true/false"}), 400

    if name:
        like = f"%{name}%"
        query = query.filter(Product.name.ilike(like))

    products = query.order_by(Product.id.asc()).all()
    return jsonify(products_schema.dump(products)), 200
