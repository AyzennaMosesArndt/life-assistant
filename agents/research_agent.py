"""Structured overviews for complex topics, called by the learning agent."""
from core import claude_client, file_handler


def handle(message: str) -> str:
    return claude_client.chat(claude_client.load_prompt("research"), message)


def write_overview(topic: str, content: str) -> str:
    slug = topic.lower().replace(" ", "-")
    file_handler.write(f"data/research/notes/{slug}.md", f"# {topic}\n\n{content}\n")
    return f"Research note saved: {slug}.md"
