"""External API routes for OpenFoodFacts integration."""
from flask import Blueprint, request
from app.utils.external_api import OpenFoodFactsClient
from app.utils.mock_database import (
    get_product_by_barcode as mock_get_product,
    search_products_by_name as mock_search
)

external_bp = Blueprint('external', __name__)


@external_bp.route('/barcode/<barcode>', methods=['GET'])
def get_product_by_barcode(barcode):
    """Fetch product details by barcode from OpenFoodFacts or mock database."""
    if not barcode:
        return {
            'status': 'error',
            'message': 'Barcode is required'
        }, 400
    
    # Try mock database first
    mock_result = mock_get_product(barcode)
    
    if mock_result:
        product = mock_result.get('product', {})
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
        }, 200
    
    # Fallback to real OpenFoodFacts API
    client = OpenFoodFactsClient()
    result = client.get_product_by_barcode(barcode)
    
    status_code = 200
    if result.get('status') == 'error':
        status_code = 500
    elif result.get('status') == 'not_found':
        status_code = 404
    
    return result, status_code


@external_bp.route('/search/<path:name>', methods=['GET'])
def search_products(name):
    """Search products by name from OpenFoodFacts or mock database."""
    if not name:
        return {
            'status': 'error',
            'message': 'Search term is required'
        }, 400
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    # Limit page_size to prevent abuse
    page_size = min(page_size, 50)
    
    # Try mock database first
    mock_result = mock_search(name, page=page, page_size=page_size)
    
    if mock_result.get('status') == 'success' and mock_result.get('data', {}).get('count', 0) > 0:
        return mock_result, 200
    
    # Fallback to real OpenFoodFacts API
    client = OpenFoodFactsClient()
    result = client.search_products(name, page=page, page_size=page_size)
    
    status_code = 200
    if result.get('status') == 'error':
        status_code = 500
    
    return result, status_code


@external_bp.route('/search', methods=['GET'])
def search_products_query():
    """Search products by name using OpenFoodFacts or mock database."""
    query = request.args.get('query')
    if not query:
        return {
            'status': 'error',
            'message': 'Query parameter is required'
        }, 400

    # Try mock database first
    mock_results = mock_search(query)

    if mock_results:
        return {
            'status': 'success',
            'data': mock_results
        }, 200

    # Fallback to real OpenFoodFacts API
    client = OpenFoodFactsClient()
    results = client.search_products_by_name(query)

    status_code = 200
    if results.get('status') == 'error':
        status_code = 500
    elif results.get('status') == 'not_found':
        status_code = 404

    return results, status_code