"""
Life Simulation Agent (LSA) - Main orchestration module.
Autonomous system for decision simulation and life optimization.
"""

import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

# Add skills to path
sys.path.insert(0, str(Path(__file__).parent / "skills"))

from simulation_engine.simulation import SimulationEngine, Scenario
from memory_manager.memory import MemoryManager
from intervention_engine.intervention import InterventionEngine, Alert

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("lsa_agent.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class LifeSimulationAgent:
    """Main LSA agent orchestrating all subsystems."""

    def __init__(
        self,
        data_dir: str = "./data",
        telegram_token: Optional[str] = None,
        telegram_user_id: Optional[str] = None,
    ):
        """
        Initialize the Life Simulation Agent.
        
        Args:
            data_dir: Directory for memory storage
            telegram_token: Telegram bot token
            telegram_user_id: Telegram user ID for alerts
        """
        self.memory_manager = MemoryManager(data_dir=data_dir)
        self.simulation_engine = SimulationEngine()
        self.intervention_engine = InterventionEngine(
            telegram_token=telegram_token,
            user_id=telegram_user_id,
        )
        
        self.data_dir = Path(data_dir)
        self.decisions_log = self.data_dir / "decisions.jsonl"
        
        logger.info(
            "Life Simulation Agent initialized with all subsystems ready"
        )

    def log_event(
        self,
        content: str,
        category: str,
        impact_score: float = 5.0,
        tags: Optional[List[str]] = None,
        context: Optional[Dict] = None,
    ) -> str:
        """
        Log a user event or action.
        
        Args:
            content: Description of the event
            category: Event category (study, health, productivity, etc.)
            impact_score: Impact score (0-10)
            tags: Optional tags
            context: Optional context data
        
        Returns:
            Memory ID
        """
        memory_id = self.memory_manager.add_memory(
            content=content,
            category=category,
            impact_score=impact_score,
            tags=tags,
            context=context,
        )
        
        logger.info(f"Event logged: {category} - {content[:50]}...")
        
        return memory_id

    def simulate_decision(
        self,
        decision: str,
        current_state: Optional[Dict] = None,
    ) -> Dict:
        """
        Simulate outcomes for a decision.
        
        Args:
            decision: Decision to simulate (e.g., "skip study session")
            current_state: Optional current user state
        
        Returns:
            Dict with scenarios and recommendation
        """
        
        # Build user context
        user_context = current_state or {
            "goals": "Study consistently, maintain health, build projects",
            "habits": "Daily study, exercise 3x/week",
            "mood": 7,
            "energy": 8,
            "routine": "Study 8am, exercise 5pm, wind down 11pm",
        }
        
        # Get recent history for context
        recent = self.memory_manager.get_recent_context(days=7)
        
        # Generate scenarios
        scenarios = self.simulation_engine.simulate_decision(
            user_context=user_context,
            current_decision=decision,
            memory_history=recent,
        )
        
        # Evaluate scenarios
        evaluation = self.simulation_engine.evaluate_scenarios(scenarios)
        
        logger.info(f"Decision simulated: {decision}")
        logger.info(f"Recommendation: {evaluation['recommendation']}")
        
        return {
            "decision": decision,
            "timestamp": datetime.now().isoformat(),
            "scenarios": {
                "A": {
                    "name": scenarios[0].name,
                    "description": scenarios[0].description,
                    "outcomes": scenarios[0].predicted_outcomes,
                    "risk": scenarios[0].risk_level,
                    "confidence": scenarios[0].confidence_score,
                    "regret": scenarios[0].regret_prediction,
                },
                "B": {
                    "name": scenarios[1].name,
                    "description": scenarios[1].description,
                    "outcomes": scenarios[1].predicted_outcomes,
                    "risk": scenarios[1].risk_level,
                    "confidence": scenarios[1].confidence_score,
                    "regret": scenarios[1].regret_prediction,
                },
                "C": {
                    "name": scenarios[2].name,
                    "description": scenarios[2].description,
                    "outcomes": scenarios[2].predicted_outcomes,
                    "risk": scenarios[2].risk_level,
                    "confidence": scenarios[2].confidence_score,
                    "regret": scenarios[2].regret_prediction,
                },
            },
            "recommendation": evaluation["recommendation"],
            "scores": evaluation["scores"],
        }

    async def check_intervention(self) -> Optional[Alert]:
        """
        Check if any intervention is needed and generate alert.
        
        Returns:
            Alert object if intervention needed, None otherwise
        """
        
        # Analyze current patterns
        patterns = self.memory_manager.analyze_patterns(days=30)
        
        # Get recent history for scenarios
        recent = self.memory_manager.get_recent_context(days=7)
        
        # Generate test scenarios for comparison
        scenarios = self.simulation_engine.simulate_decision(
            user_context={
                "goals": "Maintain consistency",
                "habits": "Established routines",
                "mood": 7,
                "energy": 7,
                "routine": "Normal daily routine",
            },
            current_decision="Continue as-is",
            memory_history=recent,
        )
        
        # Current state
        current_state = {
            "mood": 7,
            "energy": 7,
            "hours_since_update": self._get_hours_since_update(),
        }
        
        # Generate intervention if needed
        alert = self.intervention_engine.generate_intervention(
            memory_patterns=patterns,
            scenarios=scenarios,
            current_state=current_state,
        )
        
        if alert:
            logger.info(f"Intervention triggered: {alert.priority}")
        
        return alert

    def _get_hours_since_update(self) -> float:
        """Get hours since last memory entry."""
        
        memories = self.memory_manager.get_recent_context(days=1)
        
        if not memories:
            return 24.0
        
        last_time = memories[0]["timestamp"]
        last_dt = datetime.fromisoformat(last_time)
        hours = (datetime.now() - last_dt).total_seconds() / 3600
        
        return hours

    def get_daily_report(self) -> Dict:
        """Generate daily report."""
        
        patterns = self.memory_manager.analyze_patterns(days=1)
        recent = self.memory_manager.get_recent_context(days=7)
        
        report = {
            "date": datetime.now().isoformat(),
            "activities_today": len(self.memory_manager.get_recent_context(days=1)),
            "patterns": {
                cat: {
                    "count": data.get("count", 0),
                    "avg_impact": data.get("avg_impact", 0),
                    "trend": data.get("trend", "stable"),
                }
                for cat, data in patterns.items()
            },
            "key_metrics": {
                "consistency": min(100, len(recent) / 7 * 100),
                "avg_impact": sum(m.get("impact_score", 5) for m in recent) / max(1, len(recent)),
            },
        }
        
        return report

    def get_weekly_report(self) -> Dict:
        """Generate weekly report."""
        
        patterns_week = self.memory_manager.analyze_patterns(days=7)
        patterns_prev = self.memory_manager.analyze_patterns(days=14)
        
        report = {
            "week_ending": datetime.now().isoformat(),
            "this_week": patterns_week,
            "progress_vs_last_week": {
                cat: (
                    patterns_week.get(cat, {}).get("count", 0)
                    - patterns_prev.get(cat, {}).get("count", 0)
                )
                for cat in list(patterns_week.keys()) + list(patterns_prev.keys())
            },
            "behavioral_patterns": self.memory_manager.analyze_patterns(days=30),
        }
        
        return report

    def export_data(self, filename: str = "lsa_export.json") -> str:
        """Export all data for backup."""
        
        import json
        
        export_path = self.data_dir / filename
        
        data = {
            "export_date": datetime.now().isoformat(),
            "memories": self.memory_manager.get_all_memories(),
            "patterns": self.memory_manager.analyze_patterns(days=90),
        }
        
        with open(export_path, "w") as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Data exported to {export_path}")
        
        return str(export_path)


def demo_mode():
    """
    Demo function for hackathon.
    Shows decision simulation in action.
    """
    
    print("\n" + "="*60)
    print("LIFE SIMULATION AGENT (LSA) - DEMO MODE")
    print("="*60 + "\n")
    
    # Initialize agent
    agent = LifeSimulationAgent()
    
    # Add some sample memory for context
    print("📚 Loading sample memory context...")
    agent.log_event(
        "Completed full study session (2 hours)",
        category="study",
        impact_score=9.0,
        tags=["focused", "productive"],
    )
    agent.log_event(
        "Morning jog (30 min)",
        category="health",
        impact_score=8.0,
    )
    agent.log_event(
        "Afternoon work on project",
        category="productivity",
        impact_score=7.5,
    )
    
    # Demo decision 1
    print("\n🔮 SIMULATION 1: Skipping study session")
    print("-" * 60)
    
    decision1 = "I am planning to skip studying today and watch TV instead"
    result1 = agent.simulate_decision(decision1)
    
    print(f"\n📌 Decision: {result1['decision']}")
    print(f"\n🎯 Scenarios:")
    
    for scenario_key, scenario_data in result1["scenarios"].items():
        print(f"\n  Scenario {scenario_key}: {scenario_data['name']}")
        print(f"  Description: {scenario_data['description']}")
        print(f"  Risk Level: {scenario_data['risk']}")
        print(f"  Confidence: {scenario_data['confidence']:.0f}%")
        print(f"  Predicted Outcomes:")
        for metric, value in scenario_data['outcomes'].items():
            print(f"    - {metric}: {value}")
        if scenario_data['regret']:
            print(f"  Regret Prediction: {scenario_data['regret']}")
    
    print(f"\n✅ RECOMMENDATION: {result1['recommendation']}")
    print(f"   Scoring: {result1['scores']}")
    
    # Demo decision 2
    print("\n" + "="*60)
    print("\n🔮 SIMULATION 2: Committing to optimal study routine")
    print("-" * 60)
    
    decision2 = "I commit to studying for 2 hours every morning and exercising 4x this week"
    result2 = agent.simulate_decision(decision2)
    
    print(f"\n📌 Decision: {result2['decision']}")
    print(f"\n🎯 Scenarios:")
    
    for scenario_key, scenario_data in result2["scenarios"].items():
        print(f"\n  Scenario {scenario_key}: {scenario_data['name']}")
        print(f"  Description: {scenario_data['description']}")
        print(f"  Confidence: {scenario_data['confidence']:.0f}%")
        print(f"  Predicted Outcomes:")
        for metric, value in scenario_data['outcomes'].items():
            print(f"    - {metric}: {value}")
    
    print(f"\n✅ RECOMMENDATION: {result2['recommendation']}")
    
    # Show daily report
    print("\n" + "="*60)
    print("\n📊 Today's Report:")
    print("-" * 60)
    
    daily_report = agent.get_daily_report()
    print(f"Activities logged: {daily_report['activities_today']}")
    print(f"Average impact: {daily_report['key_metrics']['avg_impact']:.1f}/10")
    print(f"Consistency: {daily_report['key_metrics']['consistency']:.0f}%")
    
    print("\n" + "="*60)
    print("✨ DEMO COMPLETE - LSA Ready for Production")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Run demo
    demo_mode()
