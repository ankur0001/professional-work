# Episode 72 — IoC and Dependency Injection

| Field | Value |
|---|---|
| Episode | 72 |
| Title | IoC and Dependency Injection |
| Catalog handbook column | 72 |
| Narration source script | `make_episode_72.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy-One introduced Spring as a platform around an IoC container.
2. Inversion of Control flips who constructs collaborators — the framework does.
3. Dependency Injection is the main technique Spring uses to achieve IoC.
4. Get this wrong — mysterious nulls, circular dependencies, and untestable code.
5. Get this right — clear graphs, easy mocks, and predictable startup.
6. Today — IoC versus DI, injection styles, bean scopes, and wiring pitfalls.

### Scene `title` (renderer: `title`)

1. Episode Seventy-Two.
2. IoC and Dependency Injection.

### Scene `ioc_vs_di` (renderer: `ioc_vs_di`)

1. IoC is the principle — DI is the mechanism.
2. Inversion of Control — your code does not new up the whole object graph.
3. Dependency Injection — dependencies are provided from outside the class.
4. Spring's ApplicationContext is the injector and lifecycle manager.
5. Factories, service locators, and events are other IoC styles — DI is the default.
6. Say IoC for the idea — DI for how Spring usually implements it.

### Scene `injection_styles` (renderer: `injection_styles`)

1. Three injection styles you will see in Spring code.
2. Constructor injection — required dependencies as final fields — preferred.
3. Setter injection — optional dependencies or reconfiguration after create.
4. Field injection with Autowired — short, but harder to test and reason about.
5. Constructor injection makes invariants obvious — object is complete after new.
6. Modern Spring and Boot samples default to constructor injection for a reason.

### Scene `scopes` (renderer: `scopes`)

1. Bean scopes control how many instances the container creates.
2. Singleton — one shared instance per context — the Spring default.
3. Prototype — a new instance every time you ask the container.
4. Request and session scopes — web-aware, tied to HTTP lifecycle.
5. Wrong scope — shared mutable state across requests is a classic bug.
6. Default to singleton services with immutable or carefully synchronized state.

### Scene `wiring` (renderer: `wiring`)

1. How Spring finds and wires beans.
2. Component scanning picks up Stereotype annotations — Service, Repository, Controller.
3. Configuration classes with Bean methods define explicit beans.
4. Qualifiers disambiguate when multiple candidates share a type.
5. Profiles activate environment-specific beans — local, staging, prod.
6. Circular dependencies signal a design smell — break the cycle with redesign.

### Scene `testing` (renderer: `testing`)

1. DI pays off hardest in tests.
2. Unit tests construct the class with mocks — no container required.
3. Slice tests load a thin Spring context — web or data layer only.
4. Full ApplicationContext tests catch wiring mistakes — slower but valuable.
5. Avoid static singletons and ServiceLocator lookups — they fight DI.
6. If you cannot inject a fake, the design is fighting you.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — field injection everywhere — invisible dependencies, awkward tests.
3. Two — singleton beans holding request-specific mutable state.
4. Three — Autowired on concrete classes with no interface — tight coupling.
5. Also — ignoring constructor failure — missing beans explode at startup for good reason.
6. Fail fast at context refresh — never with a NullPointerException in production.

### Scene `interview` (renderer: `interview`)

1. Interview question — why prefer constructor injection?
2. Required dependencies are explicit and can be final.
3. The object is fully initialized after construction — no half-ready beans.
4. Unit tests pass mocks without Spring or reflection hacks.
5. Circular dependencies surface earlier — design problems become visible.
6. Spring and the community treat constructor injection as the default style.

### Scene `teaser` (renderer: `teaser`)

1. Wiring is clear — next is how projects start fast.
2. Episode Seventy-Three — Spring Boot Basics.
3. Starters, auto-configuration, configuration properties, and the executable jar.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **72** — *IoC and Dependency Injection*.
- **Series catalog:** Episode 72 ↔ handbook lesson 72 — *IoC and Dependency Injection*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy-One introduced Spring as a platform around an IoC container._
- **`title`** — starts from: _Episode Seventy-Two._
- **`ioc_vs_di`** — starts from: _IoC is the principle — DI is the mechanism._
- **`injection_styles`** — starts from: _Three injection styles you will see in Spring code._
- **`scopes`** — starts from: _Bean scopes control how many instances the container creates._
- **`wiring`** — starts from: _How Spring finds and wires beans._
- **`testing`** — starts from: _DI pays off hardest in tests._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why prefer constructor injection?_
- **`teaser`** — starts from: _Wiring is clear — next is how projects start fast._
