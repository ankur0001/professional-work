# Episode 09 — Bean Lifecycle

| Field | Value |
|---|---|
| Episode | 09 |
| Title | Bean Lifecycle |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 9 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

```
09:00:02 INFO  RateCache get miss key=hotel:harbor:king
09:00:02 WARN  Lettuce reconnect attempt 1
09:00:03 WARN  Lettuce reconnect attempt 2
09:00:08 INFO  Lettuce connection established
```

Those lines appear only after the morning booking wave — never during deploy. The Redis rate-cache pool was empty until the first requests forced connections open. Overnight shutdowns were worse: Redis logged abrupt disconnects because nobody closed the client. The team does not need another caching library. They need lifecycle hooks: warm before traffic, close on stop.

Spring's bean lifecycle is a sequence, not a single `new`. Rough order for a managed singleton: instantiate (constructor), populate properties / inject collaborators, aware interfaces (`BeanNameAware`, `BeanFactoryAware`, `ApplicationContextAware`, …), `BeanPostProcessor.postProcessBeforeInitialization`, init callbacks (`@PostConstruct`, `InitializingBean.afterPropertiesSet`, custom init-method), `BeanPostProcessor.postProcessAfterInitialization` (AOP proxies often wrap here), bean in service, then on context close `@PreDestroy` / `DisposableBean.destroy` / custom destroy-method. You do not memorize every extension point on day one. You learn where your pool open and close belong — after injection, before traffic; on shutdown, before the JVM exits.

```java
@Component
public class RateCachePool implements InitializingBean, DisposableBean {
    private final RedisUri uri;
    private LettuceConnectionFactory factory;
    private RedisTemplate<String, String> template;

    public RateCachePool(@Value("${rates.redis.uri}") String uri) {
        this.uri = RedisUri.create(uri);
    }

    @Override
    public void afterPropertiesSet() {
        factory = new LettuceConnectionFactory(uri);
        factory.afterPropertiesSet();
        factory.start();
        template = new RedisTemplate<>();
        template.setConnectionFactory(factory);
        template.afterPropertiesSet();
        // warm: open min idle connections before requests arrive
        try (RedisConnection c = factory.getConnection()) {
            c.ping();
        }
    }

    public Optional<String> get(String key) {
        return Optional.ofNullable(template.opsForValue().get(key));
    }

    @Override
    public void destroy() {
        if (factory != null) {
            factory.destroy();
        }
    }
}
```

Runtime after the fix. During context refresh, Spring creates `RateCachePool` via the constructor — only the URI string is set; `factory` and `template` are still null. Dependency injection for this bean is already done (the `@Value` resolved through Environment). Aware callbacks run if implemented. Then init: `afterPropertiesSet` builds the Lettuce factory, starts it, builds the template, and pings to force a real connection before the web tier accepts traffic. In a typical Boot app, context refresh completes before Tomcat starts serving — so the morning wave hits a warm pool instead of reconnect warnings. Controllers call `get`; the template is ready. On SIGTERM, Boot closes the context in reverse dependency order where possible, calls `destroy` on disposables, and Redis sees an orderly shutdown instead of TCP resets. Swap `@PostConstruct` for `afterPropertiesSet` if you prefer annotations; the timing relative to injection is what matters — init runs after dependencies are set. Prefer one init style per bean to avoid double-open surprises when both `@PostConstruct` and `afterPropertiesSet` do real work.

Failure mode symptoms from the hotel rate desk. Init that opens Redis against a down host: `BeanCreationException` during refresh, process fails to start — better than serving 500s with an empty pool, unless you deliberately lazy-init and degrade. Init that assumes another bean is already warmed without `depends-on` or constructor injection: intermittent NPEs when creation order shifts. Destroy skipped because the bean was never registered as disposable (raw `new RateCachePool` outside the container) — Redis still sees hard disconnects. Calling `get` from a constructor or from a `BeanPostProcessor` that runs before init: template still null. Prototype-scoped beans get init per instance but destroy only if you asked the container to manage the instance — forgotten destroy on prototypes is a classic leak. Another tell: `@PreDestroy` methods that never run because the JVM was killed with `kill -9`, or because a non-daemon thread kept the process alive past an incomplete context close.

Trade-offs. Interface callbacks (`InitializingBean` / `DisposableBean`) couple your class to Spring APIs; `@PostConstruct` / `@PreDestroy` need a common annotation processor but keep the class freer of Spring types; custom init/destroy method names in definitions suit third-party classes you cannot annotate. Lifecycle hooks are the right place for scarce resources — pools, file watchers, subscription threads. They are the wrong place for request-scoped business logic. Lazy-init delays the cost until first use; for Redis rate cache that recreates the morning reconnect storm unless something else warms it.

Misconception unique to lifecycle: "`@PostConstruct` runs before dependency injection finishes." It does not. Injection completes first; then init callbacks. If your init method sees null collaborators, the bug is elsewhere — wrong injection, wrong bean, field access before the container finished, or you constructed the object yourself outside Spring. Another misconception: "Constructor body is the init hook." Constructors run during instantiate, before collaborators are injectable via setters or some field paths; constructor injection is safe for final deps, but opening external resources in a constructor makes testing and proxy subclassing harder — prefer init callbacks for side-effecting startup.

Pools warm cleanly now. The bank batch team watching from across the hall still configures the same lifecycle idea in 2012-era XML, and they want a migration path toward Java config without a big-bang rewrite. How you express definitions — not only when they init — becomes the next fight.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 9 (*Bean Lifecycle*).
