#!/opt/homebrew/bin/python3.11
"""
Complete System Verification Script
Checks all components and verifies the OpenClaw + LSA + WhatsApp integration
"""

import subprocess
import sys
import time
import json
import urllib.request
import urllib.error

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    """Print verification header"""
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}Agnes LSA + OpenClaw Integration - System Verification{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

def print_section(title):
    """Print section header"""
    print(f"\n{BOLD}{BLUE}{title}{RESET}")
    print(f"{BLUE}{'-'*len(title)}{RESET}")

def check_mark(condition, message):
    """Print check mark with status"""
    if condition:
        print(f"{GREEN}✅{RESET} {message}")
        return True
    else:
        print(f"{RED}❌{RESET} {message}")
        return False

def check_python():
    """Check Python version and availability"""
    print_section("1️⃣  Python Environment")
    
    results = []
    
    # Check Python 3.11
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        version = result.stdout.strip()
        results.append(check_mark(True, f"Python 3.11 available: {version}"))
    except Exception as e:
        results.append(check_mark(False, f"Python 3.11 not found: {e}"))
        return False
    
    return all(results)

def check_openclaw():
    """Check OpenClaw installation and imports"""
    print_section("2️⃣  OpenClaw Installation")
    
    results = []
    
    # Check OpenClaw import
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", "-c", "import openclaw; print('ok')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            results.append(check_mark(True, "OpenClaw module imports successfully"))
        else:
            results.append(check_mark(False, f"OpenClaw import failed: {result.stderr}"))
    except Exception as e:
        results.append(check_mark(False, f"OpenClaw test error: {e}"))
        return False
    
    # Check cmdop import
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", "-c", "import cmdop; print('ok')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            results.append(check_mark(True, "cmdop module imports successfully"))
        else:
            results.append(check_mark(False, f"cmdop import failed: {result.stderr}"))
    except Exception as e:
        results.append(check_mark(False, f"cmdop test error: {e}"))
    
    # Check TimeoutError compatibility
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", "-c", "from cmdop.exceptions import TimeoutError; print('ok')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            results.append(check_mark(True, "TimeoutError compatibility alias works"))
        else:
            results.append(check_mark(False, "TimeoutError alias missing (needs fix)"))
    except Exception as e:
        results.append(check_mark(False, f"TimeoutError test error: {e}"))
    
    return all(results)

def check_dependencies():
    """Check other required dependencies"""
    print_section("3️⃣  Python Dependencies")
    
    required_packages = [
        "flask",
        "requests",
        "sentence_transformers",
        "numpy",
        "pydantic",
        "protobuf"
    ]
    
    results = []
    
    for package in required_packages:
        try:
            result = subprocess.run(
                ["/opt/homebrew/bin/python3.11", "-c", f"import {package}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            results.append(check_mark(result.returncode == 0, f"{package}"))
        except Exception as e:
            results.append(check_mark(False, f"{package} - error: {e}"))
    
    return all(results)

def check_flask_server():
    """Check if Flask server can start"""
    print_section("4️⃣  Flask Server")
    
    # First kill any existing Flask instances
    subprocess.run(
        ["pkill", "-f", "whatsapp_server"],
        capture_output=True
    )
    time.sleep(1)
    
    # Try to start Flask
    try:
        flask_dir = "/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent"
        process = subprocess.Popen(
            ["/opt/homebrew/bin/python3.11", f"{flask_dir}/whatsapp_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=flask_dir
        )
        
        # Give it time to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            check_mark(True, "Flask server started successfully")
            
            # Try to hit the health endpoint
            try:
                response = urllib.request.urlopen("http://localhost:5001/health", timeout=5)
                if response.status == 200:
                    data = response.read().decode()
                    check_mark(True, "Health endpoint responds correctly")
                    process.terminate()
                    time.sleep(1)
                    return True
                else:
                    check_mark(False, f"Health endpoint returned {response.status}")
            except Exception as e:
                check_mark(False, f"Health check failed: {e}")
            
            process.terminate()
            return False
        else:
            stderr = process.stderr.read().decode() if process.stderr else "unknown"
            check_mark(False, f"Flask server crashed: {stderr[:100]}")
            return False
    
    except Exception as e:
        check_mark(False, f"Flask startup error: {e}")
        return False

def check_lsa_import():
    """Check if LSA modules import correctly"""
    print_section("5️⃣  LSA Modules")
    
    results = []
    
    # Check main.py imports
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", "-c", "from main import LifeSimulationAgent"],
            capture_output=True,
            text=True,
            timeout=15,
            cwd="/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent"
        )
        results.append(check_mark(result.returncode == 0, "LifeSimulationAgent imports"))
    except Exception as e:
        results.append(check_mark(False, f"LSA import error: {e}"))
    
    # Check simulation.py imports
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", "-c", "from simulation import DecisionSimulator"],
            capture_output=True,
            text=True,
            timeout=15,
            cwd="/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent"
        )
        results.append(check_mark(result.returncode == 0, "DecisionSimulator imports"))
    except Exception as e:
        results.append(check_mark(False, f"Simulator import error: {e}"))
    
    return all(results) if results else False

def check_openclaw_daemon():
    """Check if OpenClaw daemon can start"""
    print_section("6️⃣  OpenClaw Daemon")
    
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/python3.11", 
             "/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent/openclaw_daemon.py"],
            capture_output=True,
            text=True,
            timeout=3
        )
        # Will timeout after 3 seconds, which is expected (daemon keeps running)
        output = result.stderr + result.stdout
        
        if "OpenClaw module imported successfully" in output:
            check_mark(True, "OpenClaw daemon initializes correctly")
            return True
        else:
            check_mark(False, "OpenClaw daemon has initialization issues")
            return False
    
    except subprocess.TimeoutExpired:
        # This is expected - daemon runs indefinitely
        check_mark(True, "OpenClaw daemon starts and runs indefinitely (expected)")
        return True
    except Exception as e:
        check_mark(False, f"OpenClaw daemon startup error: {e}")
        return False

