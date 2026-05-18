"""Inventory CRUD routes."""
from flask import Blueprint, request, jsonify
from app.models import db, InventoryItem

inventory_bp = Blueprint('inventory', __name__)


def validate_item_payload(data):
    """Validate inventory payload for required fields and numeric constraints."""
    if not data or 'name' not in data or 'sku' not in data:
        return False, 'Missing required fields: name and sku are required'

    if 'quantity' in data and data['quantity'] is not None:
        if not isinstance(data['quantity'], int) or data['quantity'] < 0:
            return False, 'Quantity must be a non-negative integer'

    if 'price' in data and data['price'] is not None:
        try:
            price_value = float(data['price'])
        except (TypeError, ValueError):
            return False, 'Price must be a numeric value'
        if price_value < 0:
            return False, 'Price must be non-negative'

    return True, None


@inventory_bp.route('/items', methods=['GET'])
def get_items():
    """Get all inventory items with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', None)
    
    query = InventoryItem.query
    
    # Filter by category if provided
    if category:
        query = query.filter(InventoryItem.category == category)
    
    # Paginate results
    pagination = query.order_by(InventoryItem.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    items = [item.to_dict() for item in pagination.items]
    
    return jsonify({
        'status': 'success',
        'data': {
            'items': items,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }
    }), 200


@inventory_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a single inventory item by ID."""
    item = InventoryItem.query.get(item_id)
    
    if not item:
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': item.to_dict()
    }), 200


@inventory_bp.route('/items', methods=['POST'])
def add_item():
    """Add a new inventory item."""
    data = request.get_json()

    is_valid, error = validate_item_payload(data)
    if not is_valid:
        return jsonify({'status': 'error', 'message': error}), 400

    existing = InventoryItem.query.filter_by(sku=data['sku']).first()
    if existing:
        return jsonify({'status': 'error', 'message': 'SKU already exists'}), 409

    new_item = InventoryItem(**data)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'status': 'success', 'data': new_item.to_dict()}), 201


@inventory_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing inventory item."""
    data = request.get_json()
    item = InventoryItem.query.get(item_id)

    if not item:
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404

    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided for update'}), 400

    if 'sku' in data and data['sku'] != item.sku:
        existing = InventoryItem.query.filter_by(sku=data['sku']).first()
        if existing:
            return jsonify({'status': 'error', 'message': 'SKU already exists'}), 409

    if 'quantity' in data and data['quantity'] is not None:
        if not isinstance(data['quantity'], int) or data['quantity'] < 0:
            return jsonify({'status': 'error', 'message': 'Quantity must be a non-negative integer'}), 400

    if 'price' in data and data['price'] is not None:
        try:
            price_value = float(data['price'])
        except (TypeError, ValueError):
            return jsonify({'status': 'error', 'message': 'Price must be a numeric value'}), 400
        if price_value < 0:
            return jsonify({'status': 'error', 'message': 'Price must be non-negative'}), 400

    for key, value in data.items():
        if hasattr(item, key):
            setattr(item, key, value)

    db.session.commit()
    return jsonify({'status': 'success', 'data': item.to_dict()}), 200


@inventory_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an inventory item."""
    item = InventoryItem.query.get(item_id)

    if not item:
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Item deleted'}), 204


@inventory_bp.route('/items/low-stock', methods=['GET'])
def low_stock_items():
    """Get inventory items below their minimum stock level."""
    items = InventoryItem.query.filter(InventoryItem.quantity < InventoryItem.min_stock).all()
    return jsonify({
        'status': 'success',
        'data': {
            'items': [item.to_dict() for item in items],
            'count': len(items)
        }
    }), 200


@inventory_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get unique inventory categories."""
    categories = [category[0] for category in db.session.query(InventoryItem.category).distinct().all() if category[0]]
    return jsonify({
        'status': 'success',
        'data': {
            'categories': categories
        }
    }), 200