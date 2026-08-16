# Episode 10 — Object-Oriented Programming

| Field | Value |
|---|---|
| Episode | 10 |
| Title | Object-Oriented Programming |
| Catalog handbook column | 10 |
| Narration source script | `make_episode_10.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Strings and arrays hold data. Objects model the world.
2. Object-oriented programming — state, behavior, and identity working together.
3. In Java, OOP is how we manage domain complexity — not just a syntax style.
4. Classes define blueprints. Objects are living instances.
5. Get this mental model right — everything else in OOP builds on it.

### Scene `title` (renderer: `title`)

1. Episode Ten.
2. Object-Oriented Programming — classes, objects, and encapsulation.

### Scene `class_obj` (renderer: `class_obj`)

1. A class is the blueprint.
2. Fields hold state. Methods hold behavior.
3. new Order creates an object — its own identity on the heap.
4. Two Order objects can share the same class and still be different instances.
5. Identity matters. Equals can compare values — but identity is the object itself.

### Scene `encaps` (renderer: `encaps`)

1. Encapsulation hides internals behind a clear API.
2. private fields. public methods that protect invariants.
3. Callers should not poke amountInCents directly if rules apply.
4. Hide data. Expose intention — like isHighValue or applyDiscount.
5. That is how objects stay consistent as the system grows.
6. Encapsulation is not ceremony — it is protection.

### Scene `pillars` (renderer: `pillars`)

1. Four ideas you will hear forever.
2. Encapsulation — hide details.
3. Abstraction — show only what matters.
4. Inheritance — share and specialize — carefully.
5. Polymorphism — one contract, many implementations.
6. Prefer composition when inheritance trees get deep and fragile.

### Scene `compose` (renderer: `compose`)

1. Composition says has-a.
2. An Order has Money. A Customer has an Address.
3. Small objects collaborating beat one god class that knows everything.
4. Anemic models — data bags with all logic in services — often lose domain clarity.
5. Put behavior next to the data it protects.
6. That is domain modeling that survives real change.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — god services that do every use-case in one class.
3. Two — deep inheritance trees nobody can reason about.
4. Three — public mutable fields that break encapsulation overnight.
5. Also — leaking persistence entities straight through APIs.

### Scene `interview` (renderer: `interview`)

1. Interview question — class versus object?
2. Class — blueprint. Object — instance with identity and state.
3. Then encapsulation — hide fields, expose safe behavior.
4. Prefer composition over deep inheritance when design gets complex.
5. That answer sounds like an engineer, not a memorizer.

### Scene `teaser` (renderer: `teaser`)

1. Objects need boundaries. Next — who can see what.
2. Episode Eleven — access modifiers.
3. private, public, protected, package-private — ownership in code.
4. See you there.

_Total beats: **44** across **9** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **10** — *Object-Oriented Programming*.
- **Series catalog:** Episode 10 ↔ handbook lesson 10 — *Object-Oriented Programming*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 10 excerpt)

- Concept: Object-oriented programming models software as collaborating objects with state, behavior, identity, and contracts. In Java, OOP includes classes, interfaces, encapsulation, inheritance, polymorphism, composition, and abstraction. For architects, OOP 
- Mistakes: Common mistakes include anemic domain models, god services, deep inheritance trees, public mutable fields, interfaces without purpose, leaking persistence entities through APIs, and confusing Java interfaces with distrib

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 10).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Strings and arrays hold data. Objects model the world._
- **`title`** — starts from: _Episode Ten._
- **`class_obj`** — starts from: _A class is the blueprint._
- **`encaps`** — starts from: _Encapsulation hides internals behind a clear API._
- **`pillars`** — starts from: _Four ideas you will hear forever._
- **`compose`** — starts from: _Composition says has-a._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — class versus object?_
- **`teaser`** — starts from: _Objects need boundaries. Next — who can see what._
