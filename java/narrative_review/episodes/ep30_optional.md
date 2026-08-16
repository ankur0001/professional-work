# Episode 30 — Optional

| Field | Value |
|---|---|
| Episode | 30 |
| Title | Optional |
| Catalog handbook column | 30 |
| Narration source script | `make_episode_30.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Parallel streams need thread-safe design. Optional handles absence safely.
2. Null references cause bugs that compile fine and fail in production.
3. Optional is a container that may hold a value — or be empty.
4. It forces callers to acknowledge missing data explicitly.
5. Today — Optional as a design tool, not a silver bullet.
6. Present or empty — choose with intent.

### Scene `title` (renderer: `title`)

1. Episode Thirty.
2. Optional — modeling absence without null.

### Scene `present` (renderer: `present`)

1. Optional.of wraps a non-null value.
2. Optional.ofNullable accepts null — producing an empty Optional.
3. Optional.empty is the canonical empty instance.
4. isPresent and isEmpty test state without unwrapping.
5. Never call of with a value that might be null — use ofNullable.
6. Creation methods set expectations from the first line.

### Scene `absent` (renderer: `absent`)

1. An empty Optional is not null — it is an explicit absence.
2. get throws NoSuchElementException on empty — avoid in production code.
3. orElse supplies a default when empty.
4. orElseGet takes a supplier — lazy default computation.
5. orElseThrow maps absence to a meaningful exception.
6. Pick the fallback that matches your domain semantics.

### Scene `chain` (renderer: `chain`)

1. Optional chains avoid nested if-not-null checks.
2. ifPresent runs a consumer only when a value exists.
3. filter keeps the value only if a predicate passes.
4. map transforms the inner value if present.
5. flatMap transforms into another Optional — no nested Optional mess.
6. Chain fluently — stop when empty at any step.

### Scene `mapflat` (renderer: `mapflat`)

1. map is for simple transformations — String to Integer.
2. flatMap is for operations that themselves return Optional.
3. Lookup then parse. Find user then fetch profile.
4. flatMap flattens Optional of Optional into one level.
5. Combine with stream flatMap for filtering present values.
6. Readable pipelines replace defensive null ladders.

### Scene `when` (renderer: `when`)

1. When Optional shines.
2. Return types where absence is normal — findById, parse attempts.
3. Chaining transformations without null checks at every step.
4. When not to use it.
5. Fields on entities — prefer plain nullability discipline or records.
6. Method parameters — often clearer as overloads or validation.
7. Optional is for APIs and return types — not everywhere.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — Optional.of with a possibly null value.
3. Two — using get without checking — same as ignoring null.
4. Three — Optional fields in JSON entities — serialization pain.
5. Also — orElse with expensive work — use orElseGet instead.
6. Optional clarifies intent — misuse adds noise.

### Scene `interview` (renderer: `interview`)

1. Interview question — why Optional instead of null?
2. Forces explicit handling — isPresent, orElse, map chains.
3. Documents that absence is expected in the return type.
4. Mention ofNullable versus of — null safety at creation.
5. Note it is mainly for return values, not fields.
6. That answer shows modern Java API design awareness.

### Scene `teaser` (renderer: `teaser`)

1. Absence handled. Next — dates and times done right.
2. Episode Thirty-One — java.time.
3. Instant, LocalDate, ZonedDateTime — without Calendar pain.
4. See you there.

_Total beats: **55** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **30** — *Optional*.
- **Series catalog:** Episode 30 ↔ handbook lesson 30 — *Optional*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Parallel streams need thread-safe design. Optional handles absence safely._
- **`title`** — starts from: _Episode Thirty._
- **`present`** — starts from: _Optional.of wraps a non-null value._
- **`absent`** — starts from: _An empty Optional is not null — it is an explicit absence._
- **`chain`** — starts from: _Optional chains avoid nested if-not-null checks._
- **`mapflat`** — starts from: _map is for simple transformations — String to Integer._
- **`when`** — starts from: _When Optional shines._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why Optional instead of null?_
- **`teaser`** — starts from: _Absence handled. Next — dates and times done right._
