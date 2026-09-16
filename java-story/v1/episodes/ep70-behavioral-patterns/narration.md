# Episode 70 — Behavioral Patterns

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty-Nine covered structural patterns — adapting, wrapping, and composing. Behavioral patterns focus on algorithms and communication between objects. They let you vary what happens without rewriting call sites every time.

Strategy swaps algorithms — Observer broadcasts events — Command queues actions. These patterns dominate service code and interview whiteboards alike. Today — Strategy, Observer, Command, Template Method, and Iterator — then Spring next.

Episode Seventy. Behavioral Patterns. Strategy defines a family of algorithms and makes them interchangeable. Clients depend on a strategy interface — concrete strategies plug in. Comparator in Java is Strategy — sort order injected at call time.

Payment processors, pricing rules, and retry policies are classic Strategies. Prefer Strategy over deep if-else chains that grow every quarter. Keep strategies focused — one decision axis per strategy type.

Observer notifies dependents automatically when a subject changes. Publish-subscribe and event listeners are Observer in modern clothes. Swing listeners, reactive streams, and message topics follow the shape.

Decouples producers from consumers — but watch notification storms. Unregister carefully — leaked listeners are memory leak classics. Use Observer when many parties care about the same state change.

Command encapsulates a request as an object. You can queue, log, undo, and retry actions uniformly. Runnable and Callable are lightweight command shapes in Java. GUI actions, job queues, and transactional outboxes use Command ideas.

Macro commands compose smaller commands into workflows. Command separates invoker from receiver — great for undo stacks. Template Method defines an algorithm skeleton in a base class.

Subclasses override steps without changing the overall sequence. JdbcTemplate and many framework hooks follow Template Method spirit. Iterator provides sequential access without exposing collection structure.

Enhanced for-loops and Stream pipelines rest on Iterator ideas. Together they show behavior reuse — hooks and traversal, not inheritance for data. Choosing behavioral patterns in practice.

Vary an algorithm — Strategy or a simple function parameter. Broadcast state changes — Observer or an event bus with clear ownership. Queue or undo work — Command objects with explicit lifecycle.

Framework-defined steps — Template Method or modern composition hooks. Prefer small interfaces — behavioral patterns should shrink switch statements. Three common mistakes. One — Strategy explosion — dozens of one-line classes for dead branches.

Two — Observer spaghetti — unclear who listens and who owns cleanup. Three — Command without idempotency — retries double-charge users. Also — Template Method locking teams into brittle inheritance.

Behavior patterns need ownership rules — not just class diagrams. Interview question — how do Strategy and Template Method differ? Strategy composes algorithms via interfaces — swap at runtime.

Template Method inherits a skeleton — subclasses fill in steps. Strategy favors composition — Template Method favors inheritance. Modern Java often prefers Strategy plus lambdas over deep templates.

Say the force — runtime swap versus fixed sequence with customizable steps. Patterns prepared the design vocabulary — frameworks apply it at scale. Episode Seventy-One — Spring Framework Intro.

IoC, dependency injection, and why Spring beans feel like patterns in production. See you there.
