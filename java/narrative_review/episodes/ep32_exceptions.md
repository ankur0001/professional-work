# Episode 32 — Exceptions

| Field | Value |
|---|---|
| Episode | 32 |
| Title | Exceptions |
| Catalog handbook column | 32 |
| Narration source script | `make_episode_32.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Programs fail. Networks drop. Files vanish. Users type nonsense.
2. Exceptions are Java way of signaling that something went wrong.
3. Not every error is a crash — some are expected and recoverable.
4. Checked exceptions force you to acknowledge risk at compile time.
5. Unchecked exceptions flag programming bugs and broken assumptions.
6. Today — how Java models failure, and how to handle it with intent.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Two.
2. Exceptions — checked, unchecked, and handling failure.

### Scene `hierarchy` (renderer: `hierarchy`)

1. Throwable sits at the root of the error hierarchy.
2. Error is for serious JVM problems — you rarely catch these.
3. Exception is what application code usually deals with.
4. RuntimeException and its subclasses are unchecked.
5. Everything else under Exception is checked — the compiler enforces handling.
6. Know the hierarchy before you catch broadly.

### Scene `trycatch` (renderer: `trycatch`)

1. try wraps code that might throw.
2. catch handles a specific exception type — order matters, most specific first.
3. You can catch multiple types in one block since Java seven.
4. Handle what you can recover from — log, retry, or return a safe default.
5. Swallowing exceptions silently is almost always wrong.
6. A narrow catch beats catch Exception everywhere.

### Scene `throws` (renderer: `throws`)

1. throws declares that a method may propagate an exception.
2. Callers must handle checked exceptions — try-catch or declare throws.
3. Unchecked exceptions do not require a throws clause.
4. Document what can go wrong — throws is part of the contract.
5. Do not use throws to push problems up without a plan.
6. Sometimes wrapping a checked exception in an unchecked one is cleaner.

### Scene `finally` (renderer: `finally`)

1. finally runs whether the try block succeeds or throws.
2. Classic use — release resources in a finally block.
3. Modern code prefers try-with-resources — we cover that next episode.
4. Do not return from finally — it can mask the real exception.
5. finally is for cleanup that must happen no matter what.
6. Keep finally blocks short and predictable.

### Scene `custom` (renderer: `custom`)

1. Define custom exceptions when domain errors need clear names.
2. Extend Exception for checked, RuntimeException for unchecked.
3. Provide meaningful constructors — message, cause, both.
4. BankAccountOverdrawnException beats a generic IllegalStateException.
5. Do not create an exception class for every trivial case.
6. Good exception names read like answers to what went wrong.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — catching Exception or Throwable and doing nothing useful.
3. Two — using exceptions for normal control flow — they are expensive.
4. Three — throwing generic RuntimeException without context or cause.
5. Also — empty catch blocks that hide production bugs.
6. Fail loudly in development. Handle deliberately in production.

### Scene `interview` (renderer: `interview`)

1. Interview question — checked versus unchecked exceptions?
2. Checked — compiler requires handling or declaring throws.
3. Unchecked — extends RuntimeException, no compile-time enforcement.
4. Checked for recoverable conditions callers should know about.
5. Unchecked for programming errors and broken invariants.
6. Mention try-with-resources for cleanup — that shows modern Java.

### Scene `teaser` (renderer: `teaser`)

1. You know how to catch failure. Next — how to close resources safely.
2. Episode Thirty-Three — try-with-resources.
3. AutoCloseable, suppressed exceptions, and leak-free I/O.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **32** — *Exceptions*.
- **Series catalog:** Episode 32 ↔ handbook lesson 32 — *Exceptions*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Programs fail. Networks drop. Files vanish. Users type nonsense._
- **`title`** — starts from: _Episode Thirty-Two._
- **`hierarchy`** — starts from: _Throwable sits at the root of the error hierarchy._
- **`trycatch`** — starts from: _try wraps code that might throw._
- **`throws`** — starts from: _throws declares that a method may propagate an exception._
- **`finally`** — starts from: _finally runs whether the try block succeeds or throws._
- **`custom`** — starts from: _Define custom exceptions when domain errors need clear names._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — checked versus unchecked exceptions?_
- **`teaser`** — starts from: _You know how to catch failure. Next — how to close resources safely._
