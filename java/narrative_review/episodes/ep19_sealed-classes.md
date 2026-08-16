# Episode 19 — Sealed Classes

| Field | Value |
|---|---|
| Episode | 19 |
| Title | Sealed Classes |
| Catalog handbook column | 19 |
| Narration source script | `make_episode_19.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Records cleaned up data carriers. Hierarchies still sprawl.
2. Anyone can subclass. Switches stay incomplete. Domain rules leak.
3. Sealed classes close the set of permitted subtypes.
4. You design the family. The compiler enforces the guest list.
5. Today — sealed types, permits, and exhaustive switches that finally trust you.
6. Controlled inheritance — not inheritance theater.

### Scene `title` (renderer: `title`)

1. Episode Nineteen.
2. Sealed Classes — controlled hierarchies.

### Scene `idea` (renderer: `idea`)

1. A sealed class or interface restricts who may extend or implement it.
2. You list permitted subtypes with permits.
3. Those subtypes must be in the same module — or the same package if unnamed.
4. Final, sealed, or non-sealed — each child declares how open it remains.
5. The hierarchy becomes a deliberate design artifact.
6. Open by accident is the bug sealed types fix.

### Scene `syntax` (renderer: `syntax`)

1. Look at the shape.
2. sealed interface Shape permits Circle, Rectangle, Triangle.
3. Circle can be final. Rectangle can be sealed further. Triangle can be non-sealed.
4. non-sealed reopens extension for that branch only.
5. You keep control at the root and choose where flexibility returns.
6. That is intentional polymorphism — not a free-for-all.

### Scene `switch` (renderer: `switch`)

1. Exhaustive switch is the payoff.
2. Switch on a sealed Shape — cover Circle, Rectangle, Triangle.
3. No default required when every permitted type is handled.
4. Add a new subtype later — the compiler forces you to update the switches.
5. That is safer evolution than hoping teams remember every if-else.
6. Pattern matching and sealed types were built to work together.

### Scene `when` (renderer: `when`)

1. When sealed types shine.
2. Domain models with a closed set of variants — payments, events, AST nodes.
3. APIs where third parties should not invent new subtypes.
4. When not — frameworks that need open extension points, or libraries that invite plugins.
5. Sealed is a design decision, not a default for every interface.
6. Close the hierarchy when completeness matters more than openness.

### Scene `records` (renderer: `records`)

1. Records and sealed types pair beautifully.
2. sealed interface Result permits Ok, Err.
3. record Ok of value. record Err of message.
4. Compact data plus a closed variant set.
5. Your switch becomes documentation that the compiler checks.
6. That is modern Java modeling — small, explicit, enforceable.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — sealing too early, then fighting every new legitimate subtype.
3. Two — forgetting non-sealed when a branch truly needs open extension.
4. Three — relying on default in switches and losing exhaustiveness warnings.
5. Also — putting permitted types in the wrong package or module.
6. Sealed types reward careful package and module boundaries.

### Scene `interview` (renderer: `interview`)

1. Interview question — what problem do sealed classes solve?
2. They restrict which types may extend a hierarchy.
3. That enables exhaustive switches and safer domain modeling.
4. Mention permits, and final versus sealed versus non-sealed subtypes.
5. Tie it to pattern matching for a modern answer.
6. That shows language design awareness — not just syntax.

### Scene `teaser` (renderer: `teaser`)

1. Hierarchies can be closed. Next — how code is packaged for the JVM.
2. Episode Twenty — modules and JPMS.
3. Requires, exports, and strong encapsulation.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **19** — *Sealed Classes*.
- **Series catalog:** Episode 19 ↔ handbook lesson 19 — *Sealed Classes*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Records cleaned up data carriers. Hierarchies still sprawl._
- **`title`** — starts from: _Episode Nineteen._
- **`idea`** — starts from: _A sealed class or interface restricts who may extend or implement it._
- **`syntax`** — starts from: _Look at the shape._
- **`switch`** — starts from: _Exhaustive switch is the payoff._
- **`when`** — starts from: _When sealed types shine._
- **`records`** — starts from: _Records and sealed types pair beautifully._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what problem do sealed classes solve?_
- **`teaser`** — starts from: _Hierarchies can be closed. Next — how code is packaged for the JVM._
