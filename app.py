# app.py
# Main Flask application — all API routes are defined here.

from flask import Flask, jsonify, request
from database import inventory, find_item_by_id, get_next_id
from external_api import fetch_by_barcode, fetch_by_name

app = Flask(__name__)


# ──────────────────────────────────────────
# INVENTORY ROUTES (CRUD)
# ──────────────────────────────────────────

# GET /inventory — Return all items in the inventory
@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200


# GET /inventory/<id> — Return a single item by its ID
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_one_item(item_id):
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200


# POST /inventory — Add a new item to inventory
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    # Make sure the required fields are included
    required_fields = ["product_name", "brands", "price", "stock"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Build the new item with an auto-generated ID
    new_item = {
        "id": get_next_id(),
        "barcode": data.get("barcode", ""),
        "product_name": data["product_name"],
        "brands": data["brands"],
        "category": data.get("category", ""),
        "quantity": data.get("quantity", ""),
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)
    return jsonify(new_item), 201  # 201 = Created


# PATCH /inventory/<id> — Update specific fields of an existing item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    # Only update the fields that were sent in the request
    for key, value in data.items():
        if key in item:
            item[key] = value

    return jsonify(item), 200


# DELETE /inventory/<id> — Remove an item from inventory
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": f"Item {item_id} deleted"}), 200

# EXTERNAL API ROUTES

# GET /search/barcode/<barcode> — Look up a product by barcode
@app.route("/search/barcode/<barcode>", methods=["GET"])
def search_by_barcode(barcode):
    product, error = fetch_by_barcode(barcode)

    if error:
        return jsonify({"error": error}), 404

    return jsonify(product), 200


# GET /search/name/<name> — Search products by name
@app.route("/search/name/<name>", methods=["GET"])
def search_by_name(name):
    products, error = fetch_by_name(name)

    if error:
        return jsonify({"error": error}), 404

    return jsonify(products), 200


# POST /search/barcode/<barcode>/add — Fetch from API and add to inventory
@app.route("/search/barcode/<barcode>/add", methods=["POST"])
def add_from_api(barcode):
    product, error = fetch_by_barcode(barcode)

    if error:
        return jsonify({"error": error}), 404

    data = request.get_json() or {}

    # Combine API data with user-supplied price and stock
    new_item = {
        "id": get_next_id(),
        "barcode": barcode,
        "product_name": product["product_name"],
        "brands": product["brands"],
        "category": product["category"],
        "quantity": product["quantity"],
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0)
    }

    inventory.append(new_item)
    return jsonify(new_item), 201

# RUN THE APP
if __name__ == "__main__":

    app.run(debug=True)
