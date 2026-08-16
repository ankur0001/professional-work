# Episode 02 — JDK, JRE, and JVM

| Field | Value |
|---|---|
| Episode | 02 |
| Title | JDK, JRE, and JVM |
| Catalog handbook column | 2 |
| Narration source script | `make_episode_02.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. In Episode One, we learned why Java survived.
2. But beginners still mix three names — JDK, JRE, and JVM.
3. They are not the same thing.
4. Today we separate them — clearly — on screen.

### Scene `title` (renderer: `title`)

1. Episode Two.
2. JDK, JRE, and JVM — the three layers of the Java platform.

### Scene `layers` (renderer: `layers`)

1. Look at these three boxes.
2. At the top — the JDK. Your developer toolkit.
3. In the middle — the JRE. What you need to run Java apps.
4. At the bottom — the JVM. The engine that executes bytecode.
5. JDK for develop. JRE for run. JVM is the engine inside.

### Scene `jdk_tools` (renderer: `jdk_tools`)

1. Zoom into the JDK.
2. This is where javac lives — the compiler.
3. Also jar, jlink, jcmd, jmap, and Java Flight Recorder tools.
4. If you write code or debug production issues — you want the JDK.

### Scene `jre_run` (renderer: `jre_run`)

1. The JRE is the runtime layer.
2. Libraries, launchers, and everything needed to start a Java process.
3. It does not include the compiler.
4. Modern installs often ship a JDK — but the runtime idea still matters.

### Scene `jvm_engine` (renderer: `jvm_engine`)

1. And here is the JVM.
2. It loads class files, verifies bytecode, and runs your program.
3. HotSpot is the common implementation — interpreter, JIT, garbage collection.
4. Same bytecode contract. Different machines. Same result.

### Scene `flow` (renderer: `flow`)

1. Follow the arrows.
2. Your .java file goes into javac — that tool comes from the JDK.
3. Out comes a .class file — bytecode.
4. The java launcher starts a JVM process.
5. The JVM reads bytecode and runs it.
6. That is the full path — develop, package, execute.

### Scene `memory` (renderer: `memory`)

1. Now the production gotcha.
2. On screen — heap is only one slice of memory.
3. Also metaspace, thread stacks, code cache, and native memory.
4. If dash X m x equals your container limit — you leave no headroom.
5. Always leave room beyond the heap.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — shipping a full JDK into every tiny container when a slim runtime would do.
3. Two — compiling with Java twenty-one in CI, then running Java seventeen in production.
4. Three — treating the JVM as a black box until something breaks.

### Scene `interview` (renderer: `interview`)

1. Interview question — what's the difference between JDK, JRE, and JVM?
2. Point to the diagram.
3. JVM executes bytecode.
4. JRE provides the runtime to launch apps.
5. JDK adds compilers and diagnostics on top.
6. Answer that calmly — and you sound like you've shipped Java.

### Scene `teaser` (renderer: `teaser`)

1. Now the three names finally line up with the picture.
2. Next episode — Java program structure.
3. public class, main, packages — what every line is doing.
4. Episode Three. See you there.

_Total beats: **48** across **11** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **2** — *JDK, JRE, and JVM*.
- **Series catalog:** Episode 02 ↔ handbook lesson 2 — *JDK, JRE, and JVM*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 2 excerpt)

- - The JDK, JRE, and JVM define the Java platform layers. The JVM executes bytecode, the JRE supplies runtime libraries and launchers, and the JDK adds development tools such as javac, jar, jlink, jcmd, jmap, and jfr.
- - javac compiles .java files into .class files. The launcher starts a JVM process, creates runtime data areas, loads the main class, initializes dependencies, and begins bytecode execution.
- - HotSpot is the most common JVM implementation and includes class loading, bytecode interpretation, C1/C2 JIT compilers, garbage collectors, serviceability agents, Java Flight Recorder, and native integration. Other implementations may optimize startup, memor
- - The runtime allocates heap, metaspace, thread stacks, code cache, GC structures, direct memory, and native segments. Container deployments must account for total process memory, not just -Xmx.
- - Build systems use a JDK to compile and package artifacts. Runtime platforms launch a JVM using the artifact and configuration. In Spring Boot, the executable JAR embeds dependencies and starts through a launcher before reaching application code.
- - Runtime packaging affects disk and memory footprint. A full JDK image is larger than a custom jlink image. At runtime, JVM memory includes heap and non-heap areas, so container limits must leave headroom beyond Java heap.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 2).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _In Episode One, we learned why Java survived._
- **`title`** — starts from: _Episode Two._
- **`layers`** — starts from: _Look at these three boxes._
- **`jdk_tools`** — starts from: _Zoom into the JDK._
- **`jre_run`** — starts from: _The JRE is the runtime layer._
- **`jvm_engine`** — starts from: _And here is the JVM._
- **`flow`** — starts from: _Follow the arrows._
- **`memory`** — starts from: _Now the production gotcha._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what's the difference between JDK, JRE, and JVM?_
- **`teaser`** — starts from: _Now the three names finally line up with the picture._
