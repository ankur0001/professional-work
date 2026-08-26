# Episode 20 — Modules and JPMS

| Field | Value |
|---|---|
| Episode | 20 |
| Title | Modules and JPMS |
| Catalog handbook column | 20 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Sealed types closed hierarchies inside the language. Platforms still faced a different leak: on the classic classpath, every public type in every jar was fair game. Internal packages were only a naming convention. Reflection and deep dependency graphs made "please don't touch that" unenforceable. Accidental coupling across jars was normal.

So teams asked a practical question: can we declare, up front, what a library requires and what it actually exports?

Packages gave us neighborhoods. Modules give those neighborhoods a customs checkpoint: you may be public inside your module and still invisible outside it unless exported. That single rule repairs years of "but it compiled on my classpath" accidents.

That is the Java Platform Module System — JPMS. Modules restore strong encapsulation the classpath erased. The feature landed with Java 9 and reshaped how the JDK itself is packaged — which is why even classpath applications feel module-related error messages when they touch JDK internals. A module is a named collection of packages with an explicit boundary. The declaration lives in `module-info.java`.

```java
module com.shop.app {
    requires com.shop.core;
    exports com.shop.app.api;
}
```

Walk the meaning. `module com.shop.app` names this module. `requires com.shop.core` states an explicit dependency — the module graph is not a pile of jars hoping their transitive types appear. `exports com.shop.app.api` makes only that package usable to other modules. Sibling packages in the same module can stay hidden even if their types are `public`. Public no longer means "visible to the whole classpath world."

`opens` appears when reflective frameworks need deep access to otherwise hidden packages. Opening is a deliberate door, not the default.

```java
module com.shop.app {
    requires com.shop.core;
    exports com.shop.app.api;
    opens com.shop.app.internal to spring.core;
}
```

Opening everything "just to make it work" recreates classpath porosity with module syntax. Prefer exporting a stable API and opening only what a known tool requires, ideally `to` a named module.

Migration can be incremental. Many applications still run on the classpath. You can modularize libraries gradually, or stay on the classpath while learning the module graph of the platform itself. JPMS is not an all-or-nothing cliff for every codebase on day one.

What problem do modules solve in one sentence? Reliable configuration and stronger encapsulation than a flat classpath. Missing `requires` fail early. Illegal access to non-exported packages fails clearly instead of succeeding by accident.

Modules alone do not equal good architecture. You can still invent tangled exports and leaky APIs inside a modular build. The module system enforces boundaries you declare; it does not invent a clean domain for you.

Picture two jars on an old classpath: `shop-core` and `shop-app`. A public class named `InternalHasher` lived in `com.shop.core.internal`. Nothing stopped `shop-app` from calling it. A year later the core team renamed the hasher and half the apps broke. Packages said "internal" in the name; the platform did not enforce it.

With modules, `com.shop.core` simply does not export `com.shop.core.internal`. The app must use the exported API. That failure happens at launch or compile time for modular apps, not as a surprise `NoSuchMethodError` after a refactor.

If you are maintaining a library, exporting fewer packages is usually kinder than exporting everything "for flexibility." Flexibility for callers becomes fragility for you. Start narrow. Export more only when a real client need appears. The same advice applies to `opens`: grant reflective access specifically, never as a blanket default.

The classpath erased strong encapsulation. Modules restored explicit `requires`, `exports`, and careful `opens`. Incremental migration kept classpath apps in the real world.

With the language and platform boundaries clearer, everyday programs still need to hold sequences of values — shopping carts, timelines, search results. Arrays were fixed-size. The next natural tool is a resizable, ordered collection you will use constantly.

That tool is a list.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 20 (*Modules and JPMS*).

Narration technique: classpath encapsulation leak → module-info as answer → requires/exports/opens walkthrough → incremental migration → architecture caution → next natural problem (ordered collections / lists). Continuity-checked transitions.