def check_files():
    """Check required files exist"""
    print_section("7️⃣  Required Files")
    
    files_to_check = [
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent/openclaw_daemon.py", "OpenClaw daemon"),
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent/whatsapp_server.py", "Flask server"),
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent/main.py", "LSA main"),
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/lsa-agent/simulation.py", "Decision simulation"),
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/start_lsa_openclaw.sh", "Startup script"),
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/test_integration.py", "Test script"),
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/README.md", "Master README"),
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/QUICK_START.md", "Quick start guide"),
        ("/Users/HariKrishnaD/Downloads/Agnes_AI/OPENCLAW_SETUP.md", "Setup guide"),
    ]
    
    results = []
    for filepath, description in files_to_check:
        import os
        exists = os.path.exists(filepath)
        results.append(check_mark(exists, filepath))
    
    return all(results)

def main():
    """Run all verification checks"""
    print_header()
    
    checks = [
        ("Python Environment", check_python),
        ("OpenClaw Installation", check_openclaw),
        ("Dependencies", check_dependencies),
        ("LSA Modules", check_lsa_import),
        ("Required Files", check_files),
        ("OpenClaw Daemon", check_openclaw_daemon),
        ("Flask Server", check_flask_server),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"{RED}Error in {name}: {e}{RESET}")
            results.append((name, False))
    
    # Summary
    print_section(f"\n{BOLD}Summary{RESET}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{status} - {name}")
    
    print(f"\n{BOLD}Total: {passed}/{total} checks passed{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}{BOLD}🎉 All systems operational! Ready to use.{RESET}")
        print(f"\n{BOLD}Next steps:{RESET}")
        print(f"1. Run: {BOLD}./start_lsa_openclaw.sh{RESET}")
        print(f"2. Test: {BOLD}./test_integration.py{RESET}")
        print(f"3. Use: Send WhatsApp message to +91 7010384691")
        return 0
    else:
        print(f"\n{RED}{BOLD}⚠️  Some checks failed. See details above.{RESET}")
        print(f"\n{BOLD}Troubleshooting:{RESET}")
        print(f"See OPENCLAW_SETUP.md for detailed troubleshooting")
        return 1

if __name__ == "__main__":
    sys.exit(main())
