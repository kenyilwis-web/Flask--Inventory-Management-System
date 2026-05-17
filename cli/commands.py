"""Click CLI commands for Inventory Management System."""
import click
import json
import requests
import sys
from pathlib import Path
from requests.exceptions import RequestException

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.models import db, InventoryItem
from app.utils.external_api import OpenFoodFactsClient
from app.utils.mock_database import (
    get_product_by_barcode as mock_get_product,
    search_products_by_name as mock_search
)

API_DEFAULT_BASE_URL = 'http://127.0.0.1:5000'


def api_request(method, endpoint, base_url=None, **kwargs):
    """Send an HTTP request to the inventory API."""
    base_url = base_url or API_DEFAULT_BASE_URL
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.HTTPError:
        try:
            return response.json(), response.status_code
        except ValueError:
            return {'status': 'error', 'message': f'HTTP error {response.status_code}'}, response.status_code
    except RequestException as exc:
        return {'status': 'error', 'message': str(exc)}, None


def format_item(item):
    """Return a formatted string for inventory item display."""
    return (
        f"[{item.get('id')}] {item.get('name')} (SKU: {item.get('sku')})\n"
        f"    Quantity: {item.get('quantity')} | Price: ${item.get('price', 0.0):.2f}\n"
        f"    Category: {item.get('category') or 'N/A'}\n"
        f"    Barcode: {item.get('barcode') or 'N/A'}\n"
        f"    Description: {item.get('description') or 'N/A'}"
    )


@click.group()
def cli():
    """Inventory Management System CLI."""
    pass


@cli.group()
def items():
    """Manage inventory items."""
    pass


