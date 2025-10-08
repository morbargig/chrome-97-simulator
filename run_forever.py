#!/usr/bin/env python3
"""
INFINITE Chrome 97 session - Runs FOREVER with bulletproof recovery!
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import datetime
import sys
import signal
import os

class ForeverChrome:
    def __init__(self, port=3000):
        self.port = port
        self.frontend_url = f"http://host.docker.internal:{port}"
        self.driver = None
        self.start_time = datetime.datetime.now()
        self.reconnect_count = 0
        self.total_uptime = 0
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received shutdown signal ({signum})")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def create_chrome_options(self):
        """Create bulletproof Chrome options"""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1600,1000')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-background-networking')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Keep browser alive
        options.add_argument('--keep-alive-for-test')
        options.add_argument('--disable-hang-monitor')
        
        return options
    
    def connect_with_retry(self, max_retries=10):
        """Connect to Chrome with aggressive retry logic"""
        for attempt in range(max_retries):
            try:
                print(f"🔄 Connection attempt {attempt + 1}/{max_retries}...")
                
                options = self.create_chrome_options()
                self.driver = webdriver.Remote(
                    command_executor="http://localhost:4444/wd/hub",
                    options=options
                )
                
                # Configure timeouts
                self.driver.implicitly_wait(10)
                self.driver.set_page_load_timeout(30)
                self.driver.set_script_timeout(30)
                
                # Remove automation indicators
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                print(f"📱 Navigating to {self.frontend_url}...")
                self.driver.get(self.frontend_url)
                
                # Wait for page to load
                WebDriverWait(self.driver, 30).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                
                title = self.driver.title
                print(f"✅ Connected! Page title: {title}")
                return True
                
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.driver = None
                
                if attempt < max_retries - 1:
                    wait_time = min(30, (attempt + 1) * 5)  # Progressive backoff
                    print(f"⏳ Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print("💥 All connection attempts failed!")
                    return False
        
        return False
    
    def keep_session_alive(self):
        """Advanced session keep-alive with health checks"""
        try:
            # Multi-level health check
            
            # 1. Check if driver exists
            if not self.driver:
                return False
            
            # 2. Check session ID
            session_id = self.driver.session_id
            if not session_id:
                return False
            
            # 3. Check current URL
            current_url = self.driver.current_url
            if not current_url or "data:" in current_url:
                print(f"🔄 Invalid URL detected: {current_url}")
                self.driver.get(self.frontend_url)
                time.sleep(2)
            
            # 4. Execute JavaScript to keep session active
            result = self.driver.execute_script("""
                // Keep session alive
                try {
                    // Touch the DOM
                    document.title = document.title;
                    
                    // Keep network active
                    if (window.fetch) {
                        fetch(window.location.href, {method: 'HEAD'}).catch(() => {});
                    }
                    
                    // Return health status
                    return {
                        url: window.location.href,
                        title: document.title,
                        readyState: document.readyState,
                        timestamp: Date.now()
                    };
                } catch (e) {
                    return {error: e.toString()};
                }
            """)
            
            if result and 'error' not in result:
                return True
            else:
                print(f"⚠️  JavaScript health check failed: {result}")
                return False
                
        except WebDriverException as e:
            print(f"⚠️  Session health check failed: {e}")
            return False
        except Exception as e:
            print(f"⚠️  Unexpected error in health check: {e}")
            return False
    
    def restart_container_if_needed(self):
        """Restart Selenium container if it's unresponsive"""
        try:
            print("🔄 Checking Selenium container status...")
            result = os.system("docker-compose ps selenium-chrome | grep -q 'Up'")
            
            if result != 0:
                print("🚨 Container is down! Restarting...")
                os.system("docker-compose restart selenium-chrome")
                time.sleep(15)  # Wait for container to be ready
                return True
            
            # Check if WebDriver endpoint is responsive
            import requests
            try:
                response = requests.get("http://localhost:4444/wd/hub/status", timeout=10)
                if response.status_code != 200:
                    print("🚨 WebDriver not responsive! Restarting container...")
                    os.system("docker-compose restart selenium-chrome")
                    time.sleep(15)
                    return True
            except:
                print("🚨 WebDriver endpoint unreachable! Restarting container...")
                os.system("docker-compose restart selenium-chrome")
                time.sleep(15)
                return True
                
        except Exception as e:
            print(f"⚠️  Container check failed: {e}")
        
        return False
    
    def run_forever(self):
        """Main infinite loop - RUNS FOREVER!"""
        
        print("🚀 STARTING INFINITE CHROME 97 SESSION!")
        print("=" * 60)
        print(f"📍 URL: {self.frontend_url}")
        print(f"🖥️ Watch in noVNC: http://localhost:7900")
        print(f"⏰ Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔄 Will run FOREVER until manually stopped!")
        print("=" * 60)
        
        # Initial connection
        if not self.connect_with_retry():
            print("💥 Failed to establish initial connection!")
            return
        
        print("\n🎮 Chrome 97 is now connected FOREVER!")
        print("🖥️ Go to http://localhost:7900 to interact with it")
        print("⌨️ Features:")
        print("   • INFINITE runtime - never stops!")
        print("   • Auto-reconnection every 30 seconds")
        print("   • Container restart on failure")
        print("   • Progressive retry backoff")
        print("   • Advanced health monitoring")
        print("   • Bulletproof error recovery")
        print("\n🛑 Press Ctrl+C to stop (only way to stop!)")
        print("=" * 60)
        
        loop_count = 0
        last_health_check = time.time()
        last_status_report = time.time()
        
        # INFINITE LOOP - RUNS FOREVER!
        while self.running:
            try:
                loop_count += 1
                current_time = time.time()
                
                # Health check every 30 seconds
                if current_time - last_health_check >= 30:
                    if not self.keep_session_alive():
                        print(f"🚨 Health check failed! Attempting recovery...")
                        
                        # Try to reconnect
                        if self.driver:
                            try:
                                self.driver.quit()
                            except:
                                pass
                            self.driver = None
                        
                        # Check if container needs restart
                        self.restart_container_if_needed()
                        
                        # Reconnect
                        if self.connect_with_retry():
                            self.reconnect_count += 1
                            print(f"✅ Recovered successfully! (Recovery #{self.reconnect_count})")
                        else:
                            print("💥 Recovery failed! Trying container restart...")
                            self.restart_container_if_needed()
                            if self.connect_with_retry():
                                self.reconnect_count += 1
                                print(f"✅ Recovered after container restart! (Recovery #{self.reconnect_count})")
                    
                    last_health_check = current_time
                
                # Status report every 10 minutes
                if current_time - last_status_report >= 600:
                    uptime = datetime.datetime.now() - self.start_time
                    hours = int(uptime.total_seconds() // 3600)
                    minutes = int((uptime.total_seconds() % 3600) // 60)
                    
                    try:
                        current_url = self.driver.current_url if self.driver else "No active session"
                        session_id = self.driver.session_id if self.driver else "None"
                    except:
                        current_url = "Session error"
                        session_id = "None"
                    
                    print(f"📊 FOREVER SESSION STATUS:")
                    print(f"   ⏰ Uptime: {hours}h {minutes}m")
                    print(f"   🔄 Recoveries: {self.reconnect_count}")
                    print(f"   🔗 Session ID: {session_id}")
                    print(f"   📍 URL: {current_url}")
                    print(f"   🔢 Loop: {loop_count}")
                    
                    last_status_report = current_time
                
                # Sleep for 1 second
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping infinite session...")
                self.running = False
                break
                
            except Exception as e:
                print(f"💥 Unexpected error in main loop: {e}")
                print("🔄 Continuing anyway (FOREVER mode!)...")
                time.sleep(5)
        
        # Final cleanup
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        end_time = datetime.datetime.now()
        total_runtime = end_time - self.start_time
        
        print(f"\n🏁 INFINITE SESSION ENDED")
        print(f"⏰ Total runtime: {total_runtime}")
        print(f"🔄 Total recoveries: {self.reconnect_count}")
        
        if self.driver:
            try:
                self.driver.quit()
                print("🔚 Browser session closed")
            except:
                print("🔚 Browser session cleanup completed")

def main():
    """Main function"""
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    
    print("🌟 CHROME 97 FOREVER MODE")
    print("=" * 40)
    print("⚠️  WARNING: This will run FOREVER!")
    print("🛑 Only way to stop: Ctrl+C")
    print("=" * 40)
    
    forever_chrome = ForeverChrome(port)
    forever_chrome.run_forever()

if __name__ == "__main__":
    main()

