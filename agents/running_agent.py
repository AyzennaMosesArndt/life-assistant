"""Training session logging and zone-based plan generation."""
from core import claude_client, file_handler


def handle(message: str) -> str:
    return claude_client.chat(claude_client.load_prompt("running"), message)


def log_session(session: dict) -> str:
    formatted = "\n".join(f"- {k}: {v}" for k, v in session.items())
    file_handler.append_entry("running", formatted)
    return f"Logged session: {session.get('date', '?')} — {session.get('distance', '?')}"


def generate_plan(goal: str, weeks: int) -> str:
    return claude_client.chat(
        claude_client.load_prompt("running"),
        f"Generate a {weeks}-week training plan for: {goal}",
    )
