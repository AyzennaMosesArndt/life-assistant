"""Research assistant with quick, deep, and academic modes."""
import logging
import re
from datetime import date
from pathlib import Path

logger = logging.getLogger(__name__)

_QUICK_PATTERNS = ["erkläre", "was ist", "unterschied", "wie funktioniert", "kurz", "explain", "what is", "difference", "how does"]
_DEEP_PATTERNS = ["recherchiere", "ausführlich", "report", "übersicht zu", "deep dive", "research", "comprehensive", "overview"]
_ACADEMIC_PATTERNS = ["paper", "studie", "literatur", "wissenschaftlich", "aktuelle forschung", "publikation", "zitiert", "study", "literature", "scientific", "recent research", "publication", "cited"]


def intent(message: str) -> str:
    """Classify research intent: academic > deep > quick (priority order)."""
    lower = message.lower()

    # Check which pattern groups match
    has_academic = any(p in lower for p in _ACADEMIC_PATTERNS)
    has_deep = any(p in lower for p in _DEEP_PATTERNS)
    has_quick = any(p in lower for p in _QUICK_PATTERNS)

    # If multiple modes match, ask for clarification
    matches = sum([has_academic, has_deep, has_quick])
    if matches > 1:
        return "clarify"

    # Priority order: academic > deep > quick
    if has_academic:
        return "academic"
    if has_deep:
        return "deep"
    return "quick"


def quick(message: str, claude_client) -> dict:
    """Quick explanation, 4-6 sentences, nothing saved."""
    system = claude_client.load_prompt("research")
    response = claude_client.chat(system, f"Quick mode: {message}")
    return {"success": True, "message": response, "data": None}


def deep(message: str, claude_client, file_handler) -> dict:
    """Structured markdown report, saved to file."""
    system = claude_client.load_prompt("research")
    response = claude_client.chat(system, f"Deep mode: {message}")

    # Generate filename slug from message
    slug = _slugify(message)[:50]  # limit slug length
    today = date.today().isoformat()
    filename = f"{today}-{slug}.md"
    filepath = Path("data/research/notes") / filename

    # Save report
    file_handler.write(str(filepath), response)
    logger.info("Deep research saved to %s", filepath)

    # Extract first paragraph as summary
    summary = response.split("\n\n")[0].strip()
    return {
        "success": True,
        "message": f"{summary}\n\nSaved: {filename}",
        "data": {"filepath": str(filepath), "content": response}
    }


def academic(message: str, claude_client, file_handler) -> dict:
    """Academic literature overview, saved to file."""
    system = claude_client.load_prompt("research")
    response = claude_client.chat(system, f"Academic mode: {message}")

    # Generate filename slug from message
    slug = _slugify(message)[:50]
    today = date.today().isoformat()
    filename = f"{today}-{slug}-academic.md"
    filepath = Path("data/research/notes") / filename

    # Save report
    file_handler.write(str(filepath), response)
    logger.info("Academic research saved to %s", filepath)

    # Extract first paragraph as summary
    summary = response.split("\n\n")[0].strip()
    return {
        "success": True,
        "message": f"{summary}\n\nSaved: {filename}",
        "data": {"filepath": str(filepath), "content": response}
    }


def _slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    # Remove everything that's not alphanumeric, space, or hyphen
    text = re.sub(r"[^\w\s-]", "", text.lower())
    # Replace spaces with hyphens
    text = re.sub(r"[\s]+", "-", text)
    # Remove consecutive hyphens
    text = re.sub(r"-+", "-", text)
    return text.strip("-")
