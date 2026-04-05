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
        """Generate scenarios using heuristic fallback with DECISION-SPECIFIC details and DYNAMIC SCORES."""
        
        # Extract patterns from memory
        patterns = self._extract_patterns(memory_history)
        
        # Generate decision-specific scenario descriptions
        scenario_descriptions = self._generate_scenario_descriptions(current_decision, patterns)
        
        # Generate decision-specific outcome scores
        outcome_scores = self._generate_outcome_scores(current_decision, patterns)
        
        # Build scenarios based on decision
        scenarios = []
        
        # Scenario A: Minimal/Conservative choice
        scenario_a = Scenario(
            name="A: Minimal Effort / Conservative",
            description=scenario_descriptions[0],
            timeframe="7 days",
            predicted_outcomes=outcome_scores["A"],
            risk_level="low",
            confidence_score=85.0,
            key_metrics={
                "effort_level": "Minimal (0-10%)",
                "outcome": "Maintain status quo",
                "satisfaction": "Neutral to regretful"
            },
            regret_prediction="High regret. You'll likely wish you took action."
        )
        scenarios.append(scenario_a)
        
        # Scenario B: Balanced choice
        scenario_b = Scenario(
            name="B: Balanced / Moderate Effort (RECOMMENDED)",
            description=scenario_descriptions[1],
            timeframe="7 days",
            predicted_outcomes=outcome_scores["B"],
            risk_level="low",
            confidence_score=88.0,
            key_metrics={
                "effort_level": "Moderate (40-60%)",
                "outcome": "Sustainable progress",
                "satisfaction": "Good. Balanced effort & reward."
            },
            regret_prediction="Low regret. Best balance of effort and outcome."
        )
        scenarios.append(scenario_b)
        
        # Scenario C: High effort choice
        scenario_c = Scenario(
            name="C: Maximum Effort / Ambitious",
            description=scenario_descriptions[2],
            timeframe="7 days",
            predicted_outcomes=outcome_scores["C"],
            risk_level="high",
            confidence_score=72.0,
            key_metrics={
                "effort_level": "High (80-100%)",
                "outcome": "Maximum results but exhausting",
                "satisfaction": "Accomplished but tired"
            },
            regret_prediction="Variable. May feel proud but burnt out. Not sustainable."
        )
        scenarios.append(scenario_c)
        
        return scenarios

    def _generate_outcome_scores(self, decision: str, patterns: Dict) -> Dict:
        """Generate DECISION-SPECIFIC outcome scores (not hardcoded)."""
        
        decision_lower = decision.lower()
        base_consistency = patterns.get("consistency", 60)
        base_progress = patterns.get("progress", 30)
        
        is_class = any(w in decision_lower for w in ["class", "attend", "school"])
        is_study = any(w in decision_lower for w in ["study", "homework", "exam"])
        is_work = any(w in decision_lower for w in ["work", "code", "project"])
        is_exercise = any(w in decision_lower for w in ["gym", "workout", "exercise"])
        is_rest = any(w in decision_lower for w in ["break", "rest", "vacation"])
        is_sleep = any(w in decision_lower for w in ["sleep", "nap"])
        
        is_skip = any(w in decision_lower for w in ["skip", "avoid", "ditch"])
        
        # Scenario A: Minimal effort - minimal gains
        if is_skip:
            cons_a, prog_a = base_consistency - 10, base_progress - 15
        else:
            cons_a, prog_a = base_consistency, base_progress
        
        # Scenario B: Balanced - good gains (1.5-1.8x multiplier)
        if is_class or is_study:
            cons_b, prog_b = min(90, int(base_consistency * 1.5)), int(base_progress * 1.8)
        elif is_exercise:
            cons_b, prog_b = min(95, int(base_consistency * 1.6)), int(base_progress * 2.0)
        elif is_work:
            cons_b, prog_b = min(85, int(base_consistency * 1.4)), int(base_progress * 2.2)
        else:
            cons_b, prog_b = min(100, int(base_consistency * 1.4)), int(base_progress * 1.8)
        
        # Scenario C: Maximum effort - best gains but high risk (2.5-3.5x multiplier)
        if is_class or is_study:
            cons_c, prog_c = 98, int(base_progress * 3.2)
        elif is_exercise:
            cons_c, prog_c = 99, int(base_progress * 3.8)
        elif is_work:
            cons_c, prog_c = 92, int(base_progress * 3.5)
        else:
            cons_c, prog_c = 95, int(base_progress * 3.0)
        
        return {
            "A": {
                "consistency_score": max(0, cons_a),
                "goal_progress": max(0, prog_a),
                "momentum_change": -5 if is_skip else 0,
                "energy_trend": -5,
            },
            "B": {
                "consistency_score": min(100, cons_b),
                "goal_progress": prog_b,
                "momentum_change": 15,
                "energy_trend": 8,
            },
            "C": {
                "consistency_score": min(100, cons_c),
                "goal_progress": prog_c,
                "momentum_change": 35,
                "energy_trend": 20,
            },
        }

    def _generate_scenario_descriptions(self, decision: str, patterns: Dict) -> List[str]:
        """Generate SPECIFIC scenario descriptions based on the user's actual decision."""
        
        decision_lower = decision.lower()
        
        # First, identify the DECISION TYPE (what activity/decision is being made)
        is_class_related = any(word in decision_lower for word in ["class", "classes", "attend", "school", "lecture", "course"])
        is_study_related = any(word in decision_lower for word in ["study", "study session", "homework", "assignment", "exam", "revise", "practice problem"])
        is_work_related = any(word in decision_lower for word in ["work", "code", "project", "job", "task", "deadline", "meeting"])
        is_exercise_related = any(word in decision_lower for word in ["exercise", "gym", "workout", "run", "walk", "sport", "yoga", "training"])
        is_rest_related = any(word in decision_lower for word in ["break", "rest", "vacation", "weekend", "relax", "chill"])
        is_sleep_related = any(word in decision_lower for word in ["sleep", "nap", "bed", "sleep in"])
        
        # Now identify the ACTION (should I do it, skip it, etc.)
        is_skip_action = any(word in decision_lower for word in ["skip", "avoid", "ditch", "bail", "not do", "not take"])
        
        # Scenario A: Minimal Effort / Don't Do It
        if is_class_related or (is_skip_action and "class" in decision_lower):
            desc_a = "Skip/avoid entirely. Sleep in, relax, no commitment. Short-term comfort but likely regret later about lost opportunity."
        elif is_study_related and is_skip_action:
            desc_a = "Don't do it at all. Stick to current routine. No new effort. Stay comfortable but miss learning."
        elif is_exercise_related or (is_skip_action and any(w in decision_lower for w in ["gym", "workout", "exercise"])):
            desc_a = "Skip exercise entirely. Stay home, relax. Short-term comfort but no fitness gains. Risk losing momentum."
        elif is_work_related and is_skip_action:
            desc_a = "Don't work on it. Procrastinate. Short-term relief but deadline stress builds."
        elif is_rest_related:
            desc_a = "No break. Keep grinding. No time off. Continue as-is. Risk burnout but maintain short-term momentum."
        elif is_sleep_related:
            desc_a = "Don't sleep. Keep working. Short-term productivity but health suffers."
        else:
            desc_a = "Do nothing / maintain current pattern. Risk staying stagnant but safe."
        
        # Scenario B: Balanced / Moderate Effort (RECOMMENDED)
        if is_class_related:
            desc_b = "Attend but come late (30 min) or leave early. Get 70% attendance. Compromise: some learning + some rest."
        elif is_study_related:
            desc_b = "Study for 60-90 minutes instead of 2-3 hours. Quality > quantity. Get meaningful progress with reasonable effort."
        elif is_work_related:
            desc_b = "Work for 1-2 more hours then stop. Productive progress without excessive overtime. Protect your sleep."
        elif is_exercise_related:
            desc_b = "30-minute workout instead of full session. Still active, less exhausting. Hit 70% of benefits."
        elif is_rest_related:
            desc_b = "Take partial break (3-4 days). Recharge without fully stopping. Find balance between rest and momentum."
        elif is_sleep_related:
            desc_b = "Take 20-30 minute nap. Quick refresh without affecting nighttime sleep. Energy boost."
        else:
            desc_b = "Moderate approach. Apply 50% effort for balanced results."
        
        # Scenario C: Maximum Effort / Full Commitment
        if is_class_related:
            desc_c = "Attend full class + review notes after. 100% engagement. Maximum learning but uses your evening."
        elif is_study_related:
            desc_c = "Study 2-3 hours intensely as planned. Deep understanding. Finish assignments early. High output, energy-draining."
        elif is_work_related:
            desc_c = "Work 3+ extra hours. Complete multiple projects/tasks. Major progress but risk tomorrow's fatigue."
        elif is_exercise_related:
            desc_c = "Full 90-minute workout + stretching. Maximum fitness gains. Feel accomplished but very tired after."
        elif is_rest_related:
            desc_c = "Full 1-week break. Complete rest. Maximum recovery. Back at 100% but lose momentum."
        elif is_sleep_related:
            desc_c = "Full 2-3 hour deep sleep. Complete rest. Maximum recovery but may affect night sleep."
        else:
            desc_c = "Go all-in. Maximum effort and commitment. Highest returns but most taxing."
        
        return [desc_a, desc_b, desc_c]

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
