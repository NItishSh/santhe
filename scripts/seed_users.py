import urllib.request
import urllib.error
import json
import time
import random

BASE_URL = "http://localhost:8080/api"
OUTPUT_FILE = "test_users_data.json"

roles = ["farmer", "middleman", "admin"]
first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan"]
last_names = ["Patel", "Sharma", "Singh", "Kumar", "Gupta", "Rao", "Reddy", "Nair", "Iyer", "Verma"]

users_created = []

print(f"Starting seed of 10 users...")

def make_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    if data:
        data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status >= 200 and response.status < 300:
                resp_data = response.read().decode("utf-8")
                return json.loads(resp_data) if resp_data else {}
            else:
                print(f"Request failed: {response.status} {response.read().decode('utf-8')}")
                return None
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

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
