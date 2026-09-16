# Episode 67 — Design Patterns Intro

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty-Six wrapped JVM interview answers — heap, GC, JIT, and measurement. Architecture interviews shift next — from how the JVM runs code to how you structure code. Design patterns are reusable solutions to recurring software design problems.

They are not libraries — they are named ideas teams use to communicate intent. Junior engineers memorize names — seniors know when a pattern helps and when it hurts. Today — what patterns are, the three GoF categories, and how Java already uses them.

Episode Sixty-Seven. Design Patterns Intro. A design pattern names a proven structure for a common problem. The Gang of Four book cataloged twenty-three classic object-oriented patterns.

Each pattern has a problem, a structure, consequences, and known uses. Patterns create a shared vocabulary — say Adapter and teammates know the shape. They are tools for clarity — not badges to sprinkle on every class.

Prefer the simplest design that communicates intent — patterns when complexity earns them. Patterns group into three categories by intent. Creational — control how objects are created — Singleton, Factory, Builder.

Structural — compose classes and objects — Adapter, Decorator, Facade, Proxy. Behavioral — organize communication and algorithms — Strategy, Observer, Command. Episodes Sixty-Eight through Seventy walk each category with Java examples.

Category first — then pick the pattern that matches the force you are balancing. Java's standard library is full of patterns you already use. Iterator — for-each loops walk collections without exposing structure.

Observer — listeners and reactive streams notify interested parties. Decorator — java.io streams wrap streams — BufferedInputStream over FileInputStream. Factory — Calendar.getInstance and Paths.get hide concrete construction.

Recognizing patterns in the JDK trains your eye for application design. Use a pattern when the problem matches — not when you want a fancy name. Duplicated construction logic — consider Factory or Builder.

Need to swap algorithms at runtime — Strategy fits cleanly. Legacy API mismatch — Adapter bridges without rewriting callers. If a pattern adds classes without reducing coupling — skip it.

Readability for your team beats purity from a textbook. Pattern abuse is a real failure mode. Singleton everywhere — hidden global state that breaks tests. Abstract factory for two concrete types — ceremony without payoff.

Observer graphs so tangled that change ripples unpredictably. Also — renaming a simple method call a Strategy without a family of algorithms. Patterns serve design — design does not serve pattern checklists.

Three common mistakes. One — memorizing twenty-three names without a problem they solve. Two — forcing patterns into code that is already clear. Three — confusing design patterns with architectural styles like microservices.

Also — skipping trade-offs — every pattern adds indirection cost. Name the force, then the pattern — never the reverse. Interview question — what is a design pattern and why use one?

A named, reusable solution to a recurring design problem. It improves communication — teams share intent with one word. It packages trade-offs — you adopt known consequences deliberately.

Java's JDK uses patterns heavily — Iterator, Decorator, Factory. Use them when they reduce coupling or clarify variation — not for prestige. Next we go deep on object creation. Episode Sixty-Eight — Creational Patterns.

Singleton, Factory Method, Abstract Factory, Builder, and Prototype. See you there.
