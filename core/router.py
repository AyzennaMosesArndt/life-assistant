"""Classifies messages by domain and dispatches to the right agent."""
import logging

from core import claude_client, file_handler
from agents import music_agent, literature_agent, art_agent, food_agent, learning_agent, travel_agent

logger = logging.getLogger(__name__)

_DOMAINS = "music, literature, art, food, running, learning, research, travel"
_CLASSIFY_SYSTEM = (
    f"You classify user messages into exactly one domain: {_DOMAINS}. "
    "The user may write in German or English. "
    "Reply with the domain name only, lowercase, no punctuation. "
    "If none match, reply: none"
)


def classify(message: str) -> str | None:
    result = claude_client.chat(_CLASSIFY_SYSTEM, message).strip().lower()
    logger.info("classify() raw response: %r", result)
    return None if result == "none" else result


def dispatch(message: str) -> dict:
    domain = classify(message)

    if domain is None:
        return {"success": False, "message": "I couldn't match your message to a domain. Try being more specific.", "data": None}

    if domain == "music":
        if music_agent.intent(message) == "query":
            return music_agent.query(message, claude_client, file_handler)
        return music_agent.add_entry(message, claude_client, file_handler)

    if domain == "literature":
        if literature_agent.intent(message) == "query":
            return literature_agent.query(message, claude_client, file_handler)
        return literature_agent.add_entry(message, claude_client, file_handler)

    if domain == "art":
        if art_agent.intent(message) == "query":
            return art_agent.query(message, claude_client, file_handler)
        return art_agent.add_entry(message, claude_client, file_handler)

    if domain == "food":
        if food_agent.intent(message) == "query":
            return food_agent.query(message, claude_client, file_handler)
        return food_agent.add_entry(message, claude_client, file_handler)

    if domain == "learning":
        if learning_agent.intent(message) == "query":
            return learning_agent.query(message, claude_client, file_handler)
        return learning_agent.add_entry(message, claude_client, file_handler)

    if domain == "travel":
        return travel_agent.query(message, claude_client, file_handler)

    return {"success": False, "message": f"The {domain} agent is not yet implemented.", "data": None}
