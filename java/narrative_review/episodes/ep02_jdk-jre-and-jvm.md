# Episode 02 — JDK, JRE, and JVM

| Field | Value |
|---|---|
| Episode | 02 |
| Title | JDK, JRE, and JVM |
| Catalog handbook column | 2 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Quick continuity from Episode One.
2. We learned why Java survives — bytecode, the JVM, Write Once Run Anywhere.
3. But on day one, beginners slam into three names that sound interchangeable.
4. JDK. JRE. JVM.
5. Install Java — which one did you actually install?
6. Today we separate those layers clearly — with a diagram in your head and commands on screen.
7. Once this clicks, Docker images, CI builds, and production incidents make more sense.

### Scene `title` (renderer: `title`)

1. Episode Two.
2. JDK, JRE, and JVM — the three layers of the Java platform.
3. By the end you'll know who compiles, who launches, and who executes.

### Scene `layers` (renderer: `layers`)

1. Picture three nested boxes.
2. At the bottom — the JVM. The engine. It executes bytecode.
3. Wrap that with the JRE idea — runtime libraries, launchers, the standard APIs your app calls at run time.
4. On top — the JDK. Everything in the runtime plus developer tools.
5. javac to compile. jar to package. jlink to trim runtimes. jcmd, jmap, jfr for diagnostics.
6. Mnemonic that actually helps: JDK for develop. JRE for run. JVM is the engine inside.
7. Modern distributions often ship a JDK by default — but the conceptual split still matters in containers and CI.

### Scene `jdk_tools` (renderer: `jdk_tools`)

1. Zoom into the JDK — this is your developer toolkit.
2. javac turns .java source into .class bytecode.
3. jar bundles classes and resources. jdeps analyzes dependencies.
4. jlink builds custom runtimes — smaller than shipping a full JDK when you only need java.base plus a few modules.
5. jcmd attaches to running processes. jmap and jfr help you debug memory and latency in production.
6. If you write code — or troubleshoot live services — you want JDK tools available somewhere in your pipeline.
7. Production containers sometimes carry only a runtime image — but then you need another path for thread dumps and flight recordings.

### Scene `jre_run` (renderer: `jre_run`)

1. The JRE is the runtime layer — what you need to launch a Java process.
2. Standard libraries. The java launcher. Core APIs like java.lang and java.util.
3. Historically you could install a standalone JRE without compilers.
4. Today many teams ship a JDK everywhere for consistency — or a slim jlink image that is runtime-shaped.
5. The JRE concept still explains why a container might omit javac — and why missing diagnostics hurts at three a.m.
6. Runtime-only packaging saves disk — until you need jcmd and it is not there.

### Scene `jvm_engine` (renderer: `jvm_engine`)

1. And here is the JVM — where bytecode becomes behavior.
2. It loads class files, verifies bytecode safety, allocates heap and stacks, runs garbage collection.
3. HotSpot is the common implementation — interpreter first, then JIT for hot methods.
4. Class loaders, bytecode verifier, linker, interpreter, C1 and C2 compilers — the pipeline from Episode One, now with names.
5. Other JVMs exist — OpenJ9, GraalVM — with different tradeoffs for startup, memory, and native image.
6. Same bytecode contract. Different engines. That is why we say JVM as specification and HotSpot as one implementation.

### Scene `flow` (renderer: `flow`)

1. Follow the arrows from source to running process.
2. Your .java file goes to javac — a JDK tool.
3. Out comes HelloWorld.class — platform-neutral bytecode.
4. The java launcher starts a JVM process, creates runtime data areas, loads the main class, calls main.
5. Behind the scenes: class loading, static initialization, then your println.
6. Build systems compile with a JDK. Deployment platforms launch a JVM with your artifact and flags.
7. Spring Boot fat JARs add a launcher layer — but the story ends the same way: JVM executes bytecode.
8. Let's make that concrete with commands you'd run every day.
```bash
java -version
javac -version
javac PaymentCalculator.java
java PaymentCalculator
jar --describe-module --file app.jar
jcmd <pid> VM.version
```

9. java -version tells you what runtime you're holding — vendor, version, sometimes LTS.
10. javac -version should match your build JDK — mismatch is a classic incident seed.
11. Compile, then run — notice you pass the class name to java, not the .class filename.
12. jar --describe-module inspects modular JARs. jcmd VM.version attaches to a live PID when serviceability tools are present.

### Scene `memory` (renderer: `memory`)

1. Now the production gotcha nobody warns you about on day one.
2. When ops says set heap to four gigabytes — that is not the whole process.
3. The JVM also allocates metaspace for class metadata, thread stacks, code cache for JIT code, direct memory for NIO, native structures for GC.
4. Container limit equals -Xmx is a famous failure mode.
5. You starve metaspace, threads, or direct buffers — and the process dies with errors that blame the wrong layer.
6. Always leave headroom beyond heap. Account for total RSS, not just -Xmx on a slide.
7. Episode One showed stack versus heap — today add non-heap as first-class in your mental model.

### Scene `deeper` (renderer: `deeper`)

