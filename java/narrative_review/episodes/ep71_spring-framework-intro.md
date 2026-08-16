# Episode 71 — Spring Framework Intro

| Field | Value |
|---|---|
| Episode | 71 |
| Title | Spring Framework Intro |
| Catalog handbook column | 71 |
| Narration source script | `make_episode_71.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy closed behavioral patterns — Strategy, Observer, and Command.
2. Patterns name design ideas — Spring turns many of those ideas into a production platform.
3. Most Java services today start as a Spring application, not a raw main method.
4. Spring is not one jar — it is a family of projects around a core container.
5. Understanding the container unlocks Boot, MVC, Data, Security, and Cloud.
6. Today — what Spring is, why it won, the module map, and the mental model.

### Scene `title` (renderer: `title`)

1. Episode Seventy-One.
2. Spring Framework Intro.

### Scene `what_spring` (renderer: `what_spring`)

1. Spring is an application framework centered on inversion of control.
2. You declare components — Spring wires their dependencies and manages lifecycle.
3. The ApplicationContext is the runtime heart — beans live inside it.
4. Around the core sit modules for web, data access, messaging, and testing.
5. Spring Boot sits on top — opinionated defaults that start projects faster.
6. Think platform, not library — Spring shapes how the whole application runs.

### Scene `why_won` (renderer: `why_won`)

1. Why Spring became the default for enterprise Java.
2. It replaced heavyweight EJB ceremony with plain objects and annotations.
3. Dependency injection made code testable — swap collaborators in unit tests.
4. A huge ecosystem — Boot starters, Data, Security, Cloud — compounds the value.
5. Consistency across teams — shared conventions lower onboarding cost.
6. Alternatives exist — Quarkus, Micronaut — but Spring remains the interview baseline.

### Scene `module_map` (renderer: `module_map`)

1. A practical Spring module map for interviews.
2. spring-core and spring-context — container, beans, events.
3. spring-web and spring-webmvc — HTTP, REST controllers, filters.
4. spring-data and spring-tx — repositories and transactions.
5. spring-security — authentication and authorization filters.
6. Spring Boot stitches these with auto-configuration and an embedded server.

### Scene `mental_model` (renderer: `mental_model`)

1. Carry this mental model into every Spring conversation.
2. Your code defines beans — Spring creates and injects them.
3. Configuration is code or annotations — not a giant XML file anymore.
4. The context starts, beans initialize, then your application serves traffic.
5. Cross-cutting concerns — transactions, security, metrics — ride on proxies and AOP.
6. When something fails — ask which bean, which config, which phase of startup.

### Scene `boot_preview` (renderer: `boot_preview`)

1. Spring Boot preview — what changes day to day.
2. starters pull curated dependency sets — web, data-jpa, validation.
3. auto-configuration turns classpath signals into ready beans.
4. application.properties or yaml externalizes environment settings.
5. embedded Tomcat or Netty means java -jar is enough to run.
6. Episode Seventy-Three goes deep on Boot — first we nail IoC next.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — treating Spring as magic — skip the container mental model.
3. Two — putting business logic in controllers instead of services.
4. Three — assuming Boot auto-config always matches production needs.
5. Also — learning annotations by rote without knowing which module owns them.
6. Name the container first — features second.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is the Spring Framework?
2. An IoC container plus a modular ecosystem for enterprise Java apps.
3. It manages bean lifecycle and wires dependencies for you.
4. Modules cover web, data, security, messaging, and testing.
5. Spring Boot adds conventions and auto-configuration on top.
6. The value is testability, consistency, and a battle-tested ecosystem.

### Scene `teaser` (renderer: `teaser`)

1. The container is the core idea — next we open it.
2. Episode Seventy-Two — IoC and Dependency Injection.
3. Beans, injection styles, scopes, and how Spring actually wires your graph.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **71** — *Spring Framework Intro*.
- **Series catalog:** Episode 71 ↔ handbook lesson 71 — *Spring Framework Intro*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy closed behavioral patterns — Strategy, Observer, and Command._
- **`title`** — starts from: _Episode Seventy-One._
- **`what_spring`** — starts from: _Spring is an application framework centered on inversion of control._
- **`why_won`** — starts from: _Why Spring became the default for enterprise Java._
- **`module_map`** — starts from: _A practical Spring module map for interviews._
- **`mental_model`** — starts from: _Carry this mental model into every Spring conversation._
- **`boot_preview`** — starts from: _Spring Boot preview — what changes day to day._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is the Spring Framework?_
- **`teaser`** — starts from: _The container is the core idea — next we open it._
