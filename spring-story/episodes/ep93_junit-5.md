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

Harbor Cloud patterns without tests are folklore. Phase 10 starts underneath Spring’s `@WebMvcTest` and `@SpringBootTest`, at the engine that discovers methods, runs them, and reports pass or fail: JUnit 5 — Jupiter for the programming model, Vintage only if you still carry JUnit 4. Maven Surefire or Gradle’s test task launches the JUnit Platform; the Platform finds engines; Jupiter finds your `@Test` methods.

Hold three verbs for the whole episode: discovery, execution, reporting. Discovery scans the test classpath for Jupiter APIs — `@Test`, `@ParameterizedTest`, `@TestFactory`, `@Nested`. Execution creates an instance (per-method by default), runs lifecycle callbacks, invokes the method, records outcomes. Reporting publishes events — started, skipped, successful, failed, aborted — that Surefire prints and CI parses.

Here is a real unit test for tariff math — pure Java, no Spring context — so you can hear those verbs in one file.

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

class TariffCalculatorTest {

    TariffCalculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new TariffCalculator(new StandardSurchargePolicy());
    }

    @Test
    @DisplayName("applies hazardous surcharge on top of base TEU rate")
    void appliesHazardousSurcharge() {
        Money result = calculator.quote(Money.of("100.00"), HazardClass.IMDG_3);
        assertEquals(Money.of("118.00"), result);
    }

    @ParameterizedTest(name = "base={0}, hazard={1} -> {2}")
    @CsvSource({
            "100.00, NONE, 100.00",
            "100.00, IMDG_3, 118.00",
            "100.00, IMDG_1, 140.00"
    })
    void hazardMatrix(String base, HazardClass hazard, String expected) {
        assertEquals(Money.of(expected), calculator.quote(Money.of(base), hazard));
    }

    @Test
    void rejectsNullBase() {
        assertThrows(IllegalArgumentException.class,
                () -> calculator.quote(null, HazardClass.NONE));
    }

    @AfterEach
    void tearDown() {
        calculator = null;
    }
}
```

Discovery: Surefire asks Jupiter for tests in `TariffCalculatorTest`. Jupiter finds `appliesHazardousSurcharge`, three parameterized invocations from `hazardMatrix`, and `rejectsNullBase`. Execution: `@BeforeEach` builds a fresh calculator; assertions check money; `assertThrows` verifies the guard. Reporting: a failure in `appliesHazardousSurcharge` prints the display name, expected versus actual, and a stack trace at the assertion line — CI goes red from that report, not from a vague “build failed.”

Lifecycle annotations shape execution. `@BeforeAll` / `@AfterAll` run once per class (static unless you change the lifecycle). `@BeforeEach` / `@AfterEach` wrap every test. `@Disabled` skips and reports skipped, not passed. `Assumptions.assumeTrue` aborts as skipped when an environment prerequisite is missing — different from failure.

```java
@Test
void onlyWhenTariffFixturePresent() {
    Assumptions.assumeTrue(Files.exists(Path.of("src/test/resources/tariff-fixture.json")));
    // load fixture-backed scenario
}
```

Extensions are Jupiter’s plugin model. `@ExtendWith` registers parameter resolvers and callbacks. Mockito’s Jupiter extension and Spring’s `SpringExtension` plug in here — which is why later harbor tests feel like “annotations that work with JUnit,” not a separate runner universe like old `SpringJUnit4ClassRunner`.

A misconception is treating green bars as proof the booth is safe when tests only cover happy-path TEU math. Another is sharing mutable static tariff tables across tests and chasing order-dependent failures — Jupiter may run in parallel if you enable it. A third is asserting on log lines or `Thread.sleep` instead of return values; flaky reports train teams to ignore CI.

JUnit runs the method. It does not invent stand-ins for `DutyProvider` when tariff logic depends on a port. That is Mockito’s job.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 93 (*JUnit 5*).
