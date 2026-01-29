import pytest
from playwright.sync_api import Page, expect
import requests
import time
import random

BASE_URL = "http://localhost:8080"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="function")
def test_user():
    """Creates a unique test user and returns credentials."""
    unique_id = int(time.time() * 1000)
    username = f"testuser_{unique_id}"
    email = f"test_{unique_id}@example.com"
    password = "password123"
    
    # Register via API
    resp = requests.post(f"{BASE_URL}/api/users/register", json={
        "username": username,
        "email": email,
        "password": password,
        "role": "middleman"
    })
    if resp.status_code != 201:
        print(f"Registration Error: {resp.text}")
    resp.raise_for_status()

    return {
        "username": username,
        "email": email,
        "password": password
    }

@pytest.fixture(scope="function")
def auth_page(page: Page, base_url, test_user):
    """Logs in the test user and returns the authenticated page."""
    # Login via UI
    page.goto(f"{base_url}/login")
    page.fill("#email", test_user["username"])
    page.fill("#password", test_user["password"])
    page.click("button[type='submit']")
    
    # Wait for redirect to home
    expect(page).to_have_url(f"{base_url}/")
    
    return page
