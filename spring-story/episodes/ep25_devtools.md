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

Actuator helps you observe a running process. DevTools helps you survive the hours before that process is worth observing — the local edit-compile-restart loop.

Picture a developer changing a single `@GetMapping` path. Without help, they stop the JVM, rebuild, start again, wait for context refresh, then click the browser. Do that sixty times a day and the feedback loop becomes the product. Some teams bolt on external reloaders with uneven Spring awareness. Others just live with the pain and ship slower.

Is there a Boot-aware development mode that restarts quickly when application classes change — and stays out of production classpaths?

Spring Boot DevTools is that mode. Add `spring-boot-devtools` with a development-only dependency scope. On the classpath in local runs, it watches application classes and resources. When it detects a change, it performs a restart that reloads the application classloader while keeping a base classloader for third-party jars. That split is why restart is faster than a cold JVM launch: Boot does not reload Spring itself from scratch every time — it reloads your code.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-devtools</artifactId>
  <optional>true</optional>
</dependency>
```

In Gradle, use a development-only configuration so the jar never ships to production. Runtime behavior: save a controller, trigger a compile (IDE auto-build or build tool), DevTools notices, logs a restart, and the context comes back with the new mapping. Static resources can update with live reload in the browser when the LiveReload server is enabled. Property defaults also shift slightly under DevTools — for example template caches disable so UI edits show up — which is convenient locally and wrong for production perf tests.

```yaml
# application-local.yml — only for laptop profiles
spring:
  devtools:
    restart:
      additional-paths: src/main/java
      exclude: static/**,public/**
```

Tune excludes when generated files or static assets cause noisy restarts. Disable restart entirely if you are debugging a lifecycle issue and need a stable JVM. Remote DevTools exists for specialized setups; most teams only need local restart and should not expose remote restart over the network casually.

The wrong belief is "DevTools belongs in the production fat jar." It does not. Keep it optional / development-only, and verify your packaging excludes it. Another wrong belief is that DevTools replaces proper tests — it speeds manual feedback; it does not prove correctness. A third is expecting hot-swap of every change: structural signature changes still need restart; DevTools accelerates that restart, it does not turn Java into a dynamic scripting language.

Faster restarts still leave you staring at console noise. When something fails, you need controlled, environment-aware logging — levels, loggers, and Boot's logging defaults — not a wall of undifferentiated INFO.

That is the logging lesson next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 25 (*DevTools*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
