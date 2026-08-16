# Episode 20 — Modules and JPMS

| Field | Value |
|---|---|
| Episode | 20 |
| Title | Modules and JPMS |
| Catalog handbook column | 20 |
| Narration source script | `make_episode_20.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Sealed types close hierarchies. Modules close the classpath.
2. For years, every public type was fair game if the JAR was on the path.
3. JPMS — the Java Platform Module System — adds explicit boundaries.
4. What you require. What you export. What stays internal.
5. Today — module-info, strong encapsulation, and when modules earn their keep.
6. Packages organize names. Modules organize trust.

### Scene `title` (renderer: `title`)

1. Episode Twenty.
2. Modules and JPMS — strong encapsulation.

### Scene `why` (renderer: `why`)

1. Why modules exist.
2. The classpath is flat — order and accidents decide visibility.
3. Split packages, accidental API leakage, brittle shading wars.
4. Modules declare dependencies and exported packages up front.
5. The JVM can refuse illegal access instead of hoping conventions hold.
6. Reliability beats classpath folklore.

### Scene `info` (renderer: `info`)

1. module-info.java is the contract.
2. module com.shop.payments.
3. requires java.sql. requires com.shop.common.
4. exports com.shop.payments.api.
5. Internal packages stay hidden even if types are public.
6. Public no longer means globally reachable.

### Scene `directives` (renderer: `directives`)

1. Know the key directives.
2. requires — and requires transitive when consumers need your dependency too.
3. exports — and exports to specific modules when the API is narrow.
4. opens — for reflection frameworks that need deep access at runtime.
5. provides and uses — for service loading with clear providers.
6. Each keyword is a deliberate encapsulation choice.

### Scene `unnamed` (renderer: `unnamed`)

1. Reality check — the unnamed module.
2. Classic classpath JARs still run. They become the unnamed module.
3. They can read everything, but modular code cannot require them by name.
4. Migration is often incremental — modularize libraries you own first.
5. Automatic modules bridge JARs with a derived module name.
6. Plan the boundary. Do not flip a monolith overnight.

### Scene `when` (renderer: `when`)

1. When modules help.
2. Platform libraries. Large multi-JAR systems. Clear API versus internal split.
3. When you need reliable encapsulation and smaller runtime images with jlink.
4. When not — tiny apps where classpath simplicity wins and tooling friction hurts.
5. Spring Boot apps often stay on the classpath path unless you have a reason.
6. Use JPMS when boundaries are a product feature — not a fashion statement.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — exporting everything — encapsulation theater with no teeth.
3. Two — opens for convenience forever instead of narrowing reflective needs.
4. Three — split packages across modules — the JVM will not forgive that.
5. Also — ignoring transitive requires until consumers break at compile time.
6. Module graphs should be boring and intentional.

### Scene `interview` (renderer: `interview`)

1. Interview question — what does JPMS add over packages and JARs?
2. Explicit module dependencies and exported packages.
3. Strong encapsulation — public is not enough to be accessible.
4. Mention module-info, requires, exports, and the unnamed module.
5. Bonus — jlink for custom runtimes.
6. That answer separates classpath history from modular design.

### Scene `teaser` (renderer: `teaser`)

1. Language features are in place. Next — the collections you use every day.
2. Episode Twenty-One — Lists, and the java.util foundation.
3. Interfaces, implementations, and choosing the right structure.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **20** — *Modules and JPMS*.
- **Series catalog:** Episode 20 ↔ handbook lesson 20 — *Modules and JPMS*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Sealed types close hierarchies. Modules close the classpath._
- **`title`** — starts from: _Episode Twenty._
- **`why`** — starts from: _Why modules exist._
- **`info`** — starts from: _module-info.java is the contract._
- **`directives`** — starts from: _Know the key directives._
- **`unnamed`** — starts from: _Reality check — the unnamed module._
- **`when`** — starts from: _When modules help._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what does JPMS add over packages and JARs?_
- **`teaser`** — starts from: _Language features are in place. Next — the collections you use every day._
