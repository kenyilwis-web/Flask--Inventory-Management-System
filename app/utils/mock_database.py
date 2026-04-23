"""Mock database simulating OpenFoodFacts API responses."""
from typing import Dict, List, Optional


# Mock product database with OpenFoodFacts-style data
MOCK_PRODUCTS_DB: List[Dict] = [
    {
        "id": 1,
        "barcode": "1234567890123",
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "quantity": "1L",
            "nutriscore_grade": "A",
            "categories": "Beverages > Plant-based > Almond Milk",
            "image_url": "https://images.openfoodfacts.org/almond-milk.jpg",
            "ingredients_text": "Filtered water, almonds (2%), cane sugar, tricalcium phosphate, sea salt, xanthan gum, carrageenan, vitamin D2, vitamin B12.",
            "nutriments": {
                "energy-kcal": 15,
                "fat": 1.2,
                "carbohydrates": 0.3,
                "proteins": 0.5
            },
            "allergens": "tree nuts",
            "labels": "Organic, Vegan"
        }
    },
    {
        "id": 2,
        "barcode": "2345678901234",
        "status": 1,
        "product": {
            "product_name": "Greek Plain Yogurt",
            "brands": "Fage",
            "quantity": "500g",
            "nutriscore_grade": "A",
            "categories": "Dairy > Yogurt > Greek Yogurt",
            "image_url": "https://images.openfoodfacts.org/greek-yogurt.jpg",
            "ingredients_text": "Milk, cream, milk protein, live bacterial cultures.",
            "nutriments": {
                "energy-kcal": 97,
                "fat": 5.0,
                "carbohydrates": 3.6,
                "proteins": 9.0
            },
            "allergens": "milk",
            "labels": "None"
        }
    },
    {
        "id": 3,
        "barcode": "3456789012345",
        "status": 1,
        "product": {
            "product_name": "Whole Wheat Bread",
            "brands": "Nature's Own",
            "quantity": "600g",
            "nutriscore_grade": "B",
            "categories": "Bakery > Bread > Whole Wheat",
            "image_url": "https://images.openfoodfacts.org/wheat-bread.jpg",
            "ingredients_text": "Whole wheat flour, water, yeast, salt, wheat gluten, soybean oil.",
            "nutriments": {
                "energy-kcal": 247,
                "fat": 3.4,
                "carbohydrates": 41.0,
                "proteins": 10.0
            },
            "allergens": "wheat",
            "labels": "Whole Grain"
        }
    },
    {
        "id": 4,
        "barcode": "4567890123456",
        "status": 1,
        "product": {
            "product_name": "Extra Virgin Olive Oil",
            "brands": "Bertolli",
            "quantity": "500ml",
            "nutriscore_grade": "A",
            "categories": "Oils > Olive Oil",
            "image_url": "https://images.openfoodfacts.org/olive-oil.jpg",
            "ingredients_text": "100% extra virgin olive oil.",
            "nutriments": {
                "energy-kcal": 884,
                "fat": 100.0,
                "carbohydrates": 0.0,
                "proteins": 0.0
            },
            "allergens": "None",
            "labels": "Cold Pressed, Non-GMO"
        }
    },
    {
        "id": 5,
        "barcode": "5678901234567",
        "status": 1,
        "product": {
            "product_name": "Organic Quinoa",
            "brands": "Bob's Red Mill",
            "quantity": "907g",
            "nutriscore_grade": "A",
            "categories": "Grains > Quinoa > Organic",
            "image_url": "https://images.openfoodfacts.org/quinoa.jpg",
            "ingredients_text": "Organic white quinoa.",
            "nutriments": {
                "energy-kcal": 368,
                "fat": 6.0,
                "carbohydrates": 64.0,
                "proteins": 14.0
            },
            "allergens": "None",
            "labels": "Organic, Non-GMO, Kosher"
        }
    },
    {
        "id": 6,
        "barcode": "6789012345678",
        "status": 1,
        "product": {
            "product_name": "Chicken Breast Fillets",
            "brands": "Perdue",
            "quantity": "1lb",
            "nutriscore_grade": "A",
            "categories": "Meat > Poultry > Chicken",
            "image_url": "https://images.openfoodfacts.org/chicken.jpg",
            "ingredients_text": "Chicken breast fillets.",
            "nutriments": {
                "energy-kcal": 165,
                "fat": 3.6,
                "carbohydrates": 0.0,
                "proteins": 31.0
            },
            "allergens": "None",
            "labels": "All Natural, No Antibiotics"
        }
    },
    {
        "id": 7,
        "barcode": "7890123456789",
        "status": 1,
        "product": {
            "product_name": "Atlantic Salmon Fillet",
            "brands": "Wild Catch",
            "quantity": "500g",
            "nutriscore_grade": "B",
            "categories": "Seafood > Salmon",
            "image_url": "https://images.openfoodfacts.org/salmon.jpg",
            "ingredients_text": "Atlantic salmon fillet.",
            "nutriments": {
                "energy-kcal": 208,
                "fat": 13.0,
                "carbohydrates": 0.0,
                "proteins": 20.0
            },
            "allergens": "fish",
            "labels": "Wild Caught"
        }
    },
    {
        "id": 8,
        "barcode": "8901234567890",
        "status": 1,
        "product": {
            "product_name": "Organic Baby Spinach",
            "brands": "Organic Girl",
            "quantity": "142g",
            "nutriscore_grade": "A",
            "categories": "Produce > Leafy Greens > Spinach",
            "image_url": "https://images.openfoodfacts.org/spinach.jpg",
            "ingredients_text": "Organic baby spinach leaves.",
            "nutriments": {
                "energy-kcal": 23,
                "fat": 0.4,
                "carbohydrates": 3.6,
                "proteins": 2.9
            },
            "allergens": "None",
            "labels": "Organic, Triple Washed"
        }
    },
    {
        "id": 9,
        "barcode": "9012345678901",
        "status": 1,
        "product": {
            "product_name": "Honey Raw Organic",
            "brands": "Local Hive",
            "quantity": "340g",
            "nutriscore_grade": "A",
            "categories": "Sweeteners > Honey > Raw",
            "image_url": "https://images.openfoodfacts.org/honey.jpg",
            "ingredients_text": "Raw organic honey.",
            "nutriments": {
                "energy-kcal": 304,
                "fat": 0.0,
                "carbohydrates": 82.0,
                "proteins": 0.3
            },
            "allergens": "None",
            "labels": "Raw, Organic, Local"
        }
    },
    {
        "id": 10,
        "barcode": "0123456789012",
        "status": 1,
        "product": {
            "product_name": "Canned Black Beans",
            "brands": "Goya",
            "quantity": "15.5oz",
            "nutriscore_grade": "A",
            "categories": "Canned Goods > Beans > Black Beans",
            "image_url": "https://images.openfoodfacts.org/black-beans.jpg",
            "ingredients_text": "Black beans, water, salt.",
            "nutriments": {
                "energy-kcal": 132,
                "fat": 0.5,
                "carbohydrates": 24.0,
                "proteins": 9.0
            },
            "allergens": "None",
            "labels": "No Salt Added"
        }
    }
]


