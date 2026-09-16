# Episode 69 — Structural Patterns

| Field | Value |
|---|---|
| Episode | 69 |
| Title | Structural Patterns |
| Catalog handbook column | 69 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Creational patterns asked how objects are born. Structural patterns ask how objects are assembled so you can extend behavior without melting the type hierarchy. Composition wraps behavior. Inheritance is not banned — but exploding subclasses for every feature combination is how codebases become museums of `LoggedCachedSecureX`.

Suppose you have a repository. You need logging around saves. Then metrics. Then a circuit breaker. Inheritance would tempt `LoggingRepo extends JdbcRepo`, then `MetricsLoggingRepo extends LoggingRepo`. A decorator adds behavior by wrapping the same interface:

```java
class LoggingRepo implements Repo {
  private final Repo delegate;
  public void save(Entity e) { log(e); delegate.save(e); }
}
```

`LoggingRepo` is still a `Repo`. Callers need not know whether they hold the raw repository or a wrapped one. Decorator versus inheritance, asked in an interview, is exactly this: add behavior via composition without exploding subclasses. Stack decorators carefully — five wrappers with unclear order recreate the complexity you fled. Order matters: authentication before rate limiting before caching is a different system than the reverse. Document the stack.

Adapters appear when two interfaces do not match. The SMS provider wants `sendSms(Phone, Text)`. Your domain port says `notify(UserId, Notification)`. The adapter loads the phone number, formats the text, translates errors into domain failures, and isolates the SDK. When the vendor changes, one class moves. Without an adapter, vendor types leak into services and tests.

Facades simplify subsystems: one entry point that orchestrates collaborating classes so callers are not wired to every moving part. They fail in two opposite ways. Too thin: pass-through methods with no policy. Too thick: a god object that knows the entire company. A good facade encodes a few use cases your system actually owns — "charge customer for invoice" — not one hundred low-level dials. Facades and adapters often travel together: facade for your policy, adapter for their shape. Split when the vendor story and the business story stop changing for the same reasons.

Proxies control access. They stand in for a real object and intercept calls — lazy loading, security, remote access, transactional boundaries. If you have used Spring AOP, you have lived with proxies: the bean you inject may wrap your class to apply transactions or security. Sharp edges: `equals`, `final` methods, and self-invocation (`this.method()` bypassing the proxy). A method annotated transactional calls another method on `this` — the call does not pass through the proxy, so the annotation does not apply. Structural understanding prevents "Spring is broken" tickets.

Walk a design conversation. "Should we facade the payment SDK?" If three services each duplicate the same five SDK calls, yes. If one call site exists, maybe premature. "Should we decorate the repository with caching?" Only if cache policy is clear — keys, TTL, invalidation — otherwise you hide a correctness problem behind a structural pattern. Patterns amplify both good and bad policy. When reviewing wrappers, ask: does this buy a policy we can name? If the name is fuzzy, you may be looking at accidental complexity.

Composition keeps showing up as the safe default. Adapter for foreign shapes. Decorator for layered policies on one interface. Facade for a curated subsystem door. Proxy for controlled access and infrastructure concerns. Spring's AOP proxies are not a different universe; they are this idea with a framework engine. Before you leave structure, notice how these appear in reviews without the names: "wrap this client to add retries" is decorator talk; "hide these five SDK calls behind one method" is facade talk; "translate this third-party DTO at the boundary" is adapter talk.

When structural assembly is in place, the next question is how objects communicate and how algorithms vary without rewriting callers — Strategy, Observer, Command, and friends.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Structural Patterns (Episode 69).

Narration technique: subclass explosion → decorator example → adapter/facade/proxy → Spring AOP reality → design conversation → bridge to behavioral.

Teaching points preserved: composition wraps behavior; decorator; facade; proxy; Spring AOP uses proxies.
