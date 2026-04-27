"""Artwork cataloguing across all media with reception-focused notes."""
import json
import logging
from datetime import date

logger = logging.getLogger(__name__)

_QUERY_PATTERNS = ["show", "list", "find", "search", "what", "which", "query", "tell me", "how many", "recommend"]


def intent(message: str) -> str:
    lower = message.lower()
    if any(p in lower for p in _QUERY_PATTERNS):
        return "query"
    return "add"


def add_entry(message: str, claude_client, file_handler) -> dict:
    system = claude_client.load_prompt("art")
    response = claude_client.chat(system, message).strip()
    logger.info("add_entry() raw Claude response: %r", response)

    if response.startswith("CLARIFY:"):
        return {"success": False, "message": f"Clarify: {response[len('CLARIFY:'):].strip()}", "data": None}

    clean = response.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        entry = json.loads(clean)
    except json.JSONDecodeError:
        logger.error("Unparseable response: %r", response)
        return {"success": False, "message": "Couldn't parse the response. Try rephrasing.", "data": None}

    if entry.get("confidence") == "low":
        return {"success": False, "message": "Clarify: epoch or medium is unclear for this entry.", "data": None}

    today = date.today().isoformat()
    formatted = (
        f"## entry\n"
        f"- title: {entry.get('title', '')}\n"
        f"- artist: {entry.get('artist', '')}\n"
        f"- year: {entry.get('year', '')}\n"
        f"- epoch: {entry.get('epoch', '')}\n"
        f"- medium: {entry.get('medium', '')}\n"
        f"- note: {entry.get('note', '')}\n"
        f"- added: {today}"
    )
    file_handler.append_entry("art", formatted)

    return {
        "success": True,
        "message": f"Saved: {entry.get('title', '?')} by {entry.get('artist', '?')}",
        "data": {**entry, "added": today},
    }


def query(message: str, claude_client, file_handler) -> dict:
    index = file_handler.read("data/art/index.md")
    system = claude_client.load_prompt("art")
    response = claude_client.chat(system, f"Query: {message}\n\nArt index:\n{index}")
    return {"success": True, "message": response, "data": None}
