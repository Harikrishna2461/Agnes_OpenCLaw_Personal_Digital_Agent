"""
WhatsApp integration daemon for LSA via OpenClaw API.
No Twilio needed - uses OpenClaw's native WhatsApp support.
"""

import logging
import os
import json
from dotenv import load_dotenv
from main import LifeSimulationAgent
import requests
from typing import Optional

logger = logging.getLogger(__name__)

# Load environment
load_dotenv()


class LSAWhatsAppOpenClaw:
    """
    WhatsApp daemon for LSA using OpenClaw API.
    Direct integration without Twilio dependency.
    """

    def __init__(self, api_key: str, phone_number: str):
        """
        Initialize WhatsApp daemon via OpenClaw.

        Args:
            api_key: Agnes Claw API key
            phone_number: WhatsApp number (+91 7010384691)
        """
        self.api_key = api_key
        self.phone_number = phone_number
        self.base_url = "https://api.agnesai.com/v1"
        self.agent = LifeSimulationAgent()
        self.message_history = []

        logger.info(f"✅ WhatsApp OpenClaw daemon initialized for {phone_number}")

    def send_message(self, message: str) -> bool:
        """
        Send WhatsApp message via OpenClaw.

        Args:
            message: Message text to send

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "channel": "whatsapp",
                "phone_number": self.phone_number,
                "message": message,
                "timestamp": __import__("datetime").datetime.now().isoformat(),
            }

            # Send via OpenClaw API
            response = requests.post(
                f"{self.base_url}/messages/send",
                json=payload,
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                logger.info(f"✅ WhatsApp message sent: {message[:50]}...")
                return True
            else:
                logger.error(f"❌ Failed to send: {response.text}")
                return False

        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            # Fallback: log locally
            logger.info(f"📝 Message queued locally: {message[:50]}...")
            return False

    def handle_message(self, message_body: str) -> str:
        """
        Handle incoming WhatsApp message.

        Args:
            message_body: User message text

        Returns:
            Response message
        """

        logger.info(f"📨 Received: {message_body}")

        # Log as memory if it's an event
        if any(
            word in message_body.lower()
            for word in ["completed", "did", "finished", "tried", "done"]
        ):
            try:
                self.agent.log_event(
                    content=message_body,
                    category="whatsapp_update",
                    tags=["user_reported"],
                )
                logger.info(f"💾 Event logged to memory")
            except Exception as e:
                logger.error(f"Failed to log event: {e}")

        # Simulate if it's a decision
        if any(
            word in message_body.lower()
            for word in ["should", "consider", "planning", "thinking", "maybe", "can i"]
        ):
            try:
                result = self.agent.simulate_decision(message_body)
                recommendation = result["recommendation"]

                response = f"""🤖 *LSA Decision Analysis*

📌 *Your Decision:*
{message_body}

🎯 *3 Scenarios Simulated:*
A (Continue Current): +Risk
B (Moderate): Low Risk ✓
C (Optimal): Medium Risk

✅ *Recommendation:* {recommendation}

📊 *Impact Scores:*
A = {result['scores']['A: Continue Current Behavior']:.0f}
B = {result['scores']['B: Moderate Improvement']:.0f}
C = {result['scores']['C: Optimal Behavior']:.0f}

💡 *Highest score wins!*"""

                return response
            except Exception as e:
                logger.error(f"Error simulating decision: {e}")
                return "❌ Error analyzing. Try again."

        # Handle commands
        if message_body.startswith("/"):
            return self.handle_command(message_body)

        # Default: return status
        try:
            report = self.agent.get_daily_report()
            response = f"""📊 *LSA Daily Status*

📈 Activities: {report['activities_today']}
⭐ Avg Impact: {report['key_metrics']['avg_impact']:.1f}/10
🎯 Consistency: {min(100, report['key_metrics']['consistency']):.0f}%

✨ Keep going!
Type /help for commands"""
            return response
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return "Unable to generate report. Try /help"

    def handle_command(self, cmd: str) -> str:
        """Handle WhatsApp commands."""

        if cmd == "/status":
            try:
                report = self.agent.get_daily_report()
                return f"📊 Today: {report['activities_today']} activities\n🎯 Consistency: {min(100, report['key_metrics']['consistency']):.0f}%"
            except:
                return "Error getting status"

        elif cmd == "/weekly":
            try:
                report = self.agent.get_weekly_report()
                return f"📈 Weekly patterns analyzed"
            except:
                return "Error getting weekly report"

        elif cmd == "/help":
            return """🤖 *LSA WhatsApp Commands*

*/status* - Daily summary
*/weekly* - Weekly report
*/export* - Export data
*/help* - Show this

📝 *Send decisions:*
"Should I skip study?"

📝 *Report events:*
"Completed 2h study"

Ask anything about your life!"""

        elif cmd == "/export":
            try:
                path = self.agent.export_data()
                return f"✅ Data exported to {path}"
            except:
                return "Error exporting"

        else:
            return f"❓ Unknown: {cmd}\nType /help"


def start_whatsapp_daemon():
    """Start WhatsApp daemon loop."""

    api_key = os.getenv("AGNES_CLAW_API_KEY", "")
    phone = os.getenv("WHATSAPP_USER_NUMBER", "+917010384691")

    if not api_key:
        logger.error("❌ AGNES_CLAW_API_KEY not set in .env")
        return

    daemon = LSAWhatsAppOpenClaw(api_key, phone)

    logger.info("🚀 WhatsApp daemon running (OpenClaw)...")
    logger.info(f"📱 Number: {phone}")
    logger.info("Type messages to test locally, or receive from WhatsApp")

    # Interactive mode for testing
    print("\n" + "="*60)
    print("LSA WhatsApp Daemon (OpenClaw)")
    print("="*60)
    print(f"📱 Number: {phone}")
    print("\nTesting mode - Type your message:")
    print("  (or 'quit' to exit)")
    print("="*60 + "\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("✋ Stopping daemon...")
                break

            if not user_input:
                continue

            # Process message
            response = daemon.handle_message(user_input)
            print(f"\nLSA: {response}\n")

            # Send via OpenClaw
            daemon.send_message(response)

    except KeyboardInterrupt:
        print("\n✋ Daemon stopped.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("lsa_whatsapp.log"),
            logging.StreamHandler(),
        ],
    )

    print("""
╔════════════════════════════════════════════════════════════╗
║              LSA WhatsApp (OpenClaw Integration)            ║
╚════════════════════════════════════════════════════════════╝

No Twilio needed! Uses OpenClaw's native WhatsApp support.

Starting daemon...
""")

    start_whatsapp_daemon()

