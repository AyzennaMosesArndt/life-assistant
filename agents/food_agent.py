"""Dish and meal cataloguing with geographic and preparation metadata."""
import json
import logging
from datetime import date

logger = logging.getLogger(__name__)

_QUERY_PATTERNS = [
    # English patterns
    "show", "list", "find", "search", "what", "which", "query", "tell me", "how many", "recommend", "suggest",
    # German patterns
    "gib mir", "zeig", "was kann ich", "suche", "finde", "empfiehl", "vorschlagen", "rezept"
]


def intent(message: str) -> str:
    lower = message.lower()
    if any(p in lower for p in _QUERY_PATTERNS):
        return "query"
    return "add"


def add_entry(message: str, claude_client, file_handler) -> dict:
    system = claude_client.load_prompt("food")
    response = claude_client.chat(system, message).strip()
    logger.info("add_entry() raw Claude response: %r", response)

    if response.startswith("CLARIFY:"):
        return {"success": False, "message": f"Clarify: {response[len('CLARIFY:'):].strip()}", "data": None}

    clean = response.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        entry = json.loads(clean)
    except json.JSONDecodeError:
        logger.error("JSON parse failed, returning raw response: %r", response)
        return {"success": True, "message": response, "data": None}

    if entry.get("confidence") == "low":
        return {"success": False, "message": "Clarify: dish origin is ambiguous.", "data": None}

    ingredients = entry.get("ingredients", [])
    if isinstance(ingredients, list):
        ingredients_str = ", ".join(ingredients)
    else:
        ingredients_str = str(ingredients)

    today = date.today().isoformat()
    formatted = (
        f"## entry\n"
        f"- title: {entry.get('title', '')}\n"
        f"- continent: {entry.get('continent', '')}\n"
        f"- country: {entry.get('country', '')}\n"
        f"- region: {entry.get('region', '')}\n"
        f"- meal_type: {entry.get('meal_type', '')}\n"
        f"- style: {entry.get('style', '')}\n"
        f"- prep_time: {entry.get('prep_time', '')} min\n"
        f"- servings: {entry.get('servings', '')}\n"
        f"- ingredients: {ingredients_str}\n"
        f"- added: {today}"
    )
    file_handler.append_entry("food", formatted)

    return {
        "success": True,
        "message": f"Saved: {entry.get('title', '?')} ({entry.get('country', '?')})",
        "data": {**entry, "ingredients": ingredients_str, "added": today},
    }


def query(message: str, claude_client, file_handler) -> dict:
    index = file_handler.read("data/food/index.md")
    system = claude_client.load_prompt("food")
    response = claude_client.chat(system, f"Query: {message}\n\nFood index:\n{index}")
    return {"success": True, "message": response, "data": None}
