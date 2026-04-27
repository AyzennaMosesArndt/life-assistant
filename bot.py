import logging
import os
import sys
import atexit
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from core import claude_client, router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

LOCKFILE = Path(__file__).parent / "bot.lock"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Life assistant online. What do you need?")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    logger.info("Incoming message: %s", user_text)
    try:
        result = router.dispatch(user_text)
        logger.info("Dispatch result: success=%s message=%s", result["success"], result["message"])
        await update.message.reply_text(result["message"])
    except Exception:
        logger.exception("Unhandled error while processing message: %s", user_text)
        await update.message.reply_text("Something went wrong. Check the console.")


def acquire_lock() -> None:
    """Ensure only one bot instance runs. Exit if another instance is active."""
    if LOCKFILE.exists():
        try:
            pid = int(LOCKFILE.read_text().strip())
            # Check if process is still running (Windows-compatible)
            import psutil
            if psutil.pid_exists(pid):
                logger.error("Bot already running (PID %d). Exiting.", pid)
                sys.exit(1)
            else:
                logger.warning("Stale lockfile found (PID %d no longer exists). Removing.", pid)
                LOCKFILE.unlink()
        except (ValueError, ProcessLookupError):
            logger.warning("Invalid lockfile. Removing.")
            LOCKFILE.unlink()

    # Write current PID to lockfile
    LOCKFILE.write_text(str(os.getpid()))
    logger.info("Lockfile acquired (PID %d)", os.getpid())

    # Ensure cleanup on exit
    atexit.register(release_lock)


def release_lock() -> None:
    """Remove lockfile on clean exit."""
    if LOCKFILE.exists():
        try:
            LOCKFILE.unlink()
            logger.info("Lockfile released")
        except Exception:
            logger.exception("Failed to remove lockfile")


def main() -> None:
    acquire_lock()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        app.run_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        release_lock()


if __name__ == "__main__":
    main()
