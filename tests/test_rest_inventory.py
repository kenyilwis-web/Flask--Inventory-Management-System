"""Unit tests for root-level inventory REST endpoints."""
import json
from datetime import datetime
from unittest.mock import patch

import pytest
from app import create_app
from app.storage import inventory_storage
from config import TestingConfig

SAMPLE_TIMESTAMP = datetime.utcnow().isoformat()


@pytest.fixture
def app():
    app = create_app('testing')
    app.config.from_object(TestingConfig)

    with app.app_context():
        inventory_storage.clear()
        inventory_storage.extend([
            {
                'id': 'item-1',
                'name': 'Test Product',
                'sku': 'TEST-001',
                'barcode': '1234567890123',
                'description': 'A test product',
                'quantity': 10,
                'price': 9.99,
                'category': 'Test Category',
                'min_stock': 5,
                'created_at': SAMPLE_TIMESTAMP,
                'updated_at': SAMPLE_TIMESTAMP,
                'external_data': None
            },
            {
                'id': 'item-2',
                'name': 'Another Product',
                'sku': 'TEST-002',
                'barcode': '2345678901234',
                'description': 'Another test product',
                'quantity': 3,
                'price': 5.99,
                'category': 'Other Category',
                'min_stock': 5,
                'created_at': SAMPLE_TIMESTAMP,
                'updated_at': SAMPLE_TIMESTAMP,
                'external_data': None
            }
        ])

        yield app

        inventory_storage.clear()


@pytest.fixture
def client(app):
    return app.test_client()


class TestRestInventoryEndpoints:
    def test_get_all_items(self, client):
        response = client.get('/inventory')

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'
        assert len(result['data']['items']) == 2

    def test_get_single_item(self, client):
        response = client.get('/inventory/item-1')

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'
        assert result['data']['name'] == 'Test Product'
        assert result['data']['sku'] == 'TEST-001'

    def test_get_item_not_found(self, client):
        response = client.get('/inventory/nonexistent')

        assert response.status_code == 404
        result = json.loads(response.data)
        assert result['status'] == 'error'
        assert 'not found' in result['message'].lower()

    @patch('app.storage.fetch_openfoodfacts_metadata')
    def test_add_item(self, mock_fetch, client):
        mock_fetch.return_value = {
            'product_name': 'Mocked Product',
            'brands': 'Mock Brand',
            'quantity': '1L',
            'categories': 'Beverages',
            'ingredients_text': 'Water, sugar'
        }

        payload = {
            'name': 'New Item',
            'sku': 'NEW-001',
            'barcode': '9999999999999',
            'description': 'New inventory item',
            'quantity': 4,
            'price': 2.49,
            'category': 'Food',
            'min_stock': 2
        }

        response = client.post(
            '/inventory',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 201
        result = json.loads(response.data)
        assert result['status'] == 'success'
        assert result['data']['name'] == 'New Item'
        assert result['data']['external_data']['product_name'] == 'Mocked Product'

    @patch('app.storage.fetch_openfoodfacts_metadata')
    def test_update_item(self, mock_fetch, client):
        mock_fetch.return_value = {
            'product_name': 'Updated Mock',
            'categories': 'Updated Category'
        }

        payload = {
            'price': 12.99,
            'quantity': 25
        }

        response = client.patch(
            '/inventory/item-1',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'
        assert result['data']['price'] == 12.99
        assert result['data']['quantity'] == 25
        assert result['data']['external_data']['product_name'] == 'Updated Mock'

    def test_update_item_not_found(self, client):
        payload = {'quantity': 10}

        response = client.patch(
            '/inventory/nonexistent',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 404

    def test_delete_item(self, client):
        response = client.delete('/inventory/item-2')

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'
        assert 'deleted' in result['message'].lower()

        follow_up = client.get('/inventory/item-2')
        assert follow_up.status_code == 404

    def test_delete_item_not_found(self, client):
        response = client.delete('/inventory/nonexistent')

        assert response.status_code == 404

    def test_search_items(self, client):
        response = client.get('/inventory/search?q=Test')

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'
        assert result['data']['count'] == 1
        assert result['data']['items'][0]['id'] == 'item-1'
