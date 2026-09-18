# Episode 95 — Spring Test

| Field | Value |
|---|---|
| Episode | 95 |
| Title | Spring Test |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 95 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Mockito isolates a class. Spring Test loads a slice — or a full slice — of the container so you can prove that annotations, proxies, and property binding behave as wired. The Spring TestContext Framework caches an `ApplicationContext` across tests when configuration matches, starts it once, injects beans into test instances, and can roll back transactions after each test method. On JUnit 5, `@ExtendWith(SpringExtension.class)` connects Jupiter to that framework; Boot’s `@SpringBootTest` and slice annotations meta-annotate that extension for you.

Start with a focused slice rather than booting the world. `@WebMvcTest` loads only web-layer beans — controllers, JSON converters, `Validator` — and leaves `@Service` beans out unless you provide them. Combine it with `@MockBean` to replace a collaborator inside the context.

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockBean
    OrderService orderService;

    @Test
    void getOrderReturnsJson() throws Exception {
        when(orderService.get("o-1"))
                .thenReturn(new OrderResponse("o-1", "PLACED"));

        mockMvc.perform(get("/orders/o-1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value("o-1"))
                .andExpect(jsonPath("$.status").value("PLACED"));
    }
}
```

`MockMvc` drives the DispatcherServlet without a network socket. You assert status, headers, and JSON paths. `@MockBean` puts a Mockito mock into the Spring context, replacing the real `OrderService` bean — different from a plain `@Mock` field that never enters the container.

`@DataJpaTest` focuses on JPA repositories with an embedded database by default, transactional and rolled back after each test. `@JsonTest`, `@RestClientTest`, `@SecurityMockMvcRequestPostProcessors` — each slice keeps the context small so feedback stays fast. Context caching means a second test class with the same configuration reuses the started context; change an `@MockBean` set and you may force a new context — watch startup times when the suite grows.

```java
@DataJpaTest
class OrderRepositoryTest {

    @Autowired
    OrderRepository orders;

    @Test
    void findsByCustomer() {
        orders.save(OrderEntity.newFor("cust-9"));
        assertEquals(1, orders.findByCustomerId("cust-9").size());
    }
}
```

`@JdbcTest`, `@RestClientTest`, and `@JsonTest` follow the same philosophy: load only what that layer needs. When a slice surprises you by missing a bean, resist the reflex to switch immediately to `@SpringBootTest`. Often `@Import` of one configuration class or a single `@MockBean` restores the missing collaborator without booting the entire Cloud stack.

`@SpringBootTest` loads the full Boot application — or a specified set of classes — when you need multiple layers together. Pair it with `@ActiveProfiles("test")` and `src/test/resources/application-test.yml` so tests do not call production config servers. `@TestPropertySource` overrides individual keys. `@Transactional` on a test class rolls back repository writes automatically when you use a transactional manager — great for isolation, dangerous if you accidentally test code that needs a committed row visible to another transaction.

Context failures deserve a reading habit. If the test ApplicationContext fails to start, scroll to the first `Caused by` that mentions your bean — not the last `ApplicationContextException` wrapper. Many “Spring Test is flaky” reports are actually missing test beans or wrong profiles.

A misconception is using `@SpringBootTest` for every class because it feels thorough. Full context tests are slower and broader; prefer unit tests and slices until the behavior truly spans layers. Another is confusing `@MockBean` with `@Mock`: only `@MockBean` replaces a bean definition in the context. A third is mutating global static state inside a Spring test and poisoning the cached context for later classes.

Today we connected JUnit 5 to the TestContext Framework, drove a controller with `@WebMvcTest` and `MockMvc`, swapped collaborators with `@MockBean`, and noted repository slices and full Boot tests as wider dials on the same mechanism.

Slice tests still fake or embed much of the outside world. When you need confidence that your app talks to a real browser of HTTP clients, a real security filter chain, and a real schema against a real engine, you step into broader integration testing — and then into containers.

That broader proof is Integration Testing.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 95 (*Spring Test*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
