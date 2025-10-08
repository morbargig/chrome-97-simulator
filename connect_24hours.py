#!/usr/bin/env python3
"""
Connect Chrome 97 to your frontend app for 24 hours with robust session management
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import sys
import datetime

def create_chrome_options():
    """Create robust Chrome options"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1400,900')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return options

def connect_with_retry(frontend_url, max_retries=3):
    """Connect to Chrome with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"🔄 Connection attempt {attempt + 1}/{max_retries}...")
            
            options = create_chrome_options()
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                options=options
            )
            
            # Remove automation indicators
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"📱 Navigating to {frontend_url}...")
            driver.get(frontend_url)
            
            # Wait for page to load
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            title = driver.title
            print(f"✅ Connected! Page title: {title}")
            return driver
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("⏳ Waiting 5 seconds before retry...")
                time.sleep(5)
            else:
                print("💥 All connection attempts failed!")
                return None

def keep_session_alive(driver, frontend_url):
    """Keep the session alive by periodically refreshing"""
    try:
        # Check if session is still alive
        current_url = driver.current_url
        
        # If we're not on the right page, navigate back
        if "host.docker.internal:3000" not in current_url:
            print(f"🔄 Navigating back to frontend...")
            driver.get(frontend_url)
            
        # Execute a simple JavaScript to keep session active
        driver.execute_script("return document.title;")
        return True
        
    except WebDriverException as e:
        print(f"⚠️  Session lost: {e}")
        return False

def connect_for_24_hours(port=3000):
    """Connect Chrome 97 to your frontend app for 24 hours with auto-recovery"""
    
    frontend_url = f"http://host.docker.internal:{port}"
    start_time = datetime.datetime.now()
    
    print(f"🚀 Starting 24-HOUR Chrome 97 session...")
    print(f"📍 URL: {frontend_url}")
    print(f"🖥️ Watch in noVNC: http://localhost:7900")
    print(f"⏰ Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    driver = None
    total_seconds = 24 * 60 * 60  # 24 hours
    reconnect_count = 0
    
    try:
        # Initial connection
        driver = connect_with_retry(frontend_url)
        if not driver:
            print("❌ Failed to establish initial connection!")
            return
        
        print("\n🎮 Chrome 97 is now connected to your frontend!")
        print("🖥️ Go to http://localhost:7900 to interact with it")
        print("⌨️ Features:")
        print("   • Auto-reconnection if session drops")
        print("   • Session keep-alive every 2 minutes")
        print("   • 24-hour runtime with monitoring")
        print("   • Full interaction capability")
        print("\n⏰ Chrome will run for 24 HOURS...")
        print("   Press Ctrl+C to stop early")
        print("=" * 60)
        
        # Main loop - run for 24 hours
        for i in range(total_seconds):
            time.sleep(1)
            
            # Keep session alive every 2 minutes
            if i % 120 == 0 and i > 0:
                if not keep_session_alive(driver, frontend_url):
                    print(f"🔄 Attempting to reconnect... (Reconnect #{reconnect_count + 1})")
                    
                    # Close old driver if it exists
                    try:
                        driver.quit()
                    except:
                        pass
                    
                    # Reconnect
                    driver = connect_with_retry(frontend_url)
                    if driver:
                        reconnect_count += 1
                        print(f"✅ Reconnected successfully! (Total reconnects: {reconnect_count})")
                    else:
                        print("💥 Failed to reconnect! Stopping...")
                        break
            
            # Status update every 30 minutes
            if i % 1800 == 0 and i > 0:
                elapsed_hours = i // 3600
                elapsed_minutes = (i % 3600) // 60
                remaining_hours = (total_seconds - i) // 3600
                remaining_minutes = ((total_seconds - i) % 3600) // 60
                
                current_time = datetime.datetime.now()
                try:
                    current_url = driver.current_url if driver else "No active session"
                    print(f"📊 {current_time.strftime('%H:%M:%S')} | Running: {elapsed_hours}h {elapsed_minutes}m | Remaining: {remaining_hours}h {remaining_minutes}m | Reconnects: {reconnect_count}")
                    print(f"📍 Current URL: {current_url}")
                except:
                    print(f"📊 {current_time.strftime('%H:%M:%S')} | Running: {elapsed_hours}h {elapsed_minutes}m | Session check failed")
        
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        print(f"\n🎉 24-HOUR SESSION COMPLETED!")
        print(f"⏰ Total runtime: {duration}")
        print(f"🔄 Total reconnections: {reconnect_count}")
        
    except KeyboardInterrupt:
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        print(f"\n🛑 Session stopped by user")
        print(f"⏰ Runtime: {duration}")
        print(f"🔄 Total reconnections: {reconnect_count}")
        
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        
    finally:
        if driver:
            try:
                driver.quit()
                print("🔚 Browser session closed")
            except:
                print("🔚 Browser session cleanup completed")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    connect_for_24_hours(port)
