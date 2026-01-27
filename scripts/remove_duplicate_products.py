import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8080/api"

def request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    
    if data:
        body = json.dumps(data).encode('utf-8')
        req.data = body

    try:
        with urllib.request.urlopen(req) as response:
            if response.status >= 200 and response.status < 300:
                if response.status != 204 and response.read: 
                    # read() can only be called once, handle empty
                    # For delete, usually no content, but let's see
                    return True 
                return {}
    except urllib.error.HTTPError as e:
        print(f"Request failed: {e.code} {e.reason} for {url}")
        return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def get_all_products():
    # Use search with no params to get all
    url = f"{BASE_URL}/products/search"
    req = urllib.request.Request(url, method="GET")
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Failed to fetch products: {e}")
        return []

def cleanup():
    print("🧹 Cleaning up duplicate products...")
    products = get_all_products()
    
    if not products:
        print("No products found.")
        return

    name_map = {}
    duplicates = 0
    
    for p in products:
        name = p['name']
        if name not in name_map:
            name_map[name] = []
        name_map[name].append(p['id'])

    for name, ids in name_map.items():
        if len(ids) > 1:
            print(f"Duplicate found: {name} (IDs: {ids})")
            # Keep the first one (lowest ID usually), delete others
            ids.sort()
            to_keep = ids[0]
            to_delete = ids[1:]
            
            for pid in to_delete:
                print(f" - Deleting ID {pid}...")
                request("DELETE", f"/products/{pid}")
                duplicates += 1
    
    if duplicates == 0:
        print("✅ No duplicates found.")
    else:
        print(f"✅ Removed {duplicates} duplicate entries.")

if __name__ == "__main__":
    cleanup()
