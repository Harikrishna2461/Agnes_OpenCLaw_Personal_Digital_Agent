"""
Configuration and utility helpers for LSA.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Configuration manager."""
    
    def __init__(self, env_file: str = ".env"):
        """Load configuration from .env file."""
        if Path(env_file).exists():
            load_dotenv(env_file)
    
    @staticmethod
    def get_telegram_token() -> str:
        """Get Telegram bot token."""
        token = os.getenv("TELEGRAM_TOKEN", "")
        if not token:
            print("⚠️  TELEGRAM_TOKEN not set. Alerts disabled.")
        return token
    
    @staticmethod
    def get_telegram_user_id() -> str:
        """Get Telegram user ID."""
        user_id = os.getenv("TELEGRAM_USER_ID", "")
        if not user_id:
            print("⚠️  TELEGRAM_USER_ID not set. Alerts disabled.")
        return user_id
    
    @staticmethod
    def get_data_dir() -> str:
        """Get data directory path."""
        return os.getenv("DATA_DIR", "./data")
    
    @staticmethod
    def get_log_level() -> str:
        """Get logging level."""
        return os.getenv("LOG_LEVEL", "INFO")
    
    @staticmethod
    def get_quiet_hours() -> tuple:
        """Get quiet hours (start, end)."""
        start = int(os.getenv("QUIET_HOURS_START", "22"))
        end = int(os.getenv("QUIET_HOURS_END", "8"))
        return (start, end)
    
    @staticmethod
    def get_max_daily_alerts() -> int:
        """Get max alerts per day."""
        return int(os.getenv("MAX_DAILY_ALERTS", "5"))


def setup_datadir(data_dir: str = "./data") -> Path:
    """Ensure data directory exists."""
    path = Path(data_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_setup() -> bool:
    """Validate LSA setup."""
    print("\n🔍 Validating LSA Setup...")
    
    checks = {
        "Python version": _check_python_version(),
        "Data directory": _check_data_dir(),
        "Dependencies": _check_dependencies(),
        "Embedding model": _check_embedding_model(),
    }
    
    all_valid = all(checks.values())
    
    for check, result in checks.items():
        status = "✅" if result else "⚠️"
        print(f"  {status} {check}")
    
    if all_valid:
        print("\n✨ All checks passed! Ready to run.")
    else:
        print("\n⚠️  Some checks failed. See above for details.")
    
    return all_valid


def _check_python_version() -> bool:
    """Check Python version."""
    import sys
    return sys.version_info >= (3, 9)


def _check_data_dir() -> bool:
    """Check data directory."""
    try:
        setup_datadir()
        return True
    except Exception:
        return False


def _check_dependencies() -> bool:
    """Check critical dependencies."""
    required = ["numpy", "sentence_transformers"]
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            return False
    
    return True


def _check_embedding_model() -> bool:
    """Check if embedding model is available."""
    try:
        from sentence_transformers import SentenceTransformer
        SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./data/models")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    validate_setup()
