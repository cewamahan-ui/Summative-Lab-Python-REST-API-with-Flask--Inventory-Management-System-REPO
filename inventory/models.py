# models.py - In-memory inventory database (simulated with a list)
# Each item mirrors the structure returned by the OpenFoodFacts API,
# plus extra fields we need for inventory (price, stock, id).

inventory = [
    {
        "id": 1,
        "barcode": "0025293004122",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "category": "Dairy Alternatives",
        "ingredients_text": (
            "Filtered water, almonds, cane sugar, sea salt, "
            "locust bean gum, sunflower lecithin, gellan gum, "
            "calcium carbonate, vitamin A palmitate, vitamin D2."
        ),
        "image_url": "https://images.openfoodfacts.org/images/products/002/529/300/4122/front_en.jpg",
        "quantity": "1.89 L",
        "price": 4.99,
        "stock": 50,
    },
    {
        "id": 2,
        "barcode": "016000275287",
        "product_name": "Cheerios",
        "brands": "General Mills",
        "category": "Breakfast Cereals",
        "ingredients_text": (
            "Whole grain oats, modified corn starch, sugar, salt, "
            "calcium carbonate, oat bran, monoglycerides, vitamin E."
        ),
        "image_url": "https://images.openfoodfacts.org/images/products/016/000/275/287/front_en.jpg",
        "quantity": "510 g",
        "price": 5.49,
        "stock": 30,
    },
    {
        "id": 3,
        "barcode": "021130126026",
        "product_name": "Whole Wheat Bread",
        "brands": "Nature's Own",
        "category": "Breads",
        "ingredients_text": (
            "Whole wheat flour, water, sugar, yeast, wheat gluten, "
            "soybean oil, salt, monoglycerides, calcium propionate."
        ),
        "image_url": "https://images.openfoodfacts.org/images/products/021/130/126/026/front_en.jpg",
        "quantity": "570 g",
        "price": 3.29,
        "stock": 20,
    },
    {
        "id": 4,
        "barcode": "038000845017",
        "product_name": "Corn Flakes",
        "brands": "Kellogg's",
        "category": "Breakfast Cereals",
        "ingredients_text": (
            "Milled corn, sugar, malt flavoring, salt, iron, "
            "niacinamide, pyridoxine hydrochloride, riboflavin, thiamin."
        ),
        "image_url": "https://images.openfoodfacts.org/images/products/038/000/845/017/front_en.jpg",
        "quantity": "340 g",
        "price": 4.19,
        "stock": 45,
    },
    {
        "id": 5,
        "barcode": "049000028904",
        "product_name": "Coca-Cola Classic",
        "brands": "Coca-Cola",
        "category": "Soft Drinks",
        "ingredients_text": (
            "Carbonated water, high fructose corn syrup, caramel color, "
            "phosphoric acid, natural flavors, caffeine."
        ),
        "image_url": "https://images.openfoodfacts.org/images/products/049/000/028/904/front_en.jpg",
        "quantity": "355 mL",
        "price": 1.99,
        "stock": 120,
    },
]


def get_next_id():
    """Return the next available integer ID."""
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


def find_item(item_id):
    """Return the item dict with the given ID, or None."""
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None
