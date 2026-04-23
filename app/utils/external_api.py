"""OpenFoodFacts API client."""
import requests
from flask import current_app


class OpenFoodFactsClient:
    """Client for interacting with OpenFoodFacts API."""
    
    def __init__(self, base_url=None, timeout=None):
        """Initialize the client with configuration."""
        self.base_url = base_url or current_app.config.get(
            'OPENFOODFACTS_URL', 
            'https://world.openfoodfacts.org'
        )
        self.timeout = timeout or current_app.config.get(
            'OPENFOODFACTS_TIMEOUT', 
            10
        )
    
    def get_product_by_barcode(self, barcode):
        """
        Fetch product details by barcode.
        
        Args:
            barcode: Product barcode string
            
        Returns:
            dict: Product details or None if not found
        """
        url = f"{self.base_url}/api/v0/product/{barcode}.json"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 1:
                product = data.get('product', {})
                return {
                    'status': 'success',
                    'data': {
                        'product_name': product.get('product_name', ''),
                        'brands': product.get('brands', ''),
                        'quantity': product.get('quantity', ''),
                        'nutriscore': product.get('nutriscore_grade', ''),
                        'categories': product.get('categories', ''),
                        'image_url': product.get('image_url', ''),
                        'ingredients_text': product.get('ingredients_text', ''),
                        'barcode': barcode
                    }
                }
            else:
                return {
                    'status': 'not_found',
                    'message': 'Product not found',
                    'barcode': barcode
                }
                
        except requests.exceptions.Timeout:
            return {
                'status': 'error',
                'message': 'Request timed out'
            }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def search_products(self, name, page=1, page_size=20):
        """
        Search products by name.
        
        Args:
            name: Product name to search
            page: Page number (default: 1)
            page_size: Number of results per page (default: 20)
            
        Returns:
            dict: Search results or error
        """
        url = f"{self.base_url}/cgi/search.pl"
        
        params = {
            'search_terms': name,
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page': page,
            'page_size': page_size
        }
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            products = data.get('products', [])
            results = []
            
            for product in products:
                if product.get('product_name'):  # Only include products with names
                    results.append({
                        'product_name': product.get('product_name', ''),
                        'brands': product.get('brands', ''),
                        'quantity': product.get('quantity', ''),
                        'nutriscore': product.get('nutriscore_grade', ''),
                        'categories': product.get('categories', ''),
                        'image_url': product.get('image_url', ''),
                        'barcode': product.get('code', '')
                    })
            
            return {
                'status': 'success',
                'data': {
                    'count': len(results),
                    'page': page,
                    'products': results
                }
            }
            
        except requests.exceptions.Timeout:
            return {
                'status': 'error',
                'message': 'Request timed out'
            }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': str(e)
            }