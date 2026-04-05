#!/opt/homebrew/bin/python3.11
"""
Integration Test Script for LSA + OpenClaw
Tests the complete WhatsApp integration without needing real messages
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration
LSA_WEBHOOK = "http://localhost:5001/webhook/whatsapp"
LSA_TOKEN = "lsa_secure_token"

# Test scenarios
TEST_SCENARIOS = [
    {
        "name": "Skip Class",
        "message": "Should I skip class today to work on a personal project?",
        "sender": "+917010384691_test_1"
    },
    {
        "name": "Study vs Party",
        "message": "Should I study for the exam or go to the party tonight?",
        "sender": "+917010384691_test_2"
    },
    {
        "name": "Exercise Decision",
        "message": "I'm tired. Should I go to the gym or rest at home?",
        "sender": "+917010384691_test_3"
    },
    {
        "name": "Work Priority",
        "message": "Should I focus on my startup or take a corporate job offer?",
        "sender": "+917010384691_test_4"
    },
]


def print_header():
    """Print test header"""
    print("\n" + "=" * 80)
    print("LSA + OpenClaw Integration Test")
    print("=" * 80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"LSA Webhook: {LSA_WEBHOOK}")
    print("=" * 80)
    print()


def test_flask_health():
    """Test Flask server health"""
    print("1️⃣  Testing Flask Server Health...")
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Flask is healthy")
            print(f"      Service: {data.get('service', 'unknown')}")
            print(f"      Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"   ❌ Flask returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Flask connection failed: {e}")
        return False


def test_webhook_message(scenario):
    """Test webhook with a message"""
    print(f"\n2️⃣  Testing Scenario: {scenario['name']}")
    print(f"   Message: {scenario['message']}")
    
    payload = {
        "message": scenario['message'],
        "sender_id": scenario['sender'],
        "timestamp": int(time.time()),
        "token": LSA_TOKEN
    }
    
    try:
        print("   📤 Sending to webhook...")
        response = requests.post(
            LSA_WEBHOOK,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Webhook response received")
            print(f"      Status: {response.status_code}")
            
            # Parse response
            if isinstance(data, dict):
                if 'message' in data:
                    msg = data['message']
                    if len(msg) > 200:
                        print(f"      Response: {msg[:200]}...")
                    else:
                        print(f"      Response: {msg}")
                
                # Check for scenario details
                if 'scenarios' in data:
                    print(f"      Scenarios: {len(data['scenarios'])} generated")
                    for i, scenario_item in enumerate(data['scenarios'], 1):
                        if isinstance(scenario_item, dict):
                            title = scenario_item.get('title', 'Unknown')
                            print(f"        Scenario {i}: {title}")
            
            return True
        else:
            print(f"   ❌ Webhook returned status {response.status_code}")
            print(f"      Response: {response.text[:200]}")
            return False
    
    except Exception as e:
        print(f"   ❌ Webhook error: {e}")
        return False


def main():
    """Run all tests"""
    print_header()
    
    # Test Flask health
    if not test_flask_health():
        print("\n❌ Flask server is not running!")
        print("Please start it with:")
        print("  /Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent/whatsapp_server.py")
        sys.exit(1)
    
    print("\n✅ Flask server is operational")
    print("\n" + "=" * 80)
    print("Running LSA Webhook Tests")
    print("=" * 80)
    
    # Test each scenario
    passed = 0
    failed = 0
    
    for scenario in TEST_SCENARIOS:
        if test_webhook_message(scenario):
            passed += 1
            time.sleep(1)  # Delay between tests
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"✅ Passed: {passed}/{len(TEST_SCENARIOS)}")
    print(f"❌ Failed: {failed}/{len(TEST_SCENARIOS)}")
    
    if failed == 0:
        print("\n🎉 All tests passed! LSA + OpenClaw integration is working!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check server logs.")
    
    print("\n" + "=" * 80)
    print()
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
