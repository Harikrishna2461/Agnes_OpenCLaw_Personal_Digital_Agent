"""
Intervention Engine: Sends proactive alerts and recommendations.
"""

import json
import logging
from datetime import datetime, time
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Alert:
    """Represents an intervention alert."""
    priority: str  # CRITICAL, HIGH, NORMAL
    observation: str
    predicted_impact: str
    recommendation: str
    confidence: float
    timing: str
    timestamp: str


class InterventionEngine:
    """Generates and sends proactive interventions."""

    def __init__(
        self,
        telegram_token: Optional[str] = None,
        user_id: Optional[str] = None,
        quiet_hours: tuple = (22, 8),
    ):
        """
        Initialize Intervention Engine.
        
        Args:
            telegram_token: Telegram bot token
            user_id: Target Telegram user ID
            quiet_hours: (start_hour, end_hour) for quiet period
        """
        self.telegram_token = telegram_token
        self.user_id = user_id
        self.quiet_hours = quiet_hours
        self.alerts_sent = []
        
        logger.info(
            f"Intervention Engine initialized. "
            f"Quiet hours: {quiet_hours[0]:02d}:00 - {quiet_hours[1]:02d}:00"
        )

    def generate_intervention(
        self,
        memory_patterns: Dict,
        scenarios: List,
        current_state: Dict,
    ) -> Optional[Alert]:
        """
        Analyze patterns and generate intervention if needed.
        
        Args:
            memory_patterns: Output from Memory.analyze_patterns()
            scenarios: List of Scenario objects from Simulation Engine
            current_state: Current user state (mood, energy, etc.)
        
        Returns:
            Alert object if intervention triggered, else None
        """
        
        # Check for triggers
        trigger = self._check_triggers(memory_patterns, scenarios, current_state)
        
        if not trigger:
            return None
        
        # Generate alert based on trigger
        alert = self._build_alert(
            trigger, memory_patterns, scenarios, current_state
        )
        
        logger.info(f"Intervention generated: {alert.priority} - {alert.observation[:50]}")
        
        return alert

    def _check_triggers(
        self,
        memory_patterns: Dict,
        scenarios: List,
        current_state: Dict,
    ) -> Optional[Dict]:
        """Check if any intervention trigger is activated."""
        
        # Trigger 1: Inactivity (no updates in 24h)
        if current_state.get("hours_since_update", 0) > 24:
            return {
                "type": "inactivity",
                "hours": current_state.get("hours_since_update", 0),
            }
        
        # Trigger 2: Bad decision (Scenario A predicts >30% negative impact)
        if scenarios and len(scenarios) > 0:
            scenario_a = scenarios[0]
            impacts = scenario_a.predicted_outcomes
            negative_impact = 100 - impacts.get("consistency_score", 50)
            
            if negative_impact > 30:
                return {
                    "type": "bad_decision",
                    "impact": negative_impact,
                }
        
        # Trigger 3: Goal deviation (trending down)
        declining_categories = [
            cat for cat, data in memory_patterns.items()
            if data.get("trend") == "declining"
        ]
        
        if len(declining_categories) > 1:
            return {
                "type": "goal_deviation",
                "categories": declining_categories,
            }
        
        # Trigger 4: Energy crash
        if current_state.get("energy", 5) < 3:
            return {
                "type": "energy_crash",
                "energy": current_state.get("energy", 0),
            }
        
        return None

    def _build_alert(
        self,
        trigger: Dict,
        memory_patterns: Dict,
        scenarios: List,
        current_state: Dict,
    ) -> Alert:
        """Build alert based on trigger type."""
        
        trigger_type = trigger.get("type")
        
        if trigger_type == "inactivity":
            return self._alert_inactivity(trigger, memory_patterns)
        
        elif trigger_type == "bad_decision":
            return self._alert_bad_decision(trigger, scenarios)
        
        elif trigger_type == "goal_deviation":
            return self._alert_goal_deviation(trigger, memory_patterns)
        
        elif trigger_type == "energy_crash":
            return self._alert_energy_crash(trigger, current_state)
        
        else:
            return Alert(
                priority="NORMAL",
                observation="System check triggered",
                predicted_impact="Minimal",
                recommendation="Continue current activities",
                confidence=50.0,
                timing="Anytime",
                timestamp=datetime.now().isoformat(),
            )

    def _alert_inactivity(self, trigger: Dict, memory_patterns: Dict) -> Alert:
        """Generate inactivity alert."""
        hours = trigger.get("hours", 0)
        
        return Alert(
            priority="HIGH" if hours > 36 else "NORMAL",
            observation=f"No activity logged in {hours} hours. Deviation from routine detected.",
            predicted_impact=f"Momentum loss: 15-25% consistency drop per day of inactivity.",
            recommendation="Log an activity (study session, workout, or reflection) to reestablish routine.",
            confidence=78.0,
            timing="Within next 2 hours",
            timestamp=datetime.now().isoformat(),
        )

    def _alert_bad_decision(self, trigger: Dict, scenarios: List) -> Alert:
        """Generate bad decision alert."""
        impact = trigger.get("impact", 0)
        scenario_a = scenarios[0] if scenarios else None
        
        return Alert(
            priority="CRITICAL" if impact > 40 else "HIGH",
            observation=f"Predicted consistency drop of {impact:.0f}% if continuing current path.",
            predicted_impact=(
                f"7-day outcome: {scenario_a.predicted_outcomes.get('goal_progress', 50)} "
                f"vs {scenarios[2].predicted_outcomes.get('goal_progress', 80)} with optimal action"
            ),
            recommendation=f"Shift to Scenario B or C. Effort required: Low-Moderate. Time: 45-60 min.",
            confidence=scenario_a.confidence_score,
            timing="Immediately",
            timestamp=datetime.now().isoformat(),
        )

    def _alert_goal_deviation(
        self, trigger: Dict, memory_patterns: Dict
    ) -> Alert:
        """Generate goal deviation alert."""
        categories = trigger.get("categories", [])
        
        return Alert(
            priority="HIGH",
            observation=f"Multiple areas declining: {', '.join(categories)}. Pattern indicates reduced commitment.",
            predicted_impact=f"Weekly goal achievement: 35-45% if trend continues.",
            recommendation=f"Refocus on {categories[0]}. Schedule 2 short sessions (20 min each) today.",
            confidence=81.0,
            timing="Within 12 hours",
            timestamp=datetime.now().isoformat(),
        )

    def _alert_energy_crash(self, trigger: Dict, current_state: Dict) -> Alert:
        """Generate energy crash alert."""
        energy = trigger.get("energy", 0)
        
        return Alert(
            priority="CRITICAL",
            observation=f"Energy level critically low ({energy}/10). Risk of burnout and decision quality degradation.",
            predicted_impact="High likelihood of poor decisions, habit abandonment in next 24h.",
            recommendation="Take 2-hour recovery break: walk (20 min) + rest (90 min). Do NOT force productivity.",
            confidence=88.0,
            timing="Next 30 minutes",
            timestamp=datetime.now().isoformat(),
        )

    async def send_telegram_alert(self, alert: Alert) -> bool:
        """
        Send alert via Telegram.
        
        Args:
            alert: Alert object to send
        
        Returns:
            True if sent successfully, False otherwise
        """
        
        if not self.telegram_token or not self.user_id:
            logger.warning("Telegram not configured. Logging alert instead.")
            logger.info(f"ALERT: {alert.observation}")
            return False
        
        # Check quiet hours
        if not self._should_send_now(alert.priority):
            logger.info(f"Alert deferred due to quiet hours: {alert.observation}")
            return False
        
        # Format message
        message = self._format_message(alert)
        
        try:
            # Send via Telegram (would use requests library in production)
            logger.info(f"Sending Telegram alert: {alert.priority}")
            # TODO: Implement actual Telegram sending
            self.alerts_sent.append(alert)
            return True
        
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
            return False

    def _should_send_now(self, priority: str) -> bool:
        """Check if alert should be sent based on priority and quiet hours."""
        now = datetime.now().time()
        start, end = self.quiet_hours
        
        # In quiet hours?
        if start < end:
            in_quiet = start <= now < time(end, 0)
        else:  # Quiet hours cross midnight
            in_quiet = now >= time(start, 0) or now < time(end, 0)
        
        # Only send CRITICAL alerts during quiet hours
        if in_quiet and priority != "CRITICAL":
            return False
        
        return True

    def _format_message(self, alert: Alert) -> str:
        """Format alert as Telegram message."""
        
        emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟡",
            "NORMAL": "🟢",
        }.get(alert.priority, "💡")
        
        message = f"""
{emoji} **{alert.priority} ALERT**

⚠️ **Observation:**
{alert.observation}

📉 **Predicted Impact:**
{alert.predicted_impact}

✅ **Recommended Action:**
{alert.recommendation}

🎯 **Confidence:** {alert.confidence:.0f}%
⏰ **Timing:** {alert.timing}
"""
        
        return message.strip()

    def get_alerts_summary(self) -> Dict:
        """Get summary of recent alerts."""
        
        return {
            "total_alerts_sent": len(self.alerts_sent),
            "recent_alerts": [
                {
                    "priority": a.priority,
                    "observation": a.observation,
                    "timestamp": a.timestamp,
                }
                for a in self.alerts_sent[-5:]
            ],
        }
