# Command: learn

Add a topic to the curiosity backlog or update its status.

**Usage:** Triggered when the user says "I want to learn", "add to backlog", "mark as done", or references a learning topic.

**Flow:**
1. Learning agent extracts topic, complexity, and status
2. Writes or updates entry in data/learning/lernfelder.md
3. For complex topics, research agent provides an overview first

**Output:** Confirmation of what was added or updated.