@items.command('list')
@click.option('--category', '-c', help='Filter by category')
@click.option('--page', '-p', default=1, help='Page number')
@click.option('--per-page', default=20, help='Items per page')
def list_items(category, page, per_page):
    """List all inventory items."""
    app = create_app()
    
    with app.app_context():
        query = InventoryItem.query
        
        if category:
            query = query.filter(InventoryItem.category == category)
        
        pagination = query.order_by(InventoryItem.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        if not pagination.items:
            click.echo('No items found.')
            return
        
        for item in pagination.items:
            click.echo(f"[{item.id}] {item.name} (SKU: {item.sku})")
            click.echo(f"    Quantity: {item.quantity} | Price: ${item.price:.2f}")
            click.echo(f"    Category: {item.category or 'N/A'}")
            click.echo()
        
        click.echo(f"Page {page} of {pagination.pages} | Total: {pagination.total} items")


@items.command('add')
@click.argument('name')
@click.argument('sku')
@click.option('--barcode', '-b', help='Product barcode')
@click.option('--description', '-d', help='Product description')
@click.option('--quantity', '-q', default=0, type=int, help='Initial quantity')
@click.option('--price', '-p', default=0.0, type=float, help='Unit price')
@click.option('--category', '-c', help='Product category')
@click.option('--min-stock', '-m', default=0, type=int, help='Minimum stock threshold')
def add_item(name, sku, barcode, description, quantity, price, category, min_stock):
    """Add a new inventory item."""
    app = create_app()
    
    with app.app_context():
        # Check if SKU exists
        existing = InventoryItem.query.filter_by(sku=sku).first()
        if existing:
            click.echo(f"Error: SKU '{sku}' already exists.", err=True)
            return
        
        item = InventoryItem(
            name=name,
            sku=sku,
            barcode=barcode,
            description=description,
            quantity=quantity,
            price=price,
            category=category,
            min_stock=min_stock
        )
        
        db.session.add(item)
        db.session.commit()
        
        click.echo(f"Item created successfully: {item.name} (ID: {item.id})")


@items.command('update')
@click.argument('item_id', type=int)
@click.option('--name', '-n', help='Product name')
@click.option('--sku', '-s', help='SKU')
@click.option('--barcode', '-b', help='Product barcode')
@click.option('--description', '-d', help='Product description')
@click.option('--quantity', '-q', type=int, help='Quantity')
@click.option('--price', '-p', type=float, help='Unit price')
@click.option('--category', '-c', help='Product category')
@click.option('--min-stock', '-m', type=int, help='Minimum stock threshold')
def update_item(item_id, name, sku, barcode, description, quantity, price, category, min_stock):
    """Update an existing inventory item."""
    app = create_app()
    
    with app.app_context():
        item = InventoryItem.query.get(item_id)
        
        if not item:
            click.echo(f"Error: Item with ID {item_id} not found.", err=True)
            return
        
        # Update provided fields
        if name:
            item.name = name
        if sku:
            # Check if new SKU exists
            existing = InventoryItem.query.filter(
                InventoryItem.sku == sku,
                InventoryItem.id != item_id
            ).first()
            if existing:
                click.echo(f"Error: SKU '{sku}' already exists.", err=True)
                return
            item.sku = sku
        if barcode is not None:
            item.barcode = barcode
        if description is not None:
            item.description = description
        if quantity is not None:
            item.quantity = quantity
        if price is not None:
            item.price = price
        if category is not None:
            item.category = category
        if min_stock is not None:
            item.min_stock = min_stock
        
        db.session.commit()
        
        click.echo(f"Item updated successfully: {item.name} (ID: {item.id})")


@items.command('delete')
@click.argument('item_id', type=int)
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompt')
def delete_item(item_id, force):
    """Delete an inventory item."""
    app = create_app()
    
    with app.app_context():
        item = InventoryItem.query.get(item_id)
        
        if not item:
            click.echo(f"Error: Item with ID {item_id} not found.", err=True)
            return
        
        if not force:
            if not click.confirm(f"Delete '{item.name}'?"):
                click.echo("Cancelled.")
                return
        
        db.session.delete(item)
        db.session.commit()
        
        click.echo(f"Item deleted: {item.name} (ID: {item.id})")


@items.command('search')
@click.argument('query')
def search_items(query):
    """Search inventory items by name."""
    app = create_app()
    
    with app.app_context():
        items = InventoryItem.query.filter(
            InventoryItem.name.ilike(f'%{query}%')
        ).all()
        
        if not items:
            click.echo(f"No items found matching '{query}'.")
            return
        
        for item in items:
            click.echo(f"[{item.id}] {item.name} (SKU: {item.sku})")
            click.echo(f"    Quantity: {item.quantity} | Price: ${item.price:.2f}")
            click.echo()


@items.command('low-stock')
def low_stock():
    """List items below minimum stock threshold."""
    app = create_app()
    
    with app.app_context():
        items = InventoryItem.query.filter(
            InventoryItem.quantity < InventoryItem.min_stock
        ).all()
        
        if not items:
            click.echo("No low-stock items.")
            return
        
        click.echo("Low Stock Items:")
        click.echo("-" * 50)
        
        for item in items:
            click.echo(f"[{item.id}] {item.name}")
            click.echo(f"    Current: {item.quantity} | Min: {item.min_stock}")
            click.echo()


@cli.group()
def api():
    """Interact with the inventory REST API."""
    pass


@api.command('list')
@click.option('--base-url', default=API_DEFAULT_BASE_URL, help='Base URL for the REST API')
@click.option('--category', '-c', help='Filter by category')
@click.option('--page', '-p', default=1, type=int, help='Page number')
@click.option('--per-page', default=20, type=int, help='Items per page')
def api_list(base_url, category, page, per_page):
    """List inventory items through the REST API."""
    params = {'page': page, 'per_page': per_page}
    if category:
        params['category'] = category

    data, status = api_request('GET', '/inventory', base_url=base_url, params=params)

    if status != 200 or data.get('status') != 'success':
        click.echo(f"Error: {data.get('message', 'Unable to fetch inventory')}" , err=True)
        return

    items = data.get('data', {}).get('items', [])
    if not items:
        click.echo('No items found.')
        return

    for item in items:
        click.echo(format_item(item))
        click.echo()


@api.command('get')
@click.argument('item_id')
@click.option('--base-url', default=API_DEFAULT_BASE_URL, help='Base URL for the REST API')
def api_get(item_id, base_url):
    """Get inventory item details from the REST API."""
    data, status = api_request('GET', f'/inventory/{item_id}', base_url=base_url)

    if status != 200:
        click.echo(f"Error: {data.get('message', 'Item not found')}" , err=True)
        return

    item = data.get('data')
    click.echo(format_item(item))


@api.command('add')
@click.argument('name')
@click.argument('sku')
@click.option('--barcode', '-b', help='Product barcode')
@click.option('--description', '-d', help='Product description')
@click.option('--quantity', '-q', default=0, type=int, help='Initial quantity')
@click.option('--price', '-p', default=0.0, type=float, help='Unit price')
@click.option('--category', '-c', help='Product category')
@click.option('--min-stock', '-m', default=0, type=int, help='Minimum stock threshold')
@click.option('--base-url', default=API_DEFAULT_BASE_URL, help='Base URL for the REST API')
def api_add(name, sku, barcode, description, quantity, price, category, min_stock, base_url):
    """Add a new inventory item through the REST API."""
    payload = {
        'name': name,
        'sku': sku,
        'barcode': barcode,
        'description': description,
        'quantity': quantity,
        'price': price,
        'category': category,
        'min_stock': min_stock
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    data, status = api_request('POST', '/inventory', base_url=base_url, json=payload)

    if status != 201:
        click.echo(f"Error: {data.get('message', 'Unable to create item')}" , err=True)
        return

    item = data.get('data')
    click.echo(f"Item created successfully: {item.get('name')} (ID: {item.get('id')})")


@api.command('update')
@click.argument('item_id')
@click.option('--name', '-n', help='Product name')
@click.option('--sku', '-s', help='SKU')
@click.option('--barcode', '-b', help='Product barcode')
@click.option('--description', '-d', help='Product description')
@click.option('--quantity', '-q', type=int, help='Quantity')
@click.option('--price', '-p', type=float, help='Unit price')
@click.option('--category', '-c', help='Product category')
@click.option('--min-stock', '-m', type=int, help='Minimum stock threshold')
@click.option('--base-url', default=API_DEFAULT_BASE_URL, help='Base URL for the REST API')
def api_update(item_id, name, sku, barcode, description, quantity, price, category, min_stock, base_url):
    """Update an inventory item through the REST API."""
    payload = {
        'name': name,
        'sku': sku,
        'barcode': barcode,
        'description': description,
        'quantity': quantity,
        'price': price,
        'category': category,
        'min_stock': min_stock
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    if not payload:
        click.echo('No update fields were provided.', err=True)
        return

    data, status = api_request('PATCH', f'/inventory/{item_id}', base_url=base_url, json=payload)

    if status != 200:
        click.echo(f"Error: {data.get('message', 'Unable to update item')}" , err=True)
        return

    item = data.get('data')
    click.echo(f"Item updated successfully: {item.get('name')} (ID: {item.get('id')})")


@api.command('delete')
@click.argument('item_id')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompt')
@click.option('--base-url', default=API_DEFAULT_BASE_URL, help='Base URL for the REST API')
def api_delete(item_id, force, base_url):
    """Delete an inventory item through the REST API."""
    if not force and not click.confirm(f"Delete item {item_id}?"):
        click.echo('Cancelled.')
        return

    data, status = api_request('DELETE', f'/inventory/{item_id}', base_url=base_url)

    if status != 200:
        click.echo(f"Error: {data.get('message', 'Unable to delete item')}" , err=True)
        return

    click.echo(f"Item deleted successfully: {item_id}")


@api.command('find')
@click.argument('query')
@click.option('--base-url', default=API_DEFAULT_BASE_URL, help='Base URL for the REST API')
def api_find(query, base_url):
    """Find inventory items by name through the REST API."""
    params = {'q': query}
    data, status = api_request('GET', '/inventory/search', base_url=base_url, params=params)

    if status != 200 or data.get('status') != 'success':
        click.echo(f"Error: {data.get('message', 'Unable to search inventory')}" , err=True)
        return

    items = data.get('data', {}).get('items', [])
    if not items:
        click.echo(f"No items found matching '{query}'.")
        return

    for item in items:
        click.echo(format_item(item))
        click.echo()


@cli.group()
def external():
    """Query external product database (OpenFoodFacts)."""
    pass


@external.command('barcode')
@click.argument('barcode')
def fetch_by_barcode(barcode):
    """Fetch product by barcode."""
    # Try mock database first
    mock_result = mock_get_product(barcode)
    
    if mock_result:
        product = mock_result.get('product', {})
        click.echo(f"Product: {product.get('product_name')}")
        click.echo(f"Brands: {product.get('brands')}")
        click.echo(f"Quantity: {product.get('quantity')}")
        click.echo(f"Nutri-Score: {product.get('nutriscore_grade')}")
        click.echo(f"Categories: {product.get('categories')}")
        click.echo(f"Source: Mock Database")
        return
    
    # Fallback to OpenFoodFacts API
    app = create_app()
    
    with app.app_context():
        client = OpenFoodFactsClient()
        result = client.get_product_by_barcode(barcode)
        
        if result.get('status') == 'success':
            data = result['data']
            click.echo(f"Product: {data['product_name']}")
            click.echo(f"Brands: {data['brands']}")
            click.echo(f"Quantity: {data['quantity']}")
            click.echo(f"Nutri-Score: {data['nutriscore']}")
            click.echo(f"Categories: {data['categories']}")
            click.echo(f"Source: OpenFoodFacts API")
        elif result.get('status') == 'not_found':
            click.echo(f"Product not found for barcode: {barcode}", err=True)
        else:
            click.echo(f"Error: {result.get('message')}", err=True)


@external.command('search')
@click.argument('name')
@click.option('--page', '-p', default=1, type=int, help='Page number')
@click.option('--page-size', '-s', default=10, type=int, help='Results per page')
def search_external(name, page, page_size):
    """Search products by name."""
    # Try mock database first
    mock_result = mock_search(name, page=page, page_size=page_size)
    
    if mock_result.get('status') == 'success' and mock_result.get('data', {}).get('count', 0) > 0:
        data = mock_result['data']
        click.echo(f"Found {data['count']} products (Mock Database):")
        click.echo("-" * 50)
        
        for product in data['products']:
            click.echo(f"• {product['product_name']}")
            click.echo(f"  Brand: {product['brands']} | Quantity: {product['quantity']}")
            click.echo()
        return
    
    # Fallback to OpenFoodFacts API
    app = create_app()
    
    with app.app_context():
        client = OpenFoodFactsClient()
        result = client.search_products(name, page=page, page_size=page_size)
        
        if result.get('status') == 'success':
            data = result['data']
            click.echo(f"Found {data['count']} products (OpenFoodFacts API):")
            click.echo("-" * 50)
            
            for product in data['products']:
                click.echo(f"• {product['product_name']}")
                click.echo(f"  Brand: {product['brands']} | Quantity: {product['quantity']}")
                click.echo()
        else:
            click.echo(f"Error: {result.get('message')}", err=True)


@cli.command('server')
@click.option('--host', default='0.0.0.0', help='Server host')
@click.option('--port', default=5000, type=int, help='Server port')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def start_server(host, port, debug):
    """Start the Flask development server."""
    app = create_app()
    click.echo(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    cli()