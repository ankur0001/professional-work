# Episode 93 — JUnit 5

| Field | Value |
|---|---|
| Episode | 93 |
| Title | JUnit 5 |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 93 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Spring Cloud gave you patterns. Patterns without tests are folklore. Phase 10 starts underneath Spring’s test annotations, at the engine that discovers methods, runs them, and reports pass or fail: JUnit 5, also called JUnit Jupiter for the programming model, with a Vintage engine for old JUnit 4 classes if you still have them. Maven Surefire or Gradle’s test task launches the JUnit Platform; the Platform finds engines; Jupiter finds your `@Test` methods.

Hold three verbs for the whole episode: discovery, execution, reporting. Discovery: the engine scans the test classpath for classes that contain Jupiter test APIs — `@Test`, `@ParameterizedTest`, `@TestFactory`, nested `@Nested` types. Execution: for each test method, Jupiter creates an instance (per-method by default), runs lifecycle callbacks, invokes the method, and records outcomes. Reporting: the Platform publishes events — started, skipped, successful, failed, aborted — that Surefire prints and CI systems parse.

Here is a real unit test for a pure pricing component — no Spring context yet — so you can hear those three verbs in one file.

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

class PricingServiceTest {

    PricingService pricing;

    @BeforeEach
    void setUp() {
        pricing = new PricingService(new PercentageDiscountPolicy());
    }

    @Test
    @DisplayName("applies ten percent discount to subtotal")
    void appliesDiscount() {
        Money result = pricing.total(Money.of("100.00"), CustomerTier.GOLD);
        assertEquals(Money.of("90.00"), result);
    }

    @ParameterizedTest(name = "subtotal={0}, tier={1} -> {2}")
    @CsvSource({
            "100.00, GOLD, 90.00",
            "100.00, SILVER, 95.00",
            "100.00, BRONZE, 100.00"
    })
    void tierMatrix(String subtotal, CustomerTier tier, String expected) {
        assertEquals(Money.of(expected), pricing.total(Money.of(subtotal), tier));
    }

    @Test
    void rejectsNullSubtotal() {
        assertThrows(IllegalArgumentException.class,
                () -> pricing.total(null, CustomerTier.GOLD));
    }

    @AfterEach
    void tearDown() {
        pricing = null;
    }
}
```

Discovery: Surefire asks Jupiter for tests in `PricingServiceTest`. Jupiter finds `appliesDiscount`, three parameterized invocations from `tierMatrix`, and `rejectsNullSubtotal`. Execution: `@BeforeEach` runs before each invocation; assertions verify totals; `assertThrows` verifies the guard. Reporting: a failure in `appliesDiscount` prints the display name, expected versus actual, and a stack trace pointing at the assertion line — not at the build tool. CI marks the build red from that report.

Lifecycle annotations shape execution. `@BeforeAll` / `@AfterAll` run once per class (methods must be static unless you change the lifecycle). `@BeforeEach` / `@AfterEach` run around every test. `@Disabled` skips discovery’s selected method and reports it skipped, not passed. Assumptions (`Assumptions.assumeTrue`) abort a test as skipped when an environment prerequisite is missing — different from a failure.

```java
@Test
void onlyOnCi() {
    Assumptions.assumeTrue("true".equals(System.getenv("CI")));
    // expensive check that should not fail local laptops
}
```

Extensions are Jupiter’s plugin model. `@ExtendWith` registers extensions for parameter resolution, callbacks, or callbacks around tests. Mockito’s Jupiter extension and Spring’s `SpringExtension` both plug in here — which is why later episodes feel like “annotations that work with JUnit,” not a separate runner universe like old `SpringJUnit4ClassRunner`.

A misconception is treating green bars as proof of production readiness when tests only cover happy paths. Another is sharing mutable static state across tests and then chasing order-dependent failures — Jupiter may run in parallel if you enable it. A third is asserting on log lines or wall-clock sleeps instead of state and return values; flaky reports train teams to ignore CI.

Today we watched JUnit 5 discover real test methods, execute them with lifecycle hooks and assertions, and report failures with names CI can surface — the foundation every Spring test annotation sits on.

Your `PricingService` was self-contained. Most Spring services are not: they call repositories, Feign clients, clocks, or payment gateways. You need those collaborators under your control without starting the real network.

That control is Mockito.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 93 (*JUnit 5*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
