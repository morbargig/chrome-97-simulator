#!/usr/bin/env python3
"""
Connect Chrome 97 to your frontend app running on any port
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def connect_to_frontend(port=3000, keep_open=True):
    """Connect Chrome 97 to your frontend app"""
    
    frontend_url = f"http://host.docker.internal:{port}"
    
    print(f"🚀 Connecting Chrome 97 to your frontend app...")
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
        
        if keep_open:
            print("\n🎮 Chrome 97 is now connected to your frontend!")
            print("🖥️ Go to http://localhost:7900 to interact with it")
            print("⌨️ You can:")
            print("   • Click buttons and links")
            print("   • Fill forms")
            print("   • Navigate around your app")
            print("   • Test all functionality")
            print("\n⏰ Chrome will stay open for 10 minutes...")
            print("   Press Ctrl+C to close early")
            
            # Keep browser open for interaction
            try:
                for i in range(600):  # 10 minutes
                    time.sleep(1)
                    if i % 30 == 0:  # Every 30 seconds
                        current_url = driver.current_url
                        print(f"📍 Current URL: {current_url}")
            except KeyboardInterrupt:
                print("\n🛑 Closing browser...")
        
        return driver
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print(f"1. Make sure your frontend is running on localhost:{port}")
        print(f"2. Test from Mac: curl -I http://localhost:{port}")
        print("3. Ensure your app binds to 0.0.0.0, not just 127.0.0.1")
        return None
        
    finally:
        if driver and not keep_open:
            driver.quit()
            print("🔚 Browser closed")

def main():
    """Main function with port selection"""
    print("🎯 Chrome 97 Frontend Connector")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number")
            sys.exit(1)
    else:
        print("📝 Enter the port your frontend is running on:")
        print("   • React (Create React App): usually 3000")
        print("   • Next.js: usually 3000")
        print("   • Vue.js: usually 8080")
        print("   • Angular: usually 4200")
        print("   • Vite: usually 5173")
        print("   • Custom: any port")
        
        try:
            port = int(input("\n🔢 Port number: "))
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input or cancelled")
            sys.exit(1)
    
    print(f"\n🚀 Connecting to localhost:{port}...")
    driver = connect_to_frontend(port)
    
    if not driver:
        sys.exit(1)

if __name__ == "__main__":
    main()


