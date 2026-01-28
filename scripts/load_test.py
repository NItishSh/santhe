#!/usr/bin/env python3
"""
Load test script to stress microservices and measure resource usage.
Generates concurrent requests to key endpoints across all services.
"""
import asyncio
import aiohttp
import time
import random
from datetime import datetime

BASE_URL = "http://localhost:8080"

# Endpoints to test per service category
ENDPOINTS = {
    "user-service": [
        ("GET", "/api/users/me", None),
        ("POST", "/api/auth/login", {"username": "aarav0", "password": "Password@123"}),
    ],
    "product-catalog": [
        ("GET", "/api/categories", None),
        ("GET", "/api/products/search", None),
        ("GET", "/api/products/1", None),
    ],
    "cart": [
        ("GET", "/api/cart", None),
    ],
    "pricing": [
        ("GET", "/api/pricing/products/1", None),
    ],
}

# Headers for authenticated requests
async def get_auth_token(session):
    """Get auth token for authenticated endpoints."""
    try:
        async with session.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "aarav0", "password": "Password@123"}
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("access_token")
    except Exception:
        pass
    return None


async def make_request(session, method, url, data=None, headers=None):
    """Make single request and return timing."""
    start = time.monotonic()
    try:
        if method == "GET":
            async with session.get(url, headers=headers) as resp:
                await resp.read()
                return resp.status, time.monotonic() - start
        else:
            async with session.post(url, json=data, headers=headers) as resp:
                await resp.read()
                return resp.status, time.monotonic() - start
    except Exception as e:
        return 0, time.monotonic() - start


async def run_load_test(duration_seconds=60, concurrency=20):
    """Run load test for specified duration with given concurrency."""
    print(f"🔥 Starting load test: {duration_seconds}s duration, {concurrency} concurrent workers")
    print(f"   Target: {BASE_URL}")
    print()
    
    # All endpoints to hit
    endpoints_flat = []
    for service, eps in ENDPOINTS.items():
        for method, path, data in eps:
            endpoints_flat.append((service, method, path, data))
    
    stats = {
        "total": 0,
        "success": 0,
        "errors": 0,
        "latencies": [],
        "per_service": {}
    }
    
    start_time = time.monotonic()
    
    async with aiohttp.ClientSession() as session:
        # Get auth token first
        token = await get_auth_token(session)
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        async def worker():
            while time.monotonic() - start_time < duration_seconds:
                service, method, path, data = random.choice(endpoints_flat)
                url = f"{BASE_URL}{path}"
                
                status, latency = await make_request(session, method, url, data, headers)
                
                stats["total"] += 1
                if 200 <= status < 400:
                    stats["success"] += 1
                else:
                    stats["errors"] += 1
                stats["latencies"].append(latency)
                
                if service not in stats["per_service"]:
                    stats["per_service"][service] = {"count": 0, "latencies": []}
                stats["per_service"][service]["count"] += 1
                stats["per_service"][service]["latencies"].append(latency)
                
                await asyncio.sleep(0.01)  # Small delay between requests
        
        # Run concurrent workers
        workers = [worker() for _ in range(concurrency)]
        await asyncio.gather(*workers)
    
    # Calculate stats
    elapsed = time.monotonic() - start_time
    rps = stats["total"] / elapsed if elapsed > 0 else 0
    
    print("=" * 60)
    print(f"📊 LOAD TEST RESULTS")
    print("=" * 60)
    print(f"Duration: {elapsed:.1f}s")
    print(f"Total Requests: {stats['total']}")
    print(f"Success: {stats['success']} ({stats['success']/stats['total']*100:.1f}%)")
    print(f"Errors: {stats['errors']}")
    print(f"Requests/sec: {rps:.1f}")
    
    if stats["latencies"]:
        lats = sorted(stats["latencies"])
        print(f"\nLatency (ms):")
        print(f"  p50: {lats[len(lats)//2]*1000:.1f}")
        print(f"  p95: {lats[int(len(lats)*0.95)]*1000:.1f}")
        print(f"  p99: {lats[int(len(lats)*0.99)]*1000:.1f}")
    
    print(f"\nPer Service:")
    for service, sdata in stats["per_service"].items():
        slats = sorted(sdata["latencies"])
        p50 = slats[len(slats)//2]*1000 if slats else 0
        print(f"  {service}: {sdata['count']} reqs, p50={p50:.1f}ms")
    
    print("\n✅ Load test complete! Run 'kubectl top pods -n santhe' to see resource usage.")


if __name__ == "__main__":
    asyncio.run(run_load_test(duration_seconds=60, concurrency=20))
