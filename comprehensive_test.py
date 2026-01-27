#!/usr/bin/env python3
import urllib.request
import json
import time

time.sleep(3)

print("=" * 60)
print("COMPREHENSIVE API TESTS")
print("=" * 60)

tests = [
    ("GET", "/", None, "Frontend/Root"),
    ("GET", "/docs", None, "Swagger Docs"),
    ("GET", "/api/tasks/", None, "Get Tasks (no auth)"),
    ("POST", "/api/auth/register", {"email": "alice@test.com", "password": "password123"}, "Register User"),
]

results = []

for method, path, data, description in tests:
    try:
        url = f"http://localhost:6969{path}"
        
        if data:
            data_json = json.dumps(data).encode()
            req = urllib.request.Request(url, data=data_json, headers={'Content-Type': 'application/json'}, method=method)
        else:
            req = urllib.request.Request(url, method=method)
        
        response = urllib.request.urlopen(req, timeout=5)
        status = response.status
        print(f"\n✅ {description}")
        print(f"   Method: {method} {path}")
        print(f"   Status: {status}")
        
        if method == "POST":
            result = json.loads(response.read().decode())
            print(f"   Response: {json.dumps(result, indent=2)[:200]}")
        
        results.append((description, True, status))
    except urllib.error.HTTPError as e:
        status = e.code
        print(f"\n❌ {description}")
        print(f"   Method: {method} {path}")
        print(f"   Status: {status}")
        try:
            error_data = json.loads(e.read().decode())
            print(f"   Error: {error_data.get('detail', error_data)}")
        except:
            pass
        results.append((description, False, status))
    except Exception as e:
        print(f"\n❌ {description}")
        print(f"   Error: {e}")
        results.append((description, False, str(e)))

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
passed = sum(1 for _, success, _ in results if success)
print(f"Passed: {passed}/{len(results)}")
for desc, success, status in results:
    icon = "✅" if success else "❌"
    print(f"{icon} {desc}: {status}")
