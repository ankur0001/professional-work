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

Production dashboard for the tolling service shows plaza 4 still using the staging merchant schedule after a "config-only" rollout. The JAR did not change. The ConfigMap did — except the pod still mounts an old volume because the Deployment annotation never bounced. A Secret for the DB password rotated in the cluster store but the process environment was set once at start. External configuration is not a file format. It is the live story of what the running process sees — and when it last read it.

Boot's externalized configuration loads many sources into the Environment with a documented precedence: command-line arguments, Java system properties, OS environment variables, profile-specific application files outside the jar, profile-specific files inside the jar, then non-profile defaults — simplified, but directionally higher wins. Kubernetes ConfigMaps and Secrets usually appear as mounted files or env vars; they only affect Spring after the process reads them at startup (or via a refresh mechanism you deliberately add). "We updated the ConfigMap" is not the same sentence as "the JVM bound new values."

```yaml
# k8s ConfigMap data mounted at /config/application.yml
tolling:
  schedule:
    merchant-id: toll-prod-42
spring:
  datasource:
    url: jdbc:postgresql://toll-db/prod
```

```yaml
# Deployment fragment
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    metadata:
      annotations:
        checksum/config: "replace-on-configmap-change"
    spec:
      containers:
        - name: tolling
          envFrom:
            - secretRef:
                name: tolling-db
          volumeMounts:
            - name: config
              mountPath: /config
          args: ["--spring.config.additional-location=file:/config/"]
```

Walk the deploy fragment. `envFrom.secretRef` injects Secret keys as environment variables — typically `SPRING_DATASOURCE_PASSWORD` via relaxed binding if named that way. `volumeMounts` places the ConfigMap file on disk at `/config`. `args` with `--spring.config.additional-location=file:/config/` tells Boot to load application documents from that directory in addition to the classpath jar. The `checksum/config` annotation is an ops pattern: change the ConfigMap, change the checksum, Kubernetes rolls pods so processes restart and re-read files. Without that roll, new file bytes on a mount may exist while beans still hold old constructor-captured values.

Runtime at process start. Boot builds the Environment, adds property sources for system props, env vars, additional config locations, and packaged `application.yml`. `tolling.schedule.merchant-id` binds into your `@ConfigurationProperties`. Env vars from the Secret populate datasource password. A leftover debug flag in container `args` such as `--tolling.schedule.merchant-id=toll-staging-7` outranks the ConfigMap file — same staging-merchant bug, different source. Precedence charts are how you explain that without guessing.

Failure mode symptoms from the plaza 4 incident: ConfigMap in the cluster shows `toll-prod-42`; running pod still prices with staging merchant. Checklist: `kubectl describe pod` for mount and age; exec in and `cat /config/application.yml` — is the new file even there?; hit a secured actuator `env` for the property's active source; confirm Deployment rolled after ConfigMap change; search container args for overriding CLI properties. Secret rotation without restart: DB connections start failing with auth errors after password invalidate, while the app still holds the old password string — symptom is connection pool exhaustion and authentication failures, not a Spring bind exception.

Trade-offs. External config lets one artifact ride many environments; it shifts failure modes into ops plumbing (mounts, rolls, precedence). Baking config into the jar is simpler to reason about and worse for secret rotation and per-cluster overlays. Spring Cloud Config or refresh scopes can hot-reload some properties — useful and complex; do not assume file watchers exist in plain Boot. Prefer failing startup on missing required secrets over defaulting production passwords.

Precedence worth memorizing for tolling on-call, short form: command-line args and system properties beat OS environment variables; those beat profile-specific files outside the jar; those beat packaged `application-prod.yml`; those beat packaged defaults. A ConfigMap mounted as a file competes in the "file location" tier you configured with `additional-location`; a ConfigMap projected as env vars competes in the env tier. Knowing which projection your Deployment uses tells you which tier to inspect first when plaza 4 disagrees with git.

Misconception unique to external configuration: "Putting config in a ConfigMap automatically hot-reloads the Spring Environment." It does not. Mount updates may update files on disk; beans already constructed keep their fields until restart or a refresh implementation.

Tolling config finally matches prod after the roll. At 02:10 the seaport integration that shares the platform pages on-call: traffic dies, and the first question is whether the process is alive, the DB is up, or the disk is full — preferably with one curl, not a JVM attach.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 23 (*External Configuration*).
