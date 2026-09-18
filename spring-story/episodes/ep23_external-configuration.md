# Episode 23 — External Configuration

| Field | Value |
|---|---|
| Episode | 23 |
| Title | External Configuration |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 23 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You can bind typed properties. The deployment question remains: the same artifact must behave differently in a laptop, a staging cluster, and production — without rebuilding for each password.

Bake a production database URL into `application.yml` inside the JAR and you have created a security incident and a promotion nightmare. Copy entire YAML files per environment by hand and you will merge the wrong file on a Friday deploy. Teams need one build, many runtime configs, and a clear winner when two sources define the same key.

So what owns the merge order, and how do profile-specific files and environment variables override packaged defaults?

Boot builds an `Environment` from an ordered set of property sources. Packaged `application.properties` / `application.yml` provide defaults. Profile-specific documents like `application-prod.yml` layer on when that profile is active. Outside the JAR, `./config/` and the working directory can supply replacements. OS environment variables and JVM system properties override file values. Command-line arguments usually win last among common sources. Exact precedence has a documented ladder; the teaching point is simpler: external beats packaged, and more specific beats more general.

```yaml
# application.yml — safe defaults shipped in the JAR
server:
  port: 8080
payments:
  base-url: http://localhost:9090
  timeout: 5s
```

```yaml
# application-prod.yml — activated with spring.profiles.active=prod
payments:
  base-url: https://payments.prod.internal/api
  timeout: 2s
```

```bash
# runtime overrides — no rebuild
export PAYMENTS_BASE_URL=https://payments.prod.internal/api
export PAYMENTS_TIMEOUT=2s
java -jar orders.jar --spring.profiles.active=prod --server.port=8081
```

Walk a single key. `payments.base-url` starts as the local default in `application.yml`. Activate `prod` and the profile file replaces it. Set `PAYMENTS_BASE_URL` in the process environment and that value overrides the file. Pass `--payments.base-url=...` on the command line and you can override again for a one-off. Your `@ConfigurationProperties` object sees the winning value after the Environment is prepared — before most beans initialize.

Profiles are not only YAML suffixes. `@Profile("prod")` beans participate only when that profile is active. Boot also supports `spring.config.import` for additional documents and, in Cloud setups, external config servers — same Environment idea, more sources. For this episode, master local files, env vars, and the habit of keeping secrets out of the repo.

People confuse "external configuration" with "edit the JAR after build." Prefer env vars or mounted config files in containers. Another mistake is assuming YAML maps one-to-one with env var names without relaxed binding — Boot maps `PAYMENTS_BASE_URL` to `payments.base-url`, but inventing arbitrary env names that do not follow the rules will silently miss the property. A third is activating overlapping profiles until nobody can state which file supplied the effective URL — print or actuate env views in non-prod to verify.

Once config can differ per environment, operators still need a way to ask a running process questions: is it up, is the database reachable, what build is this?

That operational door is Actuator.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 23 (*External Configuration*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
