"""
Cron job scheduler for autonomous LSA operations.
"""

import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from main import LifeSimulationAgent

logger = logging.getLogger(__name__)


class LSAScheduler:
    """Manages automated LSA tasks via cron-like scheduling."""

    def __init__(self):
        """Initialize scheduler."""
        self.scheduler = BackgroundScheduler()
        self.agent = LifeSimulationAgent()
        logger.info("LSA Scheduler initialized")

    def schedule_daily_report(self, hour: int = 9, minute: int = 0):
        """Schedule daily report at HH:MM."""
        self.scheduler.add_job(
            self._generate_daily_report,
            "cron",
            hour=hour,
            minute=minute,
            id="daily_report",
        )
        logger.info(f"Daily report scheduled for {hour:02d}:{minute:02d}")

    def schedule_weekly_report(self, day: str = "mon", hour: int = 10):
        """Schedule weekly report on DAY at HH:00."""
        self.scheduler.add_job(
            self._generate_weekly_report,
            "cron",
            day_of_week=day,
            hour=hour,
            minute=0,
            id="weekly_report",
        )
        logger.info(f"Weekly report scheduled for {day.upper()} {hour:02d}:00")

    def schedule_intervention_check(self, minutes: int = 240):
        """Check for interventions every N minutes."""
        self.scheduler.add_job(
            self._check_interventions,
            "interval",
            minutes=minutes,
            id="intervention_check",
        )
        logger.info(f"Intervention check scheduled every {minutes} minutes")

    def schedule_backup(self, hour: int = 2, minute: int = 0):
        """Schedule data backup at HH:MM."""
        self.scheduler.add_job(
            self._backup_data,
            "cron",
            hour=hour,
            minute=minute,
            id="backup",
        )
        logger.info(f"Data backup scheduled for {hour:02d}:{minute:02d}")

    def start(self):
        """Start scheduler."""
        self.scheduler.start()
        logger.info("LSA Scheduler started")

    def stop(self):
        """Stop scheduler."""
        self.scheduler.shutdown()
        logger.info("LSA Scheduler stopped")

    def _generate_daily_report(self):
        """Generate and log daily report."""
        try:
            report = self.agent.get_daily_report()
            logger.info(f"Daily Report: {report}")
        except Exception as e:
            logger.error(f"Failed to generate daily report: {e}")

    def _generate_weekly_report(self):
        """Generate and log weekly report."""
        try:
            report = self.agent.get_weekly_report()
            logger.info(f"Weekly Report: {report}")
        except Exception as e:
            logger.error(f"Failed to generate weekly report: {e}")

    async def _check_interventions(self):
        """Check for and handle interventions."""
        try:
            alert = await self.agent.check_intervention()
            if alert:
                logger.warning(
                    f"INTERVENTION: {alert.priority} - {alert.observation}"
                )
        except Exception as e:
            logger.error(f"Failed to check interventions: {e}")

    def _backup_data(self):
        """Backup all data."""
        try:
            path = self.agent.export_data()
            logger.info(f"Data backed up to {path}")
        except Exception as e:
            logger.error(f"Failed to backup data: {e}")


def setup_default_schedule(scheduler: LSAScheduler):
    """Configure default schedule."""
    # Daily report at 9am
    scheduler.schedule_daily_report(hour=9, minute=0)

    # Weekly report every Monday at 10am
    scheduler.schedule_weekly_report(day="mon", hour=10)

    # Check interventions every 4 hours
    scheduler.schedule_intervention_check(minutes=240)

    # Backup data daily at 2am
    scheduler.schedule_backup(hour=2, minute=0)


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create scheduler
    lsa_scheduler = LSAScheduler()

    # Configure default schedule
    setup_default_schedule(lsa_scheduler)

    # Start
    lsa_scheduler.start()

    print("✅ LSA Scheduler running. Press Ctrl+C to stop.")

    try:
        import time

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        lsa_scheduler.stop()
        print("\n✋ Scheduler stopped.")
