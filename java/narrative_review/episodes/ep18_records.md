# Episode 18 — Records

| Field | Value |
|---|---|
| Episode | 18 |
| Title | Records |
| Catalog handbook column | 18 |
| Narration source script | `make_episode_18.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Reflection can dig into types. Records make simple data types honest.
2. So much Java was getters, setters, equals, hashCode, toString — for a bag of fields.
3. Records say — this is a transparent data carrier.
4. Less boilerplate. Clearer intent.
5. Today we use records where they shine — and avoid where they do not.
6. Data with a contract — not a ceremony factory.

### Scene `title` (renderer: `title`)

1. Episode Eighteen.
2. Records — compact, immutable data carriers.

### Scene `declare` (renderer: `declare`)

1. A record declaration is short on purpose.
2. record Money of currency and minorUnits.
3. The compiler generates the canonical constructor.
4. Also accessors, equals, hashCode, and toString.
5. Components are final — immutability is the default story.
6. You describe the data. Java handles the noise.

### Scene `accessors` (renderer: `accessors`)

1. Accessors are named after components — currency, minorUnits.
2. Not getCurrency — unless you add that yourself.
3. That style is intentional — records are not classic JavaBeans.
4. Serialization libraries increasingly understand both styles.
5. Read the accessor names as part of the API.
6. Keep component names domain-clear.

### Scene `validation` (renderer: `validation`)

1. Records can still validate.
2. Use a compact constructor to enforce invariants.
3. Reject null currency. Reject negative minor units.
4. You get immutability and guardrails together.
5. That is why records work well for value objects.
6. Invalid data should fail at creation — not later.

### Scene `when` (renderer: `when`)

1. When to choose a record.
2. DTOs. Event payloads. Value objects. Map keys with care.
3. When identity is the data — not a mutable lifecycle entity.
4. When not — JPA entities with mutable state and proxies often want classes.
5. Do not force records into every hierarchy.
6. Use them where transparency is the point.

### Scene `limits` (renderer: `limits`)

1. Know the limits.
2. Records are implicitly final — no subclassing the record itself.
3. You can implement interfaces.
4. You can add methods — but do not turn a record into a service.
5. If behavior grows complex, extract a real domain type with intent.
6. Records carry data. Services orchestrate. Keep the roles clean.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — mutable components like lists without defensive copies.
3. Two — using records as entities while expecting mutable ORM magic.
4. Three — huge records that should have been structured types.
5. Also — ignoring compact-constructor validation.
6. Immutability is only as strong as the components you expose.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is a Java record?
2. A transparent, immutable data carrier with generated boilerplate.
3. Canonical constructor, accessors, equals, hashCode, toString.
4. Great for DTOs and value objects — not a replacement for all classes.
5. Mention compact constructors for invariants.
6. That answer is crisp and practical.

### Scene `teaser` (renderer: `teaser`)

1. Data carriers are clean. Next — restricting hierarchies.
2. Episode Nineteen — sealed classes.
3. Controlled subclasses and exhaustive switches.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **18** — *Records*.
- **Series catalog:** Episode 18 ↔ handbook lesson 18 — *Records*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Reflection can dig into types. Records make simple data types honest._
- **`title`** — starts from: _Episode Eighteen._
- **`declare`** — starts from: _A record declaration is short on purpose._
- **`accessors`** — starts from: _Accessors are named after components — currency, minorUnits._
- **`validation`** — starts from: _Records can still validate._
- **`when`** — starts from: _When to choose a record._
- **`limits`** — starts from: _Know the limits._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is a Java record?_
- **`teaser`** — starts from: _Data carriers are clean. Next — restricting hierarchies._
