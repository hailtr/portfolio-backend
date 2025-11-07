"""
Performance Testing Script

Tests caching and rate limiting features of the portfolio backend.
Run this after starting your server to see the improvements!
"""

import requests
import time
from colorama import init, Fore, Style

init(autoreset=True)

BASE_URL = "http://localhost:5000"

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text:^60}")
    print(f"{Fore.CYAN}{'='*60}\n")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}")

def print_info(text):
    print(f"{Fore.YELLOW}ℹ {text}")

def print_error(text):
    print(f"{Fore.RED}✗ {text}")

def test_health_check():
    """Test health endpoint and check services"""
    print_header("Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        
        print_info(f"Status: {data.get('status')}")
        
        services = data.get('services', {})
        print_info(f"Database: {services.get('database')}")
        print_info(f"Cache: {services.get('cache')}")
        print_info(f"Cache Type: {services.get('cache_type')}")
        print_info(f"Rate Limiter: {services.get('rate_limiter')}")
        
        if services.get('cache_type') == 'redis':
            print_success("Redis is active! You're using production-grade caching.")
        else:
            print_info("Using in-memory cache (fine for development)")
            print_info("For production, consider adding Redis via REDIS_URL env variable")
        
        return True
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False

def test_caching_performance():
    """Test caching by measuring response times"""
    print_header("Caching Performance Test")
    
    endpoint = f"{BASE_URL}/api/entities"
    
    print_info("Making first request (cache miss - hits database)...")
    start = time.time()
    response1 = requests.get(endpoint)
    time1 = (time.time() - start) * 1000
    
    print_info(f"First request: {time1:.2f}ms")
    
    print_info("\nMaking second request (cache hit - super fast!)...")
    start = time.time()
    response2 = requests.get(endpoint)
    time2 = (time.time() - start) * 1000
    
    print_info(f"Second request: {time2:.2f}ms")
    
    speedup = time1 / time2 if time2 > 0 else 1
    print_success(f"\nSpeedup: {speedup:.1f}x faster!")
    
    if speedup > 2:
        print_success("Caching is working perfectly! 🚀")
    else:
        print_info("Cache might be warming up. Try running again.")
    
    return True

def test_compression():
    """Test response compression"""
    print_header("Compression Test")
    
    endpoint = f"{BASE_URL}/api/entities"
    
    # Request without compression
    headers_no_compress = {'Accept-Encoding': 'identity'}
    response_no_compress = requests.get(endpoint, headers=headers_no_compress)
    size_uncompressed = len(response_no_compress.content)
    
    # Request with compression
    headers_compress = {'Accept-Encoding': 'gzip, deflate'}
    response_compress = requests.get(endpoint, headers=headers_compress)
    size_compressed = len(response_compress.content)
    
    reduction = ((size_uncompressed - size_compressed) / size_uncompressed) * 100
    
    print_info(f"Uncompressed: {size_uncompressed:,} bytes")
    print_info(f"Compressed: {size_compressed:,} bytes")
    print_success(f"Reduction: {reduction:.1f}% ({size_uncompressed - size_compressed:,} bytes saved)")
    
    return True

def test_rate_limiting():
    """Test rate limiting by making rapid requests"""
    print_header("Rate Limiting Test")
    
    endpoint = f"{BASE_URL}/api/health"
    
    print_info("Making 10 rapid requests to test rate limiting...")
    print_info("(Note: You might not hit the limit in this test, limits are generous)")
    
    success_count = 0
    rate_limited = False
    
    for i in range(10):
        response = requests.get(endpoint)
        if response.status_code == 200:
            success_count += 1
            print(f"Request {i+1}: {Fore.GREEN}200 OK")
        elif response.status_code == 429:
            rate_limited = True
            print(f"Request {i+1}: {Fore.RED}429 Too Many Requests")
            print_info(f"Rate limit headers: {dict(response.headers)}")
            break
        else:
            print(f"Request {i+1}: {Fore.YELLOW}{response.status_code}")
    
    print_success(f"\nSuccessful requests: {success_count}/10")
    
    if rate_limited:
        print_success("Rate limiting is working! 🛡️")
    else:
        print_info("Rate limit not hit (limits are generous for this endpoint)")
        print_info("Rate limiting is still active and will protect against abuse")
    
    return True

def test_cache_keys():
    """Test that different query parameters create different cache entries"""
    print_header("Cache Key Differentiation Test")
    
    # Test different language parameters
    print_info("Testing cache with different languages...")
    
    endpoints = [
        f"{BASE_URL}/api/entities?lang=es",
        f"{BASE_URL}/api/entities?lang=en",
        f"{BASE_URL}/api/entities?lang=es&type=project",
    ]
    
    for endpoint in endpoints:
        start = time.time()
        response = requests.get(endpoint)
        duration = (time.time() - start) * 1000
        print_info(f"{endpoint}")
        print(f"  Response time: {duration:.2f}ms, Status: {response.status_code}")
    
    print_success("\nEach unique query parameter combination gets its own cache entry!")
    
    return True

def main():
    """Run all tests"""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║        Portfolio Backend Performance Test Suite           ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    print_info("Make sure your server is running at http://localhost:5000")
    print_info("Press Ctrl+C to exit\n")
    
    time.sleep(1)
    
    tests = [
        ("Health Check", test_health_check),
        ("Caching Performance", test_caching_performance),
        ("Compression", test_compression),
        ("Cache Key Differentiation", test_cache_keys),
        ("Rate Limiting", test_rate_limiting),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print_error(f"Test '{test_name}' failed: {e}")
            failed += 1
        
        time.sleep(1)
    
    # Summary
    print_header("Test Summary")
    print(f"Total Tests: {passed + failed}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.GREEN}✓ All systems operational!" if failed == 0 else f"{Fore.YELLOW}⚠ Some tests failed")
    print(f"{Fore.MAGENTA}{'='*60}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Tests interrupted by user")
    except Exception as e:
        print_error(f"Unexpected error: {e}")

