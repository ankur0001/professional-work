# Episode 14 — Wrappers and Autoboxing

| Field | Value |
|---|---|
| Episode | 14 |
| Title | Wrappers and Autoboxing |
| Catalog handbook column | 14 |
| Narration source script | `make_episode_14.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Enums gave us type-safe states. Now look at numbers as objects.
2. int is a primitive. Integer is a wrapper — an object that can be null.
3. Autoboxing hides the conversion — and can hide costs and crashes.
4. Today we make that invisible work visible.
5. Get this mental model right — collections depend on it.
6. Lists and maps need objects — wrappers bridge that gap.

### Scene `title` (renderer: `title`)

1. Episode Fourteen.
2. Wrappers and Autoboxing — objects around primitives.

### Scene `pairs` (renderer: `pairs`)

1. Eight primitives. Eight wrappers.
2. int and Integer. long and Long. boolean and Boolean.
3. Wrappers live on the heap. They have identity. They can be null.
4. Primitives cannot be null — and that alone prevents many bugs.
5. Choose intentionally — do not default to wrappers everywhere.
6. Default to primitives unless nullability is required.

### Scene `autobox` (renderer: `autobox`)

1. Autoboxing converts automatically.
2. Integer x equals ten — boxes the int.
3. int y equals x — unboxes the Integer.
4. Convenient in Lists and Maps that need objects.
5. Dangerous when x is null — unboxing throws NullPointerException.
6. Null plus silent conversion is a classic production trap.

### Scene `cost` (renderer: `cost`)

1. Wrappers cost more than primitives.
2. Object header. Indirection. Extra allocations.
3. A List of Integer can thrash the heap versus an int array.
4. Hot loops that box every iteration pay a quiet tax.
5. Prefer primitives in hot paths. Use wrappers when null is a real signal.
6. Measure before you box every number in a tight loop.

### Scene `cache` (renderer: `cache`)

1. One more quirk — Integer caching.
2. Small values are often cached — so equals-equals may look true by accident.
3. Do not rely on that. Compare wrappers with equals.
4. Autoboxing is not a reason to forget object equality rules.
5. Be explicit — always.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — unboxing a null wrapper into a primitive.
3. Two — using wrappers in hot numeric loops without need.
4. Three — comparing wrappers with equals-equals.
5. Also — Boolean in conditions without null checks.
6. Nullability is a feature — treat it like one.

### Scene `interview` (renderer: `interview`)

1. Interview question — primitive versus wrapper?
2. Primitive — value, non-null, compact, fast.
3. Wrapper — object, nullable, overhead, autoboxing risk.
4. Then mention NullPointerException on unboxing.
5. That lands the production-level detail.
6. Interviewers listen for null and allocation awareness.

### Scene `teaser` (renderer: `teaser`)

1. Objects around values. Next — type-safe containers.
2. Episode Fifteen — generics.
3. List of Order — compile-time safety without casts.
4. See you there.

_Total beats: **47** across **9** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **14** — *Wrappers and Autoboxing*.
- **Series catalog:** Episode 14 ↔ handbook lesson 14 — *Wrappers and Autoboxing*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Enums gave us type-safe states. Now look at numbers as objects._
- **`title`** — starts from: _Episode Fourteen._
- **`pairs`** — starts from: _Eight primitives. Eight wrappers._
- **`autobox`** — starts from: _Autoboxing converts automatically._
- **`cost`** — starts from: _Wrappers cost more than primitives._
- **`cache`** — starts from: _One more quirk — Integer caching._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — primitive versus wrapper?_
- **`teaser`** — starts from: _Objects around values. Next — type-safe containers._
