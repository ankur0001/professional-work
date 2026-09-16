# Episode 02 — JDK, JRE, and JVM

| Field | Value |
|---|---|
| Episode | 02 |
| Title | JDK, JRE, and JVM |
| Catalog handbook column | 2 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode One ended on a confusion almost every beginner hits: someone says "install Java," and three acronyms appear — JDK, JRE, JVM — as if they were the same thing.

That confusion is not vocabulary trivia. We already know source becomes bytecode, and a JVM runs that bytecode. So if the JVM is the engine, what did you actually install when you typed a command and waited for a download?

Start from the moment you try to compile HelloWorld.

```bash
javac HelloWorld.java
java HelloWorld
```

If `javac` is missing, the first command fails. You can have a machine that runs Java applications and still be unable to compile anything. That failure splits the world into two jobs: building programs, and running them.

The toolkit that contains the compiler — and the other developer tools around it — is the JDK, the Java Development Kit. `javac` lives there. So do tools such as `jar`, `jlink`, and diagnostics you will meet later. When a tutorial says "install the JDK," it means: give yourself the toolbox needed to create Java software.

Compiling is only half the path. After `javac` produces `HelloWorld.class`, the second command starts a process that can load bytecode and execute it. That process is centered on the JVM — commonly HotSpot. The JVM is the engine. It does not care that you wrote the source this morning. It cares that valid bytecode arrived and needs to run.

So where does the JRE fit?

Historically, the JRE — Java Runtime Environment — named the runtime idea: the libraries and launcher you need to run an application without shipping the full developer toolbox. In older distributions, you could install a JRE on a server that should only run apps, not compile them. In modern JDK distributions the lines are blurrier, because a JDK download usually includes what you need to run as well as compile. The useful distinction remains: development tools versus the runtime that executes bytecode.

Hold the layers lightly: JDK is the toolbox, the runtime is where the program lives, the JVM is the engine inside. You write `HelloWorld.java`. The JDK's `javac` turns it into bytecode. You run `java HelloWorld`. That launcher starts a JVM, the JVM loads the class, finds `main`, and executes the print. Same story as Episode One — now with clearer labels.

Once the happy path is clear, production life introduces sharper mistakes.

First: calling everything "the JDK," including the running process. A production container may be executing a JVM with your application. That is not "the JDK running." The JDK was involved when the code was built. The running process is a JVM executing bytecode. Mixing those words at 2 a.m. makes it harder to know whether you are debugging a build problem or a runtime problem.

Second: compiling with one Java version in CI and running a different major version in production without checking compatibility. A build that succeeds on JDK 21 can still surprise a Java 17 runtime. The mismatch lives exactly where we just named the layers: the toolkit that compiled versus the engine that later tries to run.

So Episode One asked why Java exists and showed bytecode plus the JVM. Today we answered the install confusion: JDK for building, runtime for running, JVM as the engine. The commands `javac` and `java` are no longer mysterious synonyms.

And yet a new frustration appears as soon as those tools work. You write a class, name a file, maybe add a package, and the compiler or launcher refuses until the pieces agree. Why does Java care so much about where `main` lives, what the filename is, and how packages map to folders?

That structural stubbornness is how the compiler and JVM find your code — which is why the next natural question is: why do filenames, packages, and `main` have to agree before anything will run?

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 2 (*JDK, JRE, and JVM*).

Narration technique: install-confusion situation → compile vs run split → JDK/JRE/JVM as answers → command walkthrough → version misunderstandings → next natural problem (program structure). Continuity-checked transitions.
