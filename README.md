# 🌐 Chrome 97 Simulator

A comprehensive Docker-based Chrome 97 testing environment that allows you to test your web applications in an older Chrome version. Perfect for compatibility testing, legacy browser support validation, and ensuring your applications work across different Chrome versions.

## ✨ Features

- **🐳 Dockerized Chrome 97**: Isolated Chrome 97 environment using Selenium
- **🖥️ Visual Access**: noVNC desktop for real-time browser interaction
- **🔗 Localhost Access**: Seamless connection to your local development servers
- **⚡ Multiple Connection Modes**: Quick connect, timed sessions, and infinite runtime
- **🛠️ Developer Tools**: Built-in connectivity testing and debugging utilities
- **📱 Multi-Port Support**: Connect to any local port (3000, 4200, 5173, 8080, etc.)
- **🔄 Auto-Recovery**: Bulletproof session management with automatic reconnection

## 🚀 Quick Start

### 1. Prerequisites

- Docker and Docker Compose installed
- Your web application running locally
- Node.js (for JavaScript tests) or Python 3.7+ (for Python tests)

### 2. Start Chrome 97 Container

```bash
# Clone the repository
git clone https://github.com/morbargig/chrome-97-simulator.git
cd chrome-97-simulator

# Start the Chrome 97 container
docker-compose up -d

# Verify it's running
docker-compose ps
```

### 3. Connect to Your App

#### Option A: Interactive Connection (Recommended)
```bash
# Connect to your frontend (will prompt for port)
python3 connect_to_frontend.py

# Or specify port directly
python3 connect_to_frontend.py 3000
```

#### Option B: Using npm scripts
```bash
# Install dependencies
npm install

# Connect to different ports
npm run connect:3000    # React, Next.js
npm run connect:4200    # Angular
npm run connect:5173    # Vite
npm run connect:8080    # Vue.js
```

#### Option C: Infinite Session (Never Stops)
```bash
# Run forever with auto-recovery
python3 run_forever.py 3000
```

### 4. Access Your Browser

- **🖥️ Visual Desktop**: http://localhost:7900 (no password required)
- **🔧 WebDriver API**: http://localhost:4444
- **📊 Container Status**: `docker-compose ps`

## 📋 Available Scripts

### Python Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `connect_to_frontend.py` | Interactive connection to your app | `python3 connect_to_frontend.py [port]` |
| `run_forever.py` | Infinite session with auto-recovery | `python3 run_forever.py [port]` |
| `connect_24hours.py` | 24-hour continuous session | `python3 connect_24hours.py [port]` |
| `connect_2hours.py` | 2-hour timed session | `python3 connect_2hours.py [port]` |
| `selenium_test.py` | Basic Selenium functionality test | `python3 selenium_test.py` |
| `test_connectivity.py` | Test connection to localhost | `python3 test_connectivity.py` |
| `test_server.py` | Simple test server for demos | `python3 test_server.py` |

### npm Scripts

```bash
npm run start:container    # Start Docker container
npm run stop:container     # Stop Docker container
npm run logs              # View container logs
npm run status            # Check container status
npm run test              # Run JavaScript Selenium test
npm run test:python       # Run Python Selenium test
npm run test:connectivity # Test localhost connectivity
npm run test:curl         # Test with curl
```

## 🔧 Configuration

### Docker Compose Settings

The `docker-compose.yml` includes optimized settings for Chrome 97:

```yaml
services:
  selenium-chrome:
    image: selenium/standalone-chrome:97.0
    platform: linux/amd64
    ports:
      - "4444:4444"  # WebDriver
      - "7900:7900"  # noVNC
    environment:
      - SE_VNC_NO_PASSWORD=1
      - SE_SCREEN_WIDTH=1920
      - SE_SCREEN_HEIGHT=1080
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

### Frontend Server Requirements

Your development server must be accessible from Docker:

#### ✅ Correct Configuration

```bash
# Next.js
npx next dev -H 0.0.0.0

# Create React App
HOST=0.0.0.0 npm start

# Vite
npm run dev -- --host 0.0.0.0

# Express.js
app.listen(3000, '0.0.0.0', () => {
  console.log('Server running on 0.0.0.0:3000');
});
```

#### ❌ Won't Work

```bash
# These bind only to localhost/127.0.0.1
npm start                    # Default CRA
npx next dev                # Default Next.js
npm run dev                 # Default Vite
```

## 🧪 Testing Your Application

### Basic Compatibility Test

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=options
)

driver.get("http://host.docker.internal:3000")
print(f"Page title: {driver.title}")
driver.quit()
```

