# Episode 15 — Generics

| Field | Value |
|---|---|
| Episode | 15 |
| Title | Generics |
| Catalog handbook column | 15 |
| Narration source script | `make_episode_15.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Wrappers made objects from values. Generics make containers type-safe.
2. List of Order — not List of Object with casts everywhere.
3. Generics move mistakes from runtime ClassCastException to compile time.
4. Today we read angle brackets with confidence.
5. This is how modern Java APIs stay both flexible and safe.
6. Angle brackets are not ceremony — they are contracts.

### Scene `title` (renderer: `title`)

1. Episode Fifteen.
2. Generics — type parameters without the cast tax.

### Scene `why` (renderer: `why`)

1. Before generics — a raw List held anything.
2. You cast on the way out. Wrong cast — boom at runtime.
3. List angle Order documents intent and enforces it.
4. The compiler becomes your first code reviewer.
5. That alone earns generics a permanent place in your toolkit.
6. Catch type mistakes before they ship.

### Scene `declare` (renderer: `declare`)

1. Type parameters look like this.
2. class Box angle T — T is a placeholder for a type.
3. Box angle String holds strings. Box angle Order holds orders.
4. Methods can be generic too — static angle T T first of List angle T.
5. Name type parameters clearly — T for type, E for element, K V for maps.

### Scene `bounds` (renderer: `bounds`)

1. Sometimes T needs limits.
2. angle T extends Number — only numeric types.
3. Wildcards — question mark extends — for flexible consumers.
4. PECS — producer extends, consumer super — when you dig deeper.
5. For now — prefer concrete type args at call sites when you can.

### Scene `erasure` (renderer: `erasure`)

1. Important JVM truth — type erasure.
2. Generics are mainly a compile-time tool.
3. At runtime, List angle Order is largely a List.
4. You cannot new T easily. You cannot check instanceof List angle Order.
5. Design with erasure in mind — do not fight the platform.
6. Know the limits so you use the strengths.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — raw types — List without angle brackets — undoing the safety.
3. Two — ignoring unchecked warnings until ClassCastExceptions return.
4. Three — overcomplicated wildcards where a simple type parameter would do.
5. Also — using Object when a generic method would express intent.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is type erasure?
2. Generics checked at compile time; type args are largely erased at runtime.
3. Why — backward compatibility with older bytecode.
4. Then — prefer parameterized types over raw types always.
5. That answer shows language history and daily discipline.

### Scene `teaser` (renderer: `teaser`)

1. Containers are type-safe. Next — metadata on code.
2. Episode Sixteen — annotations.
3. Override, Spring markers, and what retention means.
4. See you there.

_Total beats: **44** across **9** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **15** — *Generics*.
- **Series catalog:** Episode 15 ↔ handbook lesson 15 — *Generics*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Wrappers made objects from values. Generics make containers type-safe._
- **`title`** — starts from: _Episode Fifteen._
- **`why`** — starts from: _Before generics — a raw List held anything._
- **`declare`** — starts from: _Type parameters look like this._
- **`bounds`** — starts from: _Sometimes T needs limits._
- **`erasure`** — starts from: _Important JVM truth — type erasure._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is type erasure?_
- **`teaser`** — starts from: _Containers are type-safe. Next — metadata on code._
