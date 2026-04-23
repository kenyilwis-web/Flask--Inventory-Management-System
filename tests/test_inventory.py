"""Unit tests for Inventory API."""
import pytest
import json
from app import create_app
from app.models import db, InventoryItem
from config import TestingConfig


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    app.config.from_object(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_item(app):
    """Create a sample inventory item."""
    with app.app_context():
        item = InventoryItem(
            name='Test Product',
            sku='TEST-001',
            barcode='1234567890123',
            description='A test product',
            quantity=10,
            price=9.99,
            category='Test Category',
            min_stock=5
        )
        db.session.add(item)
        db.session.commit()
        
        return item.id


class TestInventoryCRUD:
    """Test cases for Inventory CRUD operations."""
    
    def test_create_item(self, client):
        """Test creating a new inventory item."""
        payload = {
            'name': 'New Product',
            'sku': 'NEW-001',
            'barcode': '9876543210987',
            'description': 'A new product',
            'quantity': 20,
            'price': 15.99,
            'category': 'Electronics',
            'min_stock': 5
        }
        
        response = client.post(
            '/api/items',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == 'New Product'
        assert data['data']['sku'] == 'NEW-001'
    
    def test_create_item_missing_required_fields(self, client):
        """Test creating item without required fields."""
        payload = {'name': 'Incomplete Product'}
        
        response = client.post(
            '/api/items',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Missing required fields' in data['message']
    
    def test_create_item_duplicate_sku(self, client, sample_item):
        """Test creating item with duplicate SKU."""
        payload = {
            'name': 'Duplicate SKU Product',
            'sku': 'TEST-001'  # Same as sample_item
        }
        
        response = client.post(
            '/api/items',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'SKU already exists' in data['message']
    
    def test_get_all_items(self, client, sample_item):
        """Test retrieving all items."""
        response = client.get('/api/items')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']['items']) > 0
    
    def test_get_single_item(self, client, sample_item):
        """Test retrieving a single item by ID."""
        response = client.get(f'/api/items/{sample_item}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['name'] == 'Test Product'
        assert data['data']['sku'] == 'TEST-001'
    
    def test_get_single_item_not_found(self, client):
        """Test retrieving non-existent item."""
        response = client.get('/api/items/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Item not found' in data['message']
    
    def test_update_item(self, client, sample_item):
        """Test updating an existing item."""
        payload = {
            'quantity': 25,
            'price': 12.99
        }
        
        response = client.put(
            f'/api/items/{sample_item}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['quantity'] == 25
        assert data['data']['price'] == 12.99
    
    def test_update_item_not_found(self, client):
        """Test updating non-existent item."""
        payload = {'quantity': 10}
        
        response = client.put(
            '/api/items/99999',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_item(self, client, sample_item):
        """Test deleting an item."""
        response = client.delete(f'/api/items/{sample_item}')
        
        assert response.status_code == 204
        
        # Verify item is deleted
        response = client.get(f'/api/items/{sample_item}')
        assert response.status_code == 404
    
    def test_delete_item_not_found(self, client):
        """Test deleting non-existent item."""
        response = client.delete('/api/items/99999')
        
        assert response.status_code == 404


class TestInventoryValidation:
    """Test cases for input validation."""
    
    def test_negative_quantity(self, client):
        """Test that negative quantity is rejected."""
        payload = {
            'name': 'Negative Qty Product',
            'sku': 'NEG-001',
            'quantity': -5
        }
        
        response = client.post(
            '/api/items',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'negative' in data['message'].lower()
    
    def test_negative_price(self, client):
        """Test that negative price is rejected."""
        payload = {
            'name': 'Negative Price Product',
            'sku': 'NEGP-001',
            'price': -10.0
        }
        
        response = client.post(
            '/api/items',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_invalid_quantity_type(self, client):
        """Test that invalid quantity type is rejected."""
        payload = {
            'name': 'Invalid Qty',
            'sku': 'INV-001',
            'quantity': 'not a number'
        }
        
        response = client.post(
            '/api/items',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestInventoryUtilities:
    """Test cases for utility endpoints."""
    
    def test_low_stock_items(self, client, app):
        """Test getting low stock items."""
        with app.app_context():
            # Create item with low stock
            item = InventoryItem(
                name='Low Stock Item',
                sku='LOW-001',
                quantity=2,
                min_stock=10
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
        
        response = client.get('/api/items/low-stock')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['count'] >= 1
    
    def test_get_categories(self, client, sample_item):
        """Test getting all categories."""
        response = client.get('/api/categories')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'Test Category' in data['data']['categories']


class TestPagination:
    """Test cases for pagination."""
    
    def test_pagination_defaults(self, client, app):
        """Test default pagination."""
        with app.app_context():
            # Create multiple items
            for i in range(25):
                item = InventoryItem(
                    name=f'Product {i}',
                    sku=f'PROD-{i:03d}',
                    quantity=i,
                    price=i * 1.0
                )
                db.session.add(item)
            db.session.commit()
        
        response = client.get('/api/items')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['page'] == 1
        assert data['data']['per_page'] == 20
        assert data['data']['pages'] == 2
    
    def test_custom_pagination(self, client, app):
        """Test custom pagination parameters."""
        with app.app_context():
            for i in range(10):
                item = InventoryItem(
                    name=f'PageProduct {i}',
                    sku=f'PP-{i:03d}',
                    quantity=i,
                    price=i * 1.0
                )
                db.session.add(item)
            db.session.commit()
        
        response = client.get('/api/items?page=1&per_page=5')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['data']['items']) == 5
        assert data['data']['per_page'] == 5