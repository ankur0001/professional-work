# Episode 58 — Diagnostic Tools

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-Seven showed heap dumps and MAT for memory leaks. But production incidents need fast answers from a running JVM. JDK ships diagnostic tools — no extra install required.

jcmd is the Swiss Army knife — list, trigger, and inspect. jmap, jstack, and JFR each target a different runtime view. Today — jcmd, jmap, jstack, and JFR for live JVM diagnostics. Episode Fifty-Eight.

Diagnostic Tools. jcmd sends diagnostic commands to a running Java process. List JVMs with jcmd — shows PID and main class name. jcmd <pid> help — lists every available subcommand. VM.flags prints active JVM flags — verify your tuning.

GC.heap_info and GC.class_histogram — quick heap snapshot. JFR.start and JFR.dump — record and export flight recordings. jmap inspects heap layout and creates dumps. jmap -heap <pid> — summary of generations and usage.

jmap -histo:live <pid> — object histogram of live instances. jmap -dump:live,format=b,file=heap.hprof <pid> — full dump. Prefer jcmd GC.heap_dump on modern JDK — same result, cleaner API.

Histogram first — confirms leak class before multi-gigabyte dump. jstack captures thread stacks — essential for deadlocks and hangs. jstack <pid> — prints every thread name, state, and stack trace.

Look for BLOCKED threads and circular lock dependencies. jcmd <pid> Thread.print — equivalent output on modern JDK. Take multiple samples seconds apart — distinguish transient waits.

Thread dump alone does not show heap — pair with jmap or JFR. Java Flight Recorder — low-overhead event recorder built into the JDK. Enable with -XX:+FlightRecorder or jcmd JFR.start.

Records GC, allocation, lock, and method samples continuously. jcmd <pid> JFR.dump filename=rec.jfr — export for JDK Mission Control. Allocation and OldObjectSample events help find leak sources live.

Production-safe when configured — microseconds of overhead per event. A practical on-call diagnostic workflow. Step one — jcmd <pid> help and VM.flags — confirm JVM state. Step two — high CPU? async-profiler or JFR MethodProfiling.

Step three — high heap? GC.heap_info then histogram or heap dump. Step four — stuck threads? Thread.print twice, check BLOCKED. Document PID, timestamp, and command output for post-incident review.

Three common mistakes. One — running jmap -heap on a 32-gig heap under load — long STW pause. Two — single thread dump for deadlock — need two samples or JFR lock events. Three — leaving JFR recording forever without rotation — disk fills up.

Also — using tools from a different JDK version than the target JVM. Match JDK major version — diagnostic output formats change. Interview question — how do you diagnose a production JVM issue?

jcmd — list processes, VM.flags, GC.heap_info, Thread.print. jmap histogram or heap dump for memory — jstack for thread deadlocks. JFR for continuous low-overhead profiling — export to Mission Control.

Sample under load — idle JVM hides contention and allocation hotspots. Always capture timestamp, PID, and JDK version with every artifact. Diagnostics show what the JVM does at runtime — the compiler optimizes before that.

Episode Fifty-Nine — Escape Analysis. Stack allocation, scalar replacement, and when objects escape. See you there.
