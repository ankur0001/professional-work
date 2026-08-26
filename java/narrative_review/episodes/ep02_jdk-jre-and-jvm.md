# Episode 02 — JDK, JRE, and JVM

| Field | Value |
|---|---|
| Episode | 02 |
| Title | JDK, JRE, and JVM |
| Catalog handbook column | 2 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode One ended on a confusion that almost every beginner hits: someone says "install Java," and three different acronyms appear — JDK, JRE, JVM — as if they were the same thing.

That confusion is not vocabulary trivia. It is the next problem our story created. We already know Java source becomes bytecode, and a JVM runs that bytecode. So if the JVM is the engine, what did you actually install when you typed a command and waited for a download?

Let's start from the moment you try to compile the HelloWorld program from Episode One.

```bash
javac HelloWorld.java
java HelloWorld
```

If `javac` is missing, the first command fails. You can have a machine that runs Java applications and still be unable to compile anything. That single failure splits the world into two jobs: building programs, and running programs.

The toolkit that contains the compiler — and the other developer tools around it — is the JDK, the Java Development Kit. `javac` lives there. So do tools such as `jar`, `jlink`, and diagnostic utilities you will meet later. When a tutorial says "install the JDK," it is saying: give yourself the toolbox needed to create Java software.

But compiling is only half the path. After `javac` produces `HelloWorld.class`, the second command starts a process that can load bytecode and execute it. That process is centered on the JVM, the Java Virtual Machine — commonly HotSpot. The JVM is the engine. It does not care that you wrote the source this morning. It cares that valid bytecode arrived and needs to run.

So where does the JRE fit?

Historically, the JRE — Java Runtime Environment — named the runtime idea: the libraries and launcher you need to run an application without necessarily shipping the full developer toolbox. In older distributions, you could install a JRE on a server that should only run apps, not compile them. In modern JDK distributions, the lines are blurrier because a JDK download usually includes what you need to run as well as compile. The useful distinction remains: development tools versus the runtime that executes bytecode.

Hold the layers in one picture, lightly: the JDK is the toolbox on the workbench, the runtime idea is the apartment where the program lives, and the JVM is the engine in the basement. The picture only helps if we keep tying it back to commands and failures.

Now walk the full flow again with those names attached. You write `HelloWorld.java`. The JDK's `javac` turns it into bytecode in a `.class` file. You run `java HelloWorld`. That launcher starts a JVM, the JVM loads the class, finds `main`, and executes the print. Same story as Episode One — now with clearer labels for each layer.

Once the happy path is clear, production life introduces sharper mistakes.

First mistake: calling everything "the JDK," including the running process. A production container may be executing a JVM with your application. That is not "the JDK running." The JDK was involved when the code was built. The running process is a JVM executing bytecode, using the runtime libraries. When an incident happens at 2 a.m., mixing those words makes it harder to know whether you are debugging a build problem or a runtime problem.

Second mistake: compiling with one Java version in CI and running a different major version in production without checking compatibility. Bytecode and APIs are versioned. A build that succeeds on JDK 21 can still surprise a Java 17 runtime. The layers we just named are exactly where that mismatch lives: the developer toolkit that compiled the code versus the engine that later tries to run it.

Third mistake: treating heap size as the entire memory story. People set `-Xmx` equal to a container's memory limit and leave no headroom. The JVM uses more than the heap — stacks, metaspace, code cache, and native memory also count. You do not need the full memory chapter yet. You only need enough curiosity to stop equating "Java memory" with one flag.

So let's reconnect the chain. Episode One asked why Java exists and showed bytecode plus the JVM. Today we answered the install confusion: JDK for building, runtime for running, JVM as the engine inside that runtime story. The commands `javac` and `java` are no longer mysterious synonyms. They belong to different layers.

And yet a new frustration appears as soon as those tools work. You write a class, name a file, maybe add a package, and the compiler or launcher refuses to cooperate until the pieces agree with each other. Why does Java care so much about where `main` lives, what the filename is, and how packages map to folders?

That structural stubbornness is not paperwork. It is how the compiler and JVM find your code — and it is exactly where Episode Three begins.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 2 (*JDK, JRE, and JVM*).

Narration technique: install-confusion situation → compile vs run split → JDK/JRE/JVM as answers → command walkthrough → version/memory misunderstandings → next natural problem (program structure). Continuity-checked transitions.
