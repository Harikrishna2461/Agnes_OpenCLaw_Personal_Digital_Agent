"""
Context-Aware LSA - Life Simulation Agent that generates relevant options for YOUR specific decision.
No more irrelevant options. Generates A/B/C specific to what you're asking about.
"""

from typing import Dict, Optional
from behavior_manager import BehaviorManager


class ContextAwareLSA:
    """
    LSA that understands your specific decision and generates relevant options.
    Uses past behavior to inform scenario generation.
    """

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.behavior_manager = BehaviorManager(user_id)
        
        # Knowledge base for relevant options
        self.decision_templates = {
            "skip": {
                "A": "Skip entirely",
                "B": "Partially attend/participate",
                "C": "Full participation"
            },
            "time": {
                "A": "Quick version (minimal time)",
                "B": "Normal duration",
                "C": "Extended/deep dive"
            },
            "effort": {
                "A": "Minimal effort approach",
                "B": "Balanced/moderate effort",
                "C": "Maximum effort approach"
            },
            "social": {
                "A": "Solo/alone",
                "B": "With a few people",
                "C": "Large group"
            },
            "commitment": {
                "A": "Try it casually",
                "B": "Moderate commitment",
                "C": "Full commitment"
            }
        }

    def simulate_decision(self, decision_question: str) -> Dict:
        """
        Generate relevant A/B/C options for THIS specific decision.
        
        Args:
            decision_question: What the user is asking about
        
        Returns:
            Relevant scenarios with scoring
        """
        
        # Get user context
        context = self.behavior_manager.get_context_for_decision(decision_question)
        profile = self.behavior_manager.get_user_profile()
        
        # Parse what type of decision this is
        decision_type = self._identify_decision_type(decision_question)
        
        # Generate relevant scenarios
        scenarios = self._generate_relevant_scenarios(
            decision_question,
            decision_type,
            context,
            profile
        )
        
        # Score based on user's preferences
        scores = self._score_scenarios(scenarios, context)
        
        # Find recommendation
        recommendation = self._recommend_for_user(scenarios, scores, profile)
        
        return {
            "question": decision_question,
            "category": context.get("category", "general"),
            "user_style": context.get("preferred_style", "balanced"),
            "scenarios": scenarios,
            "scores": scores,
            "recommendation": recommendation,
            "reasoning": self._explain_recommendation(scenarios, scores, context),
            "user_context": f"Based on {len(profile.get('decision_categories', {}))} past {context.get('category')} decisions"
        }

    def _identify_decision_type(self, question: str) -> str:
        """Identify the type of decision being made."""
        q_lower = question.lower()
        
        if any(w in q_lower for w in ["skip", "skip", "avoid", "miss"]):
            return "skip"
        elif any(w in q_lower for w in ["how long", "time", "hours", "minutes", "duration"]):
            return "time"
        elif any(w in q_lower for w in ["social", "with", "who", "alone", "by myself"]):
            return "social"
        elif any(w in q_lower for w in ["commit", "how much", "level of", "intensity"]):
            return "commitment"
        else:
            return "effort"

    def _generate_relevant_scenarios(self, 
                                    question: str, 
                                    decision_type: str,
                                    context: Dict,
                                    profile: Dict) -> Dict:
        """Generate A/B/C scenarios RELEVANT to the actual decision."""
        
        category = context.get("category", "general")
        
        # Generate specific A/B/C based on decision_question
        if decision_type == "skip":
            scenarios = self._generate_skip_scenarios(question, category)
        elif decision_type == "time":
            scenarios = self._generate_time_scenarios(question, category)
        elif decision_type == "social":
            scenarios = self._generate_social_scenarios(question, category)
        elif decision_type == "commitment":
            scenarios = self._generate_commitment_scenarios(question, category)
        else:
            scenarios = self._generate_effort_scenarios(question, category)
        
        return scenarios

    def _generate_skip_scenarios(self, question: str, category: str) -> Dict:
        """Generate skip-related options."""
        
        skip_templates = {
            "class": {
                "A": "Skip entirely, sleep in or rest",
                "B": "Attend but arrive late after other tasks",
                "C": "Attend fully, arrive on time and stay engaged"
            },
            "gym": {
                "A": "Skip - rest day, do something relaxing instead",
                "B": "Light workout - 20-30 min walk or stretching",
                "C": "Full workout - complete your normal routine"
            },
            "work": {
                "A": "Take the day off if possible",
                "B": "Work from home or flexible hours",
                "C": "Go in as planned, do your full shift"
            },
            "social": {
                "A": "Skip the event, stay home",
                "B": "Attend briefly, say hi then leave",
                "C": "Stay for the full event and engage"
            },
            "breakfast": {
                "A": "Skip breakfast, go without food until later",
                "B": "Quick snack - coffee and toast",
                "C": "Full breakfast - eat properly before starting"
            },
            "project": {
                "A": "Skip it entirely, don't do this today",
                "B": "Do a simplified version or partial work",
                "C": "Commit fully to completing it"
            }
        }
        
        # Try to match category from templates
        for key in skip_templates:
            if key in question.lower():
                return skip_templates[key]
        
        # Default skip template
        return {
            "A": f"Skip entirely - don't do this today at all",
            "B": f"Do a lighter/shorter version instead",
            "C": f"Commit fully to doing this as planned"
        }

    def _generate_time_scenarios(self, question: str, category: str) -> Dict:
        """Generate time-based options."""
        
        return {
            "A": f"Quick version - minimal time commitment (15-30 min)",
            "B": f"Normal time - standard duration (1 hour)",
            "C": f"Deep dive - block out significant time (2+ hours)"
        }

    def _generate_social_scenarios(self, question: str, category: str) -> Dict:
        """Generate social-interaction options."""
        
        return {
            "A": "Do this alone - solo, no one else involved",
            "B": "With a close friend or small group - social but low-key",
            "C": "With many people - larger group, more social interaction"
        }

    def _generate_commitment_scenarios(self, question: str, category: str) -> Dict:
        """Generate commitment-level options."""
        
        return {
            "A": "Casual approach - don't overcommit, keep it light",
            "B": "Moderate commitment - balanced involvement",
            "C": "Full commitment - go all-in with maximum dedication"
        }

    def _generate_effort_scenarios(self, question: str, category: str) -> Dict:
        """Generate effort-level options (default)."""
        
        # Extract the specific activity
        activity = question.replace("should", "").replace("can i", "").replace("?", "").strip()
        
        return {
            "A": f"Minimal effort - {activity} with bare minimum energy/involvement",
            "B": f"Balanced approach - {activity} with moderate effort and attention",
            "C": f"Maximum effort - {activity} with full commitment and excellence"
        }

    def _score_scenarios(self, scenarios: Dict, context: Dict) -> Dict:
        """Score scenarios based on user's past patterns."""
        
        preferred = context.get("preferred_style", "balanced")
        
        base_scores = {
            "minimal": 75,
            "balanced": 120,
            "maximum": 160
        }
        
        scores = {}
        for key, scenario in scenarios.items():
            scenario_lower = scenario.lower()
            
            # Determine effort level of this scenario
            if any(w in scenario_lower for w in ["minimal", "skip", "light", "casual", "quick"]):
                effort = "minimal"
            elif any(w in scenario_lower for w in ["maximum", "full", "all-in", "commitment", "dedication"]):
                effort = "maximum"
            else:
                effort = "balanced"
            
            base_score = base_scores[effort]
            
            # Adjust based on user's preference
            if effort == preferred:
                base_score += 30  # Boost if it matches their style
            
            scores[f"{key}: {scenario}"] = base_score
        
        return scores

    def _recommend_for_user(self, scenarios: Dict, scores: Dict, profile: Dict) -> str:
        """Recommend based on user's actual patterns."""
        
        preferred = profile.get("preferred_effort_level", "balanced")
        
        recommendations = {
            "minimal": "You typically prefer lighter options - Option A aligns with your style",
            "balanced": "Balanced approach works best for you - Option B is your sweet spot",
            "maximum": "You're ambitious and driven - Option C matches your energy"
        }
        
        return recommendations.get(preferred, "Option B (Balance) is usually your best bet")

    def _explain_recommendation(self, scenarios: Dict, scores: Dict, context: Dict) -> str:
        """Explain WHY this recommendation makes sense."""
        
        category = context.get("category", "general")
        past_count = context.get("past_behaviors_in_category", 0)
        
        if past_count > 0:
            return f"Based on your {past_count} past decisions in {category}, this aligns with your patterns."
        else:
            return f"This is your first {category} decision. The recommendation balances sustainability with progress."
