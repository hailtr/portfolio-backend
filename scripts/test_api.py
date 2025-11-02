#!/usr/bin/env python
"""
Quick API test script.

Tests all API endpoints to verify they work correctly.

Usage:
    python test_api.py
"""

import requests
import sys

# API base URL
BASE_URL = "http://localhost:5000/api"

def test_endpoint(name, url, expected_status=200):
    """Test a single endpoint."""
    try:
        print(f"Testing {name}...", end=" ")
        response = requests.get(url, timeout=5)
        
        if response.status_code == expected_status:
            print(f"{response.status_code}")
            return True, response.json()
        else:
            print(f" Expected {expected_status}, got {response.status_code}")
            return False, None
    except requests.exceptions.ConnectionError:
        print(" Connection failed - is the server running?")
        return False, None
    except Exception as e:
        print(f" Error: {e}")
        return False, None

def main():
    print("=" * 60)
    print("  API ENDPOINT TESTS")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print()
    
    all_passed = True
    
    # Test health check
    success, data = test_endpoint(
        "Health Check",
        f"{BASE_URL}/health"
    )
    all_passed = all_passed and success
    
    # Test get all entities
    success, data = test_endpoint(
        "Get All Entities (ES)",
        f"{BASE_URL}/entities?lang=es"
    )
    all_passed = all_passed and success
    if success and data:
        print(f"   Found {len(data)} entities:")
        for entity in data:
            print(f"     - {entity.get('slug')} ({entity.get('type')}) - {entity.get('title')}")
    
    # Test get all entities (EN)
    success, data = test_endpoint(
        "Get All Entities (EN)",
        f"{BASE_URL}/entities?lang=en"
    )
    all_passed = all_passed and success
    
    # Test get single entity (if we have data)
    success, entities = test_endpoint(
        "Get Entities for slug test",
        f"{BASE_URL}/entities?lang=es"
    )
    
    if success and entities and len(entities) > 0:
        slug = entities[0].get('slug')
        success, data = test_endpoint(
            f"Get Entity by Slug ({slug})",
            f"{BASE_URL}/entities/{slug}?lang=es"
        )
        all_passed = all_passed and success
    else:
        print("Skipping slug test - no entities in database")
    
    # Test languages endpoint
    success, data = test_endpoint(
        "Get Available Languages",
        f"{BASE_URL}/languages"
    )
    all_passed = all_passed and success
    if success and data:
        print(f"   Available: {data.get('languages', [])}")
    
    # Test categories endpoint
    success, data = test_endpoint(
        "Get Categories",
        f"{BASE_URL}/categories"
    )
    all_passed = all_passed and success
    
    # Test tags endpoint
    success, data = test_endpoint(
        "Get Tags",
        f"{BASE_URL}/tags"
    )
    all_passed = all_passed and success
    
    print()
    print("=" * 60)
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed. Check output above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

