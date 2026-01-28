import sys
import time
from scripts.api_client import ApiClient

client = ApiClient()

def request(method, endpoint, data=None):
    return client.request(method, endpoint, data)

def seed():
    print("🌱 Seeding Santhe Data...")
    
    # 1. Categories
    category_names = ["Vegetables", "Fruits", "Grains", "Dairy", "Spices", "Snacks"]
    categories = {}

    print("\n📦 Categories:")
    for name in category_names:
        # Try create
        request("POST", "/categories", {"name": name})
    
    # Fetch all to build map (idempotent way to get IDs)
    all_cats = request("GET", "/categories")
    if all_cats:
        for cat in all_cats:
            categories[cat['name']] = cat['id']
            print(f" - {cat['name']} (ID: {cat['id']})")
    
    if not categories:
        print("❌ Failed to fetch categories. Is the service running?")
        sys.exit(1)

    # 2. Products
    products = [
        ("Fresh Tomato", "Organic locally grown", 40, "Vegetables"),
        ("Potato", "High quality potatoes", 30, "Vegetables"),
        ("Onion", "Red onions (1kg)", 25, "Vegetables"),
        ("Carrot", "Ooty Carrots", 60, "Vegetables"),
        ("Spinach", "Fresh Palak Bunch", 15, "Vegetables"),
        
        ("Apple", "Kashmir Apples (1kg)", 180, "Fruits"),
        ("Banana", "Yellaki Banana (1kg)", 60, "Fruits"),
        ("Mango", "Alphonso Mango (1 dozen)", 800, "Fruits"),
        ("Papaya", "Semi-ripe Papaya", 45, "Fruits"),
        
        ("Rice", "Sona Masoori Premium (5kg)", 350, "Grains"),
        ("Wheat Flour", "Whole Wheat Atta (5kg)", 220, "Grains"),
        ("Toor Dal", "Organic Toor Dal (1kg)", 140, "Grains"),
        
        ("Milk", "Fresh Cow Milk (1L)", 35, "Dairy"),
        ("Curd", "Homemade style Curd (500g)", 40, "Dairy"),
        ("Ghee", "Pure Desi Ghee (500ml)", 450, "Dairy"),
        
        ("Turmeric Powder", "Organic Haldi (100g)", 40, "Spices"),
        ("Chilli Powder", "Guntur Chilli Powder (100g)", 35, "Spices"),
        ("Black Pepper", "Kerala Pepper (50g)", 80, "Spices")
    ]

    print("\n🥕 Products:")
    for name, desc, price, cat_name in products:
        cat_id = categories.get(cat_name)
        if cat_id:
            # Check if exists
            safe_name = urllib.parse.quote(name)
            existing = request("GET", f"/products/search?name={safe_name}")
            
            if existing and len(existing) > 0:
                 # Check for exact match just in case search is fuzzy
                 # (Assuming search returns list of products)
                 exact_match = any(p['name'] == name for p in existing)
                 if exact_match:
                     print(f" - ⏩ Skipping {name}, already exists")
                     continue

            res = request("POST", "/products", {
                "name": name,
                "description": desc,
                "price": price,
                "category_id": cat_id
            })
            if res:
                print(f" - ✅ Added: {name}")
        else:
            print(f" - ⚠️  Skipping {name}, category {cat_name} not found")

    print("\n✅ Seeding Complete!")

if __name__ == "__main__":
    seed()
