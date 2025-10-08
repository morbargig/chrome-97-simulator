#!/bin/bash
# Test connectivity from Docker container to Mac localhost:3000

echo "🔍 Testing Docker container connectivity to Mac localhost:3000"
echo "=============================================================="

# Check if container is running
if ! docker ps | grep -q selenium-chrome-97; then
    echo "❌ Container 'selenium-chrome-97' is not running!"
    echo "Start it with: docker-compose up -d"
    exit 1
fi

echo "✅ Container is running"

# Test basic connectivity
echo "Testing basic connectivity..."
if docker exec selenium-chrome-97 curl -s -I http://host.docker.internal:3000 > /dev/null 2>&1; then
    echo "✅ SUCCESS! Can reach host.docker.internal:3000"
    
    # Get detailed response
    echo ""
    echo "📋 Response details:"
    docker exec selenium-chrome-97 curl -s -I http://host.docker.internal:3000
    
    # Test with a full request
    echo ""
    echo "📋 Full response (first 200 chars):"
    docker exec selenium-chrome-97 curl -s http://host.docker.internal:3000 | head -c 200
    echo ""
    
else
    echo "❌ FAILED! Cannot reach host.docker.internal:3000"
    echo ""
    echo "💡 Troubleshooting steps:"
    echo "1. Make sure your development server is running on localhost:3000"
    echo "2. Check if your server binds to 0.0.0.0:3000 (not just 127.0.0.1:3000)"
    echo "3. Test from your Mac: curl -I http://localhost:3000"
    echo "4. Check container logs: docker-compose logs selenium-chrome"
    echo "5. Access noVNC desktop: http://localhost:7900"
    exit 1
fi

echo ""
echo "🎉 Ready for Selenium testing!"
