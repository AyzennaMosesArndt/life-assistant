"""Anthropic SDK wrapper for the life assistant."""
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
MODEL = "claude-sonnet-4-5"
MAX_TOKENS = 1024


def chat(system: str, message: str) -> str:
    response = _client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": message}],
    )
    return response.content[0].text


def load_prompt(name: str) -> str:
    return (_PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")
