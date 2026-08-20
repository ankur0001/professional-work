# Narrative expansion style (4–15 min)

Use this for every episode file under `episodes/`.

## Duration
- Minimum spoken content ≈ **4 minutes** (~600+ words of narration)
- Comfortable target ≈ **8–12 minutes** (~1,200–1,800 words)
- Hard ceiling ≈ **15 minutes** (~2,200 words) — do not pad with fluff

## Voice
- Conversational mentor (like explaining to a junior teammate over coffee)
- Short spoken beats (1–3 sentences each), still listed as numbered beats under scenes
- Curiosity hooks, “watch this”, “here’s the trap”, “in an interview you’d say…”
- Not a textbook. Not a bullet dump.

## Structure (keep scene ids; expand beats)
1. Hook / continuity from previous episode
2. Title promise
3. Core concept explained slowly with analogy
4. Worked example (code fence when helpful — narrator can read it aloud)
5. Common mistakes
6. Interview-style wrap
7. Teaser for next episode

## Code
- Include at least one small Java snippet when the topic is code-related
- Put code in a fenced ```java block inside the scene section, then follow with spoken beats that walk through it line by line

## Source attribution
- Preserve the existing "## Source attribution" section from the prior file (update only if lesson mapping changes)
- Add a note: narration expanded for 4–15 minute runtime; handbook still used as topic reference

## File format
Keep the same markdown headers as existing files:
- Title H1
- Field table (update Spoken form / Runtime target)
- ## Full narration (spoken beats)
- scenes with ### Scene `id`
- ## Source attribution …
