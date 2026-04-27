"""Book and text cataloguing with 2-sentence analytical abstracts."""
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
    system = claude_client.load_prompt("literature")
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
        return {"success": False, "message": f"Clarify: title or author is unclear for this entry.", "data": None}

    today = date.today().isoformat()
    formatted = (
        f"## entry\n"
        f"- title: {entry.get('title', '')}\n"
        f"- author: {entry.get('author', '')}\n"
        f"- publisher: {entry.get('publisher', '')}\n"
        f"- year: {entry.get('year', '')}\n"
        f"- genre: {entry.get('genre', '')}\n"
        f"- subgenre: {entry.get('subgenre', '')}\n"
        f"- bestseller_weeks: {entry.get('bestseller_weeks', '')}\n"
        f"- abstract: {entry.get('abstract', '')}\n"
        f"- added: {today}"
    )
    file_handler.append_entry("literature", formatted)

    return {
        "success": True,
        "message": f"Saved: {entry.get('title', '?')} by {entry.get('author', '?')}",
        "data": {**entry, "added": today},
    }


def query(message: str, claude_client, file_handler) -> dict:
    index = file_handler.read("data/literature/index.md")
    system = claude_client.load_prompt("literature")
    response = claude_client.chat(system, f"Query: {message}\n\nLiterature index:\n{index}")
    return {"success": True, "message": response, "data": None}
