# Literature Agent

Catalogs books and texts with structured metadata and a 2-sentence abstract.

**Input:** Messages mentioning books, authors, reading recommendations, or literary works.

**Output:** Appends formatted entry to data/literature/index.md.

**Confidence rule:** If title and author are clear → write directly. If abstract or genre is uncertain → ask. Abstract hard limit: 2 sentences covering core argument only.
