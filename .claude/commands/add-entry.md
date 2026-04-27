# Command: add-entry

Add a new entry to a domain index.

**Usage:** Triggered when the user says "add", "log", "save", or "track" something.

**Flow:**
1. Router identifies the domain
2. Domain agent extracts structured fields from the message
3. file_handler appends the formatted entry to data/<domain>/index.md
4. Agent confirms what was written

**Output:** Confirmation with the written entry fields.
