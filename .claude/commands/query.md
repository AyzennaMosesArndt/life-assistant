# Command: query

Query or retrieve entries from a domain index.

**Usage:** Triggered when the user asks "what", "list", "show", "find", or "search".

**Flow:**
1. Router identifies the domain and query intent
2. Domain agent reads data/<domain>/index.md
3. Agent filters and formats relevant results

**Output:** Formatted list or summary of matching entries.
