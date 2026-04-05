#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║         🤖 Agnes LSA - Public Web Agent                    ║
║    Accessible from your mobile anywhere in the world        ║
╚════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${YELLOW}ℹ️  ngrok not found. Installing...${NC}"
    brew install ngrok 2>/dev/null || {
        echo -e "${RED}❌ Please install ngrok: brew install ngrok${NC}"
        exit 1
    }
fi

# Kill old processes
echo -e "${YELLOW}🧹 Cleaning up old processes...${NC}"
pkill -f "whatsapp_server.py" 2>/dev/null
sleep 1

# Start the Flask server
echo -e "${BLUE}🚀 Starting LSA Agent Server...${NC}"
cd "$(dirname "$0")" || exit
python3 whatsapp_server.py --port 5001 > /tmp/lsa_agent.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server is running
if ! ps -p $SERVER_PID > /dev/null; then
    echo -e "${RED}❌ Server failed to start. Check logs:${NC}"
    cat /tmp/lsa_agent.log
    exit 1
fi

echo -e "${GREEN}✅ Server running on port 5001${NC}"

# Start ngrok tunnel
echo -e "${YELLOW}🌐 Starting ngrok tunnel...${NC}"
echo -e "${YELLOW}(Keep this terminal open - it shows your public URL)${NC}"
echo ""

# Show tunnel info in a nice format
sleep 2
ngrok http 5001 --log=stdout | grep -E "^t=|url=|started tunnel" &
NGROK_PID=$!

# Wait for ngrok to connect
sleep 3

# Get the public URL
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data['tunnels'] else 'error')" 2>/dev/null)

if [ "$PUBLIC_URL" != "error" ] && [ -n "$PUBLIC_URL" ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║            ✅ YOUR AGENT IS LIVE AND PUBLIC! ✅             ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}📱 Access from your phone/mobile:${NC}"
    echo -e "${GREEN}  $PUBLIC_URL${NC}"
    echo ""
    echo -e "${YELLOW}ℹ️  How to use:${NC}"
    echo "   1. Open the URL above in your mobile browser"
    echo "   2. Ask Agnes any decision question"
    echo "   3. Get instant LSA analysis with multiple scenarios"
    echo ""
    echo -e "${YELLOW}ℹ️  This URL stays active for 2 hours${NC}"
    echo "   (Restart this script to get a new URL)"
    echo ""
    echo -e "${YELLOW}📋 Test locally on this machine:${NC}"
    echo "   http://localhost:5001/"
    echo ""
else
    echo -e "${YELLOW}⏳ Waiting for ngrok to initialize...${NC}"
    sleep 2
fi

# Keep processes running and show logs
trap "pkill -f 'ngrok http'; pkill -f 'whatsapp_server.py'; exit" INT TERM

echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server and ngrok tunnel${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

wait $NGROK_PID
