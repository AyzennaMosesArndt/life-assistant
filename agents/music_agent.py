"""Music discovery and genre-aware cataloguing."""
import json
import logging
from datetime import date

logger = logging.getLogger(__name__)

_ADD_PATTERNS = ["add", "save", "log", "track", "heard", "listened", "discovered", "found", "like"]
_QUERY_PATTERNS = ["show", "list", "find", "search", "what", "which", "query", "tell me", "how many"]


def intent(message: str) -> str:
    lower = message.lower()
    if any(p in lower for p in _QUERY_PATTERNS):
        return "query"
    return "add"


def add_entry(message: str, claude_client, file_handler) -> dict:
    genres_content = file_handler.read("data/music/genres.md")
    system = claude_client.load_prompt("music")
    user_prompt = f"{message}\n\nExisting genres:\n{genres_content}"

    response = claude_client.chat(system, user_prompt).strip()
    logger.info("add_entry() raw Claude response: %r", response)

    if response.startswith("CLARIFY:"):
        question = response[len("CLARIFY:"):].strip()
        return {"success": False, "message": f"Clarify: {question}", "data": None}

    # strip markdown code fences Claude sometimes adds
    clean = response.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        entry = json.loads(clean)
    except json.JSONDecodeError:
        logger.error("Unparseable Claude response: %r", response)
        return {"success": False, "message": "Couldn't parse the response. Try rephrasing.", "data": None}

    if entry.get("confidence") == "low":
        title = entry.get("title", "this entry")
        return {"success": False, "message": f"Clarify: genre or subgenre is unclear for '{title}'.", "data": None}

    genre = entry.get("genre", "").lower().strip()
    existing = {l.lstrip("- ").strip().lower() for l in genres_content.splitlines() if l.startswith("- ")}
    if genre and genre not in existing:
        file_handler.write("data/music/genres.md", genres_content.rstrip() + f"\n- {genre}\n")

    today = date.today().isoformat()
    formatted = (
        f"## entry\n"
        f"- title: {entry.get('title', '')}\n"
        f"- artist: {entry.get('artist', '')}\n"
        f"- album: {entry.get('album', '')}\n"
        f"- year: {entry.get('year', '')}\n"
        f"- genre: {entry.get('genre', '')}\n"
        f"- subgenre: {entry.get('subgenre', '')}\n"
        f"- added: {today}"
    )
    file_handler.append_entry("music", formatted)

    return {
        "success": True,
        "message": f"Saved: {entry.get('title', '?')} by {entry.get('artist', '?')}",
        "data": {**entry, "added": today},
    }


def query(message: str, claude_client, file_handler) -> dict:
    index = file_handler.read("data/music/index.md")
    system = claude_client.load_prompt("music")
    response = claude_client.chat(system, f"Query: {message}\n\nMusic index:\n{index}")
    return {"success": True, "message": response, "data": None}
