#!/usr/bin/env python3
"""
Direct WhatsApp Business API Integration for LSA
Bypasses OpenClaw daemon issues by connecting directly to WhatsApp Business API
Receives messages and forwards to LSA via webhook
"""

import asyncio
import json
import os
import requests
import logging
from flask import Flask, request
from datetime import datetime
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - WhatsApp Direct - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
WHATSAPP_API_ENDPOINT = "https://graph.instagram.com/v18.0/me/messages"
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID")
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
LSA_WEBHOOK = "http://localhost:5001/webhook/whatsapp"
LSA_TOKEN = "lsa_secure_token"

# If not set via env, try to use sensible defaults
if not WHATSAPP_API_TOKEN:
    # For demo/testing purposes, this would need real credentials
    logger.warning("⚠️  WhatsApp API credentials not set in environment")
    WHATSAPP_API_TOKEN = "test_token"  # Placeholder


@app.route("/webhook/messages", methods=["GET"])
def webhook_verify():
    """Webhook verification endpoint for WhatsApp Business API"""
    verify_token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if verify_token == "lsa_whatsapp_verify":
        logger.info("✅ WhatsApp webhook verified")
        return challenge
    
    logger.warning("❌ Webhook verification failed")
    return "Unauthorized", 401


@app.route("/webhook/messages", methods=["POST"])
def receive_whatsapp_message():
    """Receive messages from WhatsApp Business API"""
    try:
        data = request.get_json()
        
        # Extract message details
        if "entry" not in data:
            return {"status": "ok"}, 200
        
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                # Check if it's a message
                if "messages" not in value:
                    continue
                
                for message in value["messages"]:
                    sender_id = message.get("from")
                    message_text = message.get("text", {}).get("body", "")
                    timestamp = message.get("timestamp")
                    
                    logger.info(f"📨 Received from {sender_id}: {message_text}")
                    
                    # Forward to LSA webhook
                    forward_to_lsa(sender_id, message_text, timestamp)
        
        return {"status": "ok"}, 200
    
    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")
        return {"error": str(e)}, 500


def forward_to_lsa(sender_id, message_text, timestamp):
    """Forward message to LSA webhook and send response back to WhatsApp"""
    try:
        # Create LSA payload
        lsa_payload = {
            "message": message_text,
            "sender_id": sender_id,
            "timestamp": timestamp,
            "token": LSA_TOKEN
        }
        
        logger.info(f"🔄 Forwarding to LSA: {message_text}")
        
        # Send to LSA webhook
        response = requests.post(
            LSA_WEBHOOK,
            json=lsa_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            lsa_response = response.json()
            logger.info(f"✅ LSA response: {lsa_response}")
            
            # Send response back to WhatsApp
            send_whatsapp_message(sender_id, lsa_response.get("message", "Processing complete"))
        else:
            logger.error(f"❌ LSA error: {response.status_code}")
    
    except Exception as e:
        logger.error(f"❌ Error forwarding to LSA: {e}")


def send_whatsapp_message(recipient_id, message_text):
    """Send message back to user via WhatsApp Business API"""
    try:
        headers = {
            "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "text",
            "text": {
                "body": message_text
            }
        }
        
        response = requests.post(
            WHATSAPP_API_ENDPOINT,
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            logger.info(f"✅ WhatsApp message sent to {recipient_id}")
        else:
            logger.error(f"❌ Failed to send WhatsApp message: {response.status_code}")
    
    except Exception as e:
        logger.error(f"❌ Error sending WhatsApp message: {e}")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return {
        "service": "WhatsApp Direct Integration",
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }, 200


def main():
    """Start the WhatsApp direct integration server"""
    logger.info("=" * 70)
    logger.info("WhatsApp Direct Business API Integration for LSA")
    logger.info("=" * 70)
    logger.info("")
    logger.info("📱 Integration Flow:")
    logger.info("   WhatsApp Message → Business API → This Server → LSA")
    logger.info("")
    logger.info("🔧 Configuration:")
    logger.info(f"   WhatsApp Phone: +91 7010384691")
    logger.info(f"   LSA Webhook: {LSA_WEBHOOK}")
    logger.info(f"   Server Port: 5002")
    logger.info("")
    logger.info("⚙️  To setup WhatsApp Business API:")
    logger.info("   1. Get credentials from https://developers.facebook.com")
    logger.info("   2. Set environment variables:")
    logger.info("      export WHATSAPP_BUSINESS_ACCOUNT_ID='your_id'")
    logger.info("      export WHATSAPP_API_TOKEN='your_token'")
    logger.info("      export PHONE_NUMBER_ID='your_phone_id'")
    logger.info("   3. Configure webhook on Facebook dashboard:")
    logger.info("      https://your-ngrok-url.ngrok-free.dev/webhook/messages")
    logger.info("")
    logger.info("✅ Server starting on http://localhost:5002")
    logger.info("")
    
    app.run(
        host='0.0.0.0',
        port=5002,
        debug=False,
        use_reloader=False
    )


if __name__ == "__main__":
    main()
