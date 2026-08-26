# Episode 69 — Structural Patterns

| Field | Value |
|---|---|
| Episode | 69 |
| Title | Structural Patterns |
| Catalog handbook column | 69 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Creational patterns asked how objects are born. Structural patterns ask how objects are assembled so you can extend behavior without melting the type hierarchy. Composition wraps behavior. That sentence is the spine of today. Inheritance is not banned — but exploding subclasses for every combination of features is how codebases become museums of `LoggedCachedSecureX`.

Suppose you have a repository. You need logging around saves. Then metrics. Then a circuit breaker. Inheritance would tempt `LoggingRepo extends JdbcRepo`, then `MetricsLoggingRepo extends LoggingRepo`, and so on. A decorator adds behavior by wrapping the same interface:

```java
class LoggingRepo implements Repo {
  private final Repo delegate;
  public void save(Entity e) { log(e); delegate.save(e); }
}
```

`LoggingRepo` is still a `Repo`. Callers need not know whether they hold the raw repository or a wrapped one. Decorator versus inheritance, asked in an interview, is exactly this: add behavior via composition without exploding subclasses. Stack decorators carefully. Decorator stacks nobody understands — five wrappers with unclear order — recreate the complexity you fled.

Adapters appear when two interfaces do not match. You have a vendor SDK with a weird method shape and an internal port your domain expects. An adapter translates without forcing your domain to speak vendor dialect. Facades simplify subsystems: one entry point that orchestrates several collaborating classes so callers are not wired to every moving part. Facades fail when they hide too much — when errors are swallowed, or when the facade becomes a god object that knows the entire company. Simplifying access is not the same as erasing necessary complexity.

Proxies control access. They stand in for a real object and intercept calls — for lazy loading, security checks, remote access, or transactional boundaries. If you have used Spring AOP, you have lived with proxies: the bean you inject may be a proxy that wraps your class to apply transactions or security. That power has sharp edges. Proxy surprises around `equals`, `final` methods, and self-invocation (`this.method()` bypassing the proxy) confuse people who thought annotations were magic. Structural honesty helps: know you are talking to a proxy, and know what it can and cannot intercept.

Walk a design conversation. "Should we facade the payment SDK?" If three services each duplicate the same five SDK calls and error translations, yes — a facade names the policy. If one call site exists, a facade may be premature. "Should we decorate the repository with caching?" Only if cache policy is clear — keys, TTL, invalidation — otherwise you are hiding a correctness problem behind a structural pattern. Patterns amplify both good and bad policy.

Composition keeps showing up as the safe default for growing behavior. Adapter for foreign shapes. Decorator for layered policies on one interface. Facade for a curated subsystem door. Proxy for controlled access and infrastructure concerns. Spring's AOP proxies are not a different universe; they are this idea with a framework engine.

Adapters deserve a concrete vendor story. The SMS provider wants `sendSms(Phone, Text)`. Your domain port says `notify(UserId, Notification)`. The adapter loads the phone number, formats the text, translates errors into domain failures, and isolates the SDK. When the vendor changes, one class moves. Without an adapter, vendor types leak into services and tests.

Facades fail in two opposite ways. Too thin: they add a pass-through method per SDK call with no policy, so callers still need deep knowledge. Too thick: they absorb every business workflow and become an untestable blob. A good facade encodes a few use cases your system actually owns — "charge customer for invoice" — not one hundred low-level dials.

Proxy self-invocation bites Spring users weekly. A method annotated transactional calls another method on `this`. The call does not pass through the proxy, so the annotation does not apply as expected. Structural understanding prevents "Spring is broken" tickets. You restructure so the call goes through the proxy bean, or you separate the components.

Decorator order matters. Authentication before rate limiting before caching is a different system than caching before authentication. Document the stack. If nobody can explain the order, the stack is already too deep.

When reviewing structural changes, ask: does this wrapper buy a policy we can name? If the name is fuzzy, you may be looking at accidental complexity rather than a pattern.

Composition wraps behavior — say it again with a metrics example. A metrics repository times save and increments counters, then delegates. Callers still see the repository interface. You can disable the metrics wrapper in tests by injecting the delegate directly. Inheritance would have forced a subclass tree tied to a concrete parent. Structural patterns buy replaceability at the seams.

Facades and adapters often travel together. A facade may own a use case and call an adapter for the vendor dial tone. Naming both keeps responsibilities sharp: facade for your policy, adapter for their shape. If one class does both and grows forever, split it when the vendor story and the business story stop changing for the same reasons.

Spring AOP proxies bring this episode into everyday enterprise Java. Transactions, security, and retries often arrive as proxy advice. Understanding proxies turns annotation surprises into predictable mechanics.

Before you leave structure, notice how these patterns show up in code reviews without the names. "Can we wrap this client to add retries?" is decorator talk. "Can we hide these five SDK calls behind one service method?" is facade talk. "Can we translate this third-party DTO at the boundary?" is adapter talk. Teaching the names simply gives the team compression for conversations they are already having.

When structural assembly is in place, the next question is how objects communicate and how algorithms vary without rewriting callers. That is behavioral patterns — Strategy, Observer, Command, and friends — in Episode Seventy.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Structural Patterns (Episode 69).

Narration technique: subclass explosion problem → decorator example → adapter/facade/proxy → Spring AOP proxy reality → design conversation → bridge to behavioral.

Teaching points preserved: composition wraps behavior; decorator; facade; proxy; Spring AOP uses proxies.
