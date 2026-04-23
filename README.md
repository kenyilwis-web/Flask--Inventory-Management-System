# Flask Inventory Management System

A Flask-based REST API for managing inventory with CRUD operations, OpenFoodFacts external API integration, and CLI interface.

## Features

- **REST API** — Full CRUD operations for inventory management
- **External API Integration** — Fetch product details from OpenFoodFacts by barcode or name
- **CLI Interface** — Command-line tools for managing inventory
- **Unit Tests** — Comprehensive test coverage

## Project Structure

```
Flask--Inventory-Management-System/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy models
│   ├── routes/
│   │   ├── inventory.py     # Inventory CRUD routes
│   │   └── external.py       # External API routes
│   └── utils/
│       └── external_api.py   # OpenFoodFacts client
├── cli/
│   ├── commands.py          # Click CLI commands
│   └── __main__.py          # CLI entry point
├── tests/
│   ├── test_inventory.py    # Inventory API tests
│   └── test_external.py    # External API tests
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── SPEC.md                  # Specification document
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python run.py
```

Or via CLI:

```bash
python -m cli server
```

The server will start on `http://0.0.0.0:5000`

## API Endpoints

### Inventory CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items` | List all inventory items |
| GET | `/api/items/<id>` | Get single item by ID |
| POST | `/api/items` | Create new inventory item |
| PUT | `/api/items/<id>` | Update existing item |
| DELETE | `/api/items/<id>` | Delete an item |

### External API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/external/barcode/<barcode>` | Fetch product by barcode |
| GET | `/api/external/search/<name>` | Search products by name |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items/low-stock` | Get items below min_stock |
| GET | `/api/categories` | List all categories |

## CLI Commands

### Inventory Management

```bash
# List all items
python -m cli items list

# Add new item
python -m cli items add "Product Name" SKU-001 --quantity 10 --price 9.99

# Update item
python -m cli items update 1 --quantity 20

# Delete item
python -m cli items delete 1

# Search items
python -m cli items search "milk"

# Low stock items
python -m cli items low-stock
```

### External API

```bash
# Fetch by barcode
python -m cli external barcode 1234567890123

# Search products
python -m cli external search "organic milk"
```

### Server

```bash
# Start development server
python -m cli server
python -m cli server --host 127.0.0.1 --port 8080
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Example API Usage

### Create Item

```bash
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Organic Milk",
    "sku": "MILK-001",
    "barcode": "1234567890123",
    "description": "Fresh organic milk 1L",
    "quantity": 50,
    "price": 4.99,
    "category": "Dairy",
    "min_stock": 10
  }'
```

### Get All Items

```bash
curl http://localhost:5000/api/items
```

### Get Low Stock Items

```bash
curl http://localhost:5000/api/items/low-stock
```

## Configuration

Edit `config.py` to modify:

- Database URL
- OpenFoodFacts API settings
- Server host/port
- Debug mode

## Technology Stack

- **Framework**: Flask 3.x
- **Database**: SQLite (SQLAlchemy ORM)
- **External API**: OpenFoodFacts
- **CLI**: Click
- **Testing**: pytest