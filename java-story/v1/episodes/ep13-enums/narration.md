# Episode 13 — Enums

**Cut:** v1 (original)

## Transcript (from captions)

Packages organize types. Enums organize fixed choices. PENDING. PAID. CANCELLED — states that should never be free-form strings. An enum is a type-safe set of named constants — with room for behavior.

Today we replace magic strings with real domain states. Treat enum structure as architecture you can see in the type system. Episode Thirteen. Enums — type-safe states instead of magic strings.

Declare an enum like a special class. enum OrderStatus — PENDING, PAID, SHIPPED, CANCELLED. Each constant is a singleton instance of that enum type. Compare with equals-equals safely — identity is stable.

Switch expressions love enums — finite cases, clear exhaustiveness. Folder path and package declaration must agree — same for enum files. Enums can carry fields and methods. Attach a display label. Attach a canTransition rule.

That keeps status logic next to the status itself. Better than scattering string compares across services. Feature teams and domain packages often fit better than pure layers — enums fit domains too.

Put behavior where the state lives. Why not String status equals PAID? Typos compile. Invalid states sneak in. Refactors miss call sites. Enums make illegal states harder to represent.

Serialization still needs care — name versus ordinal. Prefer name for APIs. Ordinal is a storage trap. Honest names reduce wrong imports and wrong ownership — same for status names.

Need a set of flags? EnumSet is built for enums. Fast. Compact. Type-safe. Permission READ, WRITE, ADMIN — store combinations cleanly. Better than bit masks scattered as magic ints — unless you truly need bits.

Choose the structure that matches how the set changes. Three common mistakes. One — Stringly typed statuses that drift across services. Two — depending on ordinal in databases or APIs.

Three — stuffing volatile business config into enum constants. Also — giant enums that should have been a data table. Enums model fixed vocabularies — not every changing catalog. Interview question — why prefer enums over string constants?

Type safety. Exhaustive switches. Refactor-friendly names. Constants are real objects — can hold behavior. Avoid ordinal for persistence. Prefer name or explicit codes. That answer shows production sense.

Fixed states are clear. Next — when primitives become objects. Episode Fourteen — wrappers and autoboxing. Integer, nullability, and hidden allocations. See you there.
