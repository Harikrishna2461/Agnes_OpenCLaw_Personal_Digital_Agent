#!/bin/bash
# WhatsApp Integration Quick Setup Script

echo "🤖 LSA WhatsApp Integration Setup"
echo "=================================="
echo ""

# Install dependencies
echo "📦 Installing Twilio and Flask..."
pip install twilio flask

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env template..."
    cat > .env << EOF
# Twilio WhatsApp Credentials
# Sign up: https://www.twilio.com/whatsapp
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_USER_NUMBER=whatsapp:+917010384691

# API Configuration
AGNES_CLAW_API_KEY=sk-ai-v1-673c5930e56cff44d63d9f9ddca38aa4169ec44f3194cfd2a253e86d1ee132df
EOF
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  NEXT STEPS:"
    echo "1. Go to https://www.twilio.com/whatsapp"
    echo "2. Create account and get credentials"
    echo "3. Add TWILIO_ACCOUNT_SID to .env"
    echo "4. Add TWILIO_AUTH_TOKEN to .env"
    echo ""
    echo "Then run: python3 whatsapp_daemon.py"
else
    echo "✅ .env file exists"
fi

echo ""
echo "🚀 READY TO USE!"
echo ""
echo "Run WhatsApp daemon:"
echo "  python3 whatsapp_daemon.py"
echo ""
echo "Or test manually:"
echo "  python3 -c 'from whatsapp_daemon import LSAWhatsAppDaemon; print(\"WhatsApp ready!\")'‌"
