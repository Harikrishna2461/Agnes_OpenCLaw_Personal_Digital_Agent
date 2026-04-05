#!/usr/bin/env python3
"""
WhatsApp Polling Daemon for LSA
Polls OpenClaw API for incoming messages and responds automatically.
No web console needed.
"""

import os
import time
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv
from main import LifeSimulationAgent

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("lsa_whatsapp_polling.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("AGNES_CLAW_API_KEY")
PHONE_NUMBER = "+917010384691"
POLL_INTERVAL = 5  # Check every 5 seconds

if not API_KEY:
    logger.error("❌ AGNES_CLAW_API_KEY not set in .env")
    exit(1)

agent = LifeSimulationAgent()
processed_messages = set()  # Track processed message IDs

class WhatsAppPoller:
    def __init__(self, api_key, phone_number):
        self.api_key = api_key
        self.phone_number = phone_number
        self.base_url = "https://api.agnesai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def check_messages(self):
        """Poll for incoming messages."""
        try:
            # Try to get incoming messages
            response = requests.get(
                f"{self.base_url}/messages/incoming",
                headers=self.headers,
                timeout=10,
                verify=False,
            )
            
            if response.status_code == 200:
                messages = response.json().get("messages", [])
                return messages
            
        except Exception as e:
            logger.debug(f"Polling error: {str(e)[:60]}")
        
        return []

    def process_message(self, message):
        """Process incoming message through LSA."""
        try:
            msg_id = message.get("id", "")
            from_number = message.get("from", "")
            text = message.get("text", "")
            
            if msg_id in processed_messages:
                return  # Already processed
            
            logger.info(f"📨 Incoming: {from_number} -> {text[:50]}")
            
            # Process through LSA
            response_text = agent.simulate_decision(text)
            recommendation = response_text.get("recommendation", "Study more!")
            
            # Send response
            self.send_message(from_number, f"📊 LSA Analysis:\n{recommendation}")
            
            processed_messages.add(msg_id)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def send_message(self, to_number, message):
        """Send WhatsApp message."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "channel": "whatsapp",
                "phone_number": to_number,
                "message": message,
            }
            
            response = requests.post(
                f"{self.base_url}/messages/send",
                json=payload,
                headers=headers,
                timeout=10,
                verify=False,
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Sent to {to_number}")
            else:
                logger.error(f"❌ Send failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending: {e}")

def main():
    poller = WhatsAppPoller(API_KEY, PHONE_NUMBER)
    
    print("""
╔════════════════════════════════════════════════════════════╗
║      LSA WhatsApp Polling Daemon (No Web Console)         ║
╚════════════════════════════════════════════════════════════╝

🚀 Starting polling daemon...
📱 WhatsApp: +91 7010384691
⏱️  Polling every 5 seconds for incoming messages

Send a WhatsApp message and LSA will respond!
Press Ctrl+C to stop.
""")
    
    logger.info("✅ WhatsApp polling daemon started")
    logger.info(f"📱 Listening on: {PHONE_NUMBER}")
    
    try:
        while True:
            messages = poller.check_messages()
            
            for message in messages:
                poller.process_message(message)
            
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("🛑 Daemon stopped")
        print("\n✅ Stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
