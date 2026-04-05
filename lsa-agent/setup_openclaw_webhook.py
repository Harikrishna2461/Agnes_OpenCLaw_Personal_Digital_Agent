#!/usr/bin/env python3
"""
Configure OpenClaw webhook for WhatsApp in ~/.openclaw/openclaw.json
Automatically sets up hooks block with token and mappings.
"""

import os
import json
import secrets
from pathlib import Path

# Paths
HOME = os.path.expanduser("~")
OPENCLAW_DIR = Path(HOME) / ".openclaw"
CONFIG_FILE = OPENCLAW_DIR / "openclaw.json"
NGROK_URL = "https://haleigh-extramundane-triatomically.ngrok-free.dev"
TOKEN = secrets.token_urlsafe(32)

print("""\
╔════════════════════════════════════════════════════════════╗
║    Configure OpenClaw Webhook for WhatsApp (LSA)          ║
╚════════════════════════════════════════════════════════════╝
""")

# Create .openclaw directory if it doesn't exist
OPENCLAW_DIR.mkdir(exist_ok=True)
print(f"📁 OpenClaw dir: {OPENCLAW_DIR}")

# Load or create config
if CONFIG_FILE.exists():
    print(f"📖 Loading existing config: {CONFIG_FILE}")
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
else:
    print(f"📝 Creating new config: {CONFIG_FILE}")
    config = {}

# Configure hooks
config["hooks"] = {
    "enabled": True,
    "token": TOKEN,
    "path": "/hooks"
}

# Add WhatsApp mapping
config["hooks"]["mappings"] = [
    {
        "id": "whatsapp-lsa",
        "match": {"path": "/whatsapp"},
        "action": "agent",
        "messageTemplate": "WhatsApp from {{body.from}}: {{body.message}}",
        "forward_to": f"{NGROK_URL}/webhook/whatsapp"
    }
]

# Save config
with open(CONFIG_FILE, 'w') as f:
    json.dump(config, f, indent=2)

print(f"""
✅ OpenClaw webhook configured!

📋 Configuration Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 Token: {TOKEN}
🌐 Webhook Path: /hooks/whatsapp
📍 Local: http://localhost:18789/hooks/whatsapp
🌍 Public (ngrok): {NGROK_URL}/whatsapp

📝 Config saved to: {CONFIG_FILE}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 NEXT STEPS:

1. Start OpenClaw gateway:
   openclaw serve

2. Verify hooks are active:
   openclaw hooks list

3. Check it's working:
   curl -H "Authorization: Bearer {TOKEN}" \\
        http://localhost:18789/hooks/whatsapp

4. Send WhatsApp message to +91 7010384691
   LSA will respond!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# Show the config
print(f"\n📄 Config file content:")
print(json.dumps(config, indent=2))
