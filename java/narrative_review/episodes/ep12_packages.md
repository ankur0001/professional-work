# Episode 12 — Packages

| Field | Value |
|---|---|
| Episode | 12 |
| Title | Packages |
| Catalog handbook column | 12 |
| Narration source script | `make_episode_12.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Access needs a neighborhood. Packages are those neighborhoods.
2. A package is a namespace — and a boundary.
3. It prevents name collisions and shapes who collaborates.
4. On disk and at runtime, package plus class name is identity.
5. Treat package structure as architecture you can see.
6. Folders tell the truth about ownership — or they should.

### Scene `title` (renderer: `title`)

1. Episode Twelve.
2. Packages — namespaces, boundaries, and ownership.

### Scene `namespace` (renderer: `namespace`)

1. package com.acme.orders.domain;
2. That line is not decoration — it is part of the binary name.
3. com.acme.OrderService is not the same as com.other.OrderService.
4. Folders should match the package declaration. Java expects that.
5. Break the mapping and tools get angry fast.
6. Folder path and package declaration must agree.

### Scene `boundary` (renderer: `boundary`)

1. Packages define package-private visibility.
2. Types in the same package can collaborate quietly.
3. Types outside must use the public API — if you designed one.
4. Good packages make invalid dependencies hard to introduce.
5. Bad packages — one giant folder — erase ownership.
6. Boundaries only work if the tree reflects them.

### Scene `structure` (renderer: `structure`)

1. Organize by capability when you can.
2. api. application. domain. infrastructure.
3. Or by feature — orders, payments, shipping — when teams own features.
4. Layered-only packages can become anemic and tangled.
5. Pick a structure that mirrors how people own the code.
6. Feature teams and domain packages often fit better than pure layers.

### Scene `spring` (renderer: `spring`)

1. Spring Boot tip — scanning starts from the main class package downward.
2. Put OrdersApplication at a sensible root.
3. Bury it too deep and beans disappear mysteriously.
4. Packages are not only organization — frameworks navigate them.
5. Design the root on purpose.
6. A wrong root creates mysterious missing beans.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — every class in one package called util or common.
3. Two — cyclic dependencies between packages — architecture spaghetti.
4. Three — main class buried so component scanning misses half the app.
5. Also — package names that lie about contents.
6. Honest names reduce wrong imports and wrong ownership.

### Scene `interview` (renderer: `interview`)

1. Interview question — why do packages matter?
2. Namespace uniqueness. Access boundaries. Ownership. Framework scanning.
3. Runtime identity is package plus class name — plus classloader later.
4. Good structure makes illegal dependencies awkward.
5. That is architecture you can feel in the folder tree.

### Scene `teaser` (renderer: `teaser`)

1. Boundaries are set. Next — fixed sets of constants with behavior.
2. Episode Thirteen — enums.
3. Type-safe states instead of magic strings.
4. See you there.

_Total beats: **47** across **9** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **12** — *Packages*.
- **Series catalog:** Episode 12 ↔ handbook lesson 12 — *Packages*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 12 excerpt)

- Concept: Packages group related Java types under a namespace. They organize code, prevent class-name collisions, define package-private visibility boundaries, and map source structure to runtime class identity. com.acme.orders |-- api |-- domain |-- persistenc

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 12).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Access needs a neighborhood. Packages are those neighborhoods._
- **`title`** — starts from: _Episode Twelve._
- **`namespace`** — starts from: _package com.acme.orders.domain;_
- **`boundary`** — starts from: _Packages define package-private visibility._
- **`structure`** — starts from: _Organize by capability when you can._
- **`spring`** — starts from: _Spring Boot tip — scanning starts from the main class package downward._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why do packages matter?_
- **`teaser`** — starts from: _Boundaries are set. Next — fixed sets of constants with behavior._
