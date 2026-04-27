"""Travel suggestions based on user profile and past trips — query only."""
import logging

logger = logging.getLogger(__name__)


def intent(message: str) -> str:
    return "query"


def query(message: str, claude_client, file_handler) -> dict:
    index = file_handler.read("data/travel/index.md")
    system = claude_client.load_prompt("travel")
    response = claude_client.chat(system, f"{message}\n\nPast trips:\n{index}")
    return {"success": True, "message": response, "data": None}
