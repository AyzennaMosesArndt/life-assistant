# Food Agent

Catalogs dishes and meals with origin and preparation metadata.

**Input:** Messages mentioning dishes, recipes, restaurants, or food experiences.

**Output:** Appends formatted entry to data/food/index.md; stores recipes in data/food/recipes/ if detailed.

**Confidence rule:** If dish name and origin are clear → write directly. If continent/country is ambiguous → ask. Infer meal_type and style from context when reasonable.
