# Route Analysis & Mock Database

## 1. API Routes - Inputs, Outputs & Data Changes

### Inventory Routes

| Route | Method | Input | Output | Data Change |
|-------|--------|-------|--------|-------------|
| `/api/items` | GET | `page`, `per_page`, `category` (query params) | Paginated list of items | None (read-only) |
| `/api/items/<id>` | GET | `id` (URL path) | Single item object | None (read-only) |
| `/api/items` | POST | JSON body with `name`, `sku` (required) | Created item with ID | **Creates new record** |
| `/api/items/<id>` | PUT | `id` (URL path), JSON body | Updated item object | **Updates existing record** |
| `/api/items/<id>` | DELETE | `id` (URL path) | 204 No Content | **Deletes record** |
| `/api/items/low-stock` | GET | None | Items where `quantity < min_stock` | None (read-only) |
| `/api/categories` | GET | None | List of unique categories | None (read-only) |

### External API Routes

| Route | Method | Input | Output | Data Change |
|-------|--------|-------|--------|-------------|
| `/api/external/barcode/<barcode>` | GET | `barcode` (URL path) | Product details from OpenFoodFacts | None (read-only) |
| `/api/external/search/<name>` | GET | `name` (URL path), `page`, `page_size` (query) | Search results from OpenFoodFacts | None (read-only) |

---

## 2. CLI Commands & Triggered Routes

### Inventory Management CLI

| CLI Command | Triggers Route | Purpose |
|-------------|----------------|---------|
| `python -m cli items list` | `GET /api/items` | Display all inventory items |
| `python -m cli items add <name> <sku>` | `POST /api/items` | Create new inventory item |
| `python -m cli items update <id>` | `PUT /api/items/<id>` | Update existing item |
| `python -m cli items delete <id>` | `DELETE /api/items/<id>` | Delete an item |
| `python -m cli items search <query>` | `GET /api/items` (filtered) | Search items by name |
| `python -m cli items low-stock` | `GET /api/items/low-stock` | Show low stock items |

### External API CLI

| CLI Command | Triggers Route | Purpose |
|-------------|----------------|---------|
| `python -m cli external barcode <barcode>` | `GET /api/external/barcode/<barcode>` | Fetch product by barcode |
| `python -m cli external search <name>` | `GET /api/external/search/<name>` | Search external products |

### Server CLI

| CLI Command | Triggers | Purpose |
|-------------|----------|---------|
| `python -m cli server` | Flask `app.run()` | Start development server |

---

## 3. Mock Database (OpenFoodFacts-style)

The following mock data simulates what the OpenFoodFacts API returns. Each item contains an `id` and mirrors the API response structure.

