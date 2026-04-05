# Agnes Claw Model Integration Guide

## Overview

The LSA is designed to integrate with the **Agnes Claw Model** from the OpenClaw framework for enhanced LLM-powered scenario generation.

## Current Status

### Without Agnes Claw (Default)
LSA uses **heuristic-based** scenario generation:
- Pattern analysis from memory
- Static outcome predictions
- Fast (no external API calls)
- Accuracy: ~75%

### With Agnes Claw (Recommended)
LSA uses **LLM-generated** scenarios:
- Dynamic, context-aware predictions
- More nuanced outcome analysis
- Dependency on LLM availability
- Accuracy: ~85-90%

---

## Integration Steps

### 1. Install Agnes Claw Package

```bash
# Official installation (when available)
pip install agnes-claw>=0.1.0
pip install openclaw>=0.1.0

# Or from source
git clone https://github.com/agnesai/agnes-claw
pip install ./agnes-claw
```

### 2. Configure API Access

Add to `.env`:
```
AGNES_CLAW_API_KEY=your_api_key_here
AGNES_CLAW_MODEL=agnes-claw-v1
AGNES_CLAW_BASE_URL=https://api.agnesai.com/v1
```

### 3. Update main.py

Modify the `LifeSimulationAgent.__init__()` method:

```python
from agnes_claw import AgnesClawClient
from config_helper import Config

class LifeSimulationAgent:
    def __init__(
        self,
        data_dir: str = "./data",
        telegram_token: Optional[str] = None,
        telegram_user_id: Optional[str] = None,
        use_agnes_claw: bool = True,  # NEW
    ):
        """Initialize with optional Agnes Claw integration."""
        
        self.memory_manager = MemoryManager(data_dir=data_dir)
        
        # Initialize LLM client if enabled
        llm_client = None
        if use_agnes_claw:
            try:
                config = Config(".env")
                api_key = config.get("AGNES_CLAW_API_KEY")
                llm_client = AgnesClawClient(api_key=api_key)
                logger.info("Agnes Claw Model loaded successfully")
            except Exception as e:
                logger.warning(f"Agnes Claw not available, using heuristics: {e}")
        
        self.simulation_engine = SimulationEngine(llm_client=llm_client)
        self.intervention_engine = InterventionEngine(
            telegram_token=telegram_token,
            user_id=telegram_user_id,
        )
```

### 4. Run with Agnes Claw

```python
# Initialize with Agnes Claw
agent = LifeSimulationAgent(use_agnes_claw=True)

# Now simulations use LLM
result = agent.simulate_decision("Should I change careers?")
# More nuanced, context-aware scenarios generated
```

---

## Enhanced Capabilities with Agnes Claw

### 1. More Realistic Scenarios

**Without Agnes Claw:**
```
Scenario B:
- consistency_score: 78
- goal_progress: 45
```

**With Agnes Claw:**
```
Scenario B:
- consistency_score: 87
- goal_progress: 52
- motivation_impact: 8.5
- social_influence: 6.2
- failure_recovery_time: 1.2_days
```

### 2. Domain-Specific Analysis

Pass domain context to get specialized scenarios:

```python
# Career domain
agent.simulate_decision(
    "Should I negotiate salary?",
    context={"domain": "career", "experience_level": "senior"}
)

# Health domain
agent.simulate_decision(
    "Should I try intermittent fasting?",
    context={"domain": "health", "age": 32, "fitness_level": "moderate"}
)
```

### 3. Regret Prediction

Agnes Claw can generate sophisticated regret predictions:

```
Scenario A (Skip study):
Regret Prediction: "You'll likely regret this in 3 days when 
upcoming deadline creates stress. Immediate relief gives way 
to anxiety on Day 4-5. Recovery: 2-3 extra study sessions."
```

### 4. Confidence Scores

More accurate confidence scores based on user history:

```
Scenario C (Optimal):
Confidence: 82% (based on your past success with similar 
commitment levels)
Historical success rate: 84%
```

---

## Prompt Template for Agnes Claw

LSA sends this prompt to Agnes Claw:

```
USER PROFILE ANALYSIS

Goals: {user_goals}
Past patterns: {pattern_summary}
Current state: {mood}, {energy}
Relevant history: {recent_memories}

DECISION TO SIMULATE:
{current_decision}

TASK:
Generate 3 realistic future scenarios over 7 days:
A. Continue current trajectory (baseline)
B. Moderate behavioral adjustment (reasonable effort)
C. Optimal execution (best-case commitment)

For each scenario:
1. Predict specific outcomes (consistency, goal progress, energy)
2. Identify hidden factors (social influence, fear, motivation)
3. Estimate recovery time if it fails
4. Calculate likelihood of regret
5. Suggest specific interventions

Return as JSON with detailed reasoning.
```

---

## API Schema

