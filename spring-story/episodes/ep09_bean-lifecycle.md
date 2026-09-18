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

Scope told us how many instances exist. Lifecycle tells us what Spring does to each instance on the way in — and on the way out.

Picture a `MarketDataClient` that opens a WebSocket during construction and registers a JVM shutdown hook in a field initializer. In tests, contexts start and stop repeatedly. Sockets leak. Hooks pile up. Or the opposite failure: initialization that needs an injected collaborator runs in the constructor before injection finishes, so you read a null repository and blame Spring for "not wiring." The real issue is timing. Construction, dependency population, and custom init are different phases.

Without a clear lifecycle, teams sprinkle startup logic in constructors, static blocks, and `@PostConstruct` with no shared model of order. Destroy logic is forgotten until file handles and thread pools outlive the context. The practical question is: in what order does Spring bring a bean to life, and where can I safely run custom setup and teardown?

Spring's bean lifecycle for a typical singleton is a sequence. Instantiate the object. Populate properties and inject collaborators. Call Aware callbacks such as `BeanNameAware` or `ApplicationContextAware` if implemented. Let `BeanPostProcessor`s wrap or decorate the instance — this is where AOP proxies often appear. Invoke initialization: `@PostConstruct`, `InitializingBean.afterPropertiesSet`, or a custom init method from the definition. The bean is ready for use. On context close, run destroy: `@PreDestroy`, `DisposableBean.destroy`, or a custom destroy method.

```java
@Component
public class MarketDataClient implements DisposableBean {
    private final MeterRegistry meters;
    private WebSocketSession session;

    public MarketDataClient(MeterRegistry meters) {
        this.meters = meters;
        // constructor: only store dependencies — do not open the socket yet
    }

    @PostConstruct
    void connect() throws Exception {
        session = WebSocketClient.connect("wss://feeds.example/quotes");
        meters.counter("marketdata.connects").increment();
    }

    public Quote latest(String symbol) {
        return session.requestQuote(symbol);
    }

    @Override
    public void destroy() throws Exception {
        if (session != null) {
            session.close();
        }
    }
}
```

Follow one refresh. Spring constructs `MarketDataClient` with a real `MeterRegistry`. Injection is done before `@PostConstruct`, so `connect` can use `meters` safely. The socket opens once the bean is otherwise wired. While the context runs, `latest` uses the live session. On `context.close()`, `destroy` closes the socket. Move `connect` into the constructor and you either cannot use injected collaborators yet or you open resources before the container finished wiring — both are lifecycle mistakes.

`BeanPostProcessor`s sit in that sequence for a reason. If you log `this.getClass()` inside `@PostConstruct` and see a CGLIB proxy, a post-processor already wrapped you. Initialization methods still run on the underlying instance according to Spring's rules, but understanding the phase order stops a lot of "why is my aspect missing?" confusion.

A lifecycle-specific misconception is treating the constructor as the init hook for anything that needs collaborators or that might throw checked startup failures you want Spring to manage uniformly. Another is assuming prototype beans get the same destroy care as singletons — they do not; Spring does not track prototypes for full destruction the same way.

Once you can place init and destroy on the timeline, another authoring question appears. How should a team express all of this configuration — XML documents, stereotype annotations on classes, or Java `@Configuration` classes? Those configuration styles are the next fork in the road.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 9 (*Bean Lifecycle*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