def get_product_by_barcode(barcode: str) -> Optional[Dict]:
    """
    Get product by barcode from mock database.
    
    Args:
        barcode: Product barcode to search for
        
    Returns:
        Product dict if found, None otherwise
    """
    for product in MOCK_PRODUCTS_DB:
        if product.get("barcode") == barcode:
            return product
    return None


def search_products_by_name(name: str, page: int = 1, page_size: int = 20) -> Dict:
    """
    Search products by name in mock database.
    
    Args:
        name: Product name to search for
        page: Page number (default: 1)
        page_size: Results per page (default: 20)
        
    Returns:
        Dict with search results
    """
    name_lower = name.lower()
    
    # Filter products that contain the search term
    matching_products = [
        p for p in MOCK_PRODUCTS_DB
        if name_lower in p.get("product", {}).get("product_name", "").lower()
        or name_lower in p.get("product", {}).get("brands", "").lower()
        or name_lower in p.get("product", {}).get("categories", "").lower()
    ]
    
    # Calculate pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_products = matching_products[start_idx:end_idx]
    
    # Format results
    results = []
    for product in paginated_products:
        prod = product.get("product", {})
        results.append({
            "product_name": prod.get("product_name", ""),
            "brands": prod.get("brands", ""),
            "quantity": prod.get("quantity", ""),
            "nutriscore": prod.get("nutriscore_grade", ""),
            "categories": prod.get("categories", ""),
            "image_url": prod.get("image_url", ""),
            "barcode": product.get("barcode", "")
        })
    
    return {
        "status": "success",
        "data": {
            "count": len(matching_products),
            "page": page,
            "products": results
        }
    }


def get_all_products() -> List[Dict]:
    """Return all products from mock database."""
    return MOCK_PRODUCTS_DB