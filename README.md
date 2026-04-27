# Life Assistant

A personal AI assistant system operated via Telegram bot. Natural language in, structured data out. No web app, no server – local Markdown files as source of truth.

## What it does

Send a message to your Telegram bot. The router classifies the intent and dispatches to the right agent. The agent extracts structured metadata, writes it to the appropriate Markdown index, and confirms what was saved.

Supported domains: Music · Literature · Art · Food · Learning · Research · Travel

## Architecture

```
life-assistant/
  bot.py                  ← Telegram entry point
  core/
    router.py             ← intent classification + dispatch
    claude_client.py      ← Anthropic API wrapper
    file_handler.py       ← all file I/O
  agents/                 ← one agent per domain
  prompts/                ← system prompts per agent
  data/                   ← Markdown indexes (gitignored content)
  .claude/
    rules/                ← code style + data models
    commands/             ← slash command definitions
    agents/               ← agent descriptions for Claude Code
```

## Stack

- Python 3.11 + conda
- python-telegram-bot
- Anthropic Claude API (claude-sonnet-4-5)
- Markdown flat files (no database)

## Agents

| Agent | Add | Query | Notes |
|---|---|---|---|
| Music | ✓ | ✓ | Genre vocabulary auto-maintained in genres.md |
| Literature | ✓ | ✓ | Abstract max 2 sentences, analytical only |
| Art | ✓ | ✓ | Open medium vocabulary, reception-focused note |
| Food | ✓ | ✓ | Geographic classification, ingredient list |
| Learning | ✓ | ✓ | Lernfelder backlog + topic suggestions |
| Research | – | ✓ | Three modes: quick / deep / academic |
| Travel | – | ✓ | Profile-based recommendations |

## Research modes

- **Quick** – 4-6 sentence explanation, not saved
- **Deep** – structured report, saved to `data/research/notes/`
- **Academic** – publications only (arXiv, PubMed, Scholar), saved with `-academic` suffix

## Setup

1. Clone repo
2. Create conda environment: `conda create -n life-assistant python=3.11`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `prompts/master.example.md` to `prompts/master.md` and fill in your profile
5. Create `.env`:

```
ANTHROPIC_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
```

6. Run: `python bot.py`

## Autostart (Windows)

Use the included `start_bot_hidden.vbs` with Windows Task Scheduler.  
See `TASK_SCHEDULER_SETUP.md` for step-by-step instructions.

## Roadmap

- [ ] Frontend (editorial style, React or Svelte)
- [ ] Cover art via MusicBrainz, Open Library, Wikimedia APIs
- [ ] Spotify integration for music module
- [ ] Garmin .fit integration for running module
- [ ] AgentReach / Feynman integration for research module
- [ ] VPS deployment