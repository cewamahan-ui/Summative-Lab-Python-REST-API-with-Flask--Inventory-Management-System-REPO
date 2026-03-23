# database.py
# This is our fake database — just a list of products stored in memory.

inventory = [
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
    },
    {
        "id": 3,
        "barcode": "021130126026",
        "product_name": "Whole Wheat Bread",
        "brands": "Nature's Own",
        "category": "Breads",
        "quantity": "570 g",
        "price": 3.29,
        "stock": 20
    },
    {
        "id": 4,
        "barcode": "038000845017",
        "product_name": "Corn Flakes",
        "brands": "Kellogg's",
        "category": "Breakfast Cereals",
        "quantity": "340 g",
        "price": 4.19,
        "stock": 45
    },
    {
        "id": 5,
        "barcode": "049000028904",
        "product_name": "Coca-Cola Classic",
        "brands": "Coca-Cola",
        "category": "Soft Drinks",
        "quantity": "355 mL",
        "price": 1.99,
        "stock": 120
    }
]


def get_next_id():
    # Find the highest existing ID and add 1
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


def find_item_by_id(item_id):
    # Loop through inventory and return the item that matches the ID
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None  # Return None if nothing is found
