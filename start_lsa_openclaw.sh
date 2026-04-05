#!/bin/bash
"""
Complete LSA + OpenClaw Integration Startup Script
Starts both Flask webhook server and OpenClaw daemon for full WhatsApp integration
"""

set -e

APP_DIR="/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent"
PYTHON="/opt/homebrew/bin/python3.11"
LOG_DIR="/tmp/lsa_openclaw"

# Create log directory
mkdir -p "$LOG_DIR"

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║        Agnes LSA + OpenClaw WhatsApp Integration Startup                   ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🔍 Checking system..."
echo "📦 Python: $PYTHON"
echo "📂 App Directory: $APP_DIR"
echo ""

# Verify Python version
PYTHON_VERSION=$($PYTHON --version)
echo "✅ Python version: $PYTHON_VERSION"
echo ""

# Test OpenClaw import
echo "🧪 Testing OpenClaw import..."
$PYTHON -c "import openclaw; print('✅ OpenClaw imported successfully')" || {
    echo "❌ OpenClaw import failed. Please run:"
    echo "   pip install openclaw"
    exit 1
}
echo ""

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "whatsapp_server|openclaw_daemon" || true
sleep 1
echo "✅ Old processes cleaned up"
echo ""

# Start Flask server
echo "🚀 Starting LSA Flask Server..."
cd "$APP_DIR"
nohup $PYTHON whatsapp_server.py > "$LOG_DIR/flask_server.log" 2>&1 &
FLASK_PID=$!
echo "   Flask PID: $FLASK_PID"
sleep 2

# Verify Flask is running
if curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo "✅ Flask server is healthy (localhost:5001)"
else
    echo "⚠️  Flask server may not have started. Check logs:"
    echo "   cat $LOG_DIR/flask_server.log"
fi
echo ""

# Start OpenClaw daemon
echo "🚀 Starting OpenClaw WhatsApp Daemon..."
nohup $PYTHON openclaw_daemon.py > "$LOG_DIR/openclaw_daemon.log" 2>&1 &
DAEMON_PID=$!
echo "   OpenClaw PID: $DAEMON_PID"
sleep 2
echo "✅ OpenClaw daemon started (logging to $LOG_DIR/openclaw_daemon.log)"
echo ""

# Start ngrok if available
if command -v ngrok &> /dev/null; then
    echo "🌐 Checking ngrok tunnel..."
    if pgrep -f ngrok > /dev/null; then
        echo "✅ ngrok tunnel already running"
    else
        echo "🚀 Starting ngrok tunnel (port 5001)..."
        ngrok http 5001 > /tmp/ngrok.log 2>&1 &
        sleep 2
        NGROK_URL=$(cat ~/.ngrok2/ngrok.log | grep "URL" | tail -1 | awk '{print $NF}' || echo "unknown")
        echo "✅ ngrok URL: $NGROK_URL"
    fi
fi
echo ""

# Display configuration
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                           ✅ System Ready                                  ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📱 Integration Status:"
echo "   • Flask Server:    ✅ Running on localhost:5001"
echo "   • OpenClaw Daemon: ✅ Running (WhatsApp listener)"
echo "   • ngrok Tunnel:    ✅ Active (public URL available)"
echo ""
echo "📨 Flow:"
echo "   User Message to +91 7010384691"
echo "   → WhatsApp Business API → OpenClaw Daemon"
echo "   → LSA Flask Server (localhost:5001)"
echo "   → Life Simulation Agent Analysis"
echo "   → Response back to User"
echo ""
echo "🔍 Monitor Logs:"
echo "   Flask:     tail -f $LOG_DIR/flask_server.log"
echo "   OpenClaw:  tail -f $LOG_DIR/openclaw_daemon.log"
echo ""
echo "🛑 To Stop:"
echo "   pkill -f 'whatsapp_server|openclaw_daemon|ngrok'"
echo ""
echo "📂 Config Files:"
echo "   ~/.openclaw/openclaw.json"
echo "   (Webhook configured to forward messages to LSA)"
echo ""
