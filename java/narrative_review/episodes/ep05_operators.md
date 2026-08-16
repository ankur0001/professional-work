# Episode 05 — Operators

| Field | Value |
|---|---|
| Episode | 05 |
| Title | Operators |
| Catalog handbook column | 5 |
| Narration source script | `make_episode_05.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. In Episode Four, we chose types carefully.
2. Now those values meet operators — plus, equals, and, or.
3. Small symbols. Large consequences.
4. Overflow, equality bugs, and null crashes often start here.

### Scene `title` (renderer: `title`)

1. Episode Five.
2. Operators — arithmetic, equality, and short-circuit logic.

### Scene `families` (renderer: `families`)

1. Three families you use every day.
2. Arithmetic — plus, minus, multiply, divide.
3. Relational — less than, greater than, equals-equals.
4. Logical — and, or, not — decisions that branch your code.
5. Java evaluates left to right. Parentheses remove guesswork.

### Scene `equality` (renderer: `equality`)

1. The classic trap — equality.
2. For primitives, equals-equals compares values. Fine.
3. For objects, equals-equals compares references — same object in memory?
4. For String content — use equals. Never equals-equals for text you care about.
5. Safer pattern — put the literal first. PAID dot equals status.
6. That avoids a null pointer if status is null.

### Scene `shortcircuit` (renderer: `shortcircuit`)

1. Short-circuit logic protects you.
2. Double ampersand — and. Double pipe — or.
3. If the left side already decides the answer, the right side never runs.
4. user not null and user is active — the second call only happens when user exists.
5. Single ampersand does not short-circuit. That difference causes real bugs.
6. Use short-circuit when the second check is expensive — or unsafe.

### Scene `overflow` (renderer: `overflow`)

1. Arithmetic looks innocent.
2. int can silently wrap on overflow — no exception by default.
3. For money limits and counters, silent wrap is dangerous.
4. Prefer Math dot addExact when overflow must fail loudly.
5. Or use long — and still think about the upper bound.
6. Payment systems choose exact math for a reason.

### Scene `ternary` (renderer: `ternary`)

1. The ternary operator — question mark colon.
2. condition question result-if-true colon result-if-false.
3. Great for simple choices. Terrible for nested puzzles.
4. If the expression needs a paragraph of comments — extract a method instead.
5. Architect tip — order can be cancelled beats a pile of operators copied everywhere.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — equals-equals for String content.
3. Two — ignoring integer overflow until production numbers get big.
4. Three — side effects stuffed inside clever expressions. Hard to read. Hard to debug.
5. Also — trusting operator precedence instead of parentheses. Be kind to the next reader.

### Scene `interview` (renderer: `interview`)

1. Interview question — equals-equals versus equals?
2. Answer cleanly.
3. Equals-equals — references for objects. Values for primitives.
4. Equals — logical equality defined by the type.
5. Then add — short-circuit and protects null. That shows production sense.

### Scene `teaser` (renderer: `teaser`)

1. Operators decide. Next we control the path.
2. Episode Six — control flow.
3. if, else, switch, loops — how programs choose and repeat.
4. See you there.

_Total beats: **48** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **5** — *Operators*.
- **Series catalog:** Episode 05 ↔ handbook lesson 5 — *Operators*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 5 excerpt)

- Operators express arithmetic, comparison, logical decisions, assignment, bit manipulation, object checks, and conditional selection. In production Java, operators are small syntax with large consequences: overflow, short-circuiting, equality semantics, null sa
- Java inherited many operators from C/C++ but removed pointer arithmetic and operator overloading to improve safety and readability. Later features such as pattern matching for
- , integer overflow in financial limits, non-short-circuit boolean operations, incorrect precedence, unsafe casts, and broken bitmask logic. These bugs often pass basic tests and fail under edge data.
- Java provides a compact operator set for common operations while avoiding custom operator overloading. This keeps code predictable across teams. Special behavior is intentionally limited, such as
- Operators compile to bytecode instructions such as integer add, compare, branch, cast, and field updates. Numeric operands may be promoted before evaluation. Object equality with
- The JVM uses typed bytecode operations for primitive arithmetic and branching. The JIT may fold constants, eliminate redundant checks, inline

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 5).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _In Episode Four, we chose types carefully._
- **`title`** — starts from: _Episode Five._
- **`families`** — starts from: _Three families you use every day._
- **`equality`** — starts from: _The classic trap — equality._
- **`shortcircuit`** — starts from: _Short-circuit logic protects you._
- **`overflow`** — starts from: _Arithmetic looks innocent._
- **`ternary`** — starts from: _The ternary operator — question mark colon._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — equals-equals versus equals?_
- **`teaser`** — starts from: _Operators decide. Next we control the path._
