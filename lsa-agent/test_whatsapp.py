#!/usr/bin/env python3
"""
WhatsApp Server Testing & Local Development Tool.
Allows testing the WhatsApp integration without real WhatsApp connection.
"""

import requests
import json
import sys
from typing import Dict, Optional
import time

BASE_URL = "http://localhost:5001"


class WhatsAppTester:
    """Test LSA WhatsApp integration."""

    def __init__(self, webhook_token: str = "lsa_secure_token", phone: str = "+917010384691"):
        """Initialize tester."""
        self.token = webhook_token
        self.phone = phone
        self.base_url = BASE_URL

    def check_health(self) -> bool:
        """Check if server is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def verify_webhook(self) -> bool:
        """Verify webhook endpoint."""
        try:
            response = requests.get(f"{self.base_url}/webhook/verify", timeout=5)
            return response.status_code == 200
        except:
            return False

    def send_message(self, message: str) -> Dict:
        """
        Send test message to webhook.

        Args:
            message: Message text

        Returns:
            Response dict
        """
        payload = {
            "from": self.phone,
            "message": message,
            "token": self.token
        }

        try:
            response = requests.post(
                f"{self.base_url}/webhook/whatsapp",
                json=payload,
                timeout=15
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def test_decision(self, decision: str) -> str:
        """Test decision analysis."""
        print(f"\n📱 Sending: {decision}")
        result = self.send_message(decision)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return ""

        print(f"✅ Response received")
        return result.get("response", "")

    def test_event_logging(self, event: str) -> str:
        """Test event logging."""
        print(f"\n📱 Logging: {event}")
        result = self.send_message(event)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return ""

        print(f"✅ Event logged")
        return result.get("response", "")

    def test_command(self, cmd: str) -> str:
        """Test command."""
        print(f"\n📱 Command: {cmd}")
        result = self.send_message(cmd)

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return ""

        print(f"✅ Command executed")
        return result.get("response", "")

    def interactive_mode(self):
        """Run interactive testing mode."""
        print(f"\n{'='*60}")
        print("LSA WhatsApp Interactive Test Mode")
        print(f"{'='*60}")
        print(f"Webhook: {self.base_url}/webhook/whatsapp")
        print(f"Phone: {self.phone}")
        print(f"Token: {self.token}")
        print(f"\nType messages below:")
        print("  'quit' to exit")
        print("  '/help' for commands")
        print(f"{'='*60}\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    print("\n👋 Goodbye!")
                    break

                if not user_input:
                    continue

                # Send message
                result = self.send_message(user_input)

                if "error" in result:
                    print(f"❌ Error: {result['error']}\n")
                else:
                    print(f"✅ LSA:\n{result.get('response', 'No response')}\n")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted!")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")

    def run_test_suite(self):
        """Run automated test suite."""
        print(f"\n{'='*60}")
        print("LSA WhatsApp Test Suite")
        print(f"{'='*60}\n")

        # Test 1: Health check
        print("1️⃣  Health Check...")
        if self.check_health():
            print("   ✅ Server is running")
        else:
            print("   ❌ Server is DOWN. Start with: python3 whatsapp_server.py")
            return

        # Test 2: Webhook verify
        print("\n2️⃣  Webhook Verification...")
        if self.verify_webhook():
            print("   ✅ Webhook endpoint active")
        else:
            print("   ❌ Webhook not responding")
            return

        # Test 3: Decision simulation
        print("\n3️⃣  Decision Simulation...")
        resp = self.send_message("Should I study for 2 hours today?")
        if "error" not in resp:
            print("   ✅ Decision analysis working")
        else:
            print(f"   ❌ Error: {resp['error']}")

        # Test 4: Event logging
        print("\n4️⃣  Event Logging...")
        resp = self.send_message("Completed 90 minute study session")
        if "error" not in resp:
            print("   ✅ Event logging working")
        else:
            print(f"   ❌ Error: {resp['error']}")

        # Test 5: Commands
        print("\n5️⃣  Command Execution...")
        resp = self.send_message("/status")
        if "error" not in resp:
            print("   ✅ Commands working")
        else:
            print(f"   ❌ Error: {resp['error']}")

        print(f"\n{'='*60}")
        print("✅ Test Suite Complete!")
        print(f"{'='*60}\n")


def main():
    """Main test runner."""
    import argparse

    parser = argparse.ArgumentParser(description="LSA WhatsApp Server Tester")
    parser.add_argument("--mode", choices=["test", "interactive", "send"], default="test",
                        help="Testing mode")
    parser.add_argument("--message", type=str, help="Message to send (for --mode send)")
    parser.add_argument("--token", type=str, default="lsa_secure_token",
                        help="Webhook token")
    parser.add_argument("--phone", type=str, default="+917010384691",
                        help="WhatsApp phone number")

    args = parser.parse_args()

    tester = WhatsAppTester(webhook_token=args.token, phone=args.phone)

    if args.mode == "test":
        tester.run_test_suite()
    elif args.mode == "interactive":
        try:
            tester.interactive_mode()
        except KeyboardInterrupt:
            print("\n\n👋 Test interrupted!")
    elif args.mode == "send":
        if not args.message:
            print("❌ --message required for send mode")
            sys.exit(1)
        result = tester.send_message(args.message)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
