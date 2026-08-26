# Episode 62 — JVM Flags and Tuning

| Field | Value |
|---|---|
| Episode | 62 |
| Title | JVM Flags and Tuning |
| Catalog handbook column | 62 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

By now you know collectors, leaks, dumps, escape analysis, and memory beyond the heap. So someone pastes a twenty-flag command line into your deployment manifest and says "this is how we tune Java." That paste is not a strategy. It is an heirloom. Nobody remembers which incident invented half the flags. Nobody knows which ones still matter on the current JDK. Treat flags as experiments: change one variable, measure against SLOs, document why the flag exists, and delete it when it stops earning its keep.

Begin with intention, not folklore. Set the heap on purpose. A stable sizing story — often `-Xms` equal to `-Xmx` for server processes that should not spend time resizing — is a decision you can explain in a design review. Pair it with a collector you chose for reasons from Episode Fifty-Six, and turn on GC logging:

```bash
java -Xms512m -Xmx512m -XX:+UseG1GC -Xlog:gc*:file=gc.log -jar app.jar
```

That line is not "fully tuned." It is observable. Without logs and metrics under realistic load, the rest of the flag list is costume jewelry. Prefer evidence over folklore. If p99 fails under load, read GC pauses, allocation rate, heap occupancy, CPU steal, and queue depth. Form a hypothesis that names a mechanism. Change one thing. Remeasure. That loop is tuning. Copying a blog's ZGC flags because the title said "ultimate performance" is cosplay.

Make the experiment loop tactile. Baseline: p99 is 180ms under a load test that mirrors production mix. GC log shows mixed collections with 40ms pauses. Hypothesis: heap too small for the live set plus allocation burst. Change: raise `-Xmx`/`-Xms` together by a measured step, keep the collector constant. Remeasure. If p99 drops and pauses calm, you learned something. If nothing changes, revert and form a new hypothesis — maybe latency is lock contention, and JFR would have said so. Changing five flags at once teaches nothing either way.

Document why a flag exists. Future you will not remember that `-XX:SomethingObscure` was added during a Black Friday incident three years ago. A comment in the manifest, a runbook line, a pull-request note — anything that ties flag to symptom and proof. Remove flags that no longer earn their keep. Debug flags, ultra-verbose logging, or experimental options left on forever create overhead, noise, and false confidence.

Separate supportability flags from performance flags. GC logging and JFR configuration often stay because they make the next incident cheaper. Random micro-tuning flags must continually earn their keep against SLOs.

Cargo-cult lists fail predictably. A flag that helped a four-gigabyte heap may hurt a five-hundred-megabyte container. A flag that helped Java 11 may be default, renamed, or irrelevant on Java 21. A flag that reduced pauses may increase CPU until autoscaling costs explode. Folklore has favorite spells: `-XX:+AggressiveOpts` from an ancient blog, huge thread stacks from a desktop recipe, GC ratio flags that do not match your collector, `-Xlog:gc*=debug` left on until disks fill. Each fails the documentation test: no symptom, no measurement, no revert plan. Prefer a short, owned flag list to a long, inherited one.

This episode does not memorize every `-XX`. The catalog is large and version-dependent. What transfers is discipline: intentional heap, visible GC behavior, evidence, documentation, cleanup. When someone suggests a flag, ask "what symptom?", "what measurement changed?", and "how do we know to revert?" Missing answers mean the flag is a rumor with a dash prefix.

We turned flags from magic words into a scientific habit. Zoom in further: sometimes the "memory problem" is not GC policy but the shape of objects themselves — headers, padding, compressed oops. Episode Sixty-Three is object layout, and it explains why a "tiny" object is never as tiny as its fields suggest.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — JVM Flags and Tuning (Episode 62).

Narration technique: cargo-cult paste → flags as experiments → intentional heap + GC log → experiment loop → document/remove → supportability vs perf → misconceptions → bridge to object layout.

Teaching points preserved: set heap intentionally; GC logging; evidence over folklore; document flags; remove stale flags.
