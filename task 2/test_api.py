"""Test the login API directly"""
import urllib.request
import json

# Test login API
url = 'http://localhost:8000/api/login/'
data = json.dumps({'username': 'admin', 'password': 'admin123'}).encode('utf-8')

print("Testing login API...")
print(f"URL: {url}")
print(f"Data: {data.decode()}")

try:
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"\nStatus: {response.status}")
        print(f"Response: {json.dumps(result, indent=2)}")
except Exception as e:
    print(f"\nError: {e}")
    try:
        print(f"Error response: {e.read().decode()}")
    except:
        pass
