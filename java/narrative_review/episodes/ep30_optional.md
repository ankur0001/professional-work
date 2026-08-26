# Episode 30 — Optional

| Field | Value |
|---|---|
| Episode | 30 |
| Title | Optional |
| Catalog handbook column | 30 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Parallel streams closed a chapter on how we process many values. One value still causes outsized pain: the value that might not be there.

A `findUser` method returns `null` when the id is unknown. Callers forget to check. Somewhere deeper, `user.name()` throws `NullPointerException`. The stack trace points at a symptom, not at the API that lied by using null as a silent status code. The natural question is: can absence be part of the return type?

Optional makes absence explicit at API boundaries — not everywhere. Prefer it as a return type when "maybe none" is a normal outcome.

```java
Optional<User> u = find();
String name = u.map(User::name).orElse("unknown");
```

Walk it. `find()` returns `Optional<User>` — either a user or empty. `map(User::name)` transforms the inner value if present, otherwise stays empty. `orElse("unknown")` unwraps to a concrete string, supplying a default when absent. Callers cannot call `.name()` on a raw null they forgot to imagine; they must confront the optional.

`map`, `flatMap`, and `filter` are the vocabulary for transforming absence safely.

```java
Optional<String> city = findUser(id)
    .filter(User::active)
    .flatMap(User::address)
    .map(Address::city);
```

`filter` drops inactive users to empty. `flatMap` chains another optional-returning step without nesting. `map` extracts a city when the address exists. The chain reads like the business rules.

`orElse` versus `orElseGet` matters when the default is expensive:

```java
user.orElse(loadDefaultFromDisk());      // always loads, even when user present
user.orElseGet(() -> loadDefaultFromDisk()); // loads only when empty
```

`orElse` evaluates its argument immediately. `orElseGet` accepts a supplier and runs it only on absence. Use `orElse` for cheap constants. Use `orElseGet` for work you do not want to waste.

Avoid `Optional.of(null)`. It throws immediately. If the value might be null, use `Optional.ofNullable`. If you already know it is non-null, `Optional.of` documents that belief — and fails fast if you were wrong.

```java
Optional.of(null);            // NullPointerException
Optional.ofNullable(maybe);   // empty when maybe is null
```

Do not use Optional fields everywhere. Optional is a poor fit for fields, parameters, and collections of optionals as a general style. It shines on return types where the caller must decide what absence means. Inside a class, a nullable private field with clear invariants — or a separate empty object — is often simpler. Wrapping every field in Optional adds noise without adding boundary safety.

What if we skip Optional and keep returning null?

```java
User find(String id) {
    return map.get(id);   // null if missing
}
```

Every caller reinvents the check. One misses. Production pays. Optional does not remove null from Java; it moves the "might be missing" declaration to a place the type system can see.

A clean repository boundary looks like this:

```java
public Optional<User> findById(String id) {
    return Optional.ofNullable(store.get(id));
}

public User requireById(String id) {
    return findById(id)
        .orElseThrow(() -> new NotFoundException(id));
}
```

`findById` admits absence. `requireById` turns absence into an exception for paths that truly need a user. Both are honest. Neither pretends a missing user is a null reference waiting to explode later.


Optional in streams appears often as a bridge:

```java
List<String> names = ids.stream()
    .map(this::findUser)
    .flatMap(Optional::stream)
    .map(User::name)
    .toList();
```

Each id may or may not resolve. `Optional::stream` flattens presence into the stream and drops absence. That composition is why Optional and streams feel related without Optional being a general-purpose collection.

Resist `optional.get()` without a guard. Prefer `orElseThrow`, `ifPresent`, or explicit branching. `get` is the old null-shaped escape hatch and recreates the same blind trust Optional was meant to remove.

At team level, agree where Optional is required: public find methods yes; private helpers maybe; fields and parameters rarely. Consistency matters more than maximal Optional usage.


Serialization and Optional fields are another reason to keep Optional off fields: many tools handle nulls, fewer handle Optional wrappers consistently across versions. Return Optional from finders; store nullable references privately if you must store absence.

`orElseThrow` without a supplier message is fine when the exception type is enough; with a supplier you can include the missing id. Prefer precise failures over empty-looking defaults that mask bugs in paths that should never be empty.



If a library forces null returns, adapt at the boundary: wrap with `ofNullable` once, then speak Optional inward. Do not let nulls leak through layer after layer and then sprinkle Optional randomly in the middle. Boundaries convert; interiors stay consistent.

So let's reconnect the chain. Null returns hid absence. Optional made it explicit at boundaries. `map`/`flatMap`/`filter` transformed carefully. `orElse` versus `orElseGet` controlled default cost. `of` versus `ofNullable` avoided traps. Fields everywhere were rejected as style abuse.

With language features and collections under our feet, the next practical world is time itself — dates, instants, zones — where stringly-typed timestamps repeat the same class of mistake Optional tried to cure.

Optional is documentation you cannot ignore as easily as a JavaDoc line that says "may be null." Use that power at the seams. Inside a method, local null checks can still be the simplest tool. The episode's lesson is judgment about boundaries — not fear of null in every line.

Teams sometimes wrap collections in Optional — `Optional<List<User>>` — to mean "no list." Prefer an empty list for "no users" and Optional only for a missing singular thing. Empty collections already express absence of elements. Optional of a collection usually doubles the absence channels and confuses callers.

With Optional closing this arc of language and collections tools, you are ready for libraries that encode real-world domains — starting with time — using the same design instinct: make illegal or ambiguous states harder to represent silently.

That bridge leads to Episode Thirty-One — Java Time.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 30 (*Optional*).

Narration technique: null-return NPE situation → Optional as boundary answer → map/flatMap/filter → orElse vs orElseGet → of/ofNullable → not for fields → next natural problem (time API). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Prefer as return type.
- map/flatMap/filter.
- orElse vs orElseGet.
- Avoid Optional.of(null).
- Don't use Optional fields everywhere.
