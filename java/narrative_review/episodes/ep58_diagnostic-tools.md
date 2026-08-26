# Episode 58 — Diagnostic Tools

| Field | Value |
|---|---|
| Episode | 58 |
| Title | Diagnostic Tools |
| Catalog handbook column | 58 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Fifty-Seven taught us to dump the heap when memory climbs for the wrong reason. That is one kind of production hurt. Another kind is the process that is "up" but not answering — threads stuck, latency spiking, CPU hot with no obvious culprit. Folklore arrives fast in those moments: restart it, bump the heap, roll back the last deploy, blame the network. Sometimes a restart "works." It also erases the crime scene. The team feels productive and learns nothing.

So today's question is practical: when production hurts, what do you capture, and in what order, so tools beat folklore?

Start with the stuck or slow application. Before you kill the process, ask whether threads are blocked, waiting on locks, or parked on I/O. A thread dump answers that shape-of-now question:

```bash
jcmd <pid> Thread.print
jcmd <pid> JFR.start name=app settings=profile
```

`Thread.print` gives you stacks right now. Look for many threads in `BLOCKED` or waiting on the same monitor. Look for a deadlock section. Look for threads stuck in your application code versus stuck inside a driver or a DNS call. That single dump often turns "the app is hung" into "checkout threads are waiting on the inventory lock held by thread forty-two." Suddenly you have a code review target instead of a ritual sacrifice of the pod.

Java Flight Recorder — JFR — is the continuous story instead of a snapshot. Starting a recording during the incident captures CPU samples, allocation pressure, lock contention, GC pauses, and more, depending on settings. You are not guessing which five seconds mattered after the fact; you are recording while the pain is happening. Capture during the incident is the rule. Taking dumps after the problem vanishes is how teams collect empty files and strong opinions. The most expensive sentence in ops is "it recovered before we could capture anything."

Heap dumps still belong in the kit when memory is the symptom — we practiced that last episode. The point today is that dumps are not rivals; they are different lenses. Thread dump for concurrency shape. Heap dump for retention. JFR for a timed narrative of what the runtime was doing. Knowing which lens fits the symptom is half of diagnosis. Using every lens at once without a question is how you drown in files.

When the question is "where is CPU going?" or "who is allocating?", async-profiler earns its keep. It can sample CPU or allocation with lower overhead than many people expect, and it produces flame graphs that make hot methods obvious. Pair it with metrics you already have: request rate, error rate, heap usage, GC pause percentiles. Correlate metrics with dumps. A CPU spike that lines up with a particular endpoint in JFR is a diagnosis. A CPU spike with no recording is a story for the postmortem that never finishes. Metrics tell you when; dumps and profiles tell you why.

None of this helps if the first muscle memory is always restart. Restarting as the first step every time trains the team to lose evidence. Restart after you have a dump, a recording, or at least a clear reason that continuing to run is unsafe — disk full, runaway thread killing the node, security incident. And resist the opposite failure mode too: installing every profiler known to humanity without a playbook. Too many tools and no sequence means people argue about which dashboard to open while customers wait. A short playbook beats a museum.

Here is a simple sequence worth practicing. For a stuck app: thread dump, then JFR if you can afford the window, then decide on restart. For climbing heap: metrics confirm growth, heap dump under load, dominators. For hot CPU: async-profiler or JFR CPU view under the same load that hurts. Practice that sequence before the outage — in staging, on a game day, on a quiet afternoon — so muscle memory is not invented at 3 a.m. Practice before the outage sounds soft until the first night you have already done it once.

If an interview asks what you reach for first when an app is stuck, say thread dump and/or JFR to see blockers, then mention that restart without capture is how you guarantee a repeat incident with less data. Offer the correlation habit: metrics for timing, dumps for mechanism.

We now have collectors, leak hunting, and an incident toolkit. Step back from the war room for a moment. The JIT and the allocator are still quietly deciding whether short-lived objects ever become real heap pressure. That optimization story — escape analysis — is Episode Fifty-Nine, and it explains why some allocations you "see" in source never show up the way you expect in profiles.

Put the playbook next to a concrete night. Latency spikes at 2:14. Error rate is flat. CPU is elevated on one instance. You take a thread dump and see most request threads waiting on a database socket. JFR confirms time in socket reads. Metrics show the database failover started at 2:13. You have correlated three lenses without restarting. The fix may still be restarting a pool or failing over, but now you know why. That is the difference between tools and folklore: folklore would have bounced the pod and filed "transient issue."

Put the playbook next to a concrete night. Latency spikes at 2:14. Error rate is flat. CPU is elevated on one instance. You take a thread dump and see most request threads waiting on a database socket. JFR confirms time in socket reads. Metrics show the database failover started at 2:13. You have correlated three lenses without restarting. The fix may still be restarting a pool or failing over, but now you know why. That is the difference between tools and folklore: folklore would have bounced the pod and filed "transient issue."

Also build a capture kit into the platform before you need it. Can jcmd reach the process in the container? Are JDK tools in the image? Is JFR allowed by security policy? Is there disk space for a heap dump? Practice before the outage includes checking that the tools exist where the process runs, not only that you know their names on your laptop.

Also build a capture kit into the platform before you need it. Can jcmd reach the process in the container? Are JDK tools in the image? Is JFR allowed by security policy? Is there disk space for a heap dump? Practice before the outage includes checking that the tools exist where the process runs, not only that you know their names on your laptop.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Diagnostic Tools (Episode 58).

Narration technique: incident vs folklore → thread dump + JFR → capture-during-incident → heap/CPU lenses → async-profiler → correlate metrics → playbook vs tool museum → interview woven → bridge to escape analysis.

Teaching points preserved: jcmd/JFR/thread/heap dumps; async-profiler; capture during incident; correlate metrics; practice before outage.
