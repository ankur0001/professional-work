# Episode 09 — Strings

| Field | Value |
|---|---|
| Episode | 09 |
| Title | Strings |
| Catalog handbook column | 9 |
| Narration source script | `make_episode_09.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Arrays hold many values. Strings hold text — and text is everywhere.
2. APIs, logs, JSON, HTTP, configuration, identifiers.
3. String is immutable. That safety is powerful — and easy to misuse.
4. Today we treat String like the production type it is.
5. Small mistakes here show up in security and performance.

### Scene `title` (renderer: `title`)

1. Episode Nine.
2. Strings — immutability, equality, and careful construction.

### Scene `immutable` (renderer: `immutable`)

1. Immutability means the characters never change after creation.
2. s equals s plus world does not edit s — it creates a new String.
3. That sharing and safety help concurrency and caching.
4. But careless concatenation can allocate again and again.
5. Understand create versus modify — String only creates.
6. That one idea prevents a whole class of confusion.

### Scene `equality` (renderer: `equality`)

1. Equality is the classic trap.
2. Equals-equals compares references — same String object?
3. For text content — use equals.
4. Safer pattern — literal first. PAID dot equals status.
5. Null-safe and clear. Interviewers listen for this.
6. Make equals your default reflex for text.

### Scene `build` (renderer: `build`)

1. Building strings in a loop?
2. Do not use plus repeatedly in hot loops.
3. Use StringBuilder — append in place, then toString once.
4. Modern compilers help simple cases — but builders win when you loop.
5. Measure hot paths. Clarity first — then allocation discipline.
6. Builders are the boring correct tool — use them.

### Scene `charset` (renderer: `charset`)

1. Bytes are not characters without a charset.
2. Prefer UTF-8 explicitly when encoding or decoding.
3. toLowerCase without a locale can surprise you in Turkish and beyond.
4. For identifiers, be explicit about case rules.
5. Never assume the platform default will match production.
6. Be explicit — always.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — equals-equals for text content.
3. Two — logging secrets inside strings — tokens, passwords, cards.
4. Three — accepting unbounded string input until memory cries.
5. Also — pushing raw strings deep into domain code. Prefer typed values.
6. A CustomerId type beats a naked string passed twelve layers deep.

### Scene `interview` (renderer: `interview`)

1. Interview question — why is String immutable?
2. Safety, sharing, hash stability for maps, and simpler concurrency reasoning.
3. Then add — use StringBuilder when you mutate often.
4. And never compare text with equals-equals.
5. That trio covers language design and daily practice.

### Scene `teaser` (renderer: `teaser`)

1. Text is under control. Next we model the world.
2. Episode Ten — object-oriented programming.
3. Classes, objects, encapsulation — how Java scales design.
4. See you there.

_Total beats: **46** across **9** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **9** — *Strings*.
- **Series catalog:** Episode 09 ↔ handbook lesson 9 — *Strings*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 9 excerpt)

- Concept: String represents immutable text in Java. Strings are central to APIs, logging, configuration, SQL, JSON, HTTP, identifiers, and user-visible data. Their immutability supports safety and sharing, but careless use can create memory, encoding, security,
- Mistakes: Common mistakes include using == for comparison, ignoring charset, logging secrets, using regex for simple checks, accepting unbounded string input, lowercasing with default locale, and passing raw strings deep into domain code.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 9).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Arrays hold many values. Strings hold text — and text is everywhere._
- **`title`** — starts from: _Episode Nine._
- **`immutable`** — starts from: _Immutability means the characters never change after creation._
- **`equality`** — starts from: _Equality is the classic trap._
- **`build`** — starts from: _Building strings in a loop?_
- **`charset`** — starts from: _Bytes are not characters without a charset._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why is String immutable?_
- **`teaser`** — starts from: _Text is under control. Next we model the world._
