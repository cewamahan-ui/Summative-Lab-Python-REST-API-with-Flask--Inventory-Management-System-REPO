# cli.py
# Command-line interface to interact with the Flask API.
# Make sure the Flask app (app.py) is running before using this.

import requests

# The base URL of our running Flask app
BASE = "http://127.0.0.1:5000"


def print_divider():
    print("\n" + "=" * 40 + "\n")


def show_menu():
    print("📦 Inventory Manager")
    print("1. View all inventory")
    print("2. View one item by ID")
    print("3. Add a new item manually")
    print("4. Update an item (price or stock)")
    print("5. Delete an item")
    print("6. Search product by barcode (OpenFoodFacts)")
    print("7. Search products by name (OpenFoodFacts)")
    print("8. Fetch product by barcode and add to inventory")
    print("9. Exit")


#  1. View all items 
def view_all():
    response = requests.get(f"{BASE}/inventory")
    items = response.json()

    if not items:
        print("Inventory is empty.")
        return

    for item in items:
        print(f"[{item['id']}] {item['product_name']} | {item['brands']} | "
              f"Price: ${item['price']} | Stock: {item['stock']}")


#  2. View one item 
def view_one():
    item_id = input("Enter item ID: ").strip()

    response = requests.get(f"{BASE}/inventory/{item_id}")

    if response.status_code == 404:
        print("Item not found.")
        return

    item = response.json()
    for key, value in item.items():
        print(f"  {key}: {value}")


#  3. Add new item manually 
def add_item():
    print("Enter the new item details:")

    product_name = input("  Product name: ").strip()
    brands = input("  Brand: ").strip()
    category = input("  Category: ").strip()
    quantity = input("  Quantity (e.g. 500g): ").strip()
    barcode = input("  Barcode (optional): ").strip()

    # Handle bad price input
    try:
        price = float(input("  Price: $").strip())
    except ValueError:
        print("Invalid price. Please enter a number.")
        return

    # Handle bad stock input
    try:
        stock = int(input("  Stock count: ").strip())
    except ValueError:
        print("Invalid stock. Please enter a whole number.")
        return

    new_item = {
        "product_name": product_name,
        "brands": brands,
        "category": category,
        "quantity": quantity,
        "barcode": barcode,
        "price": price,
        "stock": stock
    }

    response = requests.post(f"{BASE}/inventory", json=new_item)
    print("✅ Item added:", response.json())


#  4. Update item 
def update_item():
    item_id = input("Enter item ID to update: ").strip()

    print("What do you want to update?")
    print("  1. Price")
    print("  2. Stock")
    print("  3. Both")
    choice = input("Choice: ").strip()

    updates = {}

    if choice in ("1", "3"):
        try:
            updates["price"] = float(input("  New price: $").strip())
        except ValueError:
            print("Invalid price.")
            return

    if choice in ("2", "3"):
        try:
            updates["stock"] = int(input("  New stock: ").strip())
        except ValueError:
            print("Invalid stock.")
            return

    if not updates:
        print("Nothing to update.")
        return

    response = requests.patch(f"{BASE}/inventory/{item_id}", json=updates)

    if response.status_code == 404:
        print("Item not found.")
        return

    print("✅ Item updated:", response.json())


#  5. Delete item 
def delete_item():
    item_id = input("Enter item ID to delete: ").strip()

    # Ask user to confirm before deleting
    confirm = input(f"Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Cancelled.")
        return

    response = requests.delete(f"{BASE}/inventory/{item_id}")

    if response.status_code == 404:
        print("Item not found.")
        return

    print("🗑️ Deleted:", response.json())


#  6. Search by barcode 
def search_barcode():
    barcode = input("Enter barcode: ").strip()
    response = requests.get(f"{BASE}/search/barcode/{barcode}")

    if response.status_code == 404:
        print("Product not found on OpenFoodFacts.")
        return

    product = response.json()
    for key, value in product.items():
        print(f"  {key}: {value}")


# 7. Search by name 
def search_name():
    name = input("Enter product name to search: ").strip()
    response = requests.get(f"{BASE}/search/name/{name}")

    if response.status_code == 404:
        print("No products found.")
        return

    results = response.json()
    for p in results:
        print(f"  [{p['barcode']}] {p['product_name']} | {p['brands']} | {p['quantity']}")


#  8. Fetch by barcode and add to inventory 
def add_from_api():
    barcode = input("Enter barcode to fetch and add: ").strip()

    try:
        price = float(input("  Price: $").strip())
        stock = int(input("  Stock count: ").strip())
    except ValueError:
        print("Invalid price or stock.")
        return

    response = requests.post(
        f"{BASE}/search/barcode/{barcode}/add",
        json={"price": price, "stock": stock}
    )

    if response.status_code == 404:
        print("Product not found on OpenFoodFacts.")
        return

    print("✅ Product added to inventory:", response.json())


# Main loop 
def main():
    while True:
        print_divider()
        show_menu()
        print_divider()

        choice = input("Choose an option (1-9): ").strip()

        print_divider()

        if choice == "1":
            view_all()
        elif choice == "2":
            view_one()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_barcode()
        elif choice == "7":
            search_name()
        elif choice == "8":
            add_from_api()
        elif choice == "9":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid option. Please choose 1–9.")


if __name__ == "__main__":
    main()