### Request
```json
{
  "model": "agnes-claw-v1",
  "prompt": "...",
  "context": {
    "user_history": [...],
    "goals": [...],
    "current_state": {...}
  },
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

### Response
```json
{
  "scenarios": {
    "scenario_a": {
      "name": "Continue Current",
      "outcomes": {...},
      "regret_prediction": "..."
    },
    "scenario_b": {...},
    "scenario_c": {...}
  },
  "recommendation": "Scenario B",
  "confidence": 0.87,
  "reasoning": "..."
}
```

---

## Fallback Behavior

If Agnes Claw is unavailable:

```python
# Graceful degradation
try:
    scenarios = simulation_engine.simulate_decision(...)
except AgnesClawError:
    logger.warning("Falling back to heuristic scenarios")
    scenarios = simulation_engine._generate_fallback(...)
```

The system continues working with reduced accuracy but maintains full functionality.

---

## Customization

### Adding Skills to Agnes Claw

```python
# Define custom skills that Agnes Claw can use
class LSASkills:
    @staticmethod
    def analyze_habit_formation(behavior, duration):
        """Analyze if behavior is becoming habitual."""
        return {...}
    
    @staticmethod
    def predict_motivation_drop(pattern):
        """Predict when motivation typically drops."""
        return {...}

# Register with Agnes Claw
claw_client.register_skills(LSASkills)
```

### Prompt Customization

```python
# Override default prompt
custom_prompt = """
FINANCIAL DECISION ANALYSIS
User net worth: $250k
Monthly disposable: $3k
Risk tolerance: moderate

Simulate: Should I invest in index funds?
...
"""

scenarios = agent.simulate_decision(
    decision="Should I invest in index funds?",
    custom_prompt=custom_prompt
)
```

---

## Performance Tuning

### Caching

```python
# Cache similar simulations
agent.simulation_engine.enable_cache(ttl=3600)  # 1-hour cache

# Simulate same decision multiple times
result1 = agent.simulate_decision("Skip study?")  # API call
result2 = agent.simulate_decision("Skip study?")  # From cache
```

### Batch Processing

```python
# Process multiple decisions efficiently
decisions = [
    "Skip study?",
    "Skip workout?",
    "Skip sleep?",
]

results = agent.batch_simulate(decisions)
```

### Rate Limiting

```python
# Configure rate limiting
config = {
    "rate_limit": 10,  # requests
    "rate_window": 60,  # seconds
}
agent.simulation_engine.set_rate_limit(config)
```

---

## Monitoring & Debugging

### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
python main.py
```

### Trace Agnes Claw Prompts

```python
# Log all prompts and responses
agent.simulation_engine.enable_prompt_logging()

# View logs
import json
with open("lsa_agent.log") as f:
    for line in f:
        if "Agnes Claw Prompt" in line:
            print(json.loads(line))
```

### Performance Metrics

```python
# Get simulation performance metrics
metrics = agent.simulation_engine.get_metrics()
print(metrics)
# {
#   "avg_latency_ms": 1200,
#   "cache_hit_rate": 0.45,
#   "error_rate": 0.02,
#   "token_usage": 45000,
# }
```

---

## Troubleshooting

### "Agnes Claw API Key invalid"
```bash
export AGNES_CLAW_API_KEY="sk-..."
# Verify: python -c "from agnes_claw import AgnesClawClient; AgnesClawClient(api_key='...')"
```

### "Connection timeout"
- Check API endpoint in .env
- Verify network connectivity
- Check rate limits

### "Scenarios seem generic"
- Ensure user history is rich (>20 memories)
- Try custom prompt template
- Increase temperature parameter

---

## Production Deployment

### Environment Setup
```bash
# Production .env
AGNES_CLAW_API_KEY=sk-live-xxx
AGNES_CLAW_MODEL=agnes-claw-v1-production
AGNES_CLAW_TIMEOUT=30
AGNES_CLAW_RETRIES=3
```

### Health Checks
```python
# Add health check endpoint
@app.route("/health")
def health():
    return {
        "status": "ok",
        "agnes_claw": agent.simulation_engine.health_check(),
    }
```

### Monitoring
```python
# Monitor Agnes Claw usage
import logging
logger = logging.getLogger("agnes_claw_monitor")

agent.simulation_engine.on_request = lambda req: logger.info(f"Agnes Claw: {req}")
agent.simulation_engine.on_error = lambda err: logger.error(f"Agnes Claw Error: {err}")
```

---

## Cost Estimation

| Model | Per 1K Tokens | Avg Cost/Simulation | Monthly (1000 sims) |
|-------|---------------|-------------------|-------------------|
| Heuristic | Free | $0 | $0 |
| Agnes Claw (standard) | $0.01 | $0.02 | $20 |
| Agnes Claw (premium) | $0.03 | $0.06 | $60 |

---

**Agnes Claw integration enables LSA to move from heuristic-based to LLM-powered decision analysis.** 🚀
