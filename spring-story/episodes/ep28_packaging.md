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

Profiles decide how the app behaves. Packaging decides what you actually copy to a server or container image — and Boot's answer is usually an executable JAR, not a hand-assembled WAR dropped into someone else's Tomcat.

Old enterprise delivery meant: build a WAR, install or allocate an application server, configure datasources in the server, deploy the WAR, hope versions of the server APIs matched. Horizontal scale meant more server installs. Local parity with production was wishful. Boot's bet is different: the application ships its dependencies and an embedded server; the unit of deployment is the process.

So what does the build produce, what does the JAR contain, and how does `java -jar` know how to start Spring?

The Spring Boot Maven Plugin (and the Gradle Boot plugin) repackage your project into an executable fat JAR — sometimes called an uber JAR. Inside, you will find your classes, a nested `BOOT-INF/lib` with dependency jars, `BOOT-INF/classes` for application classes and `application.yml`, and Boot loader classes at the root that understand that layout. The manifest points at `JarLauncher` (or a related launcher), which sets up a classloader for nested jars and then invokes your `main` — typically `SpringApplication.run`.

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-maven-plugin</artifactId>
    </plugin>
  </plugins>
</build>
```

```bash
./mvnw -DskipTests package
java -jar target/orders-0.0.1-SNAPSHOT.jar
```

Run `jar tf target/orders-*.jar | head` and read the layout: `BOOT-INF/`, `org/springframework/boot/loader/`, a `META-INF/MANIFEST.MF` with `Main-Class` and `Start-Class`. `Start-Class` is your `@SpringBootApplication` type. The loader's `Main-Class` boots the nested world. That is why a plain `jar` tool double-click mental model fails — this is a Boot-specific layout, not a flat classpath zip.

WARs still exist. You can package a WAR for an external servlet container when a platform requires it. Many cloud-native teams still prefer the executable JAR (or a container image whose entrypoint runs that JAR) because the server version travels with the app. Layered JARs help Docker caching: dependencies in one layer, application classes in another, so rebuilds ship thinner diffs.

```dockerfile
FROM eclipse-temurin:21-jre
COPY target/orders-*.jar /app/orders.jar
ENTRYPOINT ["java","-jar","/app/orders.jar"]
```

DevTools should not ride along in that production JAR — packaging is where optional scopes prove their worth. Actuator, external config, and profiles all assume you can start this single artifact with different Environment inputs.

The misconception is "fat JAR means classpath hell forever." Nested jars are isolated by Boot's launcher; you still manage versions through the BOM. Another misconception is treating the plugin as optional decoration — without repackaging, `java -jar` on a thin JAR will not find dependencies. A third is editing files inside the built JAR on the server instead of using external configuration; that path fights immutability and auditability.

You now have a process that starts, configures itself, and can be probed. The next pain shows up the moment HTTP enters the picture: a request hits the embedded server — who receives it first inside Spring, and how does it find the right controller method?

That front-controller story is the DispatcherServlet — and with it, Phase Three.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 28 (*Packaging*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
