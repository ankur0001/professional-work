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

Unit tests construct `TariffService` with mocks. Gate’s `GateController` still needs Spring MVC: mapping, JSON conversion, validation, exception advice. Booting the whole harbor for every controller tweak is slow. `@WebMvcTest` loads a slice — just the web layer for named controllers — and `MockMvc` drives `DispatcherServlet` without opening a socket.

```java
@WebMvcTest(controllers = GateController.class)
class GateControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockBean
    GateReleaseService releases;

    @Test
    void checkInReturnsAcceptedPayload() throws Exception {
        when(releases.accept(eq("G12"), any(TruckCheckIn.class)))
                .thenReturn(CheckInResponse.accepted("G12", "MSCU123"));

        mockMvc.perform(post("/gates/G12/check-ins")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"containerId":"MSCU123","hazardClass":"IMDG_3","plate":"SGP-4421"}
                                """))
                .andExpect(status().isAccepted())
                .andExpect(jsonPath("$.gateId").value("G12"))
                .andExpect(jsonPath("$.containerId").value("MSCU123"));
    }

    @Test
    void rejectsMalformedBody() throws Exception {
        mockMvc.perform(post("/gates/G12/check-ins")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isBadRequest());
    }

    @Test
    @WithMockUser(roles = "GATE_OPERATOR")
    void operatorPathReachesService() throws Exception {
        when(releases.accept(eq("G12"), any())).thenReturn(CheckInResponse.accepted("G12", "MSCU123"));

        mockMvc.perform(post("/gates/G12/check-ins")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"containerId":"MSCU123","hazardClass":"NONE","plate":"SGP-4421"}
                                """))
                .andExpect(status().isAccepted());

        verify(releases).accept(eq("G12"), any(TruckCheckIn.class));
    }
}
```

`MockMvc` exercises the dispatcher pipeline: handler mapping, argument resolution, message conversion, `@Valid`, `@ControllerAdvice`. `@MockBean` puts a Mockito mock into the slice’s ApplicationContext, replacing the real `GateReleaseService` — different from a field `@Mock` that never enters the container. If you forget `@MockBean` for a required collaborator, the slice context fails to start with an unsatisfied dependency — that failure is useful; it tells you the controller’s true wiring. Security can be disabled for the slice or shaped with `@WithMockUser` when the controller relies on the security context. Validation annotations on `TruckCheckIn` fire here; that is the point of the malformed-body test. A green unit test of the service would never see a missing `containerId` rejected at the edge.

Other slices exist. `@DataJpaTest` focuses repositories and an embedded or Testcontainers database. `@JsonTest` focuses ObjectMapper and Jackson modules — handy when tariff money serialization is picky. `@SpringBootTest` loads the full context — save that for integration flows. The dial is intentional: narrow when you are testing mapping and JSON, widen when you are testing wiring across layers.

```java
@WebMvcTest(controllers = GateController.class)
@AutoConfigureMockMvc(addFilters = false) // illustrative when filters obscure the slice intent
class GateControllerValidationFocusTest {
    // keep filters off only while proving Bean Validation; restore for security-sensitive paths
}
```

Runtime symptoms of misuse: every controller change waits on full Boot startup because someone standardized on `@SpringBootTest`; or the opposite — slices so hollowed by `@MockBean` that advice and converters you care about never load. Another symptom: tests assert `isOk()` while the trucker app needs `202 Accepted` and a body shape — status-only assertions hide contract drift until mobile QA. A subtler miss: `@WebMvcTest` without your `@ControllerAdvice` bean — if advice is component-scanned only in the full app, Problem+JSON mapping never loads in the slice until you `@Import` it. Green tests return default Spring error bodies; production returns your harbor problem type.

Trade-offs: slices are fast and focused; they will not catch a missing `@Transactional` on `GateReleaseService` or a Feign decoder mismatch. Use them for HTTP shape and validation. Pair with Mockito unit tests for domain branching and broader tests for collaboration. Caching the TestContext across methods keeps CI honest about speed without pretending a slice is an integration test. When you add security filters back, expect more setup — `@WithMockUser` or a test `SecurityFilterChain` — and treat that as the price of testing the booth’s real denial paths.

A misconception is using `@SpringBootTest` for every controller assertion and waiting minutes per CI job. Another is `@MockBean` on half the context until the slice is no longer a slice. A third is asserting only HTTP 200 without checking JSON fields the trucker app depends on.

Controller slices prove HTTP shape. They do not prove that gate release commits a ledger row and talks to a wired billing client under security. That wider confidence is integration testing.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 95 (*Spring Test*).
