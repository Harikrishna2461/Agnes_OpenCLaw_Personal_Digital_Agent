# SIMULATION ENGINE SKILL

## PURPOSE
Simulate 3 future scenarios for user decisions and predict outcomes.

## SCENARIOS

### Scenario A: Continue Current Behavior
- No change in habits
- Predict trajectory without intervention
- Show momentum/decay patterns

### Scenario B: Moderate Improvement  
- Reasonable effort adjustments
- 30-50% behavior change
- Sustainable modifications

### Scenario C: Optimal Behavior
- Full commitment to recommendations
- Best-case scenario
- May require high effort

## OUTPUT FORMAT

For each scenario:
```json
{
  "name": "Scenario A: Continue Current",
  "description": "Maintain study pattern (3x/week)",
  "timeframe": "7 days",
  "predicted_outcomes": {
    "consistency_score": 65,
    "knowledge_gain": 2.3,
    "momentum": -5,
    "goal_progress": 25
  },
  "risk_level": "moderate",
  "confidence_score": 82,
  "key_metrics": {
    "study_hours": 8,
    "completion_rate": 0.65,
    "energy_trend": "declining"
  }
}
```

## PROMPT TEMPLATE

"Given this user profile and current decision, simulate 3 future outcomes over 7 days. Be realistic—not generic. Include specific metrics based on historical patterns. Quantify impact where possible. Format as JSON."

## INTEGRATION POINTS

- **Input**: User context from Memory Manager + current decision
- **Output**: 3 scenarios to Decision Evaluator
- **Used By**: Intervention Engine (recommendations)
