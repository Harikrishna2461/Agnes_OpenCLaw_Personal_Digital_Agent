"""
Production WhatsApp Integration for LSA via OpenClaw.
Receives real WhatsApp messages and responds directly.
"""

# Suppress TensorFlow warnings and improve startup time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import logging
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from main import LifeSimulationAgent
import requests
from flask import Flask, request, jsonify
from typing import Optional, Dict

logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


class LSAWhatsAppServer:
    """
    Production WhatsApp server for LSA.
    Receives WebhookBodies and sends responses via OpenClaw.
    """

    def __init__(self, api_key: str, phone_number: str, webhook_token: str = "lsa_secure_token"):
        """
        Initialize WhatsApp server.

        Args:
            api_key: Agnes Claw API key
            phone_number: WhatsApp number (+91 7010384691)
            webhook_token: Security token for webhook validation
        """
        self.api_key = api_key
        self.phone_number = phone_number
        self.webhook_token = webhook_token
        self.base_url = "https://api.agnesai.com/v1"
        self.agent = LifeSimulationAgent()
        self.message_queue = []

        logger.info(f"✅ WhatsApp Server initialized for {phone_number}")

    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send WhatsApp message via OpenClaw API.

        Args:
            to_number: Recipient number (format: +91 7010384691)
            message: Message text

        Returns:
            True if sent successfully
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "channel": "whatsapp",
                "phone_number": to_number,
                "message": message,
                "timestamp": datetime.now().isoformat(),
            }

            response = requests.post(
                f"{self.base_url}/messages/send",
                json=payload,
                headers=headers,
                timeout=15,
            )

            if response.status_code == 200:
                logger.info(f"✅ Message sent to {to_number}")
                return True
            else:
                logger.error(f"❌ Failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"❌ Send error: {e}")
            return False

    def handle_incoming_message(self, message_body: str, from_number: str) -> str:
        """
        Process incoming WhatsApp message and generate response.

        Args:
            message_body: User message text
            from_number: Sender number

        Returns:
            Response message
        """

        logger.info(f"📨 Received from {from_number}: {message_body}")

        # Log as memory if it's an event
        if any(
            word in message_body.lower()
            for word in ["completed", "did", "finished", "tried", "done", "just"]
        ):
            try:
                self.agent.log_event(
                    content=message_body,
                    category="whatsapp_event",
                    tags=["user_reported"],
                )
                logger.info(f"💾 Event logged")
            except Exception as e:
                logger.error(f"Failed to log: {e}")

        # Simulate if it's a decision
        if any(
            word in message_body.lower()
            for word in ["should", "consider", "planning", "thinking", "maybe", "can i", "could i"]
        ):
            try:
                result = self.agent.simulate_decision(message_body)
                rec = result["recommendation"]

                response = f"""🤖 *LSA Decision Analysis*

📌 *Decision:*
{message_body}

🎯 *Scenarios (7 days):*
A - Continue: Risk ⚠️
B - Moderate: Low Risk ✓
C - Optimal: Medium Risk

✅ *Recommendation:* {rec}

📊 *Scores:*
A = {result['scores']['A: Continue Current Behavior']:.0f}
B = {result['scores']['B: Moderate Improvement']:.0f}
C = {result['scores']['C: Optimal Behavior']:.0f}

💡 Higher score = better outcome"""

                return response
            except Exception as e:
                logger.error(f"Simulation error: {e}")
                return "❌ Error analyzing decision"

        # Handle commands
        if message_body.startswith("/"):
            return self.handle_command(message_body)

        # Default: status
        try:
            report = self.agent.get_daily_report()
            consistency = min(100, report['key_metrics']['consistency'])
            response = f"""📊 *LSA Today*

📈 Activities: {report['activities_today']}
⭐ Avg Impact: {report['key_metrics']['avg_impact']:.1f}/10
🎯 Consistency: {consistency:.0f}%

✨ Keep progressing!
Type /help for commands"""
            return response
        except Exception as e:
            logger.error(f"Report error: {e}")
            return "Error generating report"

    def handle_command(self, cmd: str) -> str:
        """Handle WhatsApp commands."""

        if cmd == "/status":
            try:
                report = self.agent.get_daily_report()
                consistency = min(100, report['key_metrics']['consistency'])
                return f"📊 Activities: {report['activities_today']}\n🎯 Consistency: {consistency:.0f}%"
            except:
                return "Error getting status"

        elif cmd == "/weekly":
            try:
                report = self.agent.get_weekly_report()
                return f"📈 Weekly analysis complete"
            except:
                return "Error getting weekly report"

        elif cmd == "/help":
            return """🤖 *LSA Commands*

*/status* - Daily summary
*/weekly* - Weekly report
*/export* - Download data
*/help* - This menu

📝 *Ask decisions:*
"Should I skip study?"

📝 *Log events:*
"Completed 2h study"

Type anything to chat!"""

        elif cmd == "/export":
            try:
                path = self.agent.export_data()
                return f"✅ Exported to {path}"
            except:
                return "Error exporting"

        else:
            return "Unknown command. Type /help"

    def validate_webhook(self, token: str) -> bool:
        """Validate webhook security token."""
        return token == self.webhook_token


# Global server instance
whatsapp_server: Optional[LSAWhatsAppServer] = None


def init_server():
    """Initialize WhatsApp server."""
    global whatsapp_server
    
    api_key = os.getenv("AGNES_CLAW_API_KEY", "")
    phone = os.getenv("WHATSAPP_USER_NUMBER", "+917010384691")
    token = os.getenv("WEBHOOK_TOKEN", "lsa_secure_token")

    if not api_key:
        logger.error("❌ AGNES_CLAW_API_KEY not set")
        return False

    whatsapp_server = LSAWhatsAppServer(api_key, phone, token)
    return True


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "LSA WhatsApp",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/webhook/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """
    Receive WhatsApp messages via webhook.
    
    Expected payload:
    {
        "from": "+917010384691",
        "message": "user message",
        "token": "webhook_token"
    }
    """
    try:
        # Get data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data"}), 400

        # Validate token
        token = data.get("token", "")
        if not whatsapp_server.validate_webhook(token):
            logger.warning(f"❌ Invalid webhook token")
            return jsonify({"error": "Unauthorized"}), 401

        # Extract message info
        from_number = data.get("from", "").strip()
        message_text = data.get("message", "").strip()

        if not from_number or not message_text:
            return jsonify({"error": "Missing fields"}), 400

        logger.info(f"✅ Webhook received from {from_number}")

        # Process message
        response_text = whatsapp_server.handle_incoming_message(message_text, from_number)

        # Send response
        success = whatsapp_server.send_message(from_number, response_text)

        return jsonify({
            "status": "ok",
            "sent": success,
            "response_preview": response_text[:100]
        }), 200

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/webhook/verify", methods=["GET"])
def verify_webhook():
    """Verify webhook is working."""
    return jsonify({
        "status": "verified",
        "message": "LSA WhatsApp webhook is active",
        "endpoint": "/webhook/whatsapp"
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Server error"}), 500


def start_server(host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
    """Start Flask server."""
    if not init_server():
        logger.error("❌ Failed to initialize server")
        return

    logger.info(f"🚀 Starting LSA WhatsApp Server...")
    logger.info(f"📱 WhatsApp: {whatsapp_server.phone_number}")
    logger.info(f"🌐 Webhook: http://{host}:{port}/webhook/whatsapp")
    logger.info(f"📊 Health: http://{host}:{port}/health")
    logger.info(f"✅ Verify: http://{host}:{port}/webhook/verify")

    app.run(
        host=host,
        port=port,
        debug=False,
        use_reloader=False,
        threaded=True,
    )


if __name__ == "__main__":
    import sys
    import argparse
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("lsa_whatsapp_server.log"),
            logging.StreamHandler(),
        ],
    )

    parser = argparse.ArgumentParser(description="LSA WhatsApp Server")
    parser.add_argument("--port", type=int, default=5000, help="Port to run server on (default: 5000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    print("""
╔════════════════════════════════════════════════════════════╗
║         LSA WhatsApp Server (Production Ready)             ║
╚════════════════════════════════════════════════════════════╝

Starting WhatsApp webhook server...
""")

    start_server(host=args.host, port=args.port, debug=args.debug)
