"""Curiosity backlog (Lernfelder) management and topic suggestions."""
import json
import logging
from datetime import date

logger = logging.getLogger(__name__)

_QUERY_PATTERNS = [
    # English query patterns
    "suggest", "what should", "what can", "what could", "could i", "recommend",
    "show", "list", "what to learn", "next", "backlog",
    # German query patterns
    "könnte", "was könnte", "vorschlagen", "empfehlen", "heute lernen",
    "lernen heute", "zeigen", "was soll", "was kann"
]

_LERNFELDER_PATH = "data/learning/lernfelder.md"


def intent(message: str) -> str:
    lower = message.lower()
    if any(p in lower for p in _QUERY_PATTERNS):
        return "query"
    return "add"


def add_entry(message: str, claude_client, file_handler) -> dict:
    system = claude_client.load_prompt("learning")
    response = claude_client.chat(system, f"Add to Lernfelder: {message}").strip()
    logger.info("add_entry() raw Claude response: %r", response)

    clean = response.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        entry = json.loads(clean)
    except json.JSONDecodeError:
        logger.error("JSON parse failed, returning raw response: %r", response)
        return {"success": True, "message": response, "data": None}

    if entry.get("confidence") == "low":
        return {"success": False, "message": "Clarify: the topic is unclear.", "data": None}

    today = date.today().isoformat()
    formatted = (
        f"## entry\n"
        f"- topic: {entry.get('topic', '')}\n"
        f"- description: {entry.get('description', '')}\n"
        f"- complexity: {entry.get('complexity', '')}\n"
        f"- added: {today}\n"
        f"- status: backlog"
    )
    current = file_handler.read(_LERNFELDER_PATH)
    file_handler.write(_LERNFELDER_PATH, current.rstrip() + f"\n\n{formatted}\n")

    return {
        "success": True,
        "message": f"Added to Lernfelder: {entry.get('topic', '?')} ({entry.get('complexity', '?')})",
        "data": {**entry, "added": today, "status": "backlog"},
    }


def query(message: str, claude_client, file_handler) -> dict:
    lernfelder = file_handler.read(_LERNFELDER_PATH)
    system = claude_client.load_prompt("learning")
    response = claude_client.chat(system, f"Suggest topics: {message}\n\nLernfelder:\n{lernfelder}")
    return {"success": True, "message": response, "data": None}
