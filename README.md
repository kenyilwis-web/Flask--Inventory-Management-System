# Flask Inventory Management System

A maintainable Flask application for inventory management using REST API endpoints, CLI commands, and OpenFoodFacts enrichment.

## Overview

This project provides:

- RESTful inventory CRUD operations
- External product lookup via OpenFoodFacts
- A Click-based CLI for inventory management
- In-memory storage for quick local development
- Unit tests covering API, CLI, and external integration

## Repository Structure

```
Flask--Inventory-Management-System/
├── app/
│   ├── __init__.py          # Flask app factory and blueprint registration
│   ├── models.py            # SQLAlchemy inventory model
│   ├── storage.py           # Temporary in-memory storage and external enrichment helpers
│   ├── routes/
│   │   ├── inventory.py     # Inventory CRUD and utility API routes
│   │   ├── external.py      # External OpenFoodFacts product routes
│   │   └── rest_inventory.py# Root-level REST inventory endpoints using in-memory storage
│   └── utils/
│       ├── external_api.py  # OpenFoodFacts API client
│       └── mock_database.py # Mock product database for offline development/testing
├── cli/
│   ├── commands.py          # CLI command definitions
│   └── __main__.py          # CLI entry point
├── tests/
│   ├── test_inventory.py    # Flask inventory route tests
│   ├── test_external.py     # External API client and endpoint tests
│   └── test_cli_api.py      # CLI command tests
├── config.py                # Configuration classes
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # Project documentation
```

## Prerequisites

- Python 3.12+
- `pip` package manager

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

Start the Flask server:

```bash
python run.py
```

The server should be available at:

```text
http://0.0.0.0:5000
```

## API Endpoints

### Inventory CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items` | List inventory items with pagination and optional category filter |
| GET | `/api/items/<id>` | Retrieve a single inventory item by ID |
| POST | `/api/items` | Create a new inventory item |
| PUT | `/api/items/<id>` | Update an existing inventory item |
| DELETE | `/api/items/<id>` | Remove an inventory item |

### External Product Lookup

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/external/barcode/<barcode>` | Retrieve product details from OpenFoodFacts by barcode |
| GET | `/api/external/search/<name>` | Search OpenFoodFacts products by name |

### Inventory Utilities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items/low-stock` | List inventory items with quantity below minimum stock |
| GET | `/api/categories` | Retrieve unique inventory categories |

## CLI Commands

### Inventory Management

```bash
# List inventory items
python -m cli items list

# Add a new item
python -m cli items add "Product Name" SKU-001 --quantity 10 --price 9.99 --category "Beverages"

# Update stock or price
python -m cli items update 1 --quantity 20 --price 11.50

# Delete an item
python -m cli items delete 1 --force

# Search items by name
python -m cli items search "milk"

# Show low-stock inventory
python -m cli items low-stock
```

### External Product Search

```bash
# Lookup by barcode
python -m cli external barcode 1234567890123

# Search products by name
python -m cli external search "organic milk"
```

### API Interaction via CLI

```bash
# List inventory via API
python -m cli api list

# Get a specific item via API
python -m cli api get <item_id>

# Add item via API
python -m cli api add "New Product" SKU-002 --quantity 5 --price 7.50

# Update item via API
python -m cli api update <item_id> --quantity 10 --price 8.25

# Delete item via API
python -m cli api delete <item_id> --force

# Search inventory via API
python -m cli api find "milk"
```

## Example cURL Requests

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

### Fetch All Items

```bash
curl http://localhost:5000/api/items
```

### Lookup Product by Barcode

```bash
curl http://localhost:5000/api/external/barcode/1234567890123
```

## Testing

Run the full test suite with:

```bash
python -m pytest tests/ -v
```

## Development Notes

- `app/storage.py` contains temporary storage and OpenFoodFacts enrichment logic.
- `app/utils/external_api.py` encapsulates external API requests and normalization.
- `app/routes/inventory.py` exposes production inventory CRUD routes.
- `cli/commands.py` provides a developer-friendly interface for both local and API-based inventory operations.
- Use `config.py` to manage environment and API settings.

## Maintainability

- Keep route handlers small and focused on one responsibility.
- Add or update tests whenever you change API behavior or CLI commands.
- Keep configuration values in `config.py` rather than hard-coding.
- Use the mock database in `app/utils/mock_database.py` for offline testing.
- Document API changes clearly in this README so the project remains easy to use.