```python
# filepath: app/utils/mock_database.py
"""Mock database simulating OpenFoodFacts API responses."""

MOCK_PRODUCTS_DB = [
    {
        "id": 1,
        "barcode": "1234567890123",
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "quantity": "1L",
            "nutriscore_grade": "A",
            "categories": "Beverages > Plant-based > Almond Milk",
            "image_url": "https://images.openfoodfacts.org/almond-milk.jpg",
            "ingredients_text": "Filtered water, almonds (2%), cane sugar, tricalcium phosphate, sea salt, xanthan gum, carrageenan, vitamin D2, vitamin B12.",
            "nutriments": {
                "energy-kcal": 15,
                "fat": 1.2,
                "carbohydrates": 0.3,
                "proteins": 0.5
            },
            "allergens": "tree nuts",
            "labels": "Organic, Vegan"
        }
    },
    {
        "id": 2,
        "barcode": "2345678901234",
        "status": 1,
        "product": {
            "product_name": "Greek Plain Yogurt",
            "brands": "Fage",
            "quantity": "500g",
            "nutriscore_grade": "A",
            "categories": "Dairy > Yogurt > Greek Yogurt",
            "image_url": "https://images.openfoodfacts.org/greek-yogurt.jpg",
            "ingredients_text": "Milk, cream, milk protein, live bacterial cultures.",
            "nutriments": {
                "energy-kcal": 97,
                "fat": 5.0,
                "carbohydrates": 3.6,
                "proteins": 9.0
            },
            "allergens": "milk",
            "labels": "None"
        }
    },
    {
        "id": 3,
        "barcode": "3456789012345",
        "status": 1,
        "product": {
            "product_name": "Whole Wheat Bread",
            "brands": "Nature's Own",
            "quantity": "600g",
            "nutriscore_grade": "B",
            "categories": "Bakery > Bread > Whole Wheat",
            "image_url": "https://images.openfoodfacts.org/wheat-bread.jpg",
            "ingredients_text": "Whole wheat flour, water, yeast, salt, wheat gluten, soybean oil.",
            "nutriments": {
                "energy-kcal": 247,
                "fat": 3.4,
                "carbohydrates": 41.0,
                "proteins": 10.0
            },
            "allergens": "wheat",
            "labels": "Whole Grain"
        }
    },
    {
        "id": 4,
        "barcode": "4567890123456",
        "status": 1,
        "product": {
            "product_name": "Extra Virgin Olive Oil",
            "brands": "Bertolli",
            " "500ml",
            "nutriscore_grade": "A",
            "categories": "Oils > Olive Oil",
            "image_url": "https://images.openfoodfacts.org/olive-oil.jpg",
            "ingredients_text": "100% extra virgin olive oil.",
            "nutriments": {
                "energy-kcal": 884,
                "fat": 100.0,
                "carbohydrates": 0.0,
                "proteins": 0.0
            },
            "allergens": "None",
            "labels": "Cold Pressed, Non-GMO"
        }
    },
    {
        "id": 5,
        "barcode": "5678901234567",
        "status": 1,
        "product": {
            "product_name": "Organic Quinoa",
            "brands": "Bob's Red Mill",
            "quantity": "907g",
            "nutriscore_grade": "A",
            "categories": "Grains > Quinoa > Organic",
            "image_url": "https://images.openfoodfacts.org/quinoa.jpg",
            "ingredients_text": "Organic white quinoa.",
            "nutriments": {
                "energy-kcal": 368,
                "fat": 6.0,
                "carbohydrates": 64.0,
                "proteins": 14.0
            },
            "allergens": "None",
            "labels": "Organic, Non-GMO, Kosher"
        }
    },
    {
        "id": 6,
        "barcode": "6789012345678",
        "status": 1,
        "product": {
            "product_name": "Chicken Breast Fillets",
            "brands": "Perdue",
            "quantity": "1lb",
            "nutriscore_grade": "A",
            "categories": "Meat > Poultry > Chicken",
            "image_url": "https://images.openfoodfacts.org/chicken.jpg",
            "ingredients_text": "Chicken breast fillets.",
            "nutriments": {
                "energy-kcal": 165,
                "fat": 3.6,
                "carbohydrates": 0.0,
                "proteins": 31.0
            },
            "allergens": "None",
            "labels": "All Natural, No Antibiotics"
        }
    },
    {
        "id": 7,
        "barcode": "7890123456789",
        "status": 1,
        "product": {
            "product_name": "Atlantic Salmon Fillet",
            "brands": "Wild Catch",
            "quantity": "500g",
            "nutriscore_grade": "B",
            "categories": "Seafood > Salmon",
            "image_url": "https://images.openfoodfacts.org/salmon.jpg",
            "ingredients_text": "Atlantic salmon fillet.",
            "nutriments": {
                "energy-kcal": 208,
                "fat": 13.0,
                "carbohydrates": 0.0,
                "proteins": 20.0
            },
            "allergens": "fish",
            "labels": "Wild Caught"
        }
    },
    {
        "id": 8,
        "barcode": "8901234567890",
        "status": 1,
        "product": {
            "product_name": "Organic Baby Spinach",
            "brands": "Organic Girl",
            "quantity": "142g",
            "nutriscore_grade": "A",
            "categories": "Produce > Leafy Greens > Spinach",
            "image_url": "https://images.openfoodfacts.org/spinach.jpg",
            "ingredients_text": "Organic baby spinach leaves.",
            "nutriments": {
                "energy-kcal": 23,
                "fat": 0.4,
                "carbohydrates": 3.6,
                "proteins": 2.9
            },
            "allergens": "None",
            "labels": "Organic, Triple Washed"
        }
    },
    {
        "id": 9,
        "barcode": "9012345678901",
        "status": 1,
        "product": {
            "product_name": "Honey Raw Organic",
            "brands": "Local Hive",
            "quantity": "340g",
            "nutriscore_grade": "A",
            "categories": "Sweeteners > Honey > Raw",
            "image_url": "https://images.openfoodfacts.org/honey.jpg",
            "ingredients_text": "Raw organic honey.",
            "nutriments": {
                "energy-kcal": 304,
                "fat": 0.0,
                "carbohydrates": 82.0,
                "proteins": 0.3
            },
            "allergens": "None",
            "labels": "Raw, Organic, Local"
        }
    },
    {
        "id": 10,
        "barcode": "0123456789012",
        "status": 1,
        "product": {
            "product_name": "Canned Black Beans",
            "brands": "Goya",
            "quantity": "15.5oz",
            "nutriscore_grade": "A",
            "categories": "Canned Goods > Beans > Black Beans",
            "image_url": "https://images.openfoodfacts.org/black-beans.jpg",
            "ingredients_text": "Black beans, water, salt.",
            "nutriments": {
                "energy-kcal": 132,
                "fat": 0.5,
                "carbohydrates": 24.0,
                "proteins": 9.0
            },
            "allergens": "None",
            "labels": "No Salt Added"
        }
    }
]
```

