# Episode 73 — Spring Boot Basics

| Field | Value |
|---|---|
| Episode | 73 |
| Title | Spring Boot Basics |
| Catalog handbook column | 73 |
| Narration source script | `make_episode_73.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy-Two covered IoC, injection styles, and bean scopes.
2. Spring Boot is how most teams actually start a Spring application today.
3. Boot is still Spring — it adds conventions, starters, and auto-configuration.
4. The goal — a production-ready app with less XML and less boilerplate.
5. Misunderstanding Boot leads to fighting auto-config instead of using it.
6. Today — starters, auto-configuration, properties, actuators, and the fat jar.

### Scene `title` (renderer: `title`)

1. Episode Seventy-Three.
2. Spring Boot Basics.

### Scene `starters` (renderer: `starters`)

1. Starters are curated dependency descriptors.
2. spring-boot-starter-web pulls MVC, Tomcat, Jackson, and validation basics.
3. starter-data-jpa brings Hibernate and repository support.
4. starter-test lands JUnit, Mockito, AssertJ, and Spring Test.
5. You choose capabilities — Boot chooses compatible versions via the BOM.
6. Prefer official starters over hand-picking twenty transitive jars.

### Scene `auto_config` (renderer: `auto_config`)

1. Auto-configuration creates beans when conditions match.
2. Classpath present — DataSource auto-config may engage.
3. A user-defined bean of the same type usually wins — you can override.
4. ConditionalOnClass and ConditionalOnMissingBean drive the decisions.
5. debug equals true or ConditionEvaluationReport shows what matched.
6. Auto-config is opinionated defaults — not untouchable magic.

### Scene `properties` (renderer: `properties`)

1. Externalized configuration keeps code environment-agnostic.
2. application.properties or application.yaml hold defaults.
3. Profile-specific files — application-prod.yaml — override per environment.
4. Environment variables and command-line args outrank file values.
5. ConfigurationProperties maps typed settings into beans safely.
6. Never hardcode secrets — inject them from the environment or a vault.

### Scene `run_model` (renderer: `run_model`)

1. The Boot run model in practice.
2. SpringBootApplication enables scanning and auto-configuration.
3. SpringApplication.run boots the context and embedded server.
4. Executable jar packaging ships dependencies — java -jar app.jar.
5. Actuator exposes health, info, and metrics endpoints for operations.
6. Devtools and docker compose support speed local inner loops.

### Scene `customize` (renderer: `customize`)

1. Customization without abandoning Boot.
2. Define your own Bean when defaults are wrong — Boot backs off.
3. Exclude specific auto-config classes only with a clear reason.
4. Use application properties before writing custom configuration code.
5. Keep SpringBootApplication on a root package so scanning sees your code.
6. Read starter docs — each starter documents keys you can tune.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — excluding auto-config to fix a symptom — hide the real conflict.
3. Two — giant application.yaml with unused keys nobody understands.
4. Three — putting SpringBootApplication in a nested package — components missed.
5. Also — mixing Boot versions manually — always use the BOM managed set.
6. Work with Boot's conventions — override deliberately, not accidentally.

### Scene `interview` (renderer: `interview`)

1. Interview question — what does Spring Boot add on top of Spring?
2. Starters for curated dependencies and a managed BOM.
3. Auto-configuration that wires common stacks from the classpath.
4. Externalized config and production-ready Actuator endpoints.
5. Embedded servers and executable jars for simple deployment.
6. Same Spring container underneath — Boot accelerates the path to production.

### Scene `teaser` (renderer: `teaser`)

1. Boot starts the app — next we handle HTTP.
2. Episode Seventy-Four — Spring MVC and REST.
3. Controllers, request mapping, validation, and clean API design.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **73** — *Spring Boot Basics*.
- **Series catalog:** Episode 73 ↔ handbook lesson 73 — *Spring Boot Basics*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy-Two covered IoC, injection styles, and bean scopes._
- **`title`** — starts from: _Episode Seventy-Three._
- **`starters`** — starts from: _Starters are curated dependency descriptors._
- **`auto_config`** — starts from: _Auto-configuration creates beans when conditions match._
- **`properties`** — starts from: _Externalized configuration keeps code environment-agnostic._
- **`run_model`** — starts from: _The Boot run model in practice._
- **`customize`** — starts from: _Customization without abandoning Boot._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what does Spring Boot add on top of Spring?_
- **`teaser`** — starts from: _Boot starts the app — next we handle HTTP._
