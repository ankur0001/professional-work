# Episode 07 — Methods

**Cut:** v1 (original)

## Transcript (from captions)

Control flow chooses the path. Methods package the work. A method is named behavior — inputs, outputs, and a contract. Good method design makes APIs clear and code reusable. Bad method design hides bugs inside long, unclear routines.

Today we learn to write methods that say what they mean. Episode Seven. Methods — parameters, returns, and clean contracts. Look at the anatomy of a method. Access modifier. Return type. Name. Parameter list.

Then the body — the work. Name should say what it does. Parameters say what it needs. Return type says what you get back — or void if it only acts. Read a signature like a sentence — that is the API contract.

The signature is the contract. Same name, different parameter types — that is overloading. Overloading is compile-time. The compiler picks the match. Do not confuse it with overriding — that is runtime polymorphism for subclasses.

Keep overloads obvious. If callers guess wrong, rename. Clarity beats cleverness when two methods share a name. Design tips that scale. One job per method. Short enough to scan. Avoid boolean flag parameters that fork behavior — split into two methods.

Prefer returning a clear type over returning null without a contract. Domain methods beat scattered operator soup. order can be cancelled is better than five comparisons copied everywhere.

Instance methods need an object. Static methods do not. Static helpers are fine for pure utilities. But static mutable state is a trap — global lifetime, hard tests. In Spring, calling this dot method may skip proxies. Know when that matters.

Prefer instance behavior for domain rules — static for math and parsing. Three common mistakes. One — methods that do five jobs and fill a screen. Two — unclear names like process data or handle stuff.

Three — swallowing exceptions inside a helper so callers never learn the failure. Also — making every tiny helper public. Hide what is not an API. Interview question — overload versus override?

Overload — same name, different parameters, chosen at compile time. Override — subclass replaces a parent method, chosen at runtime. Then add — methods should express domain intent, not just steps.

That answer shows you design APIs, not just syntax. Behavior is packaged. Next we hold many values. Episode Eight — arrays. Fixed size, indexed access, and the off-by-one traps. See you there.
