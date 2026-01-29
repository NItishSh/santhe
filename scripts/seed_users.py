import time
import random
import json
import os
import sys

# Add parent dir to path to allow import "from scripts.api_client"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.api_client import ApiClient


client = ApiClient()

BASE_URL = "http://localhost:8080/api"
OUTPUT_FILE = "test_users_data.json"
users_created = []
roles = ["farmer", "middleman"]
first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"]
last_names = ["Doe", "Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis", "Rodriguez"]

def make_request(url, method="GET", data=None, headers=None):
    # Strip base URL if present since client adds it
    endpoint = url.replace(BASE_URL, "")
    return client.request(method, endpoint, data, headers)

for i in range(10):
    role = random.choice(roles)
    first_name = first_names[i]
    last_name = last_names[i]
    username = f"{first_name.lower()}{i}"
    email = f"{username}@example.com"
    password = "password123"
    phone = f"98765432{i:02d}"
    dob = f"199{i}-01-01"
    
    user_payload = {
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone,
        "address": f"{random.randint(1, 999)} Farm Rd, Village {i}",
        "date_of_birth": dob,
        "payment_method_token": f"upi-{username}@okaxis"
    }

    print(f"Registering {username}...")
    # Register
    reg_resp = make_request(f"{BASE_URL}/users/register", "POST", user_payload)
    if reg_resp:
        print(f"  Success: {username}")
        
        # Login
        login_resp = make_request(f"{BASE_URL}/auth/login", "POST", {"username": username, "password": password})
        if login_resp and "access_token" in login_resp:
            token = login_resp["access_token"]
            
            # Fetch me
            me_resp = make_request(f"{BASE_URL}/users/me", "GET", headers={"Authorization": f"Bearer {token}"})
            if me_resp:
                users_created.append({
                    "username": username,
                    "password": password,
                    "email": email,
                    "role": role,
                    "token": token,
                    "profile": me_resp
                })
            else:
                 print(f"  Failed to fetch profile")
        else:
             print(f"  Failed to login")

    time.sleep(0.5)

print(f"Finished. Writing {len(users_created)} users to {OUTPUT_FILE}")
with open(OUTPUT_FILE, "w") as f:
    json.dump(users_created, f, indent=2)
