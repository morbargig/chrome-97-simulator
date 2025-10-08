#!/usr/bin/env python3
"""
Simple test server for testing Selenium container connectivity
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import threading
import time

class TestRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Server - Chrome 97 Selenium</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #4CAF50; }
                .status { background: #4CAF50; color: white; padding: 10px; border-radius: 5px; margin: 20px 0; }
                .info { background: #2196F3; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; }
                .code { background: #f5f5f5; padding: 10px; border-left: 4px solid #4CAF50; margin: 10px 0; font-family: monospace; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎉 Test Server Running Successfully!</h1>
                <div class="status">✅ Chrome 97 Selenium container can reach your Mac's localhost:3000</div>
                
                <h2>Connection Details:</h2>
                <div class="info">Server: localhost:3000 (Mac)</div>
                <div class="info">Container Access: host.docker.internal:3000</div>
                <div class="info">WebDriver: http://localhost:4444</div>
                <div class="info">noVNC Desktop: http://localhost:7900</div>
                
                <h2>Test Elements for Selenium:</h2>
                <div id="test-element">This is a test element</div>
                <button id="test-button" onclick="alert('Button clicked!')">Test Button</button>
                <input id="test-input" type="text" placeholder="Test input field" />
                
                <h2>Next Steps:</h2>
                <div class="code">
                    # Run Python Selenium test:<br>
                    python3 selenium_test.py<br><br>
                    # Or Node.js test:<br>
                    npm install && npm test
                </div>
                
                <p><strong>Time:</strong> """ + time.strftime('%Y-%m-%d %H:%M:%S') + """</p>
            </div>
            
            <script>
                // Add some JavaScript for testing
                document.getElementById('test-button').addEventListener('click', function() {
                    console.log('Test button clicked at ' + new Date());
                });
            </script>
        </body>
        </html>
        """
        
        self.wfile.write(html_content.encode())

def start_server():
    """Start the test server"""
    server_address = ('0.0.0.0', 3000)  # Bind to all interfaces
    httpd = HTTPServer(server_address, TestRequestHandler)
    
    print("🚀 Starting test server...")
    print(f"📍 Server running at: http://localhost:3000")
    print(f"🐳 Container can access via: http://host.docker.internal:3000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    start_server()
