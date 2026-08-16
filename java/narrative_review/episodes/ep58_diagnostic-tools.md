# Episode 58 — Diagnostic Tools

| Field | Value |
|---|---|
| Episode | 58 |
| Title | Diagnostic Tools |
| Catalog handbook column | 58 |
| Narration source script | `make_episode_58.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Seven showed heap dumps and MAT for memory leaks.
2. But production incidents need fast answers from a running JVM.
3. JDK ships diagnostic tools — no extra install required.
4. jcmd is the Swiss Army knife — list, trigger, and inspect.
5. jmap, jstack, and JFR each target a different runtime view.
6. Today — jcmd, jmap, jstack, and JFR for live JVM diagnostics.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Eight.
2. Diagnostic Tools.

### Scene `jcmd_overview` (renderer: `jcmd_overview`)

1. jcmd sends diagnostic commands to a running Java process.
2. List JVMs with jcmd — shows PID and main class name.
3. jcmd <pid> help — lists every available subcommand.
4. VM.flags prints active JVM flags — verify your tuning.
5. GC.heap_info and GC.class_histogram — quick heap snapshot.
6. JFR.start and JFR.dump — record and export flight recordings.

### Scene `jmap_heap` (renderer: `jmap_heap`)

1. jmap inspects heap layout and creates dumps.
2. jmap -heap <pid> — summary of generations and usage.
3. jmap -histo:live <pid> — object histogram of live instances.
4. jmap -dump:live,format=b,file=heap.hprof <pid> — full dump.
5. Prefer jcmd GC.heap_dump on modern JDK — same result, cleaner API.
6. Histogram first — confirms leak class before multi-gigabyte dump.

### Scene `jstack_threads` (renderer: `jstack_threads`)

1. jstack captures thread stacks — essential for deadlocks and hangs.
2. jstack <pid> — prints every thread name, state, and stack trace.
3. Look for BLOCKED threads and circular lock dependencies.
4. jcmd <pid> Thread.print — equivalent output on modern JDK.
5. Take multiple samples seconds apart — distinguish transient waits.
6. Thread dump alone does not show heap — pair with jmap or JFR.

### Scene `jfr_overview` (renderer: `jfr_overview`)

1. Java Flight Recorder — low-overhead event recorder built into the JDK.
2. Enable with -XX:+FlightRecorder or jcmd JFR.start.
3. Records GC, allocation, lock, and method samples continuously.
4. jcmd <pid> JFR.dump filename=rec.jfr — export for JDK Mission Control.
5. Allocation and OldObjectSample events help find leak sources live.
6. Production-safe when configured — microseconds of overhead per event.

### Scene `diagnostic_workflow` (renderer: `diagnostic_workflow`)

1. A practical on-call diagnostic workflow.
2. Step one — jcmd <pid> help and VM.flags — confirm JVM state.
3. Step two — high CPU? async-profiler or JFR MethodProfiling.
4. Step three — high heap? GC.heap_info then histogram or heap dump.
5. Step four — stuck threads? Thread.print twice, check BLOCKED.
6. Document PID, timestamp, and command output for post-incident review.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — running jmap -heap on a 32-gig heap under load — long STW pause.
3. Two — single thread dump for deadlock — need two samples or JFR lock events.
4. Three — leaving JFR recording forever without rotation — disk fills up.
5. Also — using tools from a different JDK version than the target JVM.
6. Match JDK major version — diagnostic output formats change.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you diagnose a production JVM issue?
2. jcmd — list processes, VM.flags, GC.heap_info, Thread.print.
3. jmap histogram or heap dump for memory — jstack for thread deadlocks.
4. JFR for continuous low-overhead profiling — export to Mission Control.
5. Sample under load — idle JVM hides contention and allocation hotspots.
6. Always capture timestamp, PID, and JDK version with every artifact.

### Scene `teaser` (renderer: `teaser`)

1. Diagnostics show what the JVM does at runtime — the compiler optimizes before that.
2. Episode Fifty-Nine — Escape Analysis.
3. Stack allocation, scalar replacement, and when objects escape.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **70** — *JVM Troubleshooting*.
- **Series catalog mapping:** Episode 58 / catalog column `58` / published title *Diagnostic Tools*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 70 → episode 58). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-Seven showed heap dumps and MAT for memory leaks._
- **`title`** — starts from: _Episode Fifty-Eight._
- **`jcmd_overview`** — starts from: _jcmd sends diagnostic commands to a running Java process._
- **`jmap_heap`** — starts from: _jmap inspects heap layout and creates dumps._
- **`jstack_threads`** — starts from: _jstack captures thread stacks — essential for deadlocks and hangs._
- **`jfr_overview`** — starts from: _Java Flight Recorder — low-overhead event recorder built into the JDK._
- **`diagnostic_workflow`** — starts from: _A practical on-call diagnostic workflow._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do you diagnose a production JVM issue?_
- **`teaser`** — starts from: _Diagnostics show what the JVM does at runtime — the compiler optimizes before that._
