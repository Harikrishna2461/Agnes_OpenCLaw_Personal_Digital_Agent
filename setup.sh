#!/bin/bash
# Agnes LSA Setup Script
# Installs all dependencies and prepares system

set -e

echo "╔═════════════════════════════════════════════════════════════════╗"
echo "║   AGnes LSA + OpenClaw WhatsApp Integration - SETUP             ║"
echo "╚═════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "🐍 Checking Python installation..."
PYTHON=$(which python3)
if [ -z "$PYTHON" ]; then
    echo "❌ Python3 not found. Install with: brew install python3"
    exit 1
fi
PYTHON_VERSION=$($PYTHON --version)
echo "✅ Found $PYTHON_VERSION"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
$PYTHON -m pip install --upgrade pip setuptools wheel -q
echo "✅ pip upgraded"
echo ""

# Install core dependencies
echo "📥 Installing dependencies..."
PACKAGES=(
    "flask"
    "requests"
    "sentence-transformers"
    "numpy"
    "scikit-learn"
    "faiss-cpu"
    "python-dotenv"
    "colorlog"
    "openclaw"
)

for package in "${PACKAGES[@]}"; do
    echo "   Installing $package..."
    $PYTHON -m pip install -q "$package" || echo "   ⚠️  $package install had issues (may be OK)"
done

echo "✅ Dependencies installed"
echo ""

# Create config directory
echo "📝 Creating configuration..."
mkdir -p ~/.openclaw
cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "whatsapp": {
    "phone_number": "+917010384691",
    "webhook_url": "http://localhost:5001/webhook/whatsapp",
    "webhook_token": "lsa_secure_token",
    "port": 5001
  }
}
EOF
echo "✅ Configuration created at ~/.openclaw/openclaw.json"
echo ""

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x /Users/HariKrishnaD/Downloads/Agnes_AI/run.sh
chmod +x /Users/HariKrishnaD/Downloads/Agnes_AI/test.sh
echo "✅ Scripts ready"
echo ""

echo "╔═════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SETUP COMPLETE                           ║"
echo "╚═════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next steps:"
echo ""
echo "1️⃣  Start the system:"
echo "   ./run.sh"
echo ""
echo "2️⃣  In another terminal, run tests:"
echo "   ./test.sh"
echo ""
echo "3️⃣  For WhatsApp integration:"
echo "   cat WHATSAPP_SETUP.md"
echo ""
