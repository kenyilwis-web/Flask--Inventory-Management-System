"""Unit tests for External API integration."""
import pytest
import json
from unittest.mock import patch, MagicMock
from app import create_app
from app.models import db
from app.utils.external_api import OpenFoodFactsClient
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


class TestOpenFoodFactsClient:
    """Test cases for OpenFoodFacts client."""
    
    def test_get_product_by_barcode_success(self, app):
        """Test successful barcode lookup."""
        mock_response = {
            'status': 1,
            'product': {
                'product_name': 'Test Product',
                'brands': 'Test Brand',
                'quantity': '500g',
                'nutriscore_grade': 'A',
                'categories': 'Food > Snacks',
                'image_url': 'https://example.com/image.jpg',
                'ingredients_text': 'Water, Sugar'
            }
        }
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None
            )
            
            with app.app_context():
                client = OpenFoodFactsClient()
                result = client.get_product_by_barcode('123456789')
        
        assert result['status'] == 'success'
        assert result['data']['product_name'] == 'Test Product'
        assert result['data']['brands'] == 'Test Brand'
    
    def test_get_product_by_barcode_not_found(self, app):
        """Test barcode not found."""
        mock_response = {
            'status': 0,
            'status_verbose': 'product not found'
        }
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None
            )
            
            with app.app_context():
                client = OpenFoodFactsClient()
                result = client.get_product_by_barcode('0000000000000')
        
        assert result['status'] == 'not_found'
        assert 'not found' in result['message'].lower()
    
    def test_get_product_by_barcode_timeout(self, app):
        """Test barcode lookup timeout."""
        import requests
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout()
            
            with app.app_context():
                client = OpenFoodFactsClient()
                result = client.get_product_by_barcode('123456789')
        
        assert result['status'] == 'error'
        assert 'timed out' in result['message'].lower()
    
    def test_search_products_success(self, app):
        """Test successful product search."""
        mock_response = {
            'products': [
                {
                    'product_name': 'Product 1',
                    'brands': 'Brand A',
                    'quantity': '1L',
                    'nutriscore_grade': 'B',
                    'categories': 'Dairy',
                    'image_url': 'https://example.com/1.jpg',
                    'code': '1234567890123'
                },
                {
                    'product_name': 'Product 2',
                    'brands': 'Brand B',
                    'quantity': '500g',
                    'nutriscore_grade': 'C',
                    'categories': 'Snacks',
                    'image_url': 'https://example.com/2.jpg',
                    'code': '9876543210987'
                }
            ]
        }
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None
            )
            
            with app.app_context():
                client = OpenFoodFactsClient()
                result = client.search_products('milk')
        
        assert result['status'] == 'success'
        assert result['data']['count'] == 2
        assert len(result['data']['products']) == 2
    
    def test_search_products_empty(self, app):
        """Test search with no results."""
        mock_response = {'products': []}
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None
            )
            
            with app.app_context():
                client = OpenFoodFactsClient()
                result = client.search_products('nonexistentproduct12345')
        
        assert result['status'] == 'success'
        assert result['data']['count'] == 0
        assert result['data']['products'] == []
    
    def test_search_products_timeout(self, app):
        """Test search timeout."""
        import requests
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout()
            
            with app.app_context():
                client = OpenFoodFactsClient()
                result = client.search_products('test')
        
        assert result['status'] == 'error'
        assert 'timed out' in result['message'].lower()


class TestExternalAPIRoutes:
    """Test cases for external API routes."""
    
    def test_barcode_route_success(self, client):
        """Test barcode endpoint success."""
        mock_response = {
            'status': 1,
            'product': {
                'product_name': 'Test Product',
                'brands': 'Test Brand',
                'quantity': '500g',
                'nutriscore_grade': 'A',
                'categories': 'Food',
                'image_url': 'https://example.com/img.jpg',
                'ingredients_text': 'Ingredients'
            }
        }
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None
            )
            
            response = client.get('/api/external/barcode/123456789')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_barcode_route_not_found(self, client):
        """Test barcode endpoint not found."""
        mock_response = {'status': 0}
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None
            )
            
            response = client.get('/api/external/barcode/0000000000000')
        
        assert response.status_code == 404
    
    def test_search_route_success(self, client):
        """Test search endpoint success."""
        mock_response = {
            'products': [
                {
                    'product_name': 'Product A',
                    'brands': 'Brand A',
                    'quantity': '1L',
                    'nutriscore_grade': 'B',
                    'categories': 'Dairy',
                    'image_url': '',
                    'code': '123'
                }
            ]
        }
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None
            )
            
            response = client.get('/api/external/search/milk')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_search_route_pagination(self, client):
        """Test search with pagination parameters."""
        mock_response = {'products': []}
        
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                json=lambda: mock_response,
                raise_for_status=lambda: None
            )
            
            response = client.get('/api/external/search/test?page=2&page_size=10')
        
        assert response.status_code == 200
    
    def test_empty_barcode(self, client):
        """Test empty barcode parameter."""
        response = client.get('/api/external/barcode/')
        
        # Flask routing may handle this differently
        assert response.status_code in [404, 400]
    
    def test_empty_search_term(self, client):
        """Test empty search term."""
        response = client.get('/api/external/search/')
        
        assert response.status_code in [404, 400]