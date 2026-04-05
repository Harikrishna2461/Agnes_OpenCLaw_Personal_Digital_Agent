# Life Simulation Agent (LSA) - Complete Guide

**An autonomous system that predicts consequences of user actions, simulates multiple future scenarios, and suggests optimal decisions.**

LSA is NOT a chatbot. It's a proactive life optimization engine backed by data-driven simulations and the Agnes Claw Model.

---

## 📚 Table of Contents

1. [Quick Start](#quick-start)
2. [Features](#features)
3. [Installation](#installation)
4. [Running the Agent](#running-the-agent)
5. [WhatsApp Integration](#whatsapp-integration)
6. [Telegram Integration](#telegram-integration)
7. [Testing & Demo](#testing--demo)
8. [Advanced Usage](#advanced-usage)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### 30-Second Setup

```bash
cd /Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent

# Install dependencies (once)
pip install -r requirements.txt

# Run the demo
python3 main.py
```

**Expected output:**
```
✨ DEMO COMPLETE - LSA Ready for Production
Consistency: 100%
Activities: 6
Average impact: 8.2/10  
```

---

## ✨ Features

### 1. **Decision Simulation** 🔮
Analyze any life decision with 3 scenarios (A/B/C):
- Current trajectory
- Moderate improvement
- Optimal performance

Each scenario includes:
- Predicted outcomes
- Risk assessment
- Confidence score
- Regret prediction

### 2. **Event Logging** 📝
Track your daily activities:
- Study sessions
- Workouts
- Meals
- Work tasks
- Any custom event

### 3. **Pattern Analysis** 📊
Automatic insights:
- Consistency tracking
- Trend detection
- Behavioral patterns
- 7/30-day reports

### 4. **Real-time Integration** 📱
Chat via:
- **WhatsApp** (Direct - No Twilio)
- **Telegram** (Faster setup)
- **Python** (Direct API)

### 5. **Autonomous Monitoring** ⏰
Scheduled operations:
- Daily reports (9am)
- Weekly analysis (Monday)
- Intervention checks (every 4 hours)
- Data backup (2am)

---

## 📥 Installation

### System Requirements
- Python 3.9+
- 2GB RAM minimum
- macOS, Linux, or Windows

### Step 1: Clone & Navigate
```bash
cd /Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

First-time setup downloads embeddings (~100MB):
```bash
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Step 3: Configure
The `.env` file is already configured with:
```
AGNES_CLAW_API_KEY=sk-ai-v1-...
WHATSAPP_USER_NUMBER=+917010384691
```

---

## ▶️ Running the Agent

### Mode 1: Demo Mode (Recommended First)
```bash
python3 main.py
```

**What happens:**
- ✅ Loads sample memory (3 events)
- ✅ Simulates 2 decisions
- ✅ Shows 3 scenarios each
- ✅ Displays daily report
- ⏱️ Takes ~3 seconds

**Output includes:**
- Scenario A/B/C with outcomes
- Risk levels
- Confidence scores
- Recommendations
- Consistency metrics

### Mode 2: Test Suite
```bash
python3 test_lsa.py
```

**What it tests:**
- ✅ Memory Manager (add, retrieve, search)
- ✅ Simulation Engine (scenario generation)
- ✅ Intervention Engine (alert generation)
- ✅ Full integration

**Sample output:**
```
✅ PASSED: Memory Manager
✅ PASSED: Simulation Engine
✅ PASSED: Intervention Engine
✅ PASSED: Full Integration
✨ All tests passed! LSA is production-ready.
```

### Mode 3: White Label (Direct Python)
```python
from main import LifeSimulationAgent

agent = LifeSimulationAgent()

# Log event
agent.log_event("Completed 2-hour study", "study", impact_score=9.0)

# Simulate decision
result = agent.simulate_decision("Should I skip workout?")

# View results
print(f"Recommendation: {result['recommendation']}")

# Get report
print(agent.get_daily_report())
```

---

## 📱 WhatsApp Integration

### Option A: Local Testing (Fastest)

**Step 1: Start WhatsApp Server**
```bash
pip install flask
python3 whatsapp_server.py
```

**Step 2: In Another Terminal - Test**
```bash
python3 test_whatsapp.py --mode interactive
```

**Step 3: Send Test Messages**
```
You: Should I study for 2 hours?
LSA: 🤖 LSA Decision Analysis
[Shows 3 scenarios with scores]

You: Completed 90-minute study
LSA: ✅ Event logged!
[Shows consistency, impact]

You: /status
LSA: 📊 Activities: 5
     Consistency: 87%
```

### Option B: Production WhatsApp (Real Messages)

**Step 1: Understand the Flow**
```
Real WhatsApp Message
         ↓
OpenClaw API Receives
         ↓
Sends to LSA Webhook
         ↓
LSA Processes & Responds
         ↓
Response Sent Back to WhatsApp
```

**Step 2: Start Server**
```bash
python3 whatsapp_server.py
```

**Step 3: Expose to Internet**
```bash
# Install ngrok for tunneling
brew install ngrok  # macOS
# OR Windows: https://ngrok.com/download

# Run in another terminal
ngrok http 5000
# Copy URL: https://xxxx.ngrok.io
```

**Step 4: Configure OpenClaw**
- Go to OpenClaw Console
- Set webhook: `https://xxxx.ngrok.io/webhook/whatsapp`
- Test with: `https://xxxx.ngrok.io/webhook/verify`

**Step 5: Send WhatsApp Message**
From any WhatsApp (the number is +91 7010384691):
```
"Should I take the job?"
```

LSA responds instantly with analysis!

### WhatsApp Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/status` | Daily summary | `/status` |
| `/weekly` | Weekly report | `/weekly` |
| `/help` | Show commands | `/help` |
| `/export` | Download data | `/export` |
| *Free text decision* | Analyze | "Should I skip study?" |
| *Free text event* | Log | "Completed workout" |

### WhatsApp Features

✅ **Smart Detection**
- Automatically recognizes decisions
- Auto-logs events
- Routes to correct handler

✅ **Real-time Responses**
- 1-3 second response time
- Complete scenario analysis
- Immediate recommendations

✅ **Persistent Memory**
- All conversations logged
- Build comprehensive history
- Pattern detection across time

---

## 💬 Telegram Integration

### Setup (5 Minutes)

**Step 1: Create Telegram Bot**
```
1. Open Telegram
2. Chat with @BotFather
3. Send: /newbot
4. Follow prompts, get BOT_TOKEN
```

**Step 2: Get Your User ID**
```
1. Chat with @userinfobot
2. It shows your user ID
```

**Step 3: Set Environment**
```bash
export TELEGRAM_TOKEN="your_bot_token_here"
export TELEGRAM_USER_ID="your_user_id_here"
```

**Step 4: Start Bot**
```bash
python3 telegram_daemon.py
```

**Step 5: Chat with Bot**
In Telegram, send any message:
```
"Should I start a new project?"
LSA: 🤖 Decision Analysis...
```

### Telegram Commands
Same as WhatsApp: `/status`, `/weekly`, `/help`, `/export`

---

## 🧪 Testing & Demo

### Test 1: Run Full Demo
```bash
python3 main.py
```
**Duration:** ~3 seconds  
**Validates:** All core systems

### Test 2: Component Tests
```bash
python3 test_lsa.py
```
**Duration:** ~5 seconds  
**Validates:** Memory, Simulation, Intervention, Integration

### Test 3: WhatsApp Local
```bash
# Terminal 1
python3 whatsapp_server.py

# Terminal 2
python3 test_whatsapp.py --mode test
```
**Duration:** ~10 seconds  
**Validates:** Webhook, messaging, responses

### Test 4: WhatsApp Interactive
```bash
# Terminal 1
python3 whatsapp_server.py

# Terminal 2
python3 test_whatsapp.py --mode interactive
```
**Then type messages and see responses in real-time**

### Test 5: Manual Testing
```bash
python3 test_whatsapp.py --mode send --message "Should I study?"
```
**Sends single message and shows response**

---

## 🔧 Advanced Usage

### Custom Decision Analysis

```python
from main import LifeSimulationAgent

agent = LifeSimulationAgent()

# Define user context
user_state = {
    "goals": "Finish project, exercise 4x/week",
    "mood": 7,
    "energy": 8,
    "routine": "Daily standup at 9am",
}

# Simulate decision
result = agent.simulate_decision(
    decision="Work late into evening?",
    current_state=user_state
)

# Analyze scenarios
for scenario_key, scenario_data in result["scenarios"].items():
    print(f"\nScenario {scenario_key}")
    print(f"  Risk: {scenario_data['risk']}")
    print(f"  Outcomes: {scenario_data['outcomes']}")
    print(f"  Regret: {scenario_data['regret']}")

print(f"\n✅ Best choice: {result['recommendation']}")
```

### Pattern Analysis

```python
patterns = agent.memory_manager.analyze_patterns(days=30)

# Get trending categories
for category, data in patterns.items():
    if data['trend'] == 'declining':
        print(f"⚠️  {category} is declining")
    if data['trend'] == 'improving':
        print(f"✅ {category} is improving")
```

### Data Export

```python
# Export all data
path = agent.export_data()
print(f"Data exported to: {path}")

# View raw memories
memories = agent.memory_manager.get_all_memories()
for mem in memories[-5:]:
    print(f"{mem['timestamp']}: {mem['content']}")
```

### Scheduled Reports

```bash
# Run scheduler for autonomous operation
python3 scheduler.py

# Will automatically run:
# - Daily report at 9am
# - Weekly report Mondays 10am
# - Intervention checks every 4 hours
# - Data backup at 2am
```

---

## 📊 Use Cases & Examples

### Use Case 1: Career Decision

**You send:**
```
"Should I take the new job offer? 
It pays 20% more but requires relocation."
```

**LSA responds:**
```
Scenario A (Stay): 
  - Risk: moderate
  - Consistency: 60%
  - Growth: limited

Scenario B (Negotiate):
  - Risk: low
  - Consistency: 78%
  - Growth: moderate

Scenario C (Take job):
  - Risk: high (relocation stress)
  - Consistency: 95%
  - Growth: high

Recommendation: B
Best path: Negotiate remote option
```

### Use Case 2: Habit Building

**You send:**
```
"Started morning workouts, should I add evening study?"
```

**LSA responds:**
```
Event logged: Morning workout
Pattern detected: 4 consecutive days

Recommendation: Yes, but gradually
Suggestion: Add 30min study 2x/week first
Timeline: Build to 5x/week over 3 weeks
Predicted consistency: 87%
```

### Use Case 3: Daily Check-in

**You send:**
```
"Hi"
```

**LSA responds:**
```
📊 Today's Summary
Activities: 5
Avg impact: 8.0/10
Consistency: 85%

Pattern: On track with goals
Suggestion: Push hard today to hit 90%
```

---

## 🐛 Troubleshooting

### Issue: "SentenceTransformer not found"
```bash
pip install sentence-transformers
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Issue: "Flask not found"
```bash
pip install flask
```

### Issue: "ModuleNotFoundError: No module named 'main'"
```bash
# Make sure you're in the lsa-agent directory
cd /Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent
python3 whatsapp_server.py
```

### Issue: "Connection refused" on WhatsApp
```bash
# Check if server is running
curl http://localhost:5000/health

# Should see:
# {"status":"ok","service":"LSA WhatsApp",...}

# If not, start it:
python3 whatsapp_server.py
```

### Issue: "Invalid API key"
```bash
# Check .env file
cat .env

# Ensure AGNES_CLAW_API_KEY is set:
AGNES_CLAW_API_KEY=sk-ai-v1-673c5930e56cff44d63d9f9ddca38aa4169ec44f3194cfd2a253e86d1ee132df
```

### Issue: "Webhook token mismatch"
```bash
# Check token in .env
grep WEBHOOK_TOKEN .env

# Default is: lsa_secure_token
# Make sure test_whatsapp.py uses same token
python3 test_whatsapp.py --token lsa_secure_token
```

### Issue: "Port 5000 already in use"
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9

# Or use different port
python3 whatsapp_server.py --port 5001
```

---

## 📋 Architecture Overview

```
┌────────────────────────────────────────────────┐
│      LIFE SIMULATION AGENT (LSA) CORE         │
└────────────────────────────────────────────────┘
         │              │              │
    ┌────▼────┐    ┌────▼─────┐  ┌────▼──────────┐
    │ MEMORY  │    │SIMULATION│  │INTERVENTION  │
    │MANAGER  │    │ ENGINE   │  │ENGINE        │
    └────┬────┘    └────┬─────┘  └────┬──────────┘
         │              │              │
    ┌────▼──────────────▼──────────────▼──────┐
    │     USER INTERFACE LAYER                │
    ├───────────────────────────────────────────┤
    │  Direct Python │ WhatsApp │ Telegram    │
    │   API Usage    │ (OpenClaw)│  (Bot)     │
    └────────────────────────────────────────────┘
```

---

## 🚀 Production Checklist

- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Demo runs successfully: `python3 main.py`
- [ ] Tests pass: `python3 test_lsa.py`
- [ ] WhatsApp server starts: `python3 whatsapp_server.py`
- [ ] WhatsApp tests pass: `python3 test_whatsapp.py --mode test`
- [ ] API key configured in `.env`
- [ ] Logs monitored: `tail -f lsa_agent.log`
- [ ] Data directory writable: `ls -la data/`

---

## 📞 Quick Reference

### Commands Cheat Sheet

```bash
# Demo
python3 main.py

# Tests
python3 test_lsa.py
python3 test_whatsapp.py --mode test
python3 test_whatsapp.py --mode interactive

# Servers
python3 whatsapp_server.py
python3 telegram_daemon.py
python3 scheduler.py

# View logs
tail -f lsa_agent.log
tail -f lsa_whatsapp_server.log

# Check status
curl http://localhost:5000/health
curl http://localhost:5000/webhook/verify
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | This file - Complete guide |
| `config/SOUL.md` | Agent personality definition |
| `skills/*/SKILL.md` | Individual skill documentation |
| `GETTING_STARTED.md` | Quick setup guide |
| `AGNES_CLAW_INTEGRATION.md` | LLM integration details |
| `WHATSAPP_SETUP.md` | WhatsApp detailed setup |
| `PROJECT_STRUCTURE.md` | Project layout |

---

## 💡 Tips & Tricks

### Tip 1: Speed Up First Run
```bash
# First run downloads models (~100MB)
# Subsequent runs use cache - much faster

# See cached files:
ls -lh data/
```

### Tip 2: Debug Logs
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

python3 main.py
```

### Tip 3: Multiple Users (Testing)
```bash
# Each user gets isolated memory
agent1 = LifeSimulationAgent(data_dir="./user1_data")
agent2 = LifeSimulationAgent(data_dir="./user2_data")
```

### Tip 4: Custom Scenarios
```python
# Override default scenarios
agent.simulate_decision(
    decision="Custom decision",
    current_state={"custom_field": "value"}
)
```

---

## 🎯 What's Next?

1. **Start with demo**: `python3 main.py`
2. **Run tests**: `python3 test_lsa.py`
3. **Try WhatsApp locally**: `python3 whatsapp_server.py` + `python3 test_whatsapp.py --mode interactive`
4. **Deploy WhatsApp**: Use ngrok + configure webhooks
5. **Enable Telegram**: Quick 5-minute setup
6. **Schedule autonomously**: `python3 scheduler.py`

---

## ✨ You're Ready!

**Your LSA is fully operational:**
- ✅ Agnes Claw API configured
- ✅ WhatsApp ready (local testing)
- ✅ Telegram ready (5-min setup)
- ✅ All tests passing
- ✅ Production-ready

**Start chatting:** `python3 whatsapp_server.py`

**Questions?** Check the logs: `tail -f lsa_agent.log`

---

**Built with ❤️ by Agnes AI**  
*Your future self's advocate.*
