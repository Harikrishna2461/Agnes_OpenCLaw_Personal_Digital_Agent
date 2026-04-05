#!/usr/bin/env python3
"""
WhatsApp Simulator Daemon
Simulates real WhatsApp messages hitting your LSA webhook.
Useful for testing without OpenClaw configured.
"""

import requests
import time
import json
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test messages that simulate real user decisions
TEST_MESSAGES = [
    "can i skip class today?",
    "should i study for 3 hours?",
    "should i hit the gym?",
    "should i work late tonight?",
    "can i take a break?",
    "should i sleep now?",
    "can i skip gym today?",
    "should i study harder?",
]

WEBHOOK_URL = "http://localhost:5001/webhook/whatsapp"
WEBHOOK_TOKEN = "lsa_secure_token"
PHONE_NUMBER = "+917010384691"


def send_test_message(message: str):
    """Send a simulated WhatsApp message to the LSA webhook."""
    payload = {
        "from": PHONE_NUMBER,
        "message": message,
        "token": WEBHOOK_TOKEN,
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=10,
        )
        
        if response.status_code == 200:
            data = response.json()
            lsa_response = data.get('response', '')
            logger.info(f"✅ Message sent: '{message}'")
            logger.info(f"📱 LSA Response preview: {lsa_response[:100]}...")
            return True
        else:
            logger.error(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


def run_daemon(interval: int = 30):
    """Run the simulator daemon in interactive mode."""
    logger.info(f"🚀 WhatsApp Simulator Daemon Started")
    logger.info(f"📱 Phone: {PHONE_NUMBER}")
    logger.info(f"🌐 Webhook: {WEBHOOK_URL}")
    logger.info(f"⏱️  Interval: {interval} seconds")
    logger.info("")
    logger.info("Simulating WhatsApp messages every {} seconds...".format(interval))
    logger.info("Press Ctrl+C to stop")
    logger.info("")
    
    message_index = 0
    
    try:
        while True:
            message = TEST_MESSAGES[message_index % len(TEST_MESSAGES)]
            logger.info(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
            send_test_message(message)
            
            message_index += 1
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("\n✅ Daemon stopped")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        interval = int(sys.argv[1])
    else:
        interval = 30  # Default: send a message every 30 seconds
    
    run_daemon(interval)
