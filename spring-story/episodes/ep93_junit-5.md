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

You are about to refactor `TariffCalculator` — the hazardous-surcharge rules that finance swears are correct. There is no automated test. The last change was verified by a spreadsheet on someone’s laptop. You either ship blind or you invent a way to re-run the known cases after every edit. That pressure is why Phase 10 starts here, underneath Spring’s `@WebMvcTest` and `@SpringBootTest`: you need an engine that discovers test methods, runs them, and reports pass or fail before Spring even enters the picture.

That engine is JUnit 5. Jupiter is the programming model you write against. The JUnit Platform is what Maven Surefire or Gradle’s test task launches. Vintage exists only if you still carry JUnit 4. Hold three verbs for the whole episode: discovery, execution, reporting.

Here is the safety net you wish you had before touching surcharge math — pure Java, no Spring context — so those verbs stay audible in one file.

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
}
```

Discovery: Surefire asks the Platform for tests; the Platform asks Jupiter; Jupiter finds `appliesHazardousSurcharge`, three parameterized invocations from `hazardMatrix`, and `rejectsNullBase`. You did not register them in an XML suite — the annotations *are* the registration.

Execution: for each test, Jupiter creates an instance (per-method by default), runs `@BeforeEach`, invokes the method, and records the outcome. `assertEquals` compares money; `assertThrows` documents the guard. If surcharge math regresses, execution fails at the assertion line with expected versus actual — not with a vague “build failed.”

Reporting: Jupiter publishes events — started, skipped, successful, failed, aborted — that Surefire prints and CI parses. A red build is a failed report from this channel. Green means these methods passed, not that the harbor is safe.

Lifecycle annotations shape execution. `@BeforeAll` / `@AfterAll` run once per class. `@Disabled` skips and reports skipped, not passed. `Assumptions.assumeTrue` aborts as skipped when an environment prerequisite is missing — different from failure.

```java
@Test
void onlyWhenTariffFixturePresent() {
    Assumptions.assumeTrue(
            Files.exists(Path.of("src/test/resources/tariff-fixture.json")));
    // load fixture-backed scenario
}
```

Extensions are Jupiter’s plugin model. `@ExtendWith` registers parameter resolvers and callbacks. Mockito’s Jupiter extension and Spring’s `SpringExtension` plug in here — which is why later harbor tests feel like annotations that cooperate with JUnit, not a separate runner universe like old `SpringJUnit4ClassRunner`.

A misconception is treating green bars as proof the booth is safe when tests only cover happy-path TEU math. Another is sharing mutable static tariff tables across tests and chasing order-dependent failures — Jupiter may run in parallel if you enable it. A third is asserting on log lines or `Thread.sleep` instead of return values; flaky reports train teams to ignore CI.

JUnit runs the method. It does not invent stand-ins for `DutyProvider` when tariff logic depends on a port. When the calculator cannot be constructed without a live collaborator, you need a different tool.

That tool is Mockito.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 93 (*JUnit 5*).
