# WhatsApp Integration Setup Guide

## Overview

Your Agnes LSA system is ready to receive real WhatsApp messages. This guide explains how to connect it to WhatsApp Business API.

## Current Status

✅ **Terminal Testing**: Working perfectly (run `./test.sh`)  
⏳ **WhatsApp Integration**: Needs WhatsApp Business Account setup

## How It Will Work (End-to-End)

```
User texts +91 7010384691
   ↓
WhatsApp Business API receives message
   ↓
Webhook forwards to ngrok public URL
   ↓
ngrok tunnels to localhost:5001
   ↓
Flask server processes message
   ↓
LSA analyzes decision, generates 3 scenarios
   ↓
Response sent back through same path
   ↓
User receives full analysis on WhatsApp
```

## Setup Steps

### Step 1: Get WhatsApp Business Account

1. Go to: https://www.meta.com/en/business/tools/whatsapp-business/
2. Sign up for WhatsApp Business Account
3. Verify your phone number (+91 7010384691)
4. Create Business Profile

### Step 2: Create WhatsApp Business App

1. Go to: https://developers.facebook.com
2. Create a new App (or use existing)
3. Select "WhatsApp" product
4. Get your **Business Account ID** and **API Token**

### Step 3: Configure Webhook

1. In Facebook Developer Dashboard:
   - Go to Settings → Webhooks
   - Add Webhook URL: **YOUR_NGROK_URL/webhook/whatsapp**
   
2. To get your ngrok URL:
   ```bash
   curl http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print([t['public_url'] for t in data.get('tunnels', [])])"
   ```

3. Set Webhook Token: `lsa_secure_token`

4. Subscribe to message events:
   - Click "Subscribe to events"
   - Select: `messages`
   - Save

### Step 4: Update Configuration

Edit `~/.openclaw/openclaw.json`:

```json
{
  "whatsapp": {
    "phone_number": "+917010384691",
    "webhook_url": "http://localhost:5001/webhook/whatsapp",
    "webhook_token": "lsa_secure_token",
    "port": 5001,
    "business_account_id": "YOUR_BUSINESS_ACCOUNT_ID",
    "api_token": "YOUR_API_TOKEN",
    "phone_number_id": "YOUR_PHONE_NUMBER_ID"
  }
}
```

### Step 5: Update Flask Server

Edit `lsa-agent/whatsapp_server.py` to use real WhatsApp API:

```python
# Add near the top of LSAWhatsAppServer class:
self.business_account_id = os.getenv("BUSINESS_ACCOUNT_ID")
self.api_token = os.getenv("API_TOKEN")
self.phone_number_id = os.getenv("PHONE_NUMBER_ID")
self.api_version = "v18.0"
self.base_url = f"https://graph.instagram.com/{self.api_version}"
```

Replace the `send_message` method to use real API:

```python
def send_message(self, to_number: str, message_text: str) -> bool:
    """Send message via WhatsApp Business API."""
    try:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number.replace("+", ""),
            "type": "text",
            "text": {"body": message_text}
        }
        
        response = requests.post(
            f"{self.base_url}/{self.phone_number_id}/messages",
            json=payload,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            logger.info(f"✅ Message sent to {to_number}")
            return True
        else:
            logger.error(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Send error: {e}")
        return False
```

### Step 6: Test with Real WhatsApp

1. Keep `./run.sh` running
2. Open WhatsApp on your phone
3. Start a chat with your WhatsApp Business number
4. Send: "Can I skip class today?"
5. Wait for response with full LSA analysis

## Environment Variables (Optional)

Create `.env` file in lsa-agent directory:

```bash
WHATSAPP_PHONE=+917010384691
WHATSAPP_BUSINESS_ACCOUNT_ID=your_id
WHATSAPP_API_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WEBHOOK_TOKEN=lsa_secure_token
```

Then update `whatsapp_server.py` to load from `.env`:

```python
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv("WHATSAPP_API_TOKEN")
business_account_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
```

## Troubleshooting

### "Webhook URL keeps timing out"
- Make sure `./run.sh` is running
- Verify ngrok is active: `ps aux | grep ngrok`
- Check ngrok URL hasn't changed (expires every 2-8 hours without paid account)

### "Messages not being received"
1. Verify webhook URL in Facebook Dashboard is correct
2. Check token matches: `lsa_secure_token`
3. Verify phone number is verified: +91 7010384691
4. Check Flask logs: `tail -f /tmp/lsa_server.log`

### "Response not being sent back"
1. Verify API token is correct in code
2. Check Business Account ID is correct
3. Verify Phone Number ID is correct
4. Check WhatsApp message template is configured

### "Getting rate limiting errors"
- WhatsApp has rate limits (100 messages/day for new accounts)
- Increase with paid plan
- Test with fewer messages

## Testing Before Going Live

### Terminal Test (Free)
```bash
./test.sh
```
This sends test messages and shows responses without using WhatsApp.

### Webhook Test
```bash
curl -X POST http://localhost:5001/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "from": "+917010384691",
    "message": "Can I skip gym today?",
    "token": "lsa_secure_token"
  }'
```

### Real WhatsApp Test
1. Text your WhatsApp Business number from your phone
2. Wait for response (takes 1-3 seconds)
3. Try different decision questions

## Expected Response Format

When you text a decision question:

```
🤖 *LSA Decision Analysis*

📌 *Decision:*
Can I skip class today?

🎯 *Your Options (7 days):*

A️⃣ *Minimal Effort* 
   Do nothing / skip the activity
   Risk: Low | Confidence: 80%
   Score: 68

B️⃣ *Balanced* ✨ RECOMMENDED
   Moderate effort with good results
   Risk: Low | Confidence: 86%
   Score: 125

C️⃣ *Maximum Effort*
   Full commitment for best results
   Risk: High | Confidence: 68%
   Score: 154

✅ *Best Choice:* C: Maximum Effort
💡 Higher score = Better long-term outcome
```

## FAQ

**Q: Can I test without paying Meta?**  
A: Yes! Run `./test.sh` for terminal testing. No WhatsApp account needed.

**Q: How long does the API token last?**  
A: Indefinitely, unless you revoke it. Keep it private.

**Q: What if ngrok URL changes?**  
A: Free plan changes every 2-8 hours. Either:
1. Use paid ngrok ($5/month for fixed URL)
2. Update Facebook webhook URL when it changes
3. Use fixed domain + custom forwarding

**Q: Can I deploy to production?**  
A: Yes! Replace localhost with your server domain and set up proper SSL.

**Q: How many messages can I send?**  
A: Free accounts: 100/day. Paid plans have higher limits.

**Q: What if user sends invalid message?**  
A: System returns helpful message about how to ask decision questions.

## Next Steps

1. **Immediate**: Run `./test.sh` to verify terminal testing works
2. **Today**: Set up WhatsApp Business Account (5 min)
3. **Today**: Get API credentials from Meta (5 min)
4. **Today**: Update configuration and Flask server (10 min)
5. **Today**: Send first real message (1 min)

## Support

- Terminal not responding? → `tail -f /tmp/lsa_server.log`
- Messages not received? → Check ngrok URL and webhook configuration
- Integration questions? → See `run.sh` and `test.sh` examples

---

**Status**: Terminal testing ✅ | WhatsApp setup ready ⏳ | Production deployment ready ✅
