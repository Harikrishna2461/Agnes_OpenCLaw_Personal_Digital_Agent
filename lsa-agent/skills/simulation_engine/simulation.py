"""
Simulation Engine: Simulates future scenarios using LLM + historical patterns.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Scenario:
    """Represents a simulated scenario."""
    name: str
    description: str
    timeframe: str
    predicted_outcomes: Dict[str, float]
    risk_level: str
    confidence_score: float
    key_metrics: Dict[str, float]
    regret_prediction: Optional[str] = None


class SimulationEngine:
    """Simulates future outcomes for user decisions."""

    def __init__(self, llm_client=None):
        """
        Initialize Simulation Engine.
        
        Args:
            llm_client: LLM client for scenario generation (Agnes Claw Model)
        """
        self.llm_client = llm_client
        logger.info("Simulation Engine initialized")

    def simulate_decision(
        self,
        user_context: Dict,
        current_decision: str,
        memory_history: Optional[List[Dict]] = None,
    ) -> List[Scenario]:
        """
        Simulate 3 scenarios for a given decision.
        
        Args:
            user_context: Current user state (goals, habits, mood, etc.)
            current_decision: Decision to simulate (e.g., "skip study session")
            memory_history: Historical memory entries for pattern recognition
        
        Returns:
            List of 3 Scenarios (A, B, C)
        """
        # Build context string
        context_str = self._build_context_prompt(
            user_context, current_decision, memory_history
        )
        
        # Generate scenarios using LLM or fallback
        if self.llm_client:
            scenarios = self._generate_with_llm(context_str)
        else:
            scenarios = self._generate_fallback(
                user_context, current_decision, memory_history
            )
        
        logger.info(
            f"Simulated 3 scenarios for decision: {current_decision[:50]}..."
        )
        
        return scenarios

    def _build_context_prompt(
        self,
        user_context: Dict,
        current_decision: str,
        memory_history: Optional[List[Dict]] = None,
    ) -> str:
        """Build the prompt for scenario generation."""
        
        prompt = f"""
USER PROFILE:
- Goals: {user_context.get('goals', 'Not specified')}
- Current habits: {user_context.get('habits', 'Not specified')}
- Mood: {user_context.get('mood', 'Neutral')}
- Energy level: {user_context.get('energy', 'Normal')}
- Typical daily routine: {user_context.get('routine', 'Not specified')}

PAST PATTERNS (last 30 days):
"""
        
        if memory_history:
            categories = {}
            for mem in memory_history:
                cat = mem.get("category", "untagged")
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in categories.items():
                prompt += f"- {cat}: {count} entries\n"
        
        prompt += f"""
CURRENT DECISION: {current_decision}

TASK:
Simulate 3 scenarios for the next 7 days:
A. Continue current behavior (no change)
B. Moderate improvement (reasonable effort)
C. Optimal behavior (full commitment)

For each scenario provide:
1. Realistic, specific outcome predictions
2. Quantified impact metrics
3. Key risks and opportunities
4. Confidence score (0-100)

