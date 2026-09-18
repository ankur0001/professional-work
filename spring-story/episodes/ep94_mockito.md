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

JUnit runs the test. It does not invent stand-ins for your dependencies. Mockito does: it creates mock objects, stubs return values, and verifies interactions. In a Spring codebase, the classic unit-test move is to construct a service with mocked collaborators so you exercise branching logic without a database, without Feign, and without a Spring context.

Take an order service that must check stock through a port and then persist. In production the port is a Feign client. In a unit test the port is a mock.

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
class OrderServiceTest {

    @Mock
    InventoryPort inventory;

    @Mock
    OrderRepository orders;

    @InjectMocks
    OrderService service;

    @Test
    void placesOrderWhenStockAvailable() {
        when(inventory.getStock("SKU-1"))
                .thenReturn(new StockView("SKU-1", 5));
        when(orders.save(any(Order.class)))
                .thenAnswer(inv -> inv.getArgument(0));

        Order placed = service.place(new PlaceOrderCommand("SKU-1", 2, "cust-9"));

        assertEquals("SKU-1", placed.sku());
        assertEquals(2, placed.qty());
        verify(inventory).reserve(new ReserveRequest("SKU-1", 2));
        verify(orders).save(any(Order.class));
    }

    @Test
    void rejectsWhenInsufficientStock() {
        when(inventory.getStock("SKU-1"))
                .thenReturn(new StockView("SKU-1", 1));

        assertThrows(InsufficientStockException.class,
                () -> service.place(new PlaceOrderCommand("SKU-1", 2, "cust-9")));

        verify(inventory, never()).reserve(any());
        verify(orders, never()).save(any());
    }
}
```

Walk the first test. `@ExtendWith(MockitoExtension.class)` hooks Mockito into Jupiter. `@Mock` creates fake `InventoryPort` and `OrderRepository`. `@InjectMocks` builds `OrderService`, injecting those mocks via constructor or fields. `when(...).thenReturn(...)` stubs stock. The service runs real code paths. `verify` asserts that reserve and save happened. The second test stubs low stock, asserts the domain exception, and verifies the remote reserve never fired — exactly the regression you want when someone “refactors” and reserves before checking.

Prefer explicit construction when teaching juniors:

```java
@Test
void placesOrderWhenStockAvailable_manualWiring() {
    InventoryPort inventory = mock(InventoryPort.class);
    OrderRepository orders = mock(OrderRepository.class);
    OrderService service = new OrderService(inventory, orders);

    when(inventory.getStock("SKU-1")).thenReturn(new StockView("SKU-1", 5));
    when(orders.save(any(Order.class))).thenAnswer(inv -> inv.getArgument(0));

    Order placed = service.place(new PlaceOrderCommand("SKU-1", 2, "cust-9"));
    assertEquals(2, placed.qty());
}
```

Same collaborators, no `@InjectMocks` mystery. Use whichever style your team standardizes; both are Mockito. The point is the subject under test is real Java, and the port is a controlled fake.

Argument matchers (`any`, `eq`) and captors refine verification when you care about the payload:

```java
ArgumentCaptor<Order> captor = ArgumentCaptor.forClass(Order.class);
verify(orders).save(captor.capture());
assertEquals("cust-9", captor.getValue().customerId());
```

Stubbing exceptions exercises failure branches without a real outage:

```java
when(inventory.getStock("SKU-1"))
        .thenThrow(new InventoryUnavailableException("down"));
```

Then assert that `OrderService` maps that into a domain failure or a retry decision — whichever your design promises. The mock’s job is to make the collaborator’s failure mode reproducible on every run.

Strictness matters. Modern Mockito is strict about unused stubs; that is a feature — it catches tests that no longer mean what you think. Prefer constructor injection in the production class so `@InjectMocks` and manual `new OrderService(inventory, orders)` stay honest. Spies wrap real objects; use them sparingly when you must partially mock, not as a default.

In Spring Boot tests you will later meet `@MockBean`, which places a Mockito mock *inside* the ApplicationContext. That is still Mockito under the hood, but the lifecycle belongs to Spring Test. Keep the distinction: this episode’s unit test never starts a context.

A misconception is mocking the class under test. Mock collaborators; run the real subject. Another is verifying every getter call until tests mirror implementation noise — verify state-changing interactions and meaningful outcomes. A third is using Mockito to fake types you do not own in elaborate ways (HTTP containers, JDBC drivers) when a narrower port interface would make stubbing trivial.

Today we unit-tested `OrderService` by mocking `InventoryPort` and `OrderRepository`, stubbing stock, asserting domain behavior, and verifying reserve/save interactions — JUnit for execution, Mockito for collaborators.

Some behavior only appears when Spring wires real beans, applies AOP proxies, or binds properties. Mocks alone will not load a `@Transactional` proxy or a `@ConditionalOnProperty` bean. For that you need the Spring TestContext Framework.

That is Spring Test.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 94 (*Mockito*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
