"""Test that protected endpoints return 401 (not 403) when no token is provided"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_protected_endpoint_no_token():
    """Test that protected endpoints return 401 when no token is provided"""
    print("=" * 60)
    print("TEST 1: Protected endpoint WITHOUT token (should return 401)")
    print("=" * 60)
    
    # Test various protected endpoints
    protected_endpoints = [
        '/admin-dashboard/',
        '/professor-dashboard/',
        '/student-dashboard/',
        '/students/',
        '/faculties/',
        '/subjects/',
    ]
    
    for endpoint in protected_endpoints:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTesting: {url}")
        try:
            response = requests.get(url)
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 401:
                print("  ✓ PASS: Returned 401 (Unauthorized)")
            elif response.status_code == 403:
                print("  ✗ FAIL: Returned 403 (Forbidden) - should be 401!")
            else:
                print(f"  ? Unexpected status code: {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def test_allowany_endpoint_no_token():
    """Test that AllowAny endpoints work without token"""
    print("\n" + "=" * 60)
    print("TEST 2: AllowAny endpoints WITHOUT token (should work)")
    print("=" * 60)
    
    allowany_endpoints = [
        ('/login/', 'POST', {'username': 'admin', 'password': 'admin123'}),
        ('/logout/', 'POST', {}),
        ('/renew/', 'POST', {}),
    ]
    
    for endpoint, method, data in allowany_endpoints:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTesting: {method} {url}")
        try:
            if method == 'POST':
                response = requests.post(url, json=data)
            else:
                response = requests.get(url)
            
            print(f"  Status Code: {response.status_code}")
            if response.status_code < 400:
                print("  ✓ PASS: Endpoint works without token")
            else:
                print(f"  ✗ FAIL: Endpoint returned {response.status_code}")
                print(f"  Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def test_protected_endpoint_with_token():
    """Test that protected endpoints work WITH valid token"""
    print("\n" + "=" * 60)
    print("TEST 3: Protected endpoint WITH valid token (should work)")
    print("=" * 60)
    
    # First, login to get a token
    print("\nStep 1: Logging in to get token...")
    login_url = f"{BASE_URL}/login/"
    try:
        login_response = requests.post(
            login_url,
            json={'username': 'admin', 'password': 'admin123'}
        )
        
        if login_response.status_code == 200:
            token = login_response.json().get('access_token')
            print(f"  ✓ Login successful")
            print(f"  Token: {token[:50]}...")
            
            # Now test protected endpoint with token
            print("\nStep 2: Testing protected endpoint with token...")
            dashboard_url = f"{BASE_URL}/admin-dashboard/"
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.get(dashboard_url, headers=headers)
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("  ✓ PASS: Protected endpoint works with valid token")
            else:
                print(f"  ✗ FAIL: Returned {response.status_code}")
                print(f"  Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"  ✗ Login failed: {login_response.status_code}")
            print(f"  Response: {json.dumps(login_response.json(), indent=2)}")
    except Exception as e:
        print(f"  ✗ Error: {e}")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("AUTHENTICATION TEST SUITE")
    print("Testing that protected endpoints return 401 (not 403) without token")
    print("=" * 60)
    
    # Run all tests
    test_protected_endpoint_no_token()
    test_allowany_endpoint_no_token()
    test_protected_endpoint_with_token()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)

