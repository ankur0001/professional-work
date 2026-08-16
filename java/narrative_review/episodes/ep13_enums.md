# Episode 13 — Enums

| Field | Value |
|---|---|
| Episode | 13 |
| Title | Enums |
| Catalog handbook column | 13 |
| Narration source script | `make_episode_13.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Packages organize types. Enums organize fixed choices.
2. PENDING. PAID. CANCELLED — states that should never be free-form strings.
3. An enum is a type-safe set of named constants — with room for behavior.
4. Today we replace magic strings with real domain states.
5. Treat enum structure as architecture you can see in the type system.

### Scene `title` (renderer: `title`)

1. Episode Thirteen.
2. Enums — type-safe states instead of magic strings.

### Scene `basics` (renderer: `basics`)

1. Declare an enum like a special class.
2. enum OrderStatus — PENDING, PAID, SHIPPED, CANCELLED.
3. Each constant is a singleton instance of that enum type.
4. Compare with equals-equals safely — identity is stable.
5. Switch expressions love enums — finite cases, clear exhaustiveness.
6. Folder path and package declaration must agree — same for enum files.

### Scene `behavior` (renderer: `behavior`)

1. Enums can carry fields and methods.
2. Attach a display label. Attach a canTransition rule.
3. That keeps status logic next to the status itself.
4. Better than scattering string compares across services.
5. Feature teams and domain packages often fit better than pure layers — enums fit domains too.
6. Put behavior where the state lives.

### Scene `vs_string` (renderer: `vs_string`)

1. Why not String status equals PAID?
2. Typos compile. Invalid states sneak in. Refactors miss call sites.
3. Enums make illegal states harder to represent.
4. Serialization still needs care — name versus ordinal.
5. Prefer name for APIs. Ordinal is a storage trap.
6. Honest names reduce wrong imports and wrong ownership — same for status names.

### Scene `enumset` (renderer: `enumset`)

1. Need a set of flags? EnumSet is built for enums.
2. Fast. Compact. Type-safe.
3. Permission READ, WRITE, ADMIN — store combinations cleanly.
4. Better than bit masks scattered as magic ints — unless you truly need bits.
5. Choose the structure that matches how the set changes.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — Stringly typed statuses that drift across services.
3. Two — depending on ordinal in databases or APIs.
4. Three — stuffing volatile business config into enum constants.
5. Also — giant enums that should have been a data table.
6. Enums model fixed vocabularies — not every changing catalog.

### Scene `interview` (renderer: `interview`)

1. Interview question — why prefer enums over string constants?
2. Type safety. Exhaustive switches. Refactor-friendly names.
3. Constants are real objects — can hold behavior.
4. Avoid ordinal for persistence. Prefer name or explicit codes.
5. That answer shows production sense.

### Scene `teaser` (renderer: `teaser`)

1. Fixed states are clear. Next — when primitives become objects.
2. Episode Fourteen — wrappers and autoboxing.
3. Integer, nullability, and hidden allocations.
4. See you there.

_Total beats: **45** across **9** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **13** — *Enums*.
- **Series catalog:** Episode 13 ↔ handbook lesson 13 — *Enums*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Packages organize types. Enums organize fixed choices._
- **`title`** — starts from: _Episode Thirteen._
- **`basics`** — starts from: _Declare an enum like a special class._
- **`behavior`** — starts from: _Enums can carry fields and methods._
- **`vs_string`** — starts from: _Why not String status equals PAID?_
- **`enumset`** — starts from: _Need a set of flags? EnumSet is built for enums._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why prefer enums over string constants?_
- **`teaser`** — starts from: _Fixed states are clear. Next — when primitives become objects._
