# Episode 18 — Records

**Cut:** v1 (original)

## Transcript (from captions)

Reflection can dig into types. Records make simple data types honest. So much Java was getters, setters, equals, hashCode, toString — for a bag of fields. Records say — this is a transparent data carrier.

Less boilerplate. Clearer intent. Today we use records where they shine — and avoid where they do not. Data with a contract — not a ceremony factory. Episode Eighteen. Records — compact, immutable data carriers.

A record declaration is short on purpose. record Money of currency and minorUnits. The compiler generates the canonical constructor. Also accessors, equals, hashCode, and toString. Components are final — immutability is the default story.

You describe the data. Java handles the noise. Accessors are named after components — currency, minorUnits. Not getCurrency — unless you add that yourself. That style is intentional — records are not classic JavaBeans.

Serialization libraries increasingly understand both styles. Read the accessor names as part of the API. Keep component names domain-clear. Records can still validate. Use a compact constructor to enforce invariants.

Reject null currency. Reject negative minor units. You get immutability and guardrails together. That is why records work well for value objects. Invalid data should fail at creation — not later.

When to choose a record. DTOs. Event payloads. Value objects. Map keys with care. When identity is the data — not a mutable lifecycle entity. When not — JPA entities with mutable state and proxies often want classes.

Do not force records into every hierarchy. Use them where transparency is the point. Know the limits. Records are implicitly final — no subclassing the record itself. You can implement interfaces.

You can add methods — but do not turn a record into a service. If behavior grows complex, extract a real domain type with intent. Records carry data. Services orchestrate. Keep the roles clean.

Three common mistakes. One — mutable components like lists without defensive copies. Two — using records as entities while expecting mutable ORM magic. Three — huge records that should have been structured types.

Also — ignoring compact-constructor validation. Immutability is only as strong as the components you expose. Interview question — what is a Java record? A transparent, immutable data carrier with generated boilerplate.

Canonical constructor, accessors, equals, hashCode, toString. Great for DTOs and value objects — not a replacement for all classes. Mention compact constructors for invariants. That answer is crisp and practical.

Data carriers are clean. Next — restricting hierarchies. Episode Nineteen — sealed classes. Controlled subclasses and exhaustive switches. See you there.
