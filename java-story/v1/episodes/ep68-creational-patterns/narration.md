# Episode 68 — Creational Patterns

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty-Seven introduced design patterns and the three GoF categories. Creational patterns answer one question — who creates objects, and how. Scattered new keywords couple callers to concrete classes and construction details.

When construction grows complex — optional fields, validation, families of products — patterns help. Java codebases lean on Factory and Builder constantly — Singleton less often than people think.

Today — Singleton, Factory Method, Abstract Factory, Builder, and Prototype. Episode Sixty-Eight. Creational Patterns. Singleton ensures one instance with a global access point. Classic use — a shared configuration or a process-wide registry.

In Java — prefer enum singleton or static holder for thread-safe lazy init. Cost — hidden global state that complicates testing and parallel evolution. Dependency injection often replaces Singleton — inject one instance instead of reaching for it.

Reach for Singleton only when truly one is required — not as a default. Factory Method lets subclasses decide which concrete type to create. Callers depend on an interface — not on new ConcreteThing parentheses.

Abstract Factory builds families of related products that must stay consistent. Example — UI kits with matching buttons and dialogs per look and feel. JDK examples — Collection iterators, Charset encoders, JDBC DriverManager.

Factories shine when creation rules change more often than usage sites. Builder constructs complex objects step by step with a fluent API. Telescoping constructors — many overloads — become unreadable fast.

Builder sets fields, validates, then builds an immutable result. Java records and Lombok builders are modern flavors of the same idea. StringBuilder is a specialized builder for character sequences.

Use Builder when objects have many optional parameters or invariant checks. Prototype creates new objects by copying a prototypical instance. Useful when construction is expensive or configuration is mostly shared.

Java's Cloneable is awkward — prefer copy constructors or copy factories. Deep versus shallow copy matters — shared mutable state surprises teams. Deserialization and object pools sometimes play a similar role.

Prototype is rarer in Java apps — know it, use it when cloning beats rebuilding. How to choose among creational patterns. One shared instance — Singleton or better, a DI-managed bean.

Vary the type created — Factory Method or a simple static factory. Many optional fields — Builder with validation at build time. Families of products — Abstract Factory keeps combinations consistent.

Start with a static factory method — escalate only when forces demand it. Three common mistakes. One — Singleton as a service locator for everything — testing nightmare. Two — Abstract Factory for a single product type — unnecessary hierarchy.

Three — mutable builders reused across threads without care. Also — Cloneable without documenting deep versus shallow semantics. Creation should clarify ownership — not hide it. Interview question — Factory versus Builder — when each?

Factory chooses which type to instantiate — hides concrete classes. Builder assembles one complex object — many optional fields, clear validation. Factory returns quickly — Builder chains setters then builds.

They combine — a factory may return a preconfigured builder. Pick the one that matches the force — type variation versus construction complexity. Creation is settled — next is composition.

Episode Sixty-Nine — Structural Patterns. Adapter, Decorator, Facade, Proxy, and Composite. See you there.
