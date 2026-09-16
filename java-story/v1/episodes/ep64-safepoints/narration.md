# Episode 64 — Safepoints

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty-Three showed how object headers and padding affect heap footprint. Memory layout is static — safepoints are dynamic coordination points in the JVM. GC, deoptimization, and some JVM operations need every thread to reach a known state.

That coordination is called a safepoint — and it can pause your application threads. Long-running loops without safepoint polls can delay GC for seconds. Today — what safepoints are, when the JVM pauses, and safepoint bias.

Episode Sixty-Four. Safepoints. A safepoint is a point in compiled code where the JVM can safely inspect thread state. At a safepoint, the JVM knows every live reference and every stack frame.

GC roots are scanned, biased locking is revoked, and deoptimization can occur. Threads not at a safepoint must be brought there before STW work begins. Safepoints are not GC-only — many JVM subsystems depend on them.

Think of them as coordinated parking spots for all application threads. Stop-the-world phases require all mutator threads at safepoints. Young GC often pauses briefly — all threads must park at safepoints first.

Full GC and some old-gen collections extend STW while roots are processed. Deoptimization — switching compiled code back to interpreter — uses safepoints. Biased lock revocation and some JVMTI operations trigger safepoint synchronization.

Pause time includes time waiting for slow threads to reach a safepoint. Safepoint bias — JVM prefers certain code locations for safepoint polls. Counted loops have safepoint back-edges — every N iterations thread checks.

Non-counted loops and JNI calls may lack frequent poll sites. A tight infinite loop without polls can block GC indefinitely — rare but real. SafepointSynchronize events in JFR show time spent waiting for threads.

Long safepoint sync times point to threads stuck between poll sites. Threads poll a global safepoint flag at compiled poll sites. When a safepoint is requested, running threads trap at the next poll.

Interpreter and JIT insert polls in method prologues and loop back-edges. JNI transitions and blocking I/O eventually reach safepoints on return. UseAsyncLogDecoration and some intrinsics affect poll placement.

Understanding polls explains why CPU-bound loops affect GC responsiveness. Practical awareness for production engineers. JFR SafepointBegin and SafepointEnd events measure sync plus STW duration.

High sync time — look for long non-polling loops or JNI critical sections. ZGC and Shenandoah reduce but do not eliminate all safepoint coordination. Do not micro-optimize poll sites — fix algorithmic long loops instead.

Safepoint knowledge connects GC pauses to actual thread behavior. Three common mistakes. One — blaming GC alone for pauses — sync time may dominate. Two — writing busy loops without considering safepoint reachability.

Three — ignoring JFR safepoint events during latency investigations. Also — assuming concurrent collectors have zero STW — they still safepoint. Measure sync versus STW separately — the cause differs.

Interview question — what is a safepoint and why does it matter? Coordination point where JVM can inspect all thread stacks safely. Required for GC root scanning, deoptimization, and lock bias revocation.

Threads poll at loop back-edges — must reach safepoint before STW work. Long sync time means threads slow to park — not always GC algorithm fault. JFR safepoint events separate sync wait from actual stop-the-world work.

Safepoints coordinate runtime — startup decides how fast you reach steady state. Episode Sixty-Five — JVM Startup and Warmup. Class loading cost, CDS, and warmup strategies. See you there.
