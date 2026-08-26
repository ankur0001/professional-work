# Episode 20 — Modules and JPMS

| Field | Value |
|---|---|
| Episode | 20 |
| Title | Modules and JPMS |
| Catalog handbook column | 20 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Sealed types closed hierarchies inside the language. Platforms still faced a different leak: on the classic classpath, every public type in every jar was fair game. Internal packages were only a naming convention. Reflection and deep dependency graphs made "please don't touch that" unenforceable.

So teams asked a practical question: can we declare, up front, what a library requires and what it actually exports?

That is the Java Platform Module System — JPMS. A module is a named collection of packages with an explicit boundary. The declaration lives in `module-info.java`.

```java
module com.shop.app {
    requires com.shop.core;
    exports com.shop.app.api;
}
```

Walk the meaning. `module com.shop.app` names this module. `requires com.shop.core` states an explicit dependency — the module graph is not a pile of jars hoping their transitive types appear. `exports com.shop.app.api` makes only that package usable to other modules. Sibling packages in the same module can stay hidden even if their types are public. That is stronger encapsulation than packages alone. Public no longer means "visible to the whole classpath world."

`opens` appears when reflective frameworks need deep access to otherwise hidden packages. Opening is a deliberate door, not the default. Opening everything "just to make it work" recreates classpath porosity with module syntax. Prefer exporting a stable API and opening only what a known tool requires.

Migration can be incremental. Many applications still run on the classpath. Classpath apps still exist — know both worlds. You can modularize the JDK usage, modularize libraries gradually, or stay on the classpath while learning the module graph of the platform itself. JPMS is not an all-or-nothing cliff for every codebase on day one. It is a tool for reliable configuration and clearer boundaries when you need them.

What problem do modules solve in one sentence? Reliable configuration and stronger encapsulation than a flat classpath. Missing `requires` fail early. Illegal access to non-exported packages fail clearly. Circular module dependencies become design smells you can see in the graph instead of surprise ClassNotFound puzzles at runtime.

Modules alone do not equal good architecture. You can still invent tangled exports and leaky APIs inside a modular build. The module system enforces boundaries you declare; it does not invent a clean domain for you. Treat `module-info` as architecture visible to the compiler and runtime — write it with the same care you give package structure.

So let's reconnect the chain. The classpath erased strong encapsulation. Modules restored explicit `requires`, `exports`, and careful `opens`. Encapsulation grew sharper than public packages alone. Incremental migration kept classpath apps in the real world. Architecture discipline remained our job.

With the language and platform boundaries clearer, everyday programs still need to hold sequences of values — shopping carts, timelines, search results. Arrays were fixed-size. The next natural tool is a resizable, ordered collection you will use constantly.

That is Episode Twenty-One — Lists.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 20 (*Modules and JPMS*).

Narration technique: classpath encapsulation leak → module-info as answer → requires/exports/opens walkthrough → incremental migration → architecture caution → next natural problem (ordered collections / lists). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- module-info requires/exports/opens.
- Explicit dependencies.
- Stronger encapsulation than packages alone.
- Migration can be incremental.
- Classpath apps still exist — know both worlds.
