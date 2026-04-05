#!/usr/bin/env python3
"""
Configure OpenClaw webhook to forward WhatsApp messages to LSA.
Tries multiple API endpoints automatically.
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AGNES_CLAW_API_KEY")
WEBHOOK_URL = "https://haleigh-extramundane-triatomically.ngrok-free.dev/webhook/whatsapp"
PHONE_NUMBER = "+917010384691"

if not API_KEY:
    print("❌ AGNES_CLAW_API_KEY not in .env")
    exit(1)

print(f"\n📝 Configuring OpenClaw webhook...")
print(f"📱 Phone: {PHONE_NUMBER}")
print(f"🌐 Webhook: {WEBHOOK_URL}")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Try different API endpoints
endpoints = [
    "https://api.agnesai.com/v1/webhooks/configure",
    "https://api.openclaw.ai/v1/webhooks/configure",
    "https://api.openclaw.ai/webhooks/configure",
    "https://api.openclaw.ai/integrations/whatsapp/webhook",
]

payload = {
    "phone_number": PHONE_NUMBER,
    "webhook_url": WEBHOOK_URL,
    "webhook_events": ["message.received"],
    "webhook_active": True,
    "channel": "whatsapp",
}

success = False
for endpoint in endpoints:
    try:
        print(f"\n🔄 Trying: {endpoint}")
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=5,
            verify=False  # Skip SSL verification as workaround
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Webhook configured successfully!")
            print(f"Status: {response.json()}")
            print(f"\n🎉 Your WhatsApp webhook is LIVE!")
            print(f"Send a message to +91 7010384691 and LSA will respond.")
            success = True
            break
        else:
            print(f"   Response: {response.status_code}")
    except Exception as e:
        print(f"   Error: {str(e)[:60]}")

if not success:
    print(f"\n⚠️  None of the API endpoints worked.")
    print(f"\n📋 MANUAL SETUP REQUIRED (one-time only):")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\nGo to OpenClaw/Agnes console and set webhook to:")
    print(f"  {WEBHOOK_URL}")
    print(f"\nOR if no webhook option in console:")
    print(f"  - Copy your ngrok URL above")
    print(f"  - Contact OpenClaw support with:")
    print(f"    Phone: {PHONE_NUMBER}")
    print(f"    Webhook: {WEBHOOK_URL}")
    print(f"\n🎯 Once configured, send a WhatsApp to +91 7010384691")
    print(f"   and LSA will respond automatically.")
