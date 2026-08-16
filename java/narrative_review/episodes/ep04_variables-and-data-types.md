# Episode 04 — Variables and Data Types

| Field | Value |
|---|---|
| Episode | 04 |
| Title | Variables and Data Types |
| Catalog handbook column | 4 |
| Narration source script | `make_episode_04.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. In Episode Three, we mapped packages and classes.
2. Now — what actually lives inside those fields and methods?
3. Variables name values. Types decide what is valid.
4. Pick the wrong type… and production pays for it — overflow, nulls, money bugs.

### Scene `title` (renderer: `title`)

1. Episode Four.
2. Variables and Data Types — primitives, references, and real choices.

### Scene `families` (renderer: `families`)

1. Java has two families of types. Keep this picture.
2. On the left — primitives. Raw values. Fast. Never null.
3. On the right — references. They point to objects on the heap.
4. Assignment behaves differently in each family — that is why this split matters.
5. That mental model everything else builds on.

### Scene `primitives` (renderer: `primitives`)

1. Eight primitives — memorize the common ones first.
2. int for whole numbers. long for bigger IDs and timestamps.
3. boolean for true or false. double for binary floating point.
4. byte, short, char, float exist too — useful, but rarer in day-to-day code.
5. Primitives hold the value itself — not a pointer.
6. And they cannot be null. That alone prevents a whole class of bugs.

### Scene `memory` (renderer: `memory`)

1. Picture memory.
2. int count equals ten — the value sits in the local frame.
3. Order order equals new Order — the variable holds a reference.
4. The real object lives on the heap.
5. Assignment copies the primitive… or copies the reference — not the whole object.
6. final blocks reassignment of that variable — it does not freeze the object inside.

### Scene `money` (renderer: `money`)

1. Production gotcha — money.
2. Never store currency in double.
3. Binary floating point cannot represent many decimals exactly.
4. Prefer long minor units — cents — or a Money value type.
5. Use BigDecimal when you need precise decimal math and rounding rules.
6. Architects standardize this early — because fixing money types later is expensive.

### Scene `wrappers` (renderer: `wrappers`)

1. Wrappers look similar — Integer, Long, Boolean.
2. They are objects. They can be null. They cost more memory.
3. Autoboxing hides conversions — and can hide NullPointerExceptions too.
4. A List of Integer can thrash the heap versus an int array.
5. Prefer primitives in hot paths. Use wrappers when null is a real signal.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — double for money. Rounding bugs wait quietly.
3. Two — ignoring integer overflow on big counters.
4. Three — assuming final means deep immutability. It only blocks reassignment.
5. Bonus trap — overusing String for every domain idea. Prefer typed values when meaning matters.

### Scene `interview` (renderer: `interview`)

1. Interview question — primitive versus wrapper?
2. Answer on screen.
3. Primitive — value, non-null, compact.
4. Wrapper — object, nullable, overhead, autoboxing risk.
5. Then mention — why avoid double for money. That lands the offer-level detail.

### Scene `teaser` (renderer: `teaser`)

1. You now know how Java stores meaning.
2. Next — operators.
3. Plus, compare, and, or — and the traps that break equality checks.
4. Episode Five. See you there.

_Total beats: **48** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **4** — *Variables and Data Types*.
- **Series catalog:** Episode 04 ↔ handbook lesson 4 — *Variables and Data Types*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 4 excerpt)

- Variables name values, and data types define what values are valid and how operations behave. Java has primitive types for raw values and reference types for objects. For architects, type choices influence correctness, memory footprint, serialization, database
- Java started with eight primitive types and object references. Later releases added autoboxing, generics, var
- Incorrect type choices cause overflow, precision loss, null pointer failures, memory bloat, serialization bugs, and unclear domain models. A money field stored as double
- Java provides primitives for efficient numeric and boolean operations, references for object modeling, String
- Primitive variables hold actual values. Reference variables hold references to heap objects. Assignment copies primitive values or reference values, not full objects. final
- prevents reassignment but does not make referenced objects immutable.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 4).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _In Episode Three, we mapped packages and classes._
- **`title`** — starts from: _Episode Four._
- **`families`** — starts from: _Java has two families of types. Keep this picture._
- **`primitives`** — starts from: _Eight primitives — memorize the common ones first._
- **`memory`** — starts from: _Picture memory._
- **`money`** — starts from: _Production gotcha — money._
- **`wrappers`** — starts from: _Wrappers look similar — Integer, Long, Boolean._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — primitive versus wrapper?_
- **`teaser`** — starts from: _You now know how Java stores meaning._
