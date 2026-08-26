# Episode 58 — Diagnostic Tools

| Field | Value |
|---|---|
| Episode | 58 |
| Title | Diagnostic Tools |
| Catalog handbook column | 58 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Fifty-Seven taught us to dump the heap when memory climbs for the wrong reason. Another kind of hurt is the process that is "up" but not answering — threads stuck, latency spiking, CPU hot with no obvious culprit. Folklore arrives fast: restart it, bump the heap, roll back, blame the network. Sometimes a restart "works." It also erases the crime scene. The team feels productive and learns nothing.

So today's question is practical: when production hurts, what do you capture, and in what order, so tools beat folklore?

Start with the stuck or slow application. Before you kill the process, ask whether threads are blocked, waiting on locks, or parked on I/O:

```bash
jcmd <pid> Thread.print
jcmd <pid> JFR.start name=app settings=profile
```

`Thread.print` gives stacks right now. Look for many threads `BLOCKED` or waiting on the same monitor. Look for a deadlock section. Look for application code versus a driver or DNS call. That single dump often turns "the app is hung" into "checkout threads wait on the inventory lock held by thread forty-two" — a code review target instead of a ritual sacrifice of the pod.

Java Flight Recorder is the continuous story instead of a snapshot. A recording during the incident captures CPU samples, allocation pressure, lock contention, GC pauses, and more. Capture while the pain is happening. Taking dumps after the problem vanishes collects empty files and strong opinions. The most expensive sentence in ops is "it recovered before we could capture anything."

Heap dumps still belong when memory is the symptom — we practiced that last episode. Dumps are different lenses, not rivals: thread dump for concurrency shape, heap dump for retention, JFR for a timed narrative. Knowing which lens fits the symptom is half of diagnosis. Using every lens without a question is how you drown in files.

When the question is "where is CPU going?" or "who is allocating?", async-profiler earns its keep. It samples CPU or allocation and produces flame graphs that make hot methods obvious. Pair it with metrics you already have: request rate, error rate, heap usage, GC pause percentiles. Metrics tell you when; dumps and profiles tell you why. A CPU spike lined up with an endpoint in JFR is a diagnosis. A spike with no recording is a postmortem that never finishes.

Build a capture kit into the platform before you need it. Can jcmd reach the process in the container? Are JDK tools in the image? Is JFR allowed? Is there disk for a heap dump? Practice before the outage includes checking that the tools exist where the process runs, not only that you know their names on your laptop.

None of this helps if the first muscle memory is always restart. Restart after you have a dump, a recording, or a clear reason that continuing is unsafe. Resist the opposite failure too: a museum of profilers and no sequence. A short playbook beats arguing about dashboards while customers wait.

Practice a simple sequence. Stuck app: thread dump, then JFR if you can afford the window, then decide on restart. Climbing heap: metrics confirm growth, heap dump under load, dominators. Hot CPU: async-profiler or JFR CPU view under the same load that hurts. Practice in staging or on a game day so muscle memory is not invented at 3 a.m.

Put that playbook next to a concrete night. Latency spikes at 2:14. Error rate is flat. CPU is elevated on one instance. A thread dump shows most request threads waiting on a database socket. JFR confirms time in socket reads. Metrics show the database failover started at 2:13. Three lenses, no restart, a real why. Folklore would have bounced the pod and filed "transient issue."

If an interview asks what you reach for first when an app is stuck, say thread dump and/or JFR to see blockers — and that restart without capture guarantees a repeat incident with less data. Offer the correlation habit: metrics for timing, dumps for mechanism.

We now have collectors, leak hunting, and an incident toolkit. Step back from the war room: the JIT and the allocator still decide whether short-lived objects ever become real heap pressure. Escape analysis — Episode Fifty-Nine — explains why some allocations you "see" in source never show up the way you expect in profiles.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Diagnostic Tools (Episode 58).

Narration technique: incident vs folklore → thread dump + JFR → capture-during-incident → lenses → async-profiler → platform kit → playbook → concrete night → interview woven → bridge to escape analysis.

Teaching points preserved: jcmd/JFR/thread/heap dumps; async-profiler; capture during incident; correlate metrics; practice before outage.
