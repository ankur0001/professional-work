# Episode 28 — Packaging

| Field | Value |
|---|---|
| Episode | 28 |
| Title | Packaging |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 28 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Before: tram timetable API image rebuild after a one-line Java change re-uploads ~170MB because the fat jar is one opaque layer. After: layered jar — dependencies in a lower Docker layer, application classes on top — and the same one-line change pushes a few megabytes. Cold starts in the cluster stop waiting on registry bandwidth every commit. Packaging is not a footnote after Boot; it is how the bike-adjacent tram service's deploy loop feels.

Boot's packaging story centers on the executable "fat" jar: your classes plus dependencies plus a launcher (`JarLauncher`) that understands nested jars under `BOOT-INF`. `spring-boot-maven-plugin` / Gradle plugin builds it. Layered jars split that archive into named layers (dependencies, spring-boot-loader, snapshot-dependencies, application) so container tools can cache stable layers. Same runtime model; different layout for Docker's cache.

```xml
<plugin>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-maven-plugin</artifactId>
  <configuration>
    <layers>
      <enabled>true</enabled>
    </layers>
  </configuration>
</plugin>
```

```dockerfile
FROM eclipse-temurin:21-jre as builder
WORKDIR /app
COPY target/tram-timetable.jar app.jar
RUN java -Djarmode=tools -jar app.jar extract --layers --destination extracted

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /app/extracted/dependencies/ ./
COPY --from=builder /app/extracted/spring-boot-loader/ ./
COPY --from=builder /app/extracted/snapshot-dependencies/ ./
COPY --from=builder /app/extracted/application/ ./
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

Walk the Dockerfile. Builder stage copies the fat jar and runs Boot's layertools extract — producing directories per layer. Final image copies **dependencies** first (changes rarely), then loader, then snapshot deps, then **application** (changes every commit). Docker caches unchanged lower layers; only the application layer invalidates on a one-line Java edit. `ENTRYPOINT` still uses `JarLauncher`, which expects Boot's layout — you are not switching to `java -cp` manually. Order of `COPY` lines matters: put the most stable layers first.

Runtime launch. `JarLauncher` reads `BOOT-INF` layout, builds a classloader over nested dependency jars in `BOOT-INF/lib`, and invokes your `main`. Layer extract does not change that model — it only rearranges files for Docker cache. A classic thin jar plus external libs works too, but you own the classpath and entrypoint. Fat jar wins on "java -jar works." Layered fat jar wins on "java -jar works and containers cache." WAR deployment to an external Tomcat remains possible for shops that mandate it; you trade embedded-server simplicity for ops-standard application servers.

Failure mode symptoms before layering: CI shows image push sizes ~equal to full jar every build; nodes pull slowly; deploys lag commits by minutes of bandwidth. After enabling layers but copying the fat jar as a single `COPY app.jar` in the final image, you gain nothing — layers must be extracted and copied separately. Another failure: tools that assume a plain jar with classes at the root (`jar tf` habits, some security scanners, naive classpaths) break on nested `BOOT-INF/lib` until they speak Boot's launcher. Symptom: `ClassNotFoundException` when someone runs `java -cp tram-timetable.jar com.tram.TimetableApp` instead of `java -jar` / JarLauncher.

Trade-offs. Fat jars optimize operator simplicity and local runs; large images and poor Docker cache are the cost. Layered jars add build/Dockerfile complexity and pay back on frequent deploys with stable dependencies. Native images and custom classpaths are further optimizations with steeper constraints — not required to fix the 170MB push problem. Keep the plugin's layer enablement aligned with a Dockerfile that actually uses extract output.

Verify locally before trusting CI numbers: build the layered jar, run the extract command from the Dockerfile, and `du -sh` each extracted directory. Dependencies should dwarf `application`. If `application` is huge, you may be bundling frontend assets or fat test data into the main jar — fix that separately. Layering helps cache; it does not shrink what you put in the application layer.

Misconception unique to packaging: "A Boot fat jar is a normal zip of .class files at the root like a plain Maven jar, so `jar tf` habits transfer unchanged." Nested `BOOT-INF/lib` jars are not flat on the launcher classpath the way a shaded uber-jar merges classes. Tools that expect a plain classpath layout break until they speak Boot's launcher.

Timetable images shrink on the wire. The API still has to answer `GET` requests for stop times — and that means understanding what happens after Tomcat accepts a socket: the DispatcherServlet pipeline that turns a URL into a controller method. Packaging got the process started; request mapping decides whether the timetable responds.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 28 (*Packaging*).
