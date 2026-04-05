# Getting Started with Life Simulation Agent (LSA)

## 5-Minute Quick Start

### 1. Install Dependencies
```bash
cd lsa-agent
pip install -r requirements.txt
```

### 2. Run Demo
```bash
python3 main.py
```

Expected output shows:
- 2 decision simulations with 3 scenarios each
- Risk/confidence scoring
- Daily report with activities and consistency metrics

### 3. Next Steps

#### Option A: Try Interactive Mode
```python
from main import LifeSimulationAgent

agent = LifeSimulationAgent()

# Log an event
agent.log_event("Completed 90min study session", "study", 9.0)

# Simulate a decision
result = agent.simulate_decision("Should I skip workout today?")

# View today's report
print(agent.get_daily_report())
```

#### Option B: Setup Telegram Integration
1. Create Telegram bot: Talk to @BotFather
2. Get your user ID: Talk to @userinfobot
3. Create `.env` file:
   ```
   TELEGRAM_TOKEN=your_token
   TELEGRAM_USER_ID=your_id
   ```
4. Run daemon:
   ```bash
   python3 telegram_daemon.py
   ```
5. Message your bot a decision:
   ```
   "I'm thinking of skipping study today"
   ```

#### Option C: Enable Autonomous Operation
```bash
# Install APScheduler for cron jobs
pip install APScheduler

# Start scheduler
python3 scheduler.py
```

Scheduled tasks:
- 9:00 AM: Daily report
- Monday 10:00 AM: Weekly report
- Every 4 hours: Intervention checks
- Daily 2:00 AM: Data backup

---

## Use Case: Decision Analysis

### Example 1: Career Decision
```python
agent.simulate_decision("Should I take the new job offer or stay?")
```

**Output**: 3 scenarios with career impact, risk, and confidence scores

### Example 2: Habit Building
```python
agent.log_event("Morning workout (30 min)", "health", 8.5)
result = agent.simulate_decision("Continue 5x/week routine?")
```

**Output**: Scenarios show consistency scores over 7 days

### Example 3: Behavior Pattern
```python
# Log several activities
agent.log_event("Study: 2 hours", "study", 9.0)
agent.log_event("Skipped workout", "health", 3.0)

# Analyze patterns
patterns = agent.memory_manager.analyze_patterns(days=30)
```

**Output**: Trends, frequencies, consistency metrics

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│         LIFE SIMULATION AGENT (LSA)         │
└─────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐  ┌──────────┐  ┌──────────┐
   │ MEMORY  │  │SIMULATION│  │INTERVENTION
   │MANAGER  │  │ ENGINE   │  │ENGINE   
   └─────────┘  └──────────┘  └──────────┘
        │             │             │
        │ Context     │ Scenarios   │ Alerts
        │             │             │
        └─────────────┴─────────────┘
                      │
              ┌───────┴───────┐
              ▼               ▼
           LOGGER          TELEGRAM
        (lsa_agent.log)     (bot)
```

---

## Configuration

### Environment Variables (.env)
```bash
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_USER_ID=your_user_id
DATA_DIR=./data
LOG_LEVEL=INFO
QUIET_HOURS_START=22
QUIET_HOURS_END=8
MAX_DAILY_ALERTS=5
```

### Memory Categories
- `study`: Learning, academic work
- `health`: Exercise, nutrition, sleep
- `productivity`: Work, projects, tasks
- `social`: Relationships, interactions
- `finance`: Spending, earning, saving
- `mood`: Emotions, mental state

---

## Common Commands

### Check Status
```python
report = agent.get_daily_report()
print(report)
```

### Export Data
```python
path = agent.export_data()
print(f"Exported to {path}")
```

### Clear Test Data
```python
agent.memory_manager.clear_memories()
```

### Test Components
```bash
python3 test_lsa.py
```

---

## Troubleshooting

### Issue: "SentenceTransformer not found"
```bash
pip install sentence-transformers
```

### Issue: "Telegram token not working"
1. Check token in .env matches @BotFather
2. Ensure user ID is correct (get from @userinfobot)
3. Restart daemon

### Issue: "Memory not persisting"
```bash
# Check directory exists
ls -la data/

# Check file permissions
chmod 755 data/
```

### Issue: "Demo runs slowly"
- First run downloads embedding model (~100MB)
- Subsequent runs cached and faster
- GPU support: Install `faiss-gpu` instead of `faiss-cpu`

---

## Next Learning Steps

1. **Customize Agent Personality**
   - Edit `config/SOUL.md`
   - Adjust behavioral rules

2. **Add Custom Scenarios**
   - Enhance `SimulationEngine.simulate_decision()`
   - Add domain-specific logic

3. **Extend Memory Categories**
   - Add new tags in category system
   - Create custom analyzers

4. **Build Integrations**
   - Add calendar sync
   - Integrate with fitness trackers
   - Connect to task managers

5. **Deploy to Production**
   - Use systemd for daemon management
   - Setup monitoring with logging
   - Configure database backup

---

## Support & Resources

- **Main documentation**: See `README.md`
- **Agent personality**: See `config/SOUL.md`
- **Skill documentation**: See `skills/*/SKILL.md`
- **Component tests**: Run `python3 test_lsa.py`
- **Example usage**: Run `python3 main.py`

---

**Ready to build your better future?**

Next: Run `python3 main.py` to see the demo in action! ✨
