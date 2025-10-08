#!/usr/bin/env python3
"""
Selenium test script to access localhost:3000 from Docker container
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def create_chrome_options():
    """Create Chrome options for Docker environment"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    return options

def test_localhost_access():
    """Test accessing localhost:3000 from Selenium container"""
    print("🚀 Starting Selenium test...")
    
    # WebDriver configuration
    webdriver_url = "http://localhost:4444/wd/hub"
    target_url = "http://host.docker.internal:3000"
    
    driver = None
    try:
        # Create Chrome options
        chrome_options = create_chrome_options()
        
        # Connect to remote WebDriver
        print(f"Connecting to WebDriver at {webdriver_url}...")
        driver = webdriver.Remote(
            command_executor=webdriver_url,
            options=chrome_options
        )
        
        print(f"Navigating to {target_url}...")
        driver.get(target_url)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Get page title
        title = driver.title
        print(f"✅ Page loaded successfully!")
        print(f"Page title: {title}")
        
        # Take a screenshot
        screenshot_path = "/tmp/selenium_test_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Try to find some common elements
        try:
            # Look for common HTML elements
            body = driver.find_element(By.TAG_NAME, "body")
            print(f"Body content length: {len(body.text)} characters")
        except Exception as e:
            print(f"Could not find body element: {e}")
        
        print("✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()
            print("WebDriver session closed")

def main():
    print("🔍 Selenium Test: Accessing localhost:3000 from Docker container")
    print("=" * 70)
    
    # Check if WebDriver is accessible
    try:
        import requests
        response = requests.get("http://localhost:4444/wd/hub/status", timeout=5)
        if response.status_code == 200:
            print("✅ WebDriver is running and accessible")
        else:
            print("❌ WebDriver is not responding properly")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to WebDriver: {e}")
        print("Make sure Docker container is running: docker-compose up -d")
        sys.exit(1)
    
    # Run the test
    success = test_localhost_access()
    
    if success:
        print("\n🎉 SUCCESS! Your setup is working correctly!")
        print("You can now run Selenium tests against your localhost:3000 service.")
    else:
        print("\n💡 Troubleshooting:")
        print("1. Ensure your dev server is running on localhost:3000")
        print("2. Check Docker container: docker-compose ps")
        print("3. View container logs: docker-compose logs selenium-chrome")
        print("4. Access noVNC desktop: http://localhost:7900")
        sys.exit(1)

if __name__ == "__main__":
    main()
