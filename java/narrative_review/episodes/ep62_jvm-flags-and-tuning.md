# Episode 62 — JVM Flags and Tuning

| Field | Value |
|---|---|
| Episode | 62 |
| Title | JVM Flags and Tuning |
| Catalog handbook column | 62 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

By now you know collectors, leaks, dumps, escape analysis, and memory beyond the heap. So someone pastes a twenty-flag command line into your deployment manifest and says "this is how we tune Java." That paste is not a strategy. It is an heirloom. Nobody remembers which incident invented half the flags. Nobody knows which ones still matter on the current JDK. Today's episode is about treating flags as experiments: change one variable, measure against SLOs, document why the flag exists, and delete it when it stops earning its keep.

Begin with intention, not folklore. Set the heap on purpose. A stable heap sizing story — often `-Xms` equal to `-Xmx` for server processes that should not spend time resizing up and down — is a decision you can explain in a design review. Pair it with a collector you chose for reasons from Episode Fifty-Six, and turn on GC logging so the decision can be audited:

```bash
java -Xms512m -Xmx512m -XX:+UseG1GC -Xlog:gc*:file=gc.log -jar app.jar
```

That line is not "fully tuned." It is observable. Without logs and without metrics under realistic load, the rest of the flag list is costume jewelry. Prefer evidence over folklore. If p99 latency fails under load, read GC pauses, allocation rate, heap occupancy, CPU steal, and queue depth. Form a hypothesis that names a mechanism. Change one thing. Remeasure. That loop is tuning. Copying a blog's ZGC flags because the title said "ultimate performance" is not tuning. It is cosplay.

Document why a flag exists. Future you will not remember that `-XX:SomethingObscure` was added during a Black Friday incident three years ago. A comment in the deployment manifest, a line in the runbook, a note in the pull request — anything that ties flag to symptom and proof. Remove flags that no longer earn their keep. Leaving debug flags, ultra-verbose logging, or experimental options on forever creates overhead, noise, and false confidence. A flag that once saved you can later cost you without anyone noticing, because nobody owned the experiment's end date.

Cargo-cult lists fail in predictable ways. A flag that helped a four-gigabyte heap may hurt a five-hundred-megabyte container. A flag that helped Java 11 may be default, renamed, or irrelevant on Java 21. A flag that reduced pauses may increase CPU until autoscaling costs explode. Tuning without load tests guarantees you are optimizing for a machine that is not production — often your laptop, often with polite traffic. The first tuning step in an interview answer should sound boring and correct: gather metrics and GC logs under realistic load, then change one variable against an explicit SLO. If you cannot name the SLO, you are not ready to name the flag.

Notice how this episode does not try to memorize every `-XX`. The catalog is large and version-dependent. What transfers is the discipline: intentional heap, visible GC behavior, evidence, documentation, cleanup. When a vendor or a senior engineer suggests a flag, your questions are "what symptom?", "what measurement changed?", and "how do we know to revert?" If those answers are missing, the flag is a rumor with a dash prefix.

We turned flags from magic words into a scientific habit. Zoom in further: sometimes the "memory problem" is not GC policy but the shape of objects themselves — headers, padding, compressed oops. Episode Sixty-Three is object layout, and it explains why a "tiny" object is never as tiny as its fields suggest.

Make the experiment loop tactile. Baseline: p99 is 180ms under a load test that mirrors production mix. GC log shows mixed collections with 40ms pauses. Hypothesis: heap is too small for the live set plus allocation burst, causing frequent mixed collections. Change: raise `-Xmx`/`-Xms` together by a measured step, keep the collector constant. Remeasure. If p99 drops and pauses calm, you learned something. If nothing changes, revert and form a new hypothesis — maybe the latency is lock contention, and JFR would have said so. Changing five flags at once would have taught you nothing either way.

Folklore has favorite spells. `-XX:+AggressiveOpts` from an ancient blog. Huge thread stack sizes copied from a desktop recipe. GC ratio flags that do not match your collector. Leaving `-Xlog:gc*=debug` on forever in production until disks fill. Each of these fails the documentation test: there is no symptom, no measurement, no revert plan. Prefer a short, owned flag list to a long, inherited one.

Make the experiment loop tactile. Baseline: p99 is 180ms under a load test that mirrors production mix. GC log shows mixed collections with 40ms pauses. Hypothesis: heap is too small for the live set plus allocation burst, causing frequent mixed collections. Change: raise `-Xmx`/`-Xms` together by a measured step, keep the collector constant. Remeasure. If p99 drops and pauses calm, you learned something. If nothing changes, revert and form a new hypothesis — maybe the latency is lock contention, and JFR would have said so. Changing five flags at once would have taught you nothing either way.

Folklore has favorite spells. `-XX:+AggressiveOpts` from an ancient blog. Huge thread stack sizes copied from a desktop recipe. GC ratio flags that do not match your collector. Leaving `-Xlog:gc*=debug` on forever in production until disks fill. Each of these fails the documentation test: there is no symptom, no measurement, no revert plan. Prefer a short, owned flag list to a long, inherited one.

Also separate "supportability flags" from "performance flags." GC logging and JFR configuration are often worth keeping because they make the next incident cheaper. Random micro-tuning flags are the ones that must continually earn their keep against SLOs.

Also separate "supportability flags" from "performance flags." GC logging and JFR configuration are often worth keeping because they make the next incident cheaper. Random micro-tuning flags are the ones that must continually earn their keep against SLOs.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — JVM Flags and Tuning (Episode 62).

Narration technique: cargo-cult paste → flags as experiments → intentional heap + GC log command → evidence loop → document/remove → misconceptions → interview woven → bridge to object layout.

Teaching points preserved: set heap intentionally; GC logging; evidence over folklore; document flags; remove stale flags.