1. Spring Boot executable JAR — nested loader — still ends at JVM executing bytecode.
2. CI pipeline — compile stage needs JDK. Run stage may use slimmer runtime if diagnostics elsewhere.
3. Eclipse Temurin, Amazon Corretto, Azul Zulu — distributions share specification, differ in support and patches.
4. LTS versions — eleven, seventeen, twenty-one — enterprises standardize on LTS for support windows.
5. javac release flag — compile to older bytecode version while using newer JDK — backward compatibility.
6. Toolchain in Gradle and Maven — enforce JDK version across team — no more works on my machine Java version drift.
7. Flight Recorder — jcmd JFR.start — low overhead profiling in production when JDK present.
8. Native memory tracking — NMT — diagnose direct buffer leaks beyond heap dumps.

### Scene `mistakes` (renderer: `mistakes`)

1. Three mistakes I want burned into your brain.
2. Mistake one — shipping a full JDK into every tiny container when a jlink runtime would suffice — image bloat and attack surface.
3. Mistake two — CI compiles with Java twenty-one, production runs seventeen — subtle bytecode or API differences, or worse, silent assumptions.
4. Mistake three — treating the JVM as a black box until GC pauses or OOM kills the pod.
5. Bonus trap — assuming public types on the classpath are all equally reachable once modules enter — preview of Episode Twenty.
6. Know your layers. Version them together. Instrument the engine.

### Scene `interview` (renderer: `interview`)

1. Interview time — say this like someone who ships Java services.
2. Question: What's the difference between JDK, JRE, and JVM?
3. JVM executes bytecode — class loading, verification, JIT, GC.
4. JRE is the runtime environment — libraries and launcher to run applications.
5. JDK is the development kit — JRE plus compilers and diagnostic tools like javac, jar, jcmd.
6. Bonus line: container memory must include heap and non-heap; -Xmx alone is not the process budget.
7. If you can point to the three boxes while you answer — you're ahead of candidates who only memorized acronyms.

### Scene `container` (renderer: `container`)

1. Docker layer — FROM eclipse-temurin:21-jre — JRE-shaped runtime image.
2. Copy JAR. ENTRYPOINT java -jar app.jar — launcher starts JVM inside container.
3. Kubernetes limits — memory limit must exceed -Xmx — we covered non-heap headroom.
4. Liveness probe failing? Maybe OOM killed process — check exit code 137.
5. Readiness probe — JVM still warming JIT — first requests slower — not wrong, just warming.
6. Sidecar with JDK for diagnostics while main container runs JRE — pattern some platforms use.
7. Golden images — platform team ships approved Java version and flags — services inherit consistency.
8. Upgrade Java LTS — test GC, TLS, serialization, native libs — JDK version changes more than syntax.

### Scene `connect` (renderer: `connect`)

1. Episode One bytecode story now has names for each box in the diagram.
2. Episode Three opens Java files — you'll know javac created the class the JVM loads.
3. Every later episode assumes you can explain JDK versus JVM in one calm breath.

### Scene `summary` (renderer: `summary`)

1. Let's land the plane.
2. JDK develops. JRE runs. JVM executes bytecode.
3. javac and java are different doors into the same platform story.
4. HotSpot is the engine most of us run — with real memory areas beyond heap.
5. Match JDK versions across build and runtime. Leave container headroom.
6. Episode One gave you why Java is portable — Episode Two names the machinery you install.

### Scene `teaser` (renderer: `teaser`)

1. The three names finally line up with the picture.
2. Next — open a Java file and read it like a map.
3. Episode Three — Java Program Structure.
4. Packages, classes, main — what every line is doing.
5. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **2** — *JDK, JRE, and JVM*.
- **Series catalog:** Episode 02 ↔ handbook lesson 2 — *JDK, JRE, and JVM*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Handbook concepts reused (from recovered Lesson 2 excerpt)

- - The JDK, JRE, and JVM define the Java platform layers. The JVM executes bytecode, the JRE supplies runtime libraries and launchers, and the JDK adds development tools such as javac, jar, jlink, jcmd, jmap, and jfr.
- - javac compiles .java files into .class files. The launcher starts a JVM process, creates runtime data areas, loads the main class, initializes dependencies, and begins bytecode execution.
- - HotSpot is the most common JVM implementation and includes class loading, bytecode interpretation, C1/C2 JIT compilers, garbage collectors, serviceability agents, Java Flight Recorder, and native integration. Other implementations may optimize startup, memor
- - The runtime allocates heap, metaspace, thread stacks, code cache, GC structures, direct memory, and native segments. Container deployments must account for total process memory, not just -Xmx.
- - Build systems use a JDK to compile and package artifacts. Runtime platforms launch a JVM using the artifact and configuration. In Spring Boot, the executable JAR embeds dependencies and starts through a launcher before reaching application code.
- - Runtime packaging affects disk and memory footprint. A full JDK image is larger than a custom jlink image. At runtime, JVM memory includes heap and non-heap areas, so container limits must leave headroom beyond Java heap.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 2).

### Scene ↔ curriculum intent

- **`hook`** — continuity + three-name confusion
- **`title`** — episode promise
- **`layers`** — JDK/JRE/JVM nested model
- **`jdk_tools`** — developer toolchain
- **`jre_run`** — runtime layer
- **`jvm_engine`** — bytecode execution engine
- **`flow`** — compile-run pipeline + bash walkthrough
- **`memory`** — heap vs non-heap in containers
- **`mistakes`** — common mistakes
- **`interview`** — JDK vs JRE vs JVM interview
- **`summary`** — revision
- **`teaser`** — bridge to Episode 03

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
