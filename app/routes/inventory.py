"""Inventory CRUD routes."""
from flask import Blueprint, request, jsonify
from app.models import db, InventoryItem

inventory_bp = Blueprint('inventory', __name__)


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
    if not data or 'name' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

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

    for key, value in data.items():
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
    return jsonify({'status': 'success', 'message': 'Item deleted'}), 200