# INTERVENTION ENGINE SKILL

## PURPOSE
Send proactive alerts and recommendations via Telegram.

## TRIGGERS

### Inactivity Detection
- No memory entries for 24+ hours
- Deviation from daily routine pattern
- Send: "Observation + Predicted impact + Action"

### Bad Decision Detection
- Decision conflicts with stated goals
- Scenario A predicts >30% negative impact
- Risk score above threshold

### Goal Deviation
- Trending away from targets
- Momentum dropping 2+ consecutive days
- Energy levels trending down

## MESSAGE FORMAT

```
⚠️ Observation: [Factual finding]
📉 Predicted Impact: [Quantified outcome]
✅ Recommended Action: [Specific steps]
🎯 Confidence: [XX%]
⏰ Suggested Timing: [When to act]
```

## PRIORITY LEVELS

- 🔴 **CRITICAL**: Requires immediate action (energy crash, goal abandonment)
- 🟡 **HIGH**: Should act within 24h (momentum loss, habit breaking)
- 🟢 **NORMAL**: Routine optimization (efficiency improvements)

## CUSTOMIZATION

- Quiet hours: 22:00 - 08:00 (only critical alerts)
- Daily digest option: Combine into one message per day
- Intervention frequency: Configurable (default: 3+ per day max)

## INTEGRATION POINTS

- **Input**: Simulation Engine results + Memory patterns
- **Output**: Telegram messages
- **Logs**: Track intervention effectiveness
