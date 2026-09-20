# Episode 25 — DevTools

| Field | Value |
|---|---|
| Episode | 25 |
| Title | DevTools |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 25 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

LiveReload flickers on the museum ticket purchase page for the third time in a minute. A designer changed CSS. DevTools restarted the context. The WebSocket reload hits before Thymeleaf finishes compiling. Another save. Another restart. The developer disables LiveReload in frustration, then wonders why classpath changes no longer restart anything. DevTools is a power tool for local feedback — not a production dependency, and not magic that understands design-tool save storms on a ticket UI.

Spring Boot DevTools watches the classpath for changes, triggers a fast application restart using two classloaders (base jars stay loaded; project classes reload), and can push browser LiveReload events. It disables some caching for templates in development. Exclude the dependency from production builds — optional Maven dependency and `runtimeOnly` patterns exist so the fat jar you ship does not carry the restart agent.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-devtools</artifactId>
  <optional>true</optional>
</dependency>
```

```yaml
# application-local.yml
spring:
  thymeleaf:
    cache: false
  devtools:
    livereload:
      enabled: true
    restart:
      additional-exclude: static/**,public/**
```

Walk the local config. `thymeleaf.cache: false` ensures template edits are visible without relying only on restart. `livereload.enabled: true` opens the LiveReload server that browsers (with an extension or injected script) listen to. `restart.additional-exclude: static/**,public/**` is the museum fix: CSS and static asset saves should *not* trigger a full application restart — only a browser refresh if LiveReload remains on. Java and template class changes still restart the context. `<optional>true</optional>` helps keep DevTools from being pulled transitively into downstream modules.

Runtime while building the museum UI. Save a Java controller → DevTools detects classpath change → restart classloader discards project classes and rebuilds the ApplicationContext faster than a cold JVM start, but still re-runs bean creation, `@PostConstruct`, and connection setup. Save a static CSS file under an excluded path → no restart; LiveReload can refresh the browser alone. Leave static files inside the restart trigger set and every CSS save pays a full context reboot — the flicker loop that burned the designer. Remote DevTools exists for updating a remote app; treat it as a security surface requiring secrets, not a default for shared environments.

Failure mode symptoms: context restart thrash — logs show repeated "Restarting application" on every autosave from an IDE or design tool writing static files; browser flashes white; in-progress form state on the ticket page resets; local H2 database re-creates empty because the embedded bean was rebuilt. Another failure: DevTools accidentally on the production classpath — unexpected restart behavior or LiveReload port open; always verify the production image's dependency tree. Disabling LiveReload in the browser extension while leaving restart triggers wide still restarts on CSS if excludes are wrong — people blame LiveReload for restart cost when the restart watcher is the real bill.

Trade-offs. DevTools shortens the edit-refresh loop for server-side UI work and small API tweaks; it is not a substitute for JRebel/HotSwap when you need true method replacement without resetting singletons. Stateful beans, in-memory databases, and warm caches reset on every restart — externalize local Postgres if you need durable local data across restarts. Turn DevTools off when diagnosing timing bugs that only appear under steady state.

Classloader split, briefly: the "base" loader holds dependency jars that rarely change; the "restart" loader holds your `target/classes`. On restart, only the restart loader is discarded and rebuilt, which is why DevTools feels faster than killing the JVM — Hibernate jars do not reload. Your `@Service` singletons do. Museum ticket sessions stored only in an in-memory bean vanish; designer CSS excludes avoid paying that tax for static edits. Knowing which loader owns a class explains why a dependency bump still needs a full stop/start while a controller tweak does not.

Misconception unique to DevTools: "DevTools restart is the same as hot-swap / HotSwap agent / JRebel class redefinition." It is a restart of the application context with a clever classloader split — faster than killing the JVM, slower and broader than swapping one method body. Stateful beans reset. In-memory H2 re-creates unless you externalize it.

The ticket UI iteration speed is acceptable again. At 02:00 the ferry-booking on-call channel pastes four log lines from four pods with no shared request id — DevTools will not help. Logging strategy and correlation will.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 25 (*DevTools*).
