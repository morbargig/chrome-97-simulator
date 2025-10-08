#!/usr/bin/env python3
"""
Connect Chrome 97 to your frontend app for 2 hours
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def connect_for_2_hours(port=3000):
    """Connect Chrome 97 to your frontend app for 2 hours"""
    
    frontend_url = f"http://host.docker.internal:{port}"
    
    print(f"🚀 Connecting Chrome 97 to your frontend for 2 HOURS...")
    print(f"📍 URL: {frontend_url}")
    print(f"🖥️ Watch in noVNC: http://localhost:7900")
    print("=" * 60)
    
    # Chrome options for better interaction
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1400,900')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        print("🌐 Opening Chrome 97...")
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options
        )
        
        # Remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"📱 Navigating to {frontend_url}...")
        driver.get(frontend_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        title = driver.title
        print(f"✅ Connected! Page title: {title}")
        
        print("\n🎮 Chrome 97 is now connected to your frontend!")
        print("🖥️ Go to http://localhost:7900 to interact with it")
        print("⌨️ You can:")
        print("   • Click buttons and links")
        print("   • Fill forms")
        print("   • Navigate around your app")
        print("   • Test all functionality")
        print("\n⏰ Chrome will stay open for 2 HOURS (7200 seconds)...")
        print("   Press Ctrl+C to close early")
        
        # Keep browser open for 2 hours
        total_seconds = 7200  # 2 hours
        try:
            for i in range(total_seconds):
                time.sleep(1)
                if i % 300 == 0 and i > 0:  # Every 5 minutes
                    current_url = driver.current_url
                    minutes_elapsed = i // 60
                    minutes_remaining = (total_seconds - i) // 60
                    print(f"⏱️  {minutes_elapsed}min elapsed, {minutes_remaining}min remaining | URL: {current_url}")
        except KeyboardInterrupt:
            print("\n🛑 Closing browser early...")
        
        print(f"\n⏰ 2 hours completed! Closing browser...")
        return driver
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print(f"1. Make sure your frontend is running on localhost:{port}")
        print(f"2. Test from Mac: curl -I http://localhost:{port}")
        print("3. Ensure your app binds to 0.0.0.0, not just 127.0.0.1")
        return None
        
    finally:
        if driver:
            driver.quit()
            print("🔚 Browser closed")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    connect_for_2_hours(port)
