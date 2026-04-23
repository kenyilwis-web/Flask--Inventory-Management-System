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
def create_item():
    """Create a new inventory item."""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    required_fields = ['name', 'sku']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return jsonify({
            'status': 'error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400
    
    # Check if SKU already exists
    existing_item = InventoryItem.query.filter_by(sku=data['sku']).first()
    if existing_item:
        return jsonify({
            'status': 'error',
            'message': 'SKU already exists'
        }), 409
    
    # Validate numeric fields
    if 'quantity' in data and data['quantity'] is not None:
        try:
            data['quantity'] = int(data['quantity'])
            if data['quantity'] < 0:
                return jsonify({
                    'status': 'error',
                    'message': 'Quantity cannot be negative'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Invalid quantity value'
            }), 400
    
    if 'price' in data and data['price'] is not None:
        try:
            data['price'] = float(data['price'])
            if data['price'] < 0:
                return jsonify({
                    'status': 'error',
                    'message': 'Price cannot be negative'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Invalid price value'
            }), 400
    
    # Create new item
    item = InventoryItem(
        name=data['name'],
        sku=data['sku'],
        barcode=data.get('barcode'),
        description=data.get('description'),
        quantity=data.get('quantity', 0),
        price=data.get('price', 0.0),
        category=data.get('category'),
        min_stock=data.get('min_stock', 0)
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': item.to_dict()
    }), 201


@inventory_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing inventory item."""
    item = InventoryItem.query.get(item_id)
    
    if not item:
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    # Update fields if provided
    if 'name' in data and data['name']:
        item.name = data['name']
    
    if 'sku' in data and data['sku']:
        # Check if new SKU already exists
        existing = InventoryItem.query.filter(
            InventoryItem.sku == data['sku'],
            InventoryItem.id != item_id
        ).first()
        if existing:
            return jsonify({
                'status': 'error',
                'message': 'SKU already exists'
            }), 409
        item.sku = data['sku']
    
    if 'barcode' in data:
        item.barcode = data['barcode']
    
    if 'description' in data:
        item.description = data['description']
    
    if 'quantity' in data:
        try:
            quantity = int(data['quantity'])
            if quantity < 0:
                return jsonify({
                    'status': 'error',
                    'message': 'Quantity cannot be negative'
                }), 400
            item.quantity = quantity
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Invalid quantity value'
            }), 400
    
    if 'price' in data:
        try:
            price = float(data['price'])
            if price < 0:
                return jsonify({
                    'status': 'error',
                    'message': 'Price cannot be negative'
                }), 400
            item.price = price
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Invalid price value'
            }), 400
    
    if 'category' in data:
        item.category = data['category']
    
    if 'min_stock' in data:
        try:
            item.min_stock = int(data['min_stock'])
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Invalid min_stock value'
            }), 400
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': item.to_dict()
    }), 200


@inventory_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an inventory item."""
    item = InventoryItem.query.get(item_id)
    
    if not item:
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return '', 204


@inventory_bp.route('/items/low-stock', methods=['GET'])
def get_low_stock_items():
    """Get items below minimum stock threshold."""
    items = InventoryItem.query.filter(
        InventoryItem.quantity < InventoryItem.min_stock
    ).all()
    
    return jsonify({
        'status': 'success',
        'data': {
            'items': [item.to_dict() for item in items],
            'count': len(items)
        }
    }), 200


@inventory_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all unique categories."""
    categories = db.session.query(
        InventoryItem.category
    ).filter(
        InventoryItem.category.isnot(None)
    ).distinct().all()
    
    category_list = [cat[0] for cat in categories if cat[0]]
    
    return jsonify({
        'status': 'success',
        'data': {
            'categories': category_list,
            'count': len(category_list)
        }
    }), 200