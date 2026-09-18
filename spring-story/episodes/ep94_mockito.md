# Episode 94 — Mockito

| Field | Value |
|---|---|
| Episode | 94 |
| Title | Mockito |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 94 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`TariffCalculator` was pure. Real billing services are not: they ask a `DutyProvider` port for customs duty rates before summing the quote. In production that port may call a remote duty table. In a unit test you do not want that network. Mockito creates the stand-in, stubs returns, and verifies interactions while JUnit executes the real subject.

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TariffServiceTest {

    @Mock
    DutyProvider duties;

    @Mock
    TariffRepository tariffs;

    @InjectMocks
    TariffService service;

    @Test
    void quotesInclusiveOfDuty() {
        when(duties.rateFor("MSCU123", HazardClass.IMDG_3))
                .thenReturn(DutyRate.of("0.08"));
        when(tariffs.baseFor(HazardClass.IMDG_3))
                .thenReturn(Money.of("100.00"));

        Money quote = service.quote("MSCU123", HazardClass.IMDG_3);

        assertEquals(Money.of("108.00"), quote);
        verify(duties).rateFor("MSCU123", HazardClass.IMDG_3);
        verify(tariffs).baseFor(HazardClass.IMDG_3);
        verifyNoMoreInteractions(duties, tariffs);
    }

    @Test
    void failsWhenDutyUnavailable() {
        when(duties.rateFor(anyString(), any()))
                .thenThrow(new DutyUnavailableException("duty table down"));

        assertThrows(TariffQuoteException.class,
                () -> service.quote("MSCU123", HazardClass.IMDG_3));

        verify(tariffs, never()).baseFor(any());
    }
}
```

Walk the first test. `@ExtendWith(MockitoExtension.class)` hooks Mockito into Jupiter. `@Mock` creates fake `DutyProvider` and `TariffRepository`. `@InjectMocks` builds `TariffService` with those mocks — it prefers constructor injection when the class is written that way, which is another reason constructor DI pays off. `when(...).thenReturn(...)` stubs duty and base. The service runs real branching: multiply, round, assemble money. `verify` asserts the port was consulted. `verifyNoMoreInteractions` catches a quiet second call someone added during a “cleanup” refactor. The second test stubs a duty outage, asserts the domain exception, and verifies the repository never ran — the regression you want when someone loads base rates before checking duty availability and then throws anyway.

Prefer explicit construction when teaching:

```java
@Test
void quotesInclusiveOfDuty_manualWiring() {
    DutyProvider duties = mock(DutyProvider.class);
    TariffRepository tariffs = mock(TariffRepository.class);
    TariffService service = new TariffService(duties, tariffs);

    when(duties.rateFor("MSCU123", HazardClass.IMDG_3))
            .thenReturn(DutyRate.of("0.08"));
    when(tariffs.baseFor(HazardClass.IMDG_3))
            .thenReturn(Money.of("100.00"));

    assertEquals(Money.of("108.00"), service.quote("MSCU123", HazardClass.IMDG_3));
}
```

Argument captors refine verification when the invoice payload matters:

```java
ArgumentCaptor<DutyQuery> captor = ArgumentCaptor.forClass(DutyQuery.class);
verify(duties).query(captor.capture());
assertEquals("MSCU123", captor.getValue().containerId());
assertEquals(HazardClass.IMDG_3, captor.getValue().hazardClass());
```

Runtime failure modes of bad Mockito use show up as green tests that miss production bugs. Stubbing `any()` so widely that every path looks successful hides branching. Returning `null` from a mock where the production port never returns null turns NPEs into “flaky” CI. Over-verifying call order with `inOrder` couples tests to incidental sequencing. Strict stubbing (Mockito’s default with the Jupiter extension) failing on unused stubs is a feature — it catches tests that no longer mean what you think after a rename.

Spies wrap real objects; use them sparingly when you need a partial fake of a collaborator that is awkward to stub entirely. In Boot slice tests you will meet `@MockBean`, which places a Mockito mock inside the ApplicationContext. Same library, different lifecycle — the mock must satisfy every bean that injects that type for the context to start. This episode’s unit test never starts a context; that speed is the point when you are proving tariff math.

Trade-offs: mocks buy isolation and speed; they lie about serialization, SQL, and wire formats. Ports at the edge of the domain (`DutyProvider`) make mocking honest. Mocking types you do not own (HTTP clients, EntityManager) tends toward brittle stubbing — wrap them behind a narrow interface first.

When a stub must simulate slow duty lookups, `thenAnswer` with a sleep is a last resort that makes unit tests flaky under load; prefer injecting a clock or a `DutyProvider` fake that returns immediately with a “stale” flag and keep timing tests at the integration layer. For void collaborators (audit publishers), `verify(publisher).publish(any())` beats asserting on log output.

A misconception is mocking `TariffService` itself. Mock `DutyProvider`; run the real service. Another is verifying every getter until tests mirror implementation noise. A third is elaborately faking types you do not own (HTTP containers, JDBC drivers) when a narrow port interface would make stubbing trivial.

Mocks prove branching. They do not load a `@RestController` advice chain or bind `@WebMvcTest` filters. For gate’s HTTP slice, you need the Spring TestContext Framework.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 94 (*Mockito*).
