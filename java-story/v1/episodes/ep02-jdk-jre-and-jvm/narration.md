# Episode 02 — JDK, JRE, and JVM

**Cut:** v1 (original)

## Transcript (from captions)

In Episode One, we learned why Java survived. But beginners still mix three names — JDK, JRE, and JVM. They are not the same thing. Today we separate them — clearly — on screen. Episode Two.

JDK, JRE, and JVM — the three layers of the Java platform. Look at these three boxes. At the top — the JDK. Your developer toolkit. In the middle — the JRE. What you need to run Java apps.

At the bottom — the JVM. The engine that executes bytecode. JDK for develop. JRE for run. JVM is the engine inside. Zoom into the JDK. This is where javac lives — the compiler. Also jar, jlink, jcmd, jmap, and Java Flight Recorder tools.

If you write code or debug production issues — you want the JDK. The JRE is the runtime layer. Libraries, launchers, and everything needed to start a Java process. It does not include the compiler.

Modern installs often ship a JDK — but the runtime idea still matters. And here is the JVM. It loads class files, verifies bytecode, and runs your program. HotSpot is the common implementation — interpreter, JIT, garbage collection.

Same bytecode contract. Different machines. Same result. Follow the arrows. Your .java file goes into javac — that tool comes from the JDK. Out comes a .class file — bytecode. The java launcher starts a JVM process.

The JVM reads bytecode and runs it. That is the full path — develop, package, execute. Now the production gotcha. On screen — heap is only one slice of memory. Also metaspace, thread stacks, code cache, and native memory.

If dash X m x equals your container limit — you leave no headroom. Always leave room beyond the heap. Three common mistakes. One — shipping a full JDK into every tiny container when a slim runtime would do.

Two — compiling with Java twenty-one in CI, then running Java seventeen in production. Three — treating the JVM as a black box until something breaks. Interview question — what's the difference between JDK, JRE, and JVM?

Point to the diagram. JVM executes bytecode. JRE provides the runtime to launch apps. JDK adds compilers and diagnostics on top. Answer that calmly — and you sound like you've shipped Java.

Now the three names finally line up with the picture. Next episode — Java program structure. public class, main, packages — what every line is doing. Episode Three. See you there.
