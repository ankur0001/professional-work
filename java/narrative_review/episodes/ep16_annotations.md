# Episode 16 — Annotations

| Field | Value |
|---|---|
| Episode | 16 |
| Title | Annotations |
| Catalog handbook column | 16 |
| Narration source script | `make_episode_16.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Generics typed our containers. Annotations label our code.
2. An annotation is metadata — information about the code, attached to the code.
3. Override. Deprecated. Spring markers. Validation rules.
4. Tiny symbols. Huge framework power.
5. Today we learn what annotations are — and what they are not.
6. Angle brackets were contracts. At-signs are signals.

### Scene `title` (renderer: `title`)

1. Episode Sixteen.
2. Annotations — metadata that frameworks and compilers read.

### Scene `what` (renderer: `what`)

1. An annotation starts with an at-sign.
2. It can mark a class, a method, a field, a parameter — even another annotation.
3. By itself, most annotations do nothing magical at runtime.
4. Something must read them — the compiler, a tool, or a framework.
5. Think of them as sticky notes with structure.
6. The note matters only if someone looks.

### Scene `builtin` (renderer: `builtin`)

1. Start with built-ins you already use.
2. Override — catch signature mistakes when you think you are overriding.
3. Deprecated — warn callers that an API is going away.
4. SuppressWarnings — silence a warning you have consciously accepted.
5. FunctionalInterface — document a single abstract method type.
6. These are small, precise, and compile-time friendly.

### Scene `retention` (renderer: `retention`)

1. Retention answers — how long does this annotation live?
2. Source — only in source. Gone after compile.
3. Class — in the class file. Not necessarily visible at runtime.
4. Runtime — readable through reflection while the program runs.
5. Spring and many frameworks need runtime retention.
6. If retention is wrong, your marker is invisible when it matters.

### Scene `spring` (renderer: `spring`)

1. In Spring, annotations drive wiring.
2. SpringBootApplication. RestController. Service. Autowired.
3. They tell the framework what to scan, create, and inject.
4. That is powerful — and easy to overuse.
5. Prefer clear boundaries. Do not decorate every line into a mystery.
6. Annotations should clarify intent — not hide architecture.

### Scene `custom` (renderer: `custom`)

1. You can define your own annotations.
2. Declare an interface with an at-sign — interface RoleRequired.
3. Add retention and target so tools know where it applies.
4. Then write a processor or runtime check that enforces it.
5. Without a reader, a custom annotation is just documentation in disguise.
6. Design the annotation and the enforcement together.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — assuming an annotation does work with no processor behind it.
3. Two — wrong retention — runtime framework never sees your marker.
4. Three — annotation soup — so many markers the real flow disappears.
5. Also — using SuppressWarnings to hide problems instead of fixing types.
6. Annotations amplify discipline. They do not replace it.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is an annotation in Java?
2. Structured metadata attached to code elements.
3. Useful when compilers, tools, or frameworks read it.
4. Mention retention — source, class, runtime.
5. Then give Override versus a Spring stereotype as examples.
6. That answer covers language and ecosystem.

### Scene `teaser` (renderer: `teaser`)

1. Metadata is clear. Next — looking inside types at runtime.
2. Episode Seventeen — reflection.
3. Inspect classes, call methods, and know the costs.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **16** — *Annotations*.
- **Series catalog:** Episode 16 ↔ handbook lesson 16 — *Annotations*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Generics typed our containers. Annotations label our code._
- **`title`** — starts from: _Episode Sixteen._
- **`what`** — starts from: _An annotation starts with an at-sign._
- **`builtin`** — starts from: _Start with built-ins you already use._
- **`retention`** — starts from: _Retention answers — how long does this annotation live?_
- **`spring`** — starts from: _In Spring, annotations drive wiring._
- **`custom`** — starts from: _You can define your own annotations._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is an annotation in Java?_
- **`teaser`** — starts from: _Metadata is clear. Next — looking inside types at runtime._
