"""REST API routes for inventory management using in-memory storage."""
from flask import Blueprint, request, jsonify
from app import storage

rest_inventory_bp = Blueprint('rest_inventory', __name__)


@rest_inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    """Fetch all inventory items.
    
    Query Parameters:
        - category (optional): Filter by category
        - page (optional): Page number for pagination
        - per_page (optional): Items per page
    
    Returns:
        JSON response with list of all items
    """
    items = storage.get_all_items()
    
    # Optional category filter
    category = request.args.get('category')
    if category:
        items = [item for item in items if item.get('category') == category]
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = items[start_idx:end_idx]
    
    return jsonify({
        'status': 'success',
        'data': {
            'items': paginated_items,
            'total': len(items),
            'page': page,
            'per_page': per_page,
            'pages': (len(items) + per_page - 1) // per_page
        }
    }), 200


@rest_inventory_bp.route('/inventory/<item_id>', methods=['GET'])
def get_inventory_item(item_id):
    """Fetch a single inventory item by ID.
    
    Path Parameters:
        - item_id: The unique identifier of the item
    
    Returns:
        JSON response with the item details
    """
    item = storage.get_item_by_id(item_id)
    
    if not item:
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': item
    }), 200


@rest_inventory_bp.route('/inventory', methods=['POST'])
def add_inventory_item():
    """Add a new inventory item."""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    new_item = storage.create_item(data)
    return jsonify({'status': 'success', 'data': new_item}), 201


@rest_inventory_bp.route('/inventory/<item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    """Update an existing inventory item."""
    data = request.get_json()
    updated_item = storage.update_item(item_id, data)

    if not updated_item:
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404

    return jsonify({'status': 'success', 'data': updated_item}), 200


@rest_inventory_bp.route('/inventory/<item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    """Delete an inventory item."""
    success = storage.delete_item(item_id)

    if not success:
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404

    return jsonify({'status': 'success', 'message': 'Item deleted'}), 200


@rest_inventory_bp.route('/inventory/low-stock', methods=['GET'])
def get_low_stock():
    """Fetch items where quantity is below min_stock.
    
    Returns:
        JSON response with low stock items
    """
    items = storage.get_low_stock_items()
    
    return jsonify({
        'status': 'success',
        'data': {
            'items': items,
            'count': len(items)
        }
    }), 200


@rest_inventory_bp.route('/inventory/categories', methods=['GET'])
def get_inventory_categories():
    """Fetch all unique categories.
    
    Returns:
        JSON response with list of categories
    """
    categories = storage.get_categories()
    
    return jsonify({
        'status': 'success',
        'data': {
            'categories': categories,
            'count': len(categories)
        }
    }), 200


@rest_inventory_bp.route('/inventory/search', methods=['GET'])
def search_inventory():
    """Search inventory items by name.
    
    Query Parameters:
        - q: Search query string
    
    Returns:
        JSON response with matching items
    """
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'status': 'error',
            'message': 'Search query required'
        }), 400
    
    items = storage.search_items(query)
    
    return jsonify({
        'status': 'success',
        'data': {
            'items': items,
            'count': len(items),
            'query': query
        }
    }), 200