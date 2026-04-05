# 🚀 Agnes LSA - Quick Start Guide

## ⚡ 30-Second Setup

```bash
cd /Users/HariKrishnaD/Downloads/Agnes_AI

# 1. Install dependencies (one time only)
./setup.sh

# 2. Start the system
./run.sh

# 3. In another terminal, run tests
./test.sh
```

## ✅ What Each Script Does

### 1. `setup.sh` - First time setup
- ✅ Installs all Python dependencies (Flask, sentence-transformers, etc.)
- ✅ Creates configuration files
- ✅ Makes scripts executable
- ⏱️ Takes ~5 minutes

**Run once**: `./setup.sh`

### 2. `run.sh` - Start everything
- ✅ Starts Flask WhatsApp server (localhost:5001)
- ✅ Starts OpenClaw daemon (WhatsApp listener)
- ✅ Starts ngrok tunnel (public endpoint)
- ⏱️ Takes ~5 seconds to start

**Run this**: `./run.sh`

Then keep it running and open another terminal for testing.

### 3. `test.sh` - Terminal testing
- ✅ Tests Flask server health
- ✅ Sends test decision messages
- ✅ Shows LSA analysis responses
- ✅ No real WhatsApp needed!

**Run this in another terminal**: `./test.sh`

Perfect for verifying everything works before setting up real WhatsApp.

## 📋 Quick Example

**Terminal 1** - Start everything:
```bash
./run.sh
```

Output:
```
╔═════════════════════════════════════════════════════════════════╗
║   Agnes LSA + OpenClaw WhatsApp Integration - STARTUP           ║
╚═════════════════════════════════════════════════════════════════╝

✅ Flask server is healthy (localhost:5001)
✅ OpenClaw daemon started
✅ ngrok tunnel active

📊 SERVICES:
   ✅ Flask Server:      localhost:5001
   ✅ OpenClaw Daemon:   WhatsApp listener
   ✅ ngrok Tunnel:      Public endpoint
```

**Terminal 2** - Run tests:
```bash
./test.sh
```

Output:
```
═══════════════════════════════════════════════════════════════
📋 Test 2: Skip Class Decision
   Message: Can I skip class today?

🤖 *LSA Decision Analysis*

📌 *Decision:*
Can I skip class today?

🎯 *Your Options (7 days):*

A️⃣ *Minimal Effort* - Score: 68
B️⃣ *Balanced* - Score: 125 ✨ RECOMMENDED
C️⃣ *Maximum Effort* - Score: 154

✅ Decision analysis generated
```

## 🎯 Integration Path

### Step 1: Terminal Testing ✅ (You are here)
```bash
./setup.sh  # Install dependencies
./run.sh    # Start system
./test.sh   # Test decision analysis
```

### Step 2: Real WhatsApp Integration ⏳
Follow: [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md)

This involves:
1. Creating WhatsApp Business Account
2. Getting Meta API credentials
3. Configuring webhook in Facebook Developer Dashboard
4. Testing with real messages from your phone

### Step 3: Production Deployment (Optional)
Deploy to cloud server with fixed domain instead of ngrok.

## 📊 What Gets Tested

Running `./test.sh` verifies:

✅ **Flask Server**: Is it responding to requests?  
✅ **Decision Analysis**: Can LSA generate scenarios?  
✅ **Response Formatting**: Are emoji/scores correct?  
✅ **Different Decisions**: Class, gym, study, work, etc.  

## 🧪 Manual Testing

If you want to manually test:

```bash
# Check server is healthy
curl http://localhost:5001/health

# Send a test message
curl -X POST http://localhost:5001/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{
    "from": "+917010384691",
    "message": "Should I study for 4 hours?",
    "token": "lsa_secure_token"
  }'
```

## 📁 File Structure

```
/Users/HariKrishnaD/Downloads/Agnes_AI/
├── setup.sh                    ← Run once to install
├── run.sh                       ← Run to start system
├── test.sh                      ← Run to test
├── QUICK_START.md               ← Quick reference
├── WHATSAPP_SETUP.md            ← WhatsApp integration steps
├── INTEGRATION_COMPLETE.md      ← Integration status
└── lsa-agent/
    ├── whatsapp_server.py       ← Flask webhook server
    ├── openclaw_daemon.py        ← OpenClaw listener
    ├── main.py                   ← LSA orchestration
    └── simulation.py             ← Decision scenarios
```

## 🔧 Troubleshooting

### "Command not found: ./run.sh"
Solution: Make sure you're in the correct directory
```bash
cd /Users/HariKrishnaD/Downloads/Agnes_AI
ls -la run.sh  # Should show: -rwxr-xr-x ... run.sh
```

### "Flask not responding"
Check logs:
```bash
tail -f /tmp/lsa_server.log
```

### "Port 5001 already in use"
Kill existing process:
```bash
pkill -f whatsapp_server
```

## 📱 Next: Real WhatsApp Integration

Once terminal testing works perfectly (`./test.sh` passes):

1. Read: [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md)
2. Create WhatsApp Business Account
3. Get Meta API credentials
4. Update configuration
5. Send real message from your phone

## ✨ Key Features

✅ **Terminal Testing** - No WhatsApp needed, test everything locally  
✅ **Decision Analysis** - Get 3 scenarios with pros/cons  
✅ **Impact Scoring** - Numbered scores for each option  
✅ **Emoji Formatting** - Beautiful WhatsApp-ready output  
✅ **OpenClaw Integration** - Forwards real messages  
✅ **ngrok Tunnel** - Public access without deployment  

## 🎓 Learning Path

1. **Understand**: Read this file (2 min)
2. **Setup**: Run `./setup.sh` (5 min)
3. **Start**: Run `./run.sh` in Terminal 1 (keep running)
4. **Test**: Run `./test.sh` in Terminal 2 (see it work)
5. **Integrate**: Follow [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md) (30 min)
6. **Deploy**: Use same `run.sh` on any server (scalable)

## 📞 Support Options

| Issue | Solution |
|-------|----------|
| Terminal test fails | `tail -f /tmp/lsa_server.log` |
| Port in use | `pkill -f whatsapp_server` |
| Unclear next steps | Read `WHATSAPP_SETUP.md` |
| Want production setup | See deployment section in this readme |

## 🎉 Ready?

```bash
cd /Users/HariKrishnaD/Downloads/Agnes_AI
./setup.sh      # First time only
./run.sh        # Keep running
./test.sh       # In another terminal
```

That's it! You should see decision analysis responses within seconds.

---

**Status**: ✅ Terminal Testing Ready  
**Next Phase**: WhatsApp Business Account setup (see WHATSAPP_SETUP.md)  
**Time to WhatsApp**: ~1 hour (mostly waiting for Meta approval)
