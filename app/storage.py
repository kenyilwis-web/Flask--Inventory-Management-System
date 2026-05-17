"""In-memory storage using a temporary array."""
from typing import Dict, List, Optional
import uuid
from datetime import datetime

from app.utils.external_api import OpenFoodFactsClient


# In-memory storage array
current_timestamp = datetime.utcnow().isoformat()

inventory_storage: List[Dict] = [
    {
        'id': '1',
        'name': 'Organic Almond Milk',
        'sku': 'ALM-001',
        'barcode': '1234567890123',
        'description': 'Unsweetened organic almond milk.',
        'quantity': 18,
        'price': 3.99,
        'category': 'Beverages',
        'min_stock': 5,
        'created_at': current_timestamp,
        'updated_at': current_timestamp
    },
    {
        'id': '2',
        'name': 'Greek Plain Yogurt',
        'sku': 'YOG-002',
        'barcode': '2345678901234',
        'description': 'Thick plain Greek yogurt.',
        'quantity': 12,
        'price': 4.49,
        'category': 'Dairy',
        'min_stock': 6,
        'created_at': current_timestamp,
        'updated_at': current_timestamp
    },
    {
        'id': '3',
        'name': 'Whole Wheat Bread',
        'sku': 'BRD-003',
        'barcode': '3456789012345',
        'description': 'Whole wheat sandwich bread.',
        'quantity': 7,
        'price': 2.99,
        'category': 'Bakery',
        'min_stock': 4,
        'created_at': current_timestamp,
        'updated_at': current_timestamp
    }
]


def generate_id() -> str:
    """Generate a unique ID for each item."""
    return str(uuid.uuid4())


def get_all_items() -> List[Dict]:
    """Get all inventory items."""
    return inventory_storage.copy()


def fetch_openfoodfacts_metadata(barcode: str = None, name: str = None) -> Optional[Dict]:
    """Fetch additional product details from OpenFoodFacts by barcode or name."""
    if not barcode and not name:
        return None

    client = OpenFoodFactsClient()
    result = client.fetch_product_details(barcode=barcode, product_name=name)

    if result.get('status') == 'success':
        return result.get('data')

    return None


def merge_external_data(item: Dict, external_data: Optional[Dict]) -> None:
    """Merge OpenFoodFacts data into an inventory item."""
    if not external_data:
        return

    item['external_data'] = external_data

    if not item.get('description') and external_data.get('ingredients_text'):
        item['description'] = external_data.get('ingredients_text')

    if not item.get('category') and external_data.get('categories'):
        item['category'] = external_data.get('categories')


def get_item_by_id(item_id: str) -> Optional[Dict]:
    """Get a single item by ID."""
    for item in inventory_storage:
        if item['id'] == item_id:
            return item
    return None


def create_item(data: Dict) -> Dict:
    """Create a new inventory item."""
    item_id = generate_id()
    timestamp = datetime.utcnow().isoformat()
    
    new_item = {
        'id': item_id,
        'name': data.get('name'),
        'sku': data.get('sku'),
        'barcode': data.get('barcode'),
        'description': data.get('description'),
        'quantity': data.get('quantity', 0),
        'price': data.get('price', 0.0),
        'category': data.get('category'),
        'min_stock': data.get('min_stock', 0),
        'created_at': timestamp,
        'updated_at': timestamp,
        'external_data': None
    }

    external_metadata = fetch_openfoodfacts_metadata(
        barcode=new_item.get('barcode'),
        name=new_item.get('name')
    )
    merge_external_data(new_item, external_metadata)
    
    inventory_storage.append(new_item)
    return new_item


def update_item(item_id: str, data: Dict) -> Optional[Dict]:
    """Update an existing inventory item."""
    for item in inventory_storage:
        if item['id'] == item_id:
            # Update only provided fields
            if 'name' in data and data['name']:
                item['name'] = data['name']
            if 'sku' in data and data['sku']:
                item['sku'] = data['sku']
            if 'barcode' in data:
                item['barcode'] = data['barcode']
            if 'description' in data:
                item['description'] = data['description']
            if 'quantity' in data:
                item['quantity'] = data['quantity']
            if 'price' in data:
                item['price'] = data['price']
            if 'category' in data:
                item['category'] = data['category']
            if 'min_stock' in data:
                item['min_stock'] = data['min_stock']

            external_metadata = fetch_openfoodfacts_metadata(
                barcode=item.get('barcode'),
                name=item.get('name')
            )
            merge_external_data(item, external_metadata)
            
            item['updated_at'] = datetime.utcnow().isoformat()
            return item
    
    return None


def delete_item(item_id: str) -> bool:
    """Delete an inventory item."""
    global inventory_storage
    
    for i, item in enumerate(inventory_storage):
        if item['id'] == item_id:
            inventory_storage.pop(i)
            return True
    
    return False


def get_low_stock_items() -> List[Dict]:
    """Get items where quantity is below min_stock."""
    return [
        item for item in inventory_storage
        if item['quantity'] < item['min_stock']
    ]


def get_categories() -> List[str]:
    """Get all unique categories."""
    categories = set()
    for item in inventory_storage:
        if item.get('category'):
            categories.add(item['category'])
    return sorted(list(categories))


def search_items(query: str) -> List[Dict]:
    """Search items by name."""
    query_lower = query.lower()
    return [
        item for item in inventory_storage
        if query_lower in item.get('name', '').lower()
    ]


def sku_exists(sku: str, exclude_id: str = None) -> bool:
    """Check if SKU already exists."""
    for item in inventory_storage:
        if item.get('sku') == sku:
            if exclude_id and item['id'] == exclude_id:
                continue
            return True
    return False