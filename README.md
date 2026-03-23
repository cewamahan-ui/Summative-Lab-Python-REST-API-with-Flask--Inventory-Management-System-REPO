# Inventory Management System
A simple REST API built with Flask for managing a retail inventory.
Includes CLI interaction and live product lookups via OpenFoodFacts.

---

## Project Structure

```
inventory-management/
├── app.py            # Flask app and all API routes
├── database.py       # In-memory inventory (list of products)
├── external_api.py   # OpenFoodFacts API functions
├── cli.py            # Command-line interface
├── requirements.txt  # Python dependencies
└── tests/
    └── test_app.py   # Unit tests
```


**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Start the Flask server**
```bash
python app.py
```

**4. In a separate terminal, run the CLI**
```bash
python cli.py
```

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/inventory` | Get all items |
| GET | `/inventory/<id>` | Get one item by ID |
| POST | `/inventory` | Add a new item |
| PATCH | `/inventory/<id>` | Update price or stock |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/search/barcode/<barcode>` | Look up product on OpenFoodFacts |
| GET | `/search/name/<name>` | Search products by name |
| POST | `/search/barcode/<barcode>/add` | Fetch from API and add to inventory |

---

## Example API Usage (with curl)

**Get all items**
```bash
curl http://127.0.0.1:5000/inventory
```

**Add a new item**
```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Orange Juice", "brands": "Tropicana", "price": 3.99, "stock": 20}'
```

**Update stock**
```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"stock": 75}'
```

**Delete an item**
```bash
curl -X DELETE http://127.0.0.1:5000/inventory/2
```

**Search by barcode**
```bash
curl http://127.0.0.1:5000/search/barcode/049000028904
```

---

## Running Tests

```bash
pytest tests/test_app.py
```

---

## CLI Menu Options

```
1. View all inventory
2. View one item by ID
3. Add a new item manually
4. Update an item (price or stock)
5. Delete an item
6. Search product by barcode (OpenFoodFacts)
7. Search products by name (OpenFoodFacts)
8. Fetch product by barcode and add to inventory
9. Exit
```
