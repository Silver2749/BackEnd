import urllib.request
import json
import time

time.sleep(1)  # Wait for server

print("Testing Task Management API")
print("=" * 50)

# Test 1: Frontend
print("\n1. Frontend (GET /):")
try:
    response = urllib.request.urlopen('http://localhost:6969/', timeout=5)
    print(f"   Status: {response.status}")
    print(f"   ✅ Frontend loads")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Docs
print("\n2. API Docs (GET /docs):")
try:
    response = urllib.request.urlopen('http://localhost:6969/docs', timeout=5)
    print(f"   Status: {response.status}")
    print(f"   ✅ Docs available")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Register
print("\n3. Register (POST /api/auth/register):")
try:
    data = json.dumps({"email": "test@example.com", "password": "password123"}).encode()
    req = urllib.request.Request(
        'http://localhost:6969/api/auth/register',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    response = urllib.request.urlopen(req, timeout=5)
    result = json.loads(response.read().decode())
    print(f"   Status: {response.status}")
    print(f"   ✅ Registration successful")
    print(f"   User ID: {result.get('id')}")
except urllib.error.HTTPError as e:
    print(f"   ❌ HTTP {e.code}: {e.reason}")
    try:
        error_data = json.loads(e.read().decode())
        print(f"   Error: {error_data.get('detail')}")
    except:
        pass
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Login
print("\n4. Login (POST /api/auth/login):")
try:
    data = json.dumps({"email": "test@example.com", "password": "password123"}).encode()
    req = urllib.request.Request(
        'http://localhost:6969/api/auth/login',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    response = urllib.request.urlopen(req, timeout=5)
    result = json.loads(response.read().decode())
    print(f"   Status: {response.status}")
    print(f"   ✅ Login successful")
    print(f"   Token: {result.get('access_token', '')[:20]}...")
except urllib.error.HTTPError as e:
    print(f"   ❌ HTTP {e.code}: {e.reason}")
    try:
        error_data = json.loads(e.read().decode())
        print(f"   Error: {error_data.get('detail')}")
    except:
        pass
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("Testing complete!")
