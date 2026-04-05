"""
Digital Twin Agent - A companion that mirrors your behavior and helps with decisions.
Uses your past behavior data to provide personalized advice considering your feelings and patterns.
"""

from typing import Dict, Optional
from datetime import datetime
from behavior_manager import BehaviorManager


class DigitalTwinAgent:
    """
    Your personal digital twin that knows your patterns and helps you make better decisions.
    Considers your emotions, values, and past behavior.
    """

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.behavior_manager = BehaviorManager(user_id)
        self.conversation_history = []

    def analyze_situation(self, situation: str, emotion: Optional[str] = None) -> Dict:
        """
        Analyze a situation based on your past behavior and current feelings.
        
        Args:
            situation: What's happening or what you're thinking about
            emotion: How you're feeling (tired, happy, stressed, etc.)
        
        Returns:
            Analysis with insights specific to YOU
        """
        
        # Get your profile
        profile = self.behavior_manager.get_user_profile()
        traits = self.behavior_manager.get_personality_traits()
        context = self.behavior_manager.get_context_for_decision(situation)
        
        # Generate personalized analysis
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "situation": situation,
            "user_emotion": emotion or "neutral",
            "your_personality": self._describe_you(traits),
            "your_pattern_in_this": self._what_you_typically_do(context),
            "rationale": self._provide_rationale(situation, traits, context, emotion),
            "recommendation": self._recommend_based_on_you(context, emotion),
            "reasoning": self._explain_reasoning(traits, emotion)
        }
        
        self.conversation_history.append(analysis)
        return analysis

    def _describe_you(self, traits: Dict) -> str:
        """Describe the user's personality based on their data."""
        if not traits:
            return "I'm still learning about you..."
        
        amb = traits.get("ambition_score", 0)
        bal = traits.get("balance_score", 0)
        com = traits.get("comfort_score", 0)
        
        descriptions = []
        
        if amb > 40:
            descriptions.append("You're quite ambitious and action-oriented 💪")
        elif bal > 40:
            descriptions.append("You tend to balance effort with rest 🎯")
        else:
            descriptions.append("You value comfort and taking it easy 😴")
        
        if traits.get("decision_frequency", 0) > 10:
            descriptions.append("You make thoughtful decisions regularly")
        
        primary = traits.get("primary_interest", "")
        if primary and primary != "unknown":
            descriptions.append(f"Your decisions often center around {primary}")
        
        return " ".join(descriptions)

    def _what_you_typically_do(self, context: Dict) -> str:
        """Explain what the user typically does in similar situations."""
        similar = context.get("similar_past_decisions", [])
        category = context.get("category", "")
        
        if not similar:
            return f"This is a new type of decision for you - first time with {category}!"
        
        # Count what they usually choose
        choice_summary = {}
        for decision in similar:
            choice = decision.get("chosen_option", "")
            if "minimal" in choice.lower():
                effort = "minimal"
            elif "maximum" in choice.lower():
                effort = "maximum"
            else:
                effort = "balanced"
            
            choice_summary[effort] = choice_summary.get(effort, 0) + 1
        
        most_common = max(choice_summary, key=choice_summary.get)
        
        effort_text = {
            "minimal": "usually prefer to take it easy",
            "balanced": "usually go for the middle ground",
            "maximum": "usually go all-in"
        }
        
        return f"In {category} decisions, you {effort_text.get(most_common, 'go balanced')} ({len(similar)} similar decisions)"

    def _provide_rationale(self, situation: str, traits: Dict, context: Dict, emotion: Optional[str]) -> str:
        """Provide reasoning for the recommendation."""
        
        rationale = []
        
        # Emotional context
        if emotion:
            emotion_impacts = {
                "tired": "You're tired, so lighter options might be better for you",
                "stressed": "Stress doesn't help - consider a balanced approach",
                "happy": "In a good mood, this is a great time to push yourself!",
                "anxious": "Anxiety says slow down - don't overcommit",
                "motivated": "You're motivated - dive in if it aligns with your goals"
            }
            if emotion.lower() in emotion_impacts:
                rationale.append(emotion_impacts[emotion.lower()])
        
        # Personality-based rationale
        if traits:
            amb = traits.get("ambition_score", 0)
            if amb > 50:
                rationale.append("You're ambitious - consider pushing your limits")
            else:
                rationale.append("For you, sustainable effort beats burnout")
        
        # Pattern-based rationale
        similar = context.get("similar_past_decisions", [])
        if similar:
            recent = similar[-1]
            rationale.append(f"Last time in {context.get('category')}: you chose {recent.get('chosen_option', 'a middle path')}")
        
        return " | ".join(rationale) if rationale else "Based on your patterns..."

    def _recommend_based_on_you(self, context: Dict, emotion: Optional[str]) -> str:
        """Give a personalized recommendation."""
        preferred_style = context.get("preferred_style", "balanced")
        emotion_lower = (emotion or "").lower()
        
        # Adjust based on emotion
        if emotion_lower in ["tired", "stressed", "anxious"]:
            return "💙 Recommendation: Go lighter than usual. You need energy management."
        elif emotion_lower in ["motivated", "happy", "energized"]:
            return "🚀 Recommendation: This is your moment! Go for the challenge."
        
        # Default to their pattern
        if preferred_style == "minimal":
            return "😴 Recommendation: Rest is valid. Recharge when you can."
        elif preferred_style == "maximum":
            return "💪 Recommendation: You've got this. Go for it!"
        else:
            return "🎯 Recommendation: Balanced approach works best for you. Sustainable wins."

    def _explain_reasoning(self, traits: Dict, emotion: Optional[str]) -> str:
        """Explain why the recommendation makes sense for THIS user."""
        
        if traits.get("balance_score", 0) > 40:
            return "Your track record shows balanced choices serve you well. They prevent burnout while maintaining progress."
        elif traits.get("ambition_score", 0) > 40:
            return "You're wired for achievement. Your best results come from pushing yourself within reason."
        elif traits.get("comfort_score", 0) > 40:
            return "Well-being matters to you. That's healthy. Honor that while still growing."
        else:
            return "Your patterns suggest this approach will work best for your situation."

    def record_choice_and_outcome(self, 
                                 decision: str,
                                 your_choice: str,
                                 how_it_went: str,
                                 emotion: Optional[str] = None) -> Dict:
        """
        Record what you actually did and how it went.
        This trains your digital twin to know you better.
        """
        
        # Save to behavior manager
        self.behavior_manager.save_choice(
            decision_question=decision,
            chosen_option=your_choice,
            option_details={"outcome": how_it_went},
            emotion=emotion,
            reasoning=f"User reported: {how_it_went}"
        )
        
        return {
            "status": "recorded",
            "message": f"✅ I've learned: When you {decision}, you chose {your_choice} and {how_it_went}",
            "learning": f"This strengthens my understanding of your decision-making",
            "data_points": len(self.behavior_manager.behavior_data["decisions"])
        }

    def get_mirror_summary(self) -> Dict:
        """Get a summary of what your digital twin knows about you."""
        profile = self.behavior_manager.get_user_profile()
        traits = self.behavior_manager.get_personality_traits()
        
        return {
            "total_decisions_learned": profile.get("total_decisions", 0),
            "who_you_are": profile.get("profile_summary", "Getting to know you..."),
            "your_traits": traits,
            "your_style": profile.get("preferred_effort_level", "balanced"),
            "categories_tracked": list(profile.get("decision_categories", {}).keys()),
            "recent_patterns": [
                f"{d['question'][:40]}... → {d['choice']}"
                for d in self.behavior_manager.behavior_data["past_choices"][-5:]
            ]
        }

    def ask_followup(self, topic: str) -> str:
        """Ask clarifying questions to better understand you."""
        followup_questions = {
            "health": "How's your energy level today? That often affects health decisions.",
            "education": "Are you interested in this subject, or does it feel like an obligation?",
            "work": "Is this deadline real, or flexible? Impacts whether to push hard.",
            "social": "Do you're feeling sociable today, or prefer solo time?",
            "rest": "On a scale of 1-10, how tired are you?",
            "productivity": "What's motivating you right now - external pressure or internal drive?",
            "personal": "How much time/energy do you have for this today?"
        }
        
        return followup_questions.get(topic, 
                                     "What's your current mood and energy level?")
