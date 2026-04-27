# CLAUDE.md

# CLAUDE.md – Life Assistant

## Project context

This is a personal life assistant system built as local Markdown files + SQLite,
operated via Claude Code in the terminal. No web app. No servers. Files are the
source of truth.

Modules: Music · Literature · Art · Food · Running · Learning · Research · Travel

---

## Behavioral principles

### 1. Think before coding
- State assumptions explicitly before implementing
- If a request is ambiguous, present 2–3 interpretations and ask which one
- Push back when a simpler approach exists
- Never silently pick an interpretation and run with it

### 2. Simplicity first
- Write the minimum code that solves the problem
- No speculative features, no "future-proofing" that wasn't requested
- No abstractions for single-use code
- Test: would a senior engineer call this overcomplicated? If yes, simplify.

### 3. Surgical changes
- Only touch what was asked
- Match existing file style and structure
- Do not reformat, rename, or "improve" adjacent code
- If changes create orphaned imports or dead functions: clean them up
- Pre-existing dead code: flag it, don't delete it

### 4. Goal-driven execution
- Transform vague tasks into verifiable goals before starting
- Multi-step tasks get a plan with checkpoints: step → verify → next step
- Ask clarifying questions before implementation, not during

---

## File structure

```
/life-assistant
  /music
    index.md        ← all entries
    genres.md       ← auto-maintained genre vocabulary
    /lists          ← curated lists (queries over index)
  /literature
    index.md
    /lists
  /art
    index.md
  /food
    index.md
    /recipes
    /articles
  /running
    index.md
    /exports        ← Garmin .fit files
  /learning
    index.md
    lernfelder.md   ← curiosity backlog
  /research
    /notes
  /travel
    index.md
    /trips
  master.md         ← personality profile + system rules
```

---

## Data models

### Music entry
```
- title:
- artist:
- album:
- year:
- genre:        ← check genres.md before creating new
- subgenre:
- added:        ← YYYY-MM-DD
```

### Literature entry
```
- title:
- author:
- publisher:
- year:
- genre:
- subgenre:
- bestseller_weeks:
- abstract:     ← max 2 sentences, core argument only
- added:
```

### Art entry
```
- title:
- artist:
- year:
- epoch:
- medium:       ← open vocabulary: painting, photography, video-art, etc.
- note:         ← max 2 sentences, reception + interpretation
- added:
```

### Food entry
```
- title:
- continent:
- country:
- region:
- meal_type:    ← breakfast / lunch / dinner / snack
- style:        ← stir-fry / baked / raw / etc.
- prep_time:    ← minutes
- servings:
- ingredients:  ← list
- added:
```

### Learning field (lernfelder.md)
```
- topic:
- description:  ← one sentence, what the user wants to understand
- complexity:   ← casual / medium / deep
- added:
- status:       ← backlog / active / done
```

---

## Agent rules

### Genre vocabulary (music)
- Before adding a new genre/subgenre, check genres.md
- If a close match exists, use it (normalize: "trip hop" → "trip-hop")
- If genuinely new, add it to genres.md and use it
- Never invent genre variants silently

### Categorization confidence
- High confidence → categorize and inform user
- Low confidence → ask before writing

### Note / abstract length
- Hard limit: 2 sentences
- No summaries, no descriptions – only reception, interpretation, or key insight

### Learning agent + research agent boundary
- Simple / casual topics → learning agent handles alone
- Complex topics → research agent provides overview first, learning agent derives resources

### Running agent (placeholder – Garmin format TBD)
Training plans always include:
- Zone-based running sessions (progressive load)
- Mobility work
- Core training
- Ancestral movement (carries, crawls, ground work, natural patterns)

Principles: conservative build-up, no overreaching, balance load and recovery.

---

## Master agent – personality profile

User: active marathon runner and hiker, backpacker-style traveler (40L, carry-on only), 
Wirtschaftsinformatik Master's student, background in IT consulting and real estate. 
Based in Taipei (semester abroad), German, early-to-mid twenties.

Interests: running, hiking, cooking, literature, music, art, self-directed learning.
Travel style: authentic over touristic, local transport, local food, moves on foot.
Learning style: broad curiosity across unrelated domains, prefers concise + dense over exhaustive.
Work style: project-driven, values clean architecture, dislikes overengineering.

## Communication style

- Concise and direct, no filler
- Ask before implementing when ambiguous
- Flag concerns but don't block – state the issue once, then proceed if user confirms
- No unsolicited suggestions outside current task scope
- Language: respond in whatever language the user writes in (German or English)
