import requests
from database.db_manager import insert_product

# Fake Store API — free public REST API simulating an e-commerce store
API_URL = "https://fakestoreapi.com/products"


def scrape_products():
    """Fetch product listings from Fake Store API and store them in the database."""
    print("🔄 Fetching product data...")
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        products = resp.json()

        for product in products:
            insert_product(
                name=product.get("title", "Unknown"),
                price=product.get("price"),
                currency="USD",
                category=product.get("category"),
                url=f"https://fakestoreapi.com/products/{product.get('id')}"
            )

        print(f"✅ {len(products)} products saved.")
    except requests.RequestException as e:
        print(f"❌ Error fetching products: {e}")


if __name__ == "__main__":
    scrape_products()