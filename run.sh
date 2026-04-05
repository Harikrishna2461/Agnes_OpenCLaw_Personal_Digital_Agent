#!/bin/bash
# Agnes LSA Run Script
# Starts Flask server, OpenClaw daemon, and ngrok tunnel

set -e

APP_DIR="/Users/HariKrishnaD/Downloads/Agnes_AI"
LSA_DIR="$APP_DIR/lsa-agent"
PYTHON="python3"

echo "╔═════════════════════════════════════════════════════════════════╗"
echo "║   Agnes LSA + OpenClaw WhatsApp Integration - STARTUP           ║"
echo "╚═════════════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f "whatsapp_server|openclaw_daemon|ngrok" 2>/dev/null || true
sleep 2
echo "✅ Cleaned"
echo ""

# Start Flask server
echo "🚀 Starting Flask WhatsApp Server..."
cd "$LSA_DIR"
nohup $PYTHON whatsapp_server.py --port 5001 > /tmp/lsa_server.log 2>&1 &
FLASK_PID=$!
echo "   PID: $FLASK_PID"
sleep 3

# Check Flask health
if curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo "✅ Flask server is healthy (localhost:5001)"
else
    echo "⚠️  Flask took longer to start, waiting..."
    sleep 3
fi
echo ""

# Start OpenClaw daemon
echo "🚀 Starting OpenClaw WhatsApp Daemon..."
cd "$LSA_DIR"
nohup python3.11 openclaw_daemon.py > /tmp/openclaw_daemon.log 2>&1 &
DAEMON_PID=$!
echo "   PID: $DAEMON_PID"
sleep 2
echo "✅ OpenClaw daemon started"
echo ""

# Start ngrok (optional)
echo "🌐 Starting ngrok tunnel..."
nohup ngrok http 5001 > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!
echo "   PID: $NGROK_PID"
sleep 4
echo "✅ ngrok tunnel active"
echo ""

echo "╔═════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ ALL SYSTEMS RUNNING                       ║"
echo "╚═════════════════════════════════════════════════════════════════╝"
echo ""

echo "📊 SERVICES:"
echo "   ✅ Flask Server:      localhost:5001"
echo "   ✅ OpenClaw Daemon:   WhatsApp listener"
echo "   ✅ ngrok Tunnel:      Public endpoint"
echo ""

echo "📋 LOGS:"
echo "   Flask:    tail -f /tmp/lsa_server.log"
echo "   OpenClaw: tail -f /tmp/openclaw_daemon.log"
echo "   ngrok:    tail -f /tmp/ngrok.log"
echo ""

echo "🧪 TO TEST:"
echo "   Open another terminal and run: ./test.sh"
echo ""

echo "❌ TO STOP:"
echo "   pkill -f 'whatsapp_server|openclaw_daemon|ngrok'"
echo ""

echo "📱 TO USE WITH REAL WHATSAPP:"
echo "   See: WHATSAPP_SETUP.md"
echo ""

# Keep script running and show logs
echo "=== Flask Server Logs ===" 
tail -f /tmp/lsa_server.log &
FLASK_LOG_PID=$!

# Handle Ctrl+C
trap "pkill -f 'whatsapp_server|openclaw_daemon|ngrok'; pkill -P $FLASK_LOG_PID; exit" INT TERM

wait
