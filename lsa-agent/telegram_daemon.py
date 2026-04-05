"""
Telegram integration daemon for real-time LSA interaction.
"""

import logging
import os
from dotenv import load_dotenv
from main import LifeSimulationAgent

logger = logging.getLogger(__name__)

# Load environment
load_dotenv()


class LSATelegramDaemon:
    """
    Telegram bot daemon for LSA.
    Sends alerts and receives user updates.
    """

    def __init__(self, token: str, user_id: str):
        """
        Initialize Telegram daemon.

        Args:
            token: Telegram bot token
            user_id: Target user ID
        """
        self.token = token
        self.user_id = user_id
        self.agent = LifeSimulationAgent()

        logger.info(f"Telegram daemon initialized for user {user_id}")

    def handle_message(self, message: str) -> str:
        """
        Handle incoming Telegram message.

        Args:
            message: User message text

        Returns:
            Response message
        """

        # Log as memory if it's an event
        if any(
            word in message.lower()
            for word in ["completed", "did", "finished", "tried"]
        ):
            self.agent.log_event(
                content=message,
                category="telegram_update",
                tags=["user_reported"],
            )

        # Simulate if it's a decision
        if any(
            word in message.lower()
            for word in ["should", "consider", "planning", "thinking", "maybe"]
        ):
            result = self.agent.simulate_decision(message)
            recommendation = result["recommendation"]

            response = f"""
🤖 **Analyzed your decision**

📌 Decision: "{message}"

🎯 **Scenarios Simulated**
- Scenario A (Continue): Risk = moderate
- Scenario B (Moderate): Risk = low  
- Scenario C (Optimal): Risk = medium

✅ **Recommendation: {recommendation}**

📊 Impact Score:
- Scenario A: {result['scores']['A: Continue Current Behavior']:.1f}
- Scenario B: {result['scores']['B: Moderate Improvement']:.1f}
- Scenario C: {result['scores']['C: Optimal Behavior']:.1f}

💡 Choose your path wisely.
"""
            return response

        # Default: return status
        report = self.agent.get_daily_report()
        response = f"""
📊 **LSA Daily Status**

Activities today: {report['activities_today']}
Average impact: {report['key_metrics']['avg_impact']:.1f}/10
Consistency: {report['key_metrics']['consistency']:.0f}%

✨ Keep going!
"""
        return response

    def handle_command(self, cmd: str) -> str:
        """Handle Telegram commands."""

        if cmd == "/status":
            report = self.agent.get_daily_report()
            return f"📊 Activity: {report['activities_today']}, Consistency: {report['key_metrics']['consistency']:.0f}%"

        elif cmd == "/weekly":
            report = self.agent.get_weekly_report()
            return f"📈 Weekly patterns: {report['this_week']}"

        elif cmd == "/help":
            return """
🤖 **LSA Telegram Commands**

/status - Get today's summary
/weekly - Get weekly report  
/help - Show this help
/export - Export all data

Send decisions to analyze:
"Should I skip study today?"
"I'm tired, should I work out?"

Report events:
"Completed 2-hour study session"
"Went for a run"
"""

        elif cmd == "/export":
            path = self.agent.export_data()
            return f"✅ Data exported to {path}"

        else:
            return f"❓ Unknown command: {cmd}"


async def run_telegram_daemon():
    """Run Telegram daemon (requires python-telegram-bot)."""

    try:
        from telegram import Update
        from telegram.ext import (
            Application,
            CommandHandler,
            MessageHandler,
            filters,
            ContextTypes,
        )
    except ImportError:
        logger.error("python-telegram-bot not installed. Install with: pip install python-telegram-bot")
        return

    token = os.getenv("TELEGRAM_TOKEN", "")
    user_id = int(os.getenv("TELEGRAM_USER_ID", "0"))

    if not token or not user_id:
        logger.error("TELEGRAM_TOKEN or TELEGRAM_USER_ID not set in .env")
        return

    daemon = LSATelegramDaemon(token, str(user_id))

    async def handle_start(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        await update.message.reply_text(
            "🤖 LSA ready. Send me decisions to analyze or events to log!"
        )

    async def handle_message(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        text = update.message.text
        if text.startswith("/"):
            response = daemon.handle_command(text)
        else:
            response = daemon.handle_message(text)

        await update.message.reply_text(response)

    # Create app
    app = Application.builder().token(token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Run
    logger.info("Starting Telegram daemon...")
    await app.run_polling()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    import asyncio

    print("Starting LSA Telegram Daemon...")
    print("Stop with Ctrl+C")

    try:
        asyncio.run(run_telegram_daemon())
    except KeyboardInterrupt:
        print("\n✋ Daemon stopped.")
