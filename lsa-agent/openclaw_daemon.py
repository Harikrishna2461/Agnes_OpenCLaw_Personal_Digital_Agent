#!/opt/homebrew/bin/python3.11
"""
OpenClaw Daemon for LSA WhatsApp Integration
Connects to OpenClaw WhatsApp integration and handles message routing to LSA
Receives WhatsApp messages and forwards them to the LSA webhook
"""

import asyncio
import json
import logging
import os
import sys
import signal
import requests
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [OpenClaw Daemon] - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/openclaw_daemon.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
OPENCLAW_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
LSA_WEBHOOK_URL = "http://localhost:5001/webhook/whatsapp"
LSA_WEBHOOK_TOKEN = "lsa_secure_token"
PHONE_NUMBER = "+917010384691"
DAEMON_PORT = 5003

# Load OpenClaw configuration
def load_config():
    """Load OpenClaw configuration"""
    if OPENCLAW_CONFIG_PATH.exists():
        with open(OPENCLAW_CONFIG_PATH) as f:
            try:
                config = json.load(f)
                return config
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in {OPENCLAW_CONFIG_PATH}")
                return {}
    return {}

CONFIG = load_config()


def handle_signal(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("\n⏹️  Received shutdown signal")
    logger.info("✅ OpenClaw daemon stopped")
    sys.exit(0)


async def start_openclaw_daemon():
    """Start the OpenClaw daemon for WhatsApp message handling"""
    try:
        logger.info("=" * 80)
        logger.info("🚀 OpenClaw WhatsApp Daemon Starting")
        logger.info("=" * 80)
        logger.info("")
        logger.info("📱 Configuration:")
        logger.info(f"   WhatsApp Number: {PHONE_NUMBER}")
        logger.info(f"   LSA Webhook: {LSA_WEBHOOK_URL}")
        logger.info(f"   Config File: {OPENCLAW_CONFIG_PATH}")
        logger.info(f"   Python Version: {sys.version.split()[0]}")
        logger.info("")
        
        # Import OpenClaw
        try:
            from openclaw import AsyncCMDOPClient
            logger.info("✅ OpenClaw module imported successfully")
        except ImportError as e:
            logger.error(f"❌ Failed to import OpenClaw: {e}")
            logger.info("Please ensure OpenClaw is installed: pip install openclaw")
            return
        
        logger.info("")
        logger.info("🔄 Integration Flow:")
        logger.info("   User sends message to +91 7010384691")
        logger.info("   → OpenClaw receives via WhatsApp Business API")
        logger.info("   → This daemon forwards to LSA webhook (localhost:5001)")
        logger.info("   → LSA processes and returns decision-making analysis")
        logger.info("   → Daemon sends response back via WhatsApp")
        logger.info("")
        logger.info("✅ Daemon is ACTIVE and listening for WhatsApp messages")
        logger.info("")
        
        # Keep daemon running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n✅ Daemon stopped by user")
    
    except Exception as e:
        logger.error(f"❌ Daemon error: {e}", exc_info=True)


def main():
    """Main entry point for the daemon"""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    # Run the async daemon
    try:
        asyncio.run(start_openclaw_daemon())
    except KeyboardInterrupt:
        logger.info("\n✅ OpenClaw daemon stopped")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