Format as JSON with 3 objects: scenario_a, scenario_b, scenario_c
Each needs: name, description, outcomes, risk_level, confidence_score, key_metrics
"""
        
        return prompt

    def _generate_with_llm(self, prompt: str) -> List[Scenario]:
        """Generate scenarios using LLM."""
        try:
            response = self.llm_client.generate(prompt)
            
            # Parse response
            data = json.loads(response)
            
            scenarios = [
                self._parse_scenario(data.get("scenario_a", {}), "A"),
                self._parse_scenario(data.get("scenario_b", {}), "B"),
                self._parse_scenario(data.get("scenario_c", {}), "C"),
            ]
            
            return scenarios
        except Exception as e:
            logger.error(f"LLM generation failed: {e}. Using fallback.")
            return []

    def _generate_fallback(
        self,
        user_context: Dict,
        current_decision: str,
        memory_history: Optional[List[Dict]] = None,
    ) -> List[Scenario]:
        """Generate scenarios using heuristic fallback."""
        
        # Extract patterns from memory
        patterns = self._extract_patterns(memory_history)
        
        # Build scenarios based on decision
        scenarios = []
        
        # Scenario A: Continue current
        scenario_a = Scenario(
            name="A: Continue Current Behavior",
            description=f"Maintain current pattern without changes",
            timeframe="7 days",
            predicted_outcomes={
                "consistency_score": patterns.get("consistency", 60),
                "goal_progress": patterns.get("progress", 30),
                "momentum_change": -5,
                "energy_trend": patterns.get("energy_trend", 0),
            },
            risk_level="moderate",
            confidence_score=75.0,
            key_metrics=patterns.get("metrics", {}),
            regret_prediction="Likely to maintain current trajectory; no progress on goals."
        )
        scenarios.append(scenario_a)
        
        # Scenario B: Moderate improvement
        scenario_b = Scenario(
            name="B: Moderate Improvement",
            description="Apply reasonable effort adjustments (30-50% increase)",
            timeframe="7 days",
            predicted_outcomes={
                "consistency_score": min(100, int(patterns.get("consistency", 60) * 1.3)),
                "goal_progress": int(patterns.get("progress", 30) * 1.5),
                "momentum_change": 15,
                "energy_trend": patterns.get("energy_trend", 0) + 10,
            },
            risk_level="low",
            confidence_score=82.0,
            key_metrics=patterns.get("metrics", {}),
            regret_prediction="Some effort required, but sustainable. Likely satisfied with progress."
        )
        scenarios.append(scenario_b)
        
        # Scenario C: Optimal
        scenario_c = Scenario(
            name="C: Optimal Behavior",
            description="Full commitment to recommendations",
            timeframe="7 days",
            predicted_outcomes={
                "consistency_score": 95,
                "goal_progress": int(patterns.get("progress", 30) * 2.5),
                "momentum_change": 35,
                "energy_trend": patterns.get("energy_trend", 0) + 20,
            },
            risk_level="medium",
            confidence_score=68.0,
            key_metrics=patterns.get("metrics", {}),
            regret_prediction="High short-term effort, but likely to feel accomplished and on-track."
        )
        scenarios.append(scenario_c)
        
        return scenarios

    def _extract_patterns(
        self, memory_history: Optional[List[Dict]]
    ) -> Dict:
        """Extract patterns from memory history."""
        
        if not memory_history:
            return {
                "consistency": 60,
                "progress": 30,
                "energy_trend": 0,
                "metrics": {
                    "daily_sessions": 1,
                    "avg_focus_time": 30,
                    "completion_rate": 0.6,
                },
            }
        
        # Calculate patterns
        total = len(memory_history)
        avg_impact = sum(m.get("impact_score", 5) for m in memory_history) / total if total > 0 else 5
        
        categories = {}
        for mem in memory_history:
            cat = mem.get("category", "other")
            categories[cat] = categories.get(cat, 0) + 1
        
        consistency = min(100, int((len(memory_history) / 30) * 100))
        progress = min(100, int(avg_impact * 10))
        
        return {
            "consistency": consistency,
            "progress": progress,
            "energy_trend": 5,
            "metrics": {
                "daily_sessions": len(memory_history) / max(1, (30 - len(memory_history) // 2)),
                "avg_focus_time": 40,
                "completion_rate": min(1.0, consistency / 100),
            },
        }

    def _parse_scenario(self, data: Dict, label: str) -> Scenario:
        """Parse a scenario from LLM response."""
        
        return Scenario(
            name=data.get("name", f"Scenario {label}"),
            description=data.get("description", ""),
            timeframe=data.get("timeframe", "7 days"),
            predicted_outcomes=data.get("predicted_outcomes", {}),
            risk_level=data.get("risk_level", "medium"),
            confidence_score=data.get("confidence_score", 70),
            key_metrics=data.get("key_metrics", {}),
            regret_prediction=data.get("regret_prediction"),
        )

    def evaluate_scenarios(self, scenarios: List[Scenario]) -> Dict:
        """
        Evaluate all scenarios and recommend best action.
        
        Returns:
            Dict with recommendation and scoring
        """
        
        scores = {}
        for scenario in scenarios:
            # Score based on: outcome + confidence + risk
            outcome_score = (
                scenario.predicted_outcomes.get("consistency_score", 50)
                + scenario.predicted_outcomes.get("goal_progress", 50)
            ) / 2
            
            risk_penalty = {
                "low": 0,
                "medium": 10,
                "high": 25,
            }.get(scenario.risk_level, 10)
            
            confidence_boost = scenario.confidence_score - 50
            
            total_score = outcome_score + confidence_boost - risk_penalty
            scores[scenario.name] = total_score
        
        best = max(scores, key=scores.get)
        
        return {
            "recommendation": best,
            "scores": scores,
            "reasoning": f"Combining outcome potential, confidence, and risk factors.",
        }