### Advanced Testing Features

- **Screenshots**: Capture visual state at any point
- **Element Interaction**: Click, type, scroll, hover
- **JavaScript Execution**: Run custom scripts in Chrome 97
- **Network Monitoring**: Check requests and responses
- **Performance Testing**: Measure load times and rendering

## 🛠️ Troubleshooting

### Container Issues

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs selenium-chrome

# Restart container
docker-compose restart selenium-chrome

# Complete reset
docker-compose down && docker-compose up -d
```

### Connection Issues

1. **Can't reach localhost**: Ensure your server binds to `0.0.0.0`, not `127.0.0.1`
2. **WebDriver not responding**: Check if container is running with `docker-compose ps`
3. **noVNC not loading**: Wait 30 seconds after starting container
4. **Port conflicts**: Make sure ports 4444 and 7900 are available

### Common Solutions

```bash
# Test connectivity from your Mac
curl -I http://localhost:3000

# Test from inside container
docker exec selenium-chrome-97 curl -I http://host.docker.internal:3000

# Check firewall (macOS)
sudo pfctl -sr | grep 3000
```

## 📁 Project Structure

```
chrome-97-simulator/
├── 🐳 docker-compose.yml          # Container configuration
├── 🐍 connect_to_frontend.py      # Main connection script
├── ♾️  run_forever.py              # Infinite session runner
├── ⏰ connect_24hours.py          # 24-hour session
├── ⏰ connect_2hours.py           # 2-hour session
├── 🧪 selenium_test.py            # Basic Selenium test
├── 🔗 test_connectivity.py        # Connection tester
├── 🌐 test_server.py              # Simple test server
├── 📜 test_curl.sh                # Shell connectivity test
├── 📦 package.json                # Node.js dependencies
├── 🐍 requirements.txt            # Python dependencies
└── 📖 README.md                   # This file
```

## 🎯 Use Cases

### Development & Testing
- **Legacy Browser Support**: Test your modern app in Chrome 97
- **Regression Testing**: Ensure new features don't break in older browsers
- **CSS Compatibility**: Validate CSS Grid, Flexbox, and modern features
- **JavaScript Compatibility**: Test ES6+ features and polyfills

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Test in Chrome 97
  run: |
    docker-compose up -d
    python3 selenium_test.py
    docker-compose down
```

### Educational & Training
- **Browser Evolution**: Show differences between Chrome versions
- **Compatibility Workshops**: Hands-on legacy browser testing
- **Selenium Training**: Learn automation in a controlled environment

## 🔄 Session Management

### Quick Session (10 minutes)
```bash
python3 connect_to_frontend.py 3000
```

### Extended Sessions
```bash
python3 connect_2hours.py 3000      # 2 hours
python3 connect_24hours.py 3000     # 24 hours
```

### Infinite Session (Recommended for development)
```bash
python3 run_forever.py 3000
```

Features of infinite session:
- ♾️ Runs until manually stopped
- 🔄 Auto-reconnection on failures
- 🐳 Container restart on crashes
- 📊 Regular status reports
- 🛡️ Bulletproof error recovery

## 🌟 Advanced Features

### Custom Chrome Options
```python
options = Options()
options.add_argument('--window-size=1600,1000')
options.add_argument('--disable-web-security')
options.add_argument('--allow-running-insecure-content')
```

### Multi-Viewport Testing
```python
viewports = [
    {'width': 375, 'height': 667},   # Mobile
    {'width': 768, 'height': 1024},  # Tablet
    {'width': 1920, 'height': 1080}  # Desktop
]

for viewport in viewports:
    driver.set_window_size(viewport['width'], viewport['height'])
    # Test your responsive design
```

### Performance Monitoring
```python
# Measure page load time
start_time = time.time()
driver.get("http://host.docker.internal:3000")
load_time = time.time() - start_time
print(f"Page loaded in {load_time:.2f} seconds")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/morbargig/chrome-97-simulator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/morbargig/chrome-97-simulator/discussions)
- **Documentation**: This README and inline code comments

## 🙏 Acknowledgments

- [Selenium](https://selenium.dev/) - Web automation framework
- [Docker](https://docker.com/) - Containerization platform
- [Chrome 97](https://chromereleases.googleblog.com/) - The browser version we're simulating
- [noVNC](https://novnc.com/) - Browser-based VNC client

---

**⭐ Star this repository if it helps you test your applications in Chrome 97!**