---

## 4. Data Flow Diagram

```
CLI Command                    Route                          Database
─────────────────────────────────────────────────────────────────────────
items list              ──►   GET /api/items              ──►   SQLite
items add <name> <sku>  ──►   POST /api/items             ──►   SQLite (INSERT)
items update <id>      ──►   PUT /api/items/<id>        ──►   SQLite (UPDATE)
items delete <id>      ──►   DELETE /api/items/<id>    ──►   SQLite (DELETE)
items search <query>   ──►   GET /api/items (filtered) ──►   SQLite
items low-stock        ──►   GET /api/items/low-stock   ──►   SQLite
external barcode <barcode> ─► GET /api/external/barcode ──►   Mock DB / OpenFoodFacts
external search <name>  ──►   GET /api/external/search   ──►   Mock DB / OpenFoodFacts
```

---

## 5. Request/Response Examples

### POST /api/items (Create)

**Request:**
```json
{
  "name": "Organic Almond Milk",
  "sku": "ALMOND-001",
  "barcode": "1234567890123",
  "quantity": 50,
  "price": 4.99,
  "category": "Beverages",
  "min_stock": 10
}
```

**Response (201):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Organic Almond Milk",
    "sku": "ALMOND-001",
    "barcode": "1234567890123",
    "quantity": 50,
    "price": 4.99,
    "category": "Beverages",
    "min_stock": 10,
    "created_at": "2026-04-23T10:00:00",
    "updated_at": "2026-04-23T10:00:00"
  }
}
```

### GET /api/external/barcode/1234567890123

**Response:**
```json
{
  "status": "success",
  "data": {
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "quantity": "1L",
    "nutriscore": "A",
    "categories": "Beverages > Plant-based > Almond Milk",
    "image_url": "https://images.openfoodfacts.org/almond-milk.jpg",
    "ingredients_text": "Filtered water, almonds (2%), cane sugar, ...",
    "barcode": "1234567890123"
  }
}
```