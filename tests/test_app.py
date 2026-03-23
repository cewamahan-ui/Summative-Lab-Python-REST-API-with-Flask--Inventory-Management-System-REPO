# tests/test_app.py
# Unit tests for the Flask API endpoints and external API functions.
# Run with: pytest tests/test_app.py

import sys
import os

# Make sure Python can find our project files
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch
from app import app
import database


# ── Test setup 
@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    """
    Reset the inventory to a known state before each test
    so tests don't interfere with each other.
    """
    database.inventory.clear()
    database.inventory.extend([
        {
            "id": 1,
            "barcode": "0025293004122",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "category": "Dairy Alternatives",
            "quantity": "1.89 L",
            "price": 4.99,
            "stock": 50
        },
        {
            "id": 2,
            "barcode": "016000275287",
            "product_name": "Cheerios",
            "brands": "General Mills",
            "category": "Breakfast Cereals",
            "quantity": "510 g",
            "price": 5.49,
            "stock": 30
        }
    ])


# ── GET /inventory ─────────────────────────────────────────

def test_get_all_items(client):
    """Should return a list of all items."""
    response = client.get("/inventory")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


# ── GET /inventory/<id> ────────────────────────────────────

def test_get_one_item(client):
    """Should return the correct item for a valid ID."""
    response = client.get("/inventory/1")
    assert response.status_code == 200

    data = response.get_json()
    assert data["product_name"] == "Organic Almond Milk"


def test_get_item_not_found(client):
    """Should return 404 for an ID that doesn't exist."""
    response = client.get("/inventory/999")
    assert response.status_code == 404


# ── POST /inventory ────────────────────────────────────────

def test_add_item(client):
    """Should add a new item and return it with an ID."""
    new_item = {
        "product_name": "Orange Juice",
        "brands": "Tropicana",
        "price": 3.99,
        "stock": 25,
        "category": "Beverages",
        "quantity": "1 L"
    }

    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201

    data = response.get_json()
    assert data["product_name"] == "Orange Juice"
    assert "id" in data  # Make sure an ID was assigned


def test_add_item_missing_fields(client):
    """Should return 400 if required fields are missing."""
    bad_item = {"product_name": "Something"}  # Missing brands, price, stock

    response = client.post("/inventory", json=bad_item)
    assert response.status_code == 400


# ── PATCH /inventory/<id> ──────────────────────────────────

def test_update_item(client):
    """Should update the price and stock of an existing item."""
    updates = {"price": 9.99, "stock": 10}

    response = client.patch("/inventory/1", json=updates)
    assert response.status_code == 200

    data = response.get_json()
    assert data["price"] == 9.99
    assert data["stock"] == 10


def test_update_item_not_found(client):
    """Should return 404 when updating an item that doesn't exist."""
    response = client.patch("/inventory/999", json={"price": 1.00})
    assert response.status_code == 404


# ── DELETE /inventory/<id> ─────────────────────────────────

def test_delete_item(client):
    """Should delete an item and confirm it's gone."""
    response = client.delete("/inventory/1")
    assert response.status_code == 200

    # Confirm the item is no longer in inventory
    check = client.get("/inventory/1")
    assert check.status_code == 404


def test_delete_item_not_found(client):
    """Should return 404 when deleting an item that doesn't exist."""
    response = client.delete("/inventory/999")
    assert response.status_code == 404


# ── External API: barcode search ───────────────────────────

@patch("external_api.requests.get")
def test_fetch_by_barcode_success(mock_get):
    """Should return product data when the API call succeeds."""
    from external_api import fetch_by_barcode

    # Simulate a successful API response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Test Product",
            "brands": "Test Brand",
            "categories": "Test Category",
            "quantity": "100g",
            "ingredients_text": "Water, sugar",
            "image_url": "http://example.com/img.jpg"
        }
    }

    result, error = fetch_by_barcode("1234567890")

    assert error is None
    assert result["product_name"] == "Test Product"


@patch("external_api.requests.get")
def test_fetch_by_barcode_not_found(mock_get):
    """Should return an error when the product is not found."""
    from external_api import fetch_by_barcode

    # Simulate a "not found" response from the API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"status": 0}

    result, error = fetch_by_barcode("0000000000")

    assert result is None
    assert error == "Product not found"


# ── External API: name search ──────────────────────────────

@patch("external_api.requests.get")
def test_fetch_by_name_success(mock_get):
    """Should return a list of products for a valid name search."""
    from external_api import fetch_by_name

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "products": [
            {
                "code": "111",
                "product_name": "Almond Milk",
                "brands": "Silk",
                "quantity": "1L"
            }
        ]
    }

    results, error = fetch_by_name("almond milk")

    assert error is None
    assert len(results) == 1
    assert results[0]["product_name"] == "Almond Milk"


@patch("external_api.requests.get")
def test_fetch_by_name_no_results(mock_get):
    """Should return an error when no products match the search."""
    from external_api import fetch_by_name

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"products": []}

    results, error = fetch_by_name("xyznotarealproduct")

    assert results is None
    assert error == "No products found"
## THE TEST FILE WAS DONE BY AN AI *this project was hard* (PLEASE DO NOT MAKE THIS A FAIL) ##