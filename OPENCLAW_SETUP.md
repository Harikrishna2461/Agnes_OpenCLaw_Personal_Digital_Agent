# OpenClaw Daemon Integration - FIXED ✅

## What Was Fixed

❌ **Previous Issue**: `ImportError: cannot import name 'TimeoutError' from 'cmdop.exceptions'`

🔧 **Root Cause**: Version mismatch between OpenClaw and cmdop packages. OpenClaw expected `TimeoutError` exception class, but cmdop only provided `ConnectionTimeoutError`.

✅ **Solution**: Added compatibility alias in `/opt/homebrew/lib/python3.11/site-packages/cmdop/exceptions.py`:

```python
# Compatibility Aliases
TimeoutError = ConnectionTimeoutError
```

## Installation & Setup

### 1. Install Python 3.11 via Homebrew (If Not Already Done)

```bash
brew install python@3.11
```

### 2. Install Required Packages

```bash
pip install openclaw cmdop pydantic protobuf
```

### 3. Apply the Compatibility Fix

The fix has been automatically applied in your environment. If you need to apply it manually:

```bash
echo "
# Compatibility Aliases
TimeoutError = ConnectionTimeoutError
" >> /opt/homebrew/bin/../Cellar/python@3.11/3.11.14/lib/python3.11/site-packages/cmdop/exceptions.py
```

### 4. Verify Installation

```bash
/opt/homebrew/bin/python3.11 -c "import openclaw; print('✅ OpenClaw ready')"
```

## Running the Complete System

### Option 1: Automated Startup (Recommended)

```bash
# Start both Flask server and OpenClaw daemon automatically
./start_lsa_openclaw.sh
```

This script:
- ✅ Starts Flask webhook server (port 5001)
- ✅ Starts OpenClaw daemon (listens for WhatsApp messages)
- ✅ Starts ngrok tunnel (forwards public URLs)
- ✅ Displays configuration and logs

### Option 2: Manual Startup

**Terminal 1 - Flask Server:**
```bash
cd /Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent
/opt/homebrew/bin/python3.11 whatsapp_server.py
```

**Terminal 2 - OpenClaw Daemon:**
```bash
cd /Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent
/opt/homebrew/bin/python3.11 openclaw_daemon.py
```

**Terminal 3 - ngrok Tunnel:**
```bash
ngrok http 5001
```

### Option 3: Using the Test Script (No Real WhatsApp Needed)

```bash
# Test the complete integration with simulated messages
./test_integration.py
```

This script:
- ✅ Verifies Flask health
- ✅ Sends test decision scenarios
- ✅ Validates LSA responses work correctly
- ✅ Reports pass/fail status

## Integration Flow

```
User Message to +91 7010384691
        ↓
WhatsApp Business API
        ↓
OpenClaw Daemon (listening)
        ↓
LSA Flask Server (localhost:5001)
        ↓
Life Simulation Agent
(Analyzes decision using 3 scenarios)
        ↓
Response back through OpenClaw
        ↓
WhatsApp response to user
```

## Configuration Files

### ~/.openclaw/openclaw.json
Contains webhook mapping to forward WhatsApp messages to LSA:
```json
{
  "hooks": {
    "mappings": [{
      "match": {"path": "/whatsapp"},
      "forward_to": "https://your-ngrok-url/webhook/whatsapp"
    }]
  }
}
```

## Monitoring

### Check Flask Health
```bash
curl http://localhost:5001/health
```

### Check OpenClaw Daemon Logs
```bash
tail -f /tmp/lsa_openclaw/openclaw_daemon.log
```

### Check Flask Logs
```bash
tail -f /tmp/lsa_openclaw/flask_server.log
```

## Troubleshooting

### "TimeoutError" Import Error
✅ **Already Fixed** - The compatibility patch is in place

### OpenClaw Daemon Won't Start
1. Verify Python 3.11 installation: `/opt/homebrew/bin/python3.11 --version`
2. Check imports: `/opt/homebrew/bin/python3.11 -c "import openclaw"`
3. Check logs: `cat /tmp/lsa_openclaw/openclaw_daemon.log`

### Flask Server Won't Start
1. Ensure port 5001 is available: `lsof -i :5001`
2. Kill other services: `pkill -f whatsapp_server`
3. Check Python imports: `python3 -c "import flask, requests, sentence_transformers"`

### WhatsApp Messages Not Received
1. Verify OpenClaw daemon is running: `ps aux | grep openclaw_daemon`
2. Check daemon logs for connection status
3. Verify ngrok tunnel is active: `ps aux | grep ngrok`
4. Verify webhook URL in openclaw.json matches ngrok URL

## Files

- **`openclaw_daemon.py`** - OpenClaw WhatsApp message listener and forwarder
- **`whatsapp_server.py`** - Flask webhook endpoint (processes LSA decisions)
- **`whatsapp_direct_api.py`** - Alternative direct WhatsApp Business API integration
- **`start_lsa_openclaw.sh`** - Automated startup script for complete system
- **`test_integration.py`** - Integration test script (no real WhatsApp needed)

## Success Indicators

✅ **Flask Server Running**
```
$ curl http://localhost:5001/health
{"service":"LSA WhatsApp","status":"ok"}
```

✅ **OpenClaw Daemon Running**
```
OpenClaw WhatsApp Daemon Starting
✅ OpenClaw module imported successfully
✅ Daemon is ACTIVE and listening for WhatsApp messages
```

✅ **Test Communication**
```
$ ./test_integration.py
[...]
🎉 All tests passed! LSA + OpenClaw integration is working!
```

## Next Steps

1. ✅ OpenClaw daemon is fixed and working
2. ✅ Flask server is operational
3. ✅ ngrok tunnel is configured
4. ⏳ Configure WhatsApp Business API with your OpenClaw account
5. ⏳ Set webhook URL in WhatsApp dashboard to ngrok URL
6. ⏳ Send test message to +91 7010384691 from your WhatsApp

## Support

If issues persist:
1. Check all log files in `/tmp/lsa_openclaw/`
2. Verify Python environment: `pip list | grep -i "openclaw\|cmdop\|pydantic"`
3. Run test script: `./test_integration.py`

---

**Status**: ✅ All OpenClaw dependency issues RESOLVED
**Date Fixed**: 2026-04-05
**Python Version**: 3.11.14
**OpenClaw Version**: 2026.3.20
**cmdop Version**: 2026.3.18
