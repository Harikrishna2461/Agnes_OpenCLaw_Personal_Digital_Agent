"""
User Behavior Manager - Tracks decisions and behaviors for the digital twin.
Stores what decisions the user makes and uses them as context.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class BehaviorManager:
    """Tracks user behavior and decisions for personalization."""

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.data_dir = Path("data/users")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.user_file = self.data_dir / f"{user_id}_behavior.json"
        self.behavior_data = self._load_behavior_data()

    def _load_behavior_data(self) -> Dict:
        """Load user behavior data from file."""
        if self.user_file.exists():
            try:
                with open(self.user_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_behavior()
        return self._default_behavior()

    def _default_behavior(self) -> Dict:
        """Default behavior structure."""
        return {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "decisions": [],
            "patterns": {
                "preferred_effort_level": None,  # minimal, balanced, maximum
                "risk_tolerance": None,  # low, medium, high
                "decision_categories": {},  # category -> patterns
                "emotional_state": "neutral",
                "energy_level": "medium",
                "preference_trends": {}
            },
            "interests": [],
            "values": [],
            "past_choices": []
        }

    def save_choice(self, 
                   decision_question: str,
                   chosen_option: str,
                   option_details: Dict,
                   category: Optional[str] = None,
                   emotion: Optional[str] = None,
                   reasoning: Optional[str] = None) -> None:
        """Save a user's decision choice for future reference."""
        
        choice_entry = {
            "timestamp": datetime.now().isoformat(),
            "decision_question": decision_question,
            "chosen_option": chosen_option,
            "option_details": option_details,
            "category": category or self._categorize_decision(decision_question),
            "emotion": emotion,
            "reasoning": reasoning,
            "outcome": None  # Will be updated later
        }

        self.behavior_data["decisions"].append(choice_entry)
        self.behavior_data["past_choices"].append({
            "question": decision_question,
            "choice": chosen_option,
            "timestamp": choice_entry["timestamp"]
        })

        # Update patterns
        self._update_patterns(chosen_option, category)
        
        self._save_behavior_data()

    def _categorize_decision(self, question: str) -> str:
        """Auto-categorize decision based on keywords."""
        question_lower = question.lower()
        
        categories = {
            "health": ["gym", "exercise", "workout", "health", "sleep", "eat", "diet", "diet"],
            "education": ["class", "study", "homework", "exam", "lecture", "course", "learn"],
            "work": ["work", "job", "project", "deadline", "meeting", "presentation", "task"],
            "social": ["friend", "party", "hangout", "date", "social", "meet", "call"],
            "rest": ["break", "relax", "chill", "rest", "vacation", "time off", "nap"],
            "productivity": ["task", "project", "goal", "achieve", "complete", "finish"],
            "personal": ["hobby", "passion", "interest", "creative", "art", "music"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        return "general"

    def _update_patterns(self, chosen_option: str, category: str) -> None:
        """Update behavior patterns based on choice."""
        
        # Extract effort level from option
        if "minimal" in chosen_option.lower() or "avoid" in chosen_option.lower():
            effort = "minimal"
        elif "balanced" in chosen_option.lower() or "moderate" in chosen_option.lower():
            effort = "balanced"
        elif "maximum" in chosen_option.lower() or "ambitious" in chosen_option.lower():
            effort = "maximum"
        else:
            effort = "balanced"

        # Update preference trends
        if "preferred_effort_level" not in self.behavior_data["patterns"]:
            self.behavior_data["patterns"]["preferred_effort_level"] = {}
        
        if effort not in self.behavior_data["patterns"]["preferred_effort_level"]:
            self.behavior_data["patterns"]["preferred_effort_level"][effort] = 0
        self.behavior_data["patterns"]["preferred_effort_level"][effort] += 1

        # Update category patterns
        if category not in self.behavior_data["patterns"]["decision_categories"]:
            self.behavior_data["patterns"]["decision_categories"][category] = {
                "minimal": 0,
                "balanced": 0,
                "maximum": 0,
                "count": 0
            }
        
        self.behavior_data["patterns"]["decision_categories"][category][effort] += 1
        self.behavior_data["patterns"]["decision_categories"][category]["count"] += 1

    def _save_behavior_data(self) -> None:
        """Save behavior data to file."""
        with open(self.user_file, 'w') as f:
            json.dump(self.behavior_data, f, indent=2)

    def get_user_profile(self) -> Dict:
        """Get user behavior profile summary."""
        decisions = self.behavior_data["decisions"]
        
        if not decisions:
            return {
                "total_decisions": 0,
                "profile": "New user - no decisions yet",
                "preferred_style": "Unknown",
                "categories": {}
            }

        # Calculate preferences
        effort_counts = {}
        category_stats = {}
        
        for decision in decisions:
            # Count effort levels
            for effort in ["minimal", "balanced", "maximum"]:
                if effort in decision["chosen_option"].lower():
                    effort_counts[effort] = effort_counts.get(effort, 0) + 1
                    break
            
            # Category stats
            cat = decision.get("category", "general")
            if cat not in category_stats:
                category_stats[cat] = 0
            category_stats[cat] += 1

        preferred_effort = max(effort_counts, key=effort_counts.get, default="balanced")
        
        return {
            "total_decisions": len(decisions),
            "preferred_effort_level": preferred_effort,
            "effort_distribution": effort_counts,
            "decision_categories": category_stats,
            "recent_decisions": decisions[-5:],
            "profile_summary": self._generate_profile_text(preferred_effort, category_stats)
        }

    def _generate_profile_text(self, effort: str, categories: Dict) -> str:
        """Generate human-readable profile."""
        effort_text = {
            "minimal": "You tend to prefer comfort and rest 😴",
            "balanced": "You prefer balanced approaches 🎯",
            "maximum": "You're ambitious and action-oriented 💪"
        }
        
        top_category = max(categories, key=categories.get) if categories else "general"
        
        return f"{effort_text.get(effort, 'Balanced')}. Your most frequent decisions are about {top_category}."

    def get_context_for_decision(self, decision_question: str) -> Dict:
        """Get relevant context for a decision based on past behavior."""
        category = self._categorize_decision(decision_question)
        profile = self.get_user_profile()
        
        # Get similar past decisions
        similar_decisions = [
            d for d in self.behavior_data["decisions"]
            if d.get("category") == category
        ]

        return {
            "category": category,
            "user_profile": profile,
            "similar_past_decisions": similar_decisions[-3:],  # Last 3 similar
            "preferred_style": profile.get("preferred_effort_level", "balanced"),
            "past_behaviors_in_category": len(similar_decisions),
            "decision_history": self.behavior_data["past_choices"][-5:]  # Last 5 choices
        }

    def get_personality_traits(self) -> Dict:
        """Extract personality traits from behavior."""
        profile = self.get_user_profile()
        
        if profile["total_decisions"] == 0:
            return {}

        effort_dist = profile.get("effort_distribution", {})
        total = sum(effort_dist.values()) or 1
        
        return {
            "ambition_score": effort_dist.get("maximum", 0) / total * 100,
            "balance_score": effort_dist.get("balanced", 0) / total * 100,
            "comfort_score": effort_dist.get("minimal", 0) / total * 100,
            "decision_frequency": profile["total_decisions"],
            "primary_interest": max(profile.get("decision_categories", {}), 
                                   key=profile.get("decision_categories", {}).get, 
                                   default="unknown")
        }
