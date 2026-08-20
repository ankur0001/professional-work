# Episode 58 — Diagnostic Tools

| Field | Value |
|---|---|
| Episode | 58 |
| Title | Diagnostic Tools |
| Catalog handbook column | 58 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Seven showed heap dumps and MAT for memory leaks after the fact.
2. Production incidents need fast answers from a running JVM — not always time for a multi-gig dump.
3. The JDK ships diagnostic tools — no extra install if you have the same major version on the path.
4. jcmd is the Swiss Army knife — list processes, trigger dumps, print threads, start JFR.
5. jmap, jstack, and JFR each target a different runtime view — memory, threads, continuous events.
6. Today — jcmd, jmap, jstack, and JFR for live JVM diagnostics like an on-call engineer.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Eight.
2. Diagnostic Tools.
3. We'll walk an on-call workflow — flags, histogram, thread dump, short JFR recording.

### Scene `jcmd_overview` (renderer: `jcmd_overview`)

1. jcmd sends diagnostic commands to a running Java process by PID — same JDK major version required.
2. jcmd lists JVMs with PID and main class — find the process among containers and sidecars.
3. jcmd PID help — lists every available subcommand for that JVM — discoverability built in.
4. VM.flags prints active JVM flags — verify heap, GC, and tuning actually applied at startup.
5. GC.heap_info and GC.class_histogram — quick heap snapshot without full HPROF weight.
6. JFR.start and JFR.dump — record and export flight recordings for post-incident analysis in Mission Control.

```bash
jcmd
jcmd 12345 VM.flags
jcmd 12345 GC.class_histogram
```

7. jcmd replaces many legacy attach tricks — learn it first on every incident bridge.

### Scene `jmap_heap` (renderer: `jmap_heap`)

1. jmap inspects heap layout and creates dumps — older but still seen in runbooks.
2. jmap -heap PID — summary of generations and usage — can trigger long STW on huge heaps, use carefully.
3. jmap -histo:live PID — object histogram of live instances by class — fast leak class confirmation.
4. jmap -dump:live,format=b,file=heap.hprof PID — full dump — prefer jcmd GC.heap_dump on modern JDK.
5. Histogram first — if char array or byte array dominates unexpectedly, you know where to look before terabyte dumps.
6. Live histogram forces minor GC first — numbers reflect reachable set more closely than all objects.

### Scene `jstack_threads` (renderer: `jstack_threads`)

1. jstack captures thread stacks — essential for deadlocks, hangs, and thread pool exhaustion.
2. jstack PID — prints every thread name, state, and stack trace — BLOCKED and WAITING jump out.
3. Look for BLOCKED threads and circular lock dependencies — Java prints "waiting to lock" and owner thread.
4. jcmd PID Thread.print — equivalent output on modern JDK — prefer jcmd for consistency.
5. Take multiple samples seconds apart — distinguish permanent deadlock from transient wait on external service.
6. Thread dump alone does not show heap — pair with histogram or JFR allocation events for complete picture.

```bash
jstack 12345 > threaddump1.txt
sleep 5
jstack 12345 > threaddump2.txt
```

7. Two dumps — if same threads blocked on same locks both times, deadlock suspicion rises.

### Scene `jfr_overview` (renderer: `jfr_overview`)

1. Java Flight Recorder — low-overhead event recorder built into the JDK — not a third-party APM only.
2. Enable with -XX:StartFlightRecording at startup or jcmd JFR.start on running process.
3. Records GC, allocation, lock, method sample, and CPU events continuously into circular buffers.
4. jcmd PID JFR.dump filename=rec.jfr — export for JDK Mission Control offline analysis.
5. Allocation and OldObjectSample events help find leak sources live — which stack allocated growing classes.
6. Production-safe when configured with sensible buffer sizes — microseconds overhead per event class, not milliseconds per request.

### Scene `diagnostic_workflow` (renderer: `diagnostic_workflow`)

1. A practical on-call diagnostic workflow — order matters when pages fire.
2. Step one — jcmd PID help and VM.flags — confirm JVM identity, heap, collector, accidental bad flags.
3. Step two — high CPU — async-profiler cpu or JFR MethodProfiling sample — find hot native or Java frames.
4. Step three — high heap — GC.heap_info then GC.class_histogram — dump only if histogram implicates leak class.
5. Step four — stuck threads or slow requests — Thread.print twice, check BLOCKED and pool exhaustion.
6. Document PID, timestamp, JDK version, and command output in the incident ticket — future you will thank present you.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes I want burned into your brain.
2. Mistake one — running jmap -heap on a 32 GB heap under peak load — long STW pause makes incident worse.
3. Mistake two — single thread dump for deadlock confirmation — need two samples or JFR lock events for proof.
4. Mistake three — leaving JFR recording forever without rotation — disk fills, secondary outage.
5. Also — using jmap or jstack from JDK 21 against a JDK 17 process — attach failures and garbage output.
6. Match JDK major version for attach tools — diagnostic output formats and attach protocol evolve.

### Scene `interview` (renderer: `interview`)

1. Interview time — say this out loud like someone who has shipped code.
2. Question: How do you diagnose a production JVM issue?
3. Answer: jcmd — list processes, VM.flags, GC.heap_info, Thread.print, JFR.start and dump.
4. jmap histogram or heap dump for memory — jstack or Thread.print for thread deadlocks and pool starvation.
5. JFR for continuous low-overhead profiling — export to Mission Control for timeline analysis.
6. Sample under load — idle JVM hides contention and allocation hotspots that only appear in traffic.
7. Always capture timestamp, PID, and JDK version with every artifact — reproducibility matters in postmortems.

### Scene `teaser` (renderer: `teaser`)

1. Diagnostics show what the JVM does at runtime — the compiler optimizes allocations before tools see heap growth.
2. Episode Fifty-Nine — Escape Analysis.
3. Stack allocation, scalar replacement, and when objects escape the method scope.
4. See you there.

_Total beats: expanded for ~10–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **70** — *JVM Troubleshooting*.
- **Series catalog mapping:** Episode 58 / catalog column `58` / published title *Diagnostic Tools*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 70 → episode 58). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with on-call command examples — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — live diagnostics vs post-mortem dumps
- **`title`** — episode title card
- **`jcmd_overview`** — unified diagnostic commands
- **`jmap_heap`** — histogram and heap dump
- **`jstack_threads`** — thread dumps and deadlock detection
- **`jfr_overview`** — Flight Recorder events
- **`diagnostic_workflow`** — on-call step order
- **`mistakes`** — STW during incident, version mismatch
- **`interview`** — production JVM diagnosis answer
- **`teaser`** — bridge to Escape Analysis
