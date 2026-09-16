# Episode 10 — Object-Oriented Programming

**Cut:** v1 (original)

## Transcript (from captions)

Strings and arrays hold data. Objects model the world. Object-oriented programming — state, behavior, and identity working together. In Java, OOP is how we manage domain complexity — not just a syntax style.

Classes define blueprints. Objects are living instances. Get this mental model right — everything else in OOP builds on it. Episode Ten. Object-Oriented Programming — classes, objects, and encapsulation.

A class is the blueprint. Fields hold state. Methods hold behavior. new Order creates an object — its own identity on the heap. Two Order objects can share the same class and still be different instances.

Identity matters. Equals can compare values — but identity is the object itself. Encapsulation hides internals behind a clear API. private fields. public methods that protect invariants.

Callers should not poke amountInCents directly if rules apply. Hide data. Expose intention — like isHighValue or applyDiscount. That is how objects stay consistent as the system grows.

Encapsulation is not ceremony — it is protection. Four ideas you will hear forever. Encapsulation — hide details. Abstraction — show only what matters. Inheritance — share and specialize — carefully.

Polymorphism — one contract, many implementations. Prefer composition when inheritance trees get deep and fragile. Composition says has-a. An Order has Money. A Customer has an Address.

Small objects collaborating beat one god class that knows everything. Anemic models — data bags with all logic in services — often lose domain clarity. Put behavior next to the data it protects.

That is domain modeling that survives real change. Three common mistakes. One — god services that do every use-case in one class. Two — deep inheritance trees nobody can reason about.

Three — public mutable fields that break encapsulation overnight. Also — leaking persistence entities straight through APIs. Interview question — class versus object? Class — blueprint. Object — instance with identity and state.

Then encapsulation — hide fields, expose safe behavior. Prefer composition over deep inheritance when design gets complex. That answer sounds like an engineer, not a memorizer. Objects need boundaries. Next — who can see what.

Episode Eleven — access modifiers. private, public, protected, package-private — ownership in code. See you there.
