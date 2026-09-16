# Episode 69 — Structural Patterns

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty-Eight covered creational patterns — how objects are born. Structural patterns cover how objects and classes compose into larger structures. APIs rarely match perfectly — you adapt, wrap, and simplify interfaces constantly.

java.io is a masterclass in Decorator — wrappers adding buffering and encoding. Facades and proxies appear in every service layer and remote call path. Today — Adapter, Decorator, Facade, Proxy, and Composite.

Episode Sixty-Nine. Structural Patterns. Adapter converts one interface into another clients expect. You have a useful class — its method names or types do not match callers. Write a thin adapter that delegates — callers stay clean and testable.

Object adapters compose — class adapters inherit — prefer composition in Java. JDK — Arrays.asList adapts an array to the List interface. Adapter is integration glue — keep it thin and obvious.

Decorator attaches responsibilities dynamically by wrapping. Same interface as the core object — transparent to callers. Stack wrappers — buffer, then encrypt, then compress — open for extension.

java.io InputStream hierarchy is the textbook Java Decorator example. Unlike inheritance trees, decoration mixes features without combinatorial subclasses. Watch the stack depth — too many wrappers obscure debugging.

Facade provides a simple interface to a complex subsystem. Subsystem classes remain available — facade is a convenience entry point. Service layers often act as facades over repositories, clients, and mappers.

SLF4J over logging backends is a facade-style boundary. Facades reduce coupling — clients depend on one door, not twenty rooms. Do not let a facade become a god object — keep it a thin orchestrator.

Proxy controls access to another object with the same interface. Virtual proxy — lazy creation — remote proxy — network boundary — protection proxy — auth. Java dynamic proxies and Spring AOP wrap beans for transactions and security.

Unlike Decorator, Proxy's purpose is access control, not adding features. Caching proxies memoize expensive calls transparently. Know why the proxy exists — latency, security, laziness, or logging.

Composite treats individual objects and compositions uniformly. Trees of nodes — files and folders, UI widgets, expression trees. Clients call the same operations on leaves and composites.

Great for recursive structures — awkward when children differ wildly in API. Watch the Liskov risks — not every operation makes sense on every node. Use Composite when hierarchy and uniform treatment are real requirements.

Three common mistakes. One — Adapter that grows business logic — keep adapters thin. Two — Decorator stacks nobody can debug — document the wrap order. Three — Facade that hides too much — teams reopen the subsystem anyway.

Also — calling every wrapper a Proxy — purpose differs from Decorator. Structure should clarify boundaries — not invent new ones for sport. Interview question — Decorator versus Proxy — how do they differ?

Both wrap an object and usually share its interface. Decorator adds or alters behavior — buffering, logging, compression. Proxy controls access — lazy init, remote call, authorization, caching.

In Spring, AOP proxies often implement cross-cutting access concerns. Name the intent first — feature stacking versus access control. Structure connects objects — behavior connects collaborations.

Episode Seventy — Behavioral Patterns. Strategy, Observer, Command, Template Method, and Iterator. See you there.
