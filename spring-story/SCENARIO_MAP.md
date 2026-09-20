# Unique scenario map (anti-template)

Each bulk episode MUST use its assigned domain situation. Do **not** reuse OrderService/CheckoutService unless listed.

| Ep | Concept | Required situation (use this world) |
|---:|---|---|
| 02 | Spring Architecture | Airport baggage-tracking monolith splitting into modules |
| 03 | IoC | Hospital appointment scheduler constructing doctors/rooms/notifiers with `new` |
| 05 | BeanFactory | CLI freight-rate calculator embedding Spring only for wiring |
| 06 | ApplicationContext | Multilingual pharmacy kiosk needing messages + events + env |
| 07 | Bean Definition | Plugin marketplace loading payment plugins from YAML metadata |
| 08 | Bean Scopes | Shared shopping-cart bug across concurrent hotel-booking users |
| 09 | Bean Lifecycle | Warming a Redis connection pool before traffic; closing on shutdown |
| 10 | Configuration Styles | Migrating a 2012 XML bank batch job toward Java config |
| 11 | Component Scanning | Multi-module cargo app accidentally scanning test utilities into prod |
| 12 | @Resource vs @Autowired vs @Inject | Two `DataSource` beans (primary OLTP vs reporting) — which injection wins |
| 13 | @Configuration | Full-screen cinema ticketing wiring without component scan |
| 14 | @Bean | Wrapping a third-party SMS SDK you do not own |
| 15 | Profiles | Same artifact: local H2 vs staging Postgres vs prod Postgres+replicas |
| 16 | Environment | Feature flags + DB URLs resolved from env/files/CLI for a tolling system |
| 18 | Boot Architecture | Cold-start timeline of a bike-share API (`SpringApplication` phases) |
| 19 | Auto Configuration | Adding Postgres driver suddenly creates DataSource — who did that? |
| 20 | Starters | New hire’s `pom.xml` dependency hell before `spring-boot-starter-web` |
| 21 | @SpringBootApplication | Three annotations fused; scan-base mistake hides controllers |
| 22 | Configuration Properties | Typed `FreightRatesProperties` binding vs scattered `@Value` |
| 23 | External Configuration | K8s ConfigMap/Secret overrides for tolling service |
| 24 | Actuator | On-call curl `/actuator/health` during a seaport outage |
| 25 | DevTools | LiveReload loop while building a museum ticket UI |
| 26 | Logging | Missing correlation IDs in ferry-booking logs at 2am |
| 27 | Boot Profiles | `application-prod.yml` activates different payment merchant IDs |
| 28 | Packaging | Fat jar vs layered jar for containerized tram timetable API |
| 29 | DispatcherServlet | `GET /luggage/{tag}` through mapping → adapter → controller |
| 30 | Controllers | `@RestController` method for `/luggage/{tag}` body/status |
| 31 | REST APIs | Resource design for parcel tracking (URLs, verbs, status codes) |
| 32 | Validation | Rejecting malformed customs declaration JSON at the edge |
| 33 | Exception Handling | Consistent Problem+JSON for unknown parcel IDs |
| 34 | Filters | Adding `X-Request-Id` before security/MVC for customs API |
| 35 | Interceptors | Timing only `/admin/**` handler methods in a port console |
| 36 | File Upload | Uploading bill-of-lading PDFs with size limits |
| 37 | REST Best Practices | Idempotent parcel create + pagination of tracking events |
| 38 | JPA Fundamentals | Mapping `Vessel` entity vs hand-written JDBC |
| 39 | Hibernate Internals | Dirty checking on `BerthAssignment` flush |
| 40 | Entity Lifecycle | Detached `CargoItem` after request ends; merge mistake |
| 41 | Persistence Context | Same `Booking` instance identity inside one request |
| 42 | Repositories | `VesselRepository.findByImoNumber` derived query |
| 43 | Relationships | `Manifest`↔`CargoLine` one-to-many with orphan removal |
| 44 | JPQL | Query manifests by vessel + date without table columns |
| 45 | Criteria API | Dynamic port-search filters built at runtime |
| 46 | Specifications | Composable `CargoSpecs.isHazardous().and(inPort("SGSIN"))` |
| 47 | Caching | Cache vessel directory reads; evict on update |
| 48 | Optimistic Locking | Two clerks edit same berth capacity (`@Version`) |
| 49 | Pessimistic Locking | Seat/berth reservation requiring `PESSIMISTIC_WRITE` |
| 50 | JPA Performance | Slow schedule board — batch size, entity graph, projections |
| 51 | N+1 | Manifest list triggering per-line selects |
| 52 | @Transactional | Stock decrement + reservation + ledger must atomic |
| 53 | Propagation | Checkout audit must survive outer rollback (`REQUIRES_NEW`) |
| 54 | Isolation | Phantom berth reads under concurrent booking |
| 55 | Rollback Rules | Checked `ManifestException` must rollback |
| 56 | Distributed TX | DB + JMS booking — why 2PC hurts |
| 57 | Saga | Trip book flight+hotel+car with compensations |
| 58 | AOP | Timing + audit around harbor gate services without clutter |
| 59 | Dynamic Proxies | What object is actually injected for a transactional gate service |
| 60 | JDK Proxy | Interface-based `GateService` proxy |
| 61 | CGLIB | Concrete `@Service` without interface — subclass proxy |
| 62 | Advice | `@Around` retry for flaky tide API calls |
| 63 | Pointcuts | Narrow `execution` so advice does not hit repositories |
| 64 | Aspect Ordering | Security → transaction → metrics order matters |
| 65 | AOP Performance | Wide pointcut adding 3ms × millions of calls |
| 66 | Security Fundamentals | Open harbor API on the internet — vocabulary of authn/authz |
| 67 | Authentication | Basic/form/JWT establishing `SecurityContext` for crane operator |
| 68 | Authorization | Alice vs Bob on `/admin/berths` |
| 69 | JWT | Stateless mobile app for truckers with bearer tokens |
| 70 | OAuth2 | Calendar app accessing harbor API on user’s behalf |
| 71 | OIDC | Login with company IdP; ID token vs access token |
| 72 | Method Security | `@PreAuthorize` on `releaseGate(cargoId)` ownership |
| 73 | CSRF | Browser cookie session forged POST to release cargo |
| 74 | CORS | SPA on `https://ops.example` calling `https://api.example` |
| 75 | Security Filters | Walk `SecurityFilterChain` order for harbor API |
| 76 | Reactive Programming | Thread-per-request collapse under AIS vessel position fan-in |
| 77 | Mono | Single vessel lookup async |
| 78 | Flux | Streaming AIS positions to operators |
| 79 | Schedulers | Offload blocking PDF generation in reactive chain |
| 80 | Backpressure | Slow operator UI vs fast position publisher |
| 81 | WebFlux | Reactive `/positions/stream` endpoint |
| 82 | Reactive Security | JWT on WebFlux filter chain |
| 83 | Microservices | Splitting harbor monolith into scheduling + billing + gate |
| 84 | Config Server | 30 services reading tariff rules centrally |
| 85 | Discovery | Gate service finding billing instances by name |
| 86 | API Gateway | External truckers hit one edge; routing to internals |
| 87 | Load Balancing | WebClient/Feign choose instance among 3 billing pods |
| 88 | Feign | Declarative `BillingClient` from gate service |
| 89 | Circuit Breaker | Billing timeouts open circuit; gate degrades |
| 90 | Tracing | One truck check-in spans gateway→gate→billing |
| 91 | Resilience4j | Retry + rate limiter + bulkhead on tide API |
| 92 | Cloud Stream | Berth-changed events to Kafka binder |
| 93 | JUnit 5 | Real `TariffCalculatorTest` discovery/execution/reporting |
| 94 | Mockito | Mock `DutyProvider` port in tariff service unit test |
| 95 | Spring Test | `@WebMvcTest` for gate controller slice |
| 96 | Integration Testing | `@SpringBootTest` + MockMvc for gate release flow |
| 97 | Testcontainers | Real Postgres for `VesselRepository` tests |
| 98 | Contract Testing | Gate’s Feign contract vs billing stub |
| 99 | Micrometer | Timer around `releaseGate` |
| 100 | Prometheus | Scrape `/actuator/prometheus` for gate pods |
| 101 | Grafana | Dashboard for gate p95 + error ratio |
| 102 | OpenTelemetry | Trace + metrics correlation for check-in |
| 103 | Perf Tuning | Find hot method via flame graph / metrics |
| 104 | Memory | Leak from unbounded AIS cache; heap dump clues |
| 105 | Production Readiness | Probes, migrations, runbooks before go-live |
| 106 | Layered | Classic controller-service-repo harbor app |
| 107 | Hexagonal | Domain gate release with ports/adapters |
| 108 | Clean | Dependency rule: domain must not import Spring Web |
| 109 | DDD | `Berth` aggregate + ubiquitous language |
| 110 | Event-Driven | BerthReserved event decouples billing |
| 111 | CQRS | Write berth assignments vs read schedule board model |
| 112 | Case Studies | Three postmortems synthesizing the series |

Agents must treat this table as binding for domain flavor.
