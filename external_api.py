# external_api.py
# Functions to fetch product info from the OpenFoodFacts API.

import requests

# Base URL for the OpenFoodFacts API
BASE_URL = "https://world.openfoodfacts.org"


def fetch_by_barcode(barcode):
    """Look up a product using its barcode number."""
    url = f"{BASE_URL}/api/v0/product/{barcode}.json"

    response = requests.get(url)

    # If the request failed, return an error message
    if response.status_code != 200:
        return None, "Failed to reach OpenFoodFacts API"

    data = response.json()

    # status 1 means the product was found
    if data.get("status") != 1:
        return None, "Product not found"

    product = data["product"]

    # Pull out only the fields we care about
    result = {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "category": product.get("categories", "Unknown"),
        "quantity": product.get("quantity", "Unknown"),
        "ingredients_text": product.get("ingredients_text", "Not available"),
        "image_url": product.get("image_url", "")
    }

    return result, None  # Return result and no error


def fetch_by_name(name):
    """Search for products by name."""
    url = f"{BASE_URL}/cgi/search.pl"

    # Query parameters for the search
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5  # Only return 5 results to keep it manageable
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None, "Failed to reach OpenFoodFacts API"

    data = response.json()
    products = data.get("products", [])

    if not products:
        return None, "No products found"

    # Build a simple list of results
    results = []
    for p in products:
        results.append({
            "barcode": p.get("code", ""),
            "product_name": p.get("product_name", "Unknown"),
            "brands": p.get("brands", "Unknown"),
            "quantity": p.get("quantity", "Unknown")
        })

    return results, None
