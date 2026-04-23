# Inventory Management System - Specification

## 1. Project Overview

- **Project Name**: Flask Inventory Management System
- **Type**: REST API + CLI Application
- **Core Functionality**: A Flask-based inventory management system with CRUD operations, external API integration (OpenFoodFacts), and CLI interface
- **Target Users**: Small retail company employees

---

## 2. Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | Flask 3.x |
| Database | SQLite (SQLAlchemy ORM) |
| External API | OpenFoodFacts API |
| CLI | Click |
| Testing | pytest |
| HTTP Client | requests |

---

## 3. Data Model

### InventoryItem

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key, auto-increment |
| name | String(100) | Product name (required) |
| sku | String(50) | Stock Keeping Unit (unique) |
| barcode | String(50) | Product barcode (optional) |
| description | String(500) | Product description |
| quantity | Integer | Stock quantity (default: 0) |
| price | Float | Unit price (default: 0.0) |
| category | String(50) | Product category |
| min_stock | Integer | Minimum stock threshold |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

---

## 4. API Endpoints

### 4.1 Inventory CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items` | List all inventory items |
| GET | `/api/items/<id>` | Get single item by ID |
| POST | `/api/items` | Create new inventory item |
| PUT | `/api/items/<id>` | Update existing item |
| DELETE | `/api/items/<id>` | Delete an item |

### 4.2 External API Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/external/barcode/<barcode>` | Fetch product by barcode |
| GET | `/api/external/search/<name>` | Search product by name |

### 4.3 Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items/low-stock` | Get items below min_stock |
| GET | `/api/categories` | List all categories |

---

## 5. Request/Response Formats

### 5.1 Create Item (POST /api/items)

**Request:**
```json
{
  "name": "Organic Milk",
  "sku": "MILK-001",
  "barcode": "1234567890123",
  "description": "Fresh organic milk 1L",
  "quantity": 50,
  "price": 4.99,
  "category": "Dairy",
  "min_stock": 10
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Organic Milk",
  "sku": "MILK-001",
  "barcode": "1234567890123",
  "description": "Fresh organic milk 1L",
  "quantity": 50,
  "price": 4.99,
  "category": "Dairy",
  "min_stock": 10,
  "created_at": "2026-04-23T10:00:00",
  "updated_at": "2026-04-23T10:00:00"
}
```

### 5.2 Update Item (PUT /api/items/<id>)

**Request:**
```json
{
  "quantity": 45,
  "price": 5.49
}
```

### 5.3 External API Response

**GET /api/external/barcode/1234567890123**

```json
{
  "status": "success",
  "data": {
    "product_name": "Organic Milk",
    "brands": "Brand X",
    "quantity": "1L",
    "nutriscore": "A",
    "categories": "Dairy > Milk",
    "image_url": "https://...",
    "ingredients_text": "..."
  }
}
```

---

## 6. CLI Commands

| Command | Description |
|---------|-------------|
| `python -m cli items list` | List all inventory items |
| `python -m cli items add <name> <qty> <price>` | Add new item |
| `python -m cli items update <id> <qty>` | Update item quantity |
| `python -m cli items delete <id>` | Delete an item |
| `python -m cli items search <query>` | Search items by name |
| `python -m cli external barcode <barcode>` | Fetch product by barcode |
| `python -m cli external search <name>` | Search external products |
| `python -m cli server` | Start Flask development server |

---

## 7. Project Structure

```
Flask--Inventory-Management-System/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── inventory.py     # Inventory CRUD routes
│   │   └── external.py      # External API routes
│   └── utils/
│       ├── __init__.py
│       └── external_api.py  # OpenFoodFacts client
├── cli/
│   ├── __init__.py
│   └── commands.py          # Click CLI commands
├── tests/
│   ├── __init__.py
│   ├── test_inventory.py   # Inventory API tests
│   └── test_external.py     # External API tests
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md
```

---

## 8. Acceptance Criteria

### 8.1 API Functionality
- [ ] All CRUD endpoints return proper HTTP status codes
- [ ] POST creates item and returns 201 with created object
- [ ] PUT updates item and returns 200 with updated object
- [ ] DELETE removes item and returns 204
- [ ] GET /api/items returns paginated list

### 8.2 External API
- [ ] Barcode lookup returns product details from OpenFoodFacts
- [ ] Name search returns matching products
- [ ] Handles API errors gracefully (404, timeout)

### 8.3 CLI
- [ ] All CLI commands are functional
- [ ] Commands output proper formatted results
- [ ] Error messages are clear and helpful

### 8.4 Testing
- [ ] Unit tests for all CRUD operations
- [ ] Unit tests for external API integration
- [ ] Minimum 80% code coverage

### 8.5 Validation
- [ ] Required fields validated (name, sku)
- [ ] Unique constraint on SKU
- [ ] Price and quantity must be non-negative

---

## 9. Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | development | Environment |
| `DATABASE_URL` | sqlite:///inventory.db | Database path |
| `OPENFOODFACTS_URL` | https://world.openfoodfacts.org | API base URL |
| `DEBUG` | True | Debug mode |
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 5000 | Server port |