# Episode 17 — Reflection

| Field | Value |
|---|---|
| Episode | 17 |
| Title | Reflection |
| Catalog handbook column | 17 |
| Narration source script | `make_episode_17.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Annotations are metadata. Reflection is how code reads the structure of types at runtime.
2. Ask a class for its methods. Read fields. Create instances by name.
3. Frameworks do this constantly — Spring, serializers, test tools.
4. Powerful. Flexible. Easy to misuse.
5. Today we open the hood — carefully.
6. Know the tool. Respect the cost.

### Scene `title` (renderer: `title`)

1. Episode Seventeen.
2. Reflection — inspect and invoke types at runtime.

### Scene `basics` (renderer: `basics`)

1. Start with Class.
2. Order.class or order.getClass — you get a Class object.
3. From there — getMethods, getFields, getConstructors.
4. You can discover what a type offers without hardcoding every name.
5. That discovery is the heart of reflective programming.
6. Dynamic systems are built on this doorway.

### Scene `invoke` (renderer: `invoke`)

1. Reflection can call methods too.
2. Lookup a Method. Invoke it with arguments.
3. You can even reach private members — with setAccessible.
4. That breaks encapsulation walls — use it only with clear cause.
5. Libraries may need it. Business code usually should not.
6. If you reach for private access daily — redesign the API.

### Scene `frameworks` (renderer: `frameworks`)

1. Why frameworks love reflection.
2. Dependency injection scans annotations and constructs beans.
3. JSON mappers bind properties without hand-written glue for every class.
4. ORMs inspect entities and map tables.
5. You get productivity — the platform pays with complexity.
6. Understanding reflection makes those magic layers less magical.

### Scene `cost` (renderer: `cost`)

1. Reflection is not free.
2. Lookups are slower than direct calls.
3. Security managers and modules can restrict access.
4. Native images and Graal may need extra config for reflective use.
5. Cache Method handles if you must reflect in a hot path.
6. Prefer normal calls when the type is known at compile time.

### Scene `safety` (renderer: `safety`)

1. Safety rules of thumb.
2. Validate names and inputs — reflective calls can become injection surfaces.
3. Do not suppress access checks casually in application code.
4. Log clearly when reflective fallbacks run — they hide bugs.
5. If a feature needs reflection, quarantine it behind a small module.
6. Power without boundaries becomes an incident.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using reflection where an interface would do.
3. Two — calling setAccessible everywhere and calling it fine.
4. Three — ignoring performance until the profiler screams.
5. Also — assuming field names are a stable public API.
6. Reflect on purpose — not as a default style.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is reflection in Java?
2. Runtime inspection and interaction with classes, methods, and fields.
3. Used heavily by frameworks for wiring and mapping.
4. Tradeoffs — flexibility versus speed, safety, and clarity.
5. Mention modules and native-image constraints for senior signal.
6. That answer balances power and caution.

### Scene `teaser` (renderer: `teaser`)

1. We can inspect types. Next — a cleaner way to carry data.
2. Episode Eighteen — records.
3. Transparent data carriers with less boilerplate.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **17** — *Reflection*.
- **Series catalog:** Episode 17 ↔ handbook lesson 17 — *Reflection*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Annotations are metadata. Reflection is how code reads the structure of types at runtime._
- **`title`** — starts from: _Episode Seventeen._
- **`basics`** — starts from: _Start with Class._
- **`invoke`** — starts from: _Reflection can call methods too._
- **`frameworks`** — starts from: _Why frameworks love reflection._
- **`cost`** — starts from: _Reflection is not free._
- **`safety`** — starts from: _Safety rules of thumb._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is reflection in Java?_
- **`teaser`** — starts from: _We can inspect types. Next — a cleaner way to carry data._
