#!/usr/bin/env python3
"""
Test script to verify connectivity from Selenium container to localhost:3000
"""

import requests
import time
import sys

def test_connectivity():
    """Test if host.docker.internal:3000 is accessible"""
    url = "http://host.docker.internal:3000"
    
    print(f"Testing connectivity to {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✅ SUCCESS! Status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION FAILED: Could not connect to host.docker.internal:3000")
        print("Make sure your development server is running on localhost:3000")
        return False
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Request timed out")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Docker container connectivity to Mac localhost:3000")
    print("=" * 60)
    
    success = test_connectivity()
    
    if not success:
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure your dev server is running: npm start or similar")
        print("2. Check if server binds to 0.0.0.0:3000, not just 127.0.0.1:3000")
        print("3. Verify Docker container is running: docker ps")
        print("4. Test from container: docker exec -it selenium-chrome-97 curl -I http://host.docker.internal:3000")
        sys.exit(1)
    else:
        print("\n🎉 Ready for Selenium testing!")
