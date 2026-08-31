# Episode 30 — Optional

| Field | Value |
|---|---|
| Episode | 30 |
| Title | Optional |
| Catalog handbook column | 30 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Pipelines can run in parallel, but they still end in moments that may produce no value — an empty find, a missing key, a failed parse. Returning `null` from those moments recreates silent absence. Callers forget to check. Somewhere deeper, `user.name()` throws `NullPointerException`. The stack trace points at a symptom, not at the API that lied by using null as a silent status code. The natural question is: can absence be part of the return type?

Optional makes absence explicit at API boundaries — not everywhere. Prefer it as a return type when "maybe none" is a normal outcome.

```java
Optional<User> u = find();
String name = u.map(User::name).orElse("unknown");
```

Walk it. `find()` returns `Optional<User>` — either a user or empty. `map(User::name)` transforms the inner value if present, otherwise stays empty. `orElse("unknown")` unwraps to a concrete string, supplying a default when absent. Callers must confront the optional.

`map`, `flatMap`, and `filter` are the vocabulary for transforming absence safely.

```java
Optional<String> city = findUser(id)
    .filter(User::active)
    .flatMap(User::address)
    .map(Address::city);
```

`filter` drops inactive users to empty. `flatMap` chains another optional-returning step without nesting. `map` extracts a city when the address exists.

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

Do not use Optional fields everywhere. Optional is a poor fit for fields, parameters, and collections of optionals as a general style. It shines on return types where the caller must decide what absence means. Inside a class, a nullable private field with clear invariants is often simpler.

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

`findById` admits absence. `requireById` turns absence into an exception for paths that truly need a user. Both are honest.

Optional in streams appears often as a bridge:

```java
List<String> names = ids.stream()
    .map(this::findUser)
    .flatMap(Optional::stream)
    .map(User::name)
    .toList();
```

Each id may or may not resolve. `Optional::stream` flattens presence into the stream and drops absence. Resist `optional.get()` without a guard — prefer `orElseThrow`, `ifPresent`, or explicit branching.

Teams sometimes wrap collections in Optional — `Optional<List<User>>` — to mean "no list." Prefer an empty list for "no users" and Optional only for a missing singular thing. Empty collections already express absence of elements.

Null returns hid absence. Optional made it explicit at boundaries. `map`/`flatMap`/`filter` transformed carefully. `orElse` versus `orElseGet` controlled default cost. Fields everywhere were rejected as style abuse.

Absence is not only about missing objects. Business rules live on calendars: "expire this offer at midnight Tokyo," "schedule a job in three hours," "compare two instants from different zones." Stringly-typed timestamps recreate the same silent-mistake pattern — until parsing and zone rules fail at the worst time. How does Java talk about time without that fog?

That pressure is what `java.time` exists to answer.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 30 (*Optional*).

Narration technique: null-return NPE situation → Optional as boundary answer → map/flatMap/filter → orElse vs orElseGet → of/ofNullable → not for fields → next natural problem (time API). Continuity-checked transitions.
