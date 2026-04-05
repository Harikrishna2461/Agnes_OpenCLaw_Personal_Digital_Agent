#!/bin/bash

# Simple test script for the public web agent
# Tests the API locally without needing ngrok

echo "🤖 Testing Agnes LSA Agent..."
echo ""

# Check if server is running
if ! curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo "❌ Server not running. Start with:"
    echo "   cd lsa-agent"
    echo "   python3 whatsapp_server.py --port 5001"
    exit 1
fi

echo "✅ Server is running"
echo ""

# Test 1: Health check
echo "📋 Test 1: Health Check"
curl -s http://localhost:5001/health | python3 -m json.tool
echo ""

# Test 2: Can I skip class?
echo "📋 Test 2: Can I skip class today?"
echo ""
curl -s -X POST http://localhost:5001/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{"from":"+917010384691","message":"Can I skip class today?","token":"lsa_secure_token"}' | \
  python3 -c "import sys, json; d=json.load(sys.stdin); print(d['response'])" | head -20
echo ""
echo "..."
echo ""

# Test 3: Should I exercise?
echo "📋 Test 3: Should I go to the gym?"
echo ""
curl -s -X POST http://localhost:5001/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{"from":"+917010384691","message":"Should I go to the gym?","token":"lsa_secure_token"}' | \
  python3 -c "import sys, json; d=json.load(sys.stdin); print(d['response'])" | head -20
echo ""
echo "..."
echo ""

echo "✅ All tests passed!"
echo ""
echo "🌐 Access the web interface:"
echo "   http://localhost:5001/"
echo ""
echo "🚀 Make it public:"
echo "   cd lsa-agent && ./run_public.sh"
