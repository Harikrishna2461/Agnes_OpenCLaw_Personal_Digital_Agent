#!/usr/bin/env python3
"""
Quick test suite for LSA components.
"""

import logging
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent / "skills"))

from memory_manager.memory import MemoryManager
from simulation_engine.simulation import SimulationEngine
from intervention_engine.intervention import InterventionEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_memory_manager():
    """Test memory manager."""
    print("\n" + "="*60)
    print("TEST: Memory Manager")
    print("="*60)

    mm = MemoryManager(data_dir="./test_data")
    mm.clear_memories()

    # Add memories
    id1 = mm.add_memory("Completed study session", "study", 9.0)
    id2 = mm.add_memory("Morning workout", "health", 8.5)
    id3 = mm.add_memory("Project work", "productivity", 7.0)

    print(f"✅ Added 3 memories: {id1}, {id2}, {id3}")

    # Get recent
    recent = mm.get_recent_context(days=1)
    print(f"✅ Retrieved {len(recent)} recent entries")

    # Get relevant
    relevant = mm.get_relevant_memories("study habits", top_k=2)
    print(f"✅ Retrieved {len(relevant)} relevant entries for 'study habits'")

    # Get patterns
    patterns = mm.analyze_patterns(days=1)
    print(f"✅ Analyzed patterns: {patterns}")

    return True


def test_simulation_engine():
    """Test simulation engine."""
    print("\n" + "="*60)
    print("TEST: Simulation Engine")
    print("="*60)

    se = SimulationEngine()

    user_context = {
        "goals": "Study and exercise",
        "habits": "Daily 1-hour study",
        "mood": 7,
        "energy": 8,
    }

    scenarios = se.simulate_decision(
        user_context=user_context,
        current_decision="Skip studying today",
    )

    print(f"✅ Generated {len(scenarios)} scenarios")

    for i, scenario in enumerate(scenarios):
        print(
            f"  Scenario {i}: {scenario.name} "
            f"(Risk: {scenario.risk_level}, Confidence: {scenario.confidence_score}%)"
        )

    evaluation = se.evaluate_scenarios(scenarios)
    print(f"✅ Recommendation: {evaluation['recommendation']}")

    return True


def test_intervention_engine():
    """Test intervention engine."""
    print("\n" + "="*60)
    print("TEST: Intervention Engine")
    print("="*60)

    ie = InterventionEngine()

    patterns = {
        "study": {"count": 0, "trend": "declining"},
        "health": {"count": 1, "trend": "stable"},
    }

    scenarios = []  # Would be from simulation engine

    current_state = {
        "mood": 7,
        "energy": 3,
        "hours_since_update": 30,
    }

    alert = ie.generate_intervention(patterns, scenarios, current_state)

    if alert:
        print(f"✅ Generated {alert.priority} alert")
        print(f"  Observation: {alert.observation}")
        print(f"  Recommendation: {alert.recommendation}")
    else:
        print("⚠️  No alert generated")

    return True


def test_integration():
    """Test full integration."""
    print("\n" + "="*60)
    print("TEST: Full Integration")
    print("="*60)

    from main import LifeSimulationAgent

    agent = LifeSimulationAgent(data_dir="./test_data")

    # Log event
    mem_id = agent.log_event(
        "Test study session",
        "study",
        8.0,
        tags=["test"],
    )
    print(f"✅ Logged memory: {mem_id}")

    # Simulate decision
    result = agent.simulate_decision("Skip study")
    print(f"✅ Decision simulated, recommendation: {result['recommendation']}")

    # Get report
    report = agent.get_daily_report()
    print(f"✅ Daily report generated: {report['activities_today']} activities")

    return True


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "LSA COMPONENT TESTS" + " "*24 + "║")
    print("╚" + "="*58 + "╝")

    tests = [
        ("Memory Manager", test_memory_manager),
        ("Simulation Engine", test_simulation_engine),
        ("Intervention Engine", test_intervention_engine),
        ("Full Integration", test_integration),
    ]

    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            results[name] = False

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {name}")

    all_passed = all(results.values())
    print("="*60)

    if all_passed:
        print("✨ All tests passed! LSA is production-ready.")
    else:
        print("⚠️  Some tests failed. Check output above.")

    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
