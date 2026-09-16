# Episode 01 — Why Java Exists / Introduction to Java

**Cut:** v1 (original)

## Transcript (from captions)

Okay… imagine this. Banks. Airlines. Stock exchanges. Android apps. Enterprise software. Nearly all of them depend on one programming language. That language is Java. But here's what I find fascinating.

Java was born in the nineteen nineties. Hundreds of languages came and went. Java stayed. So why? Let's find out — in the next few minutes. Go back to the early nineties. At Sun Microsystems, James Gosling's team started with C++.

C++ was powerful — no doubt. But it came with pain. Manual memory management. One mistake — leak, or crash. And platform dependency. Code that worked on Windows could break on Unix.

For software meant to run on many devices, that was a nightmare. So they built something new. First called Oak. Later renamed Java — yes, after the coffee. The mission was clear: safer than C++, simpler to maintain, and portable across platforms.

In nineteen ninety-five, Java arrived with a bold promise. Write once. Run anywhere. And for an industry tired of rewriting the same code again and again… that promise mattered. Here's the secret. Watch carefully.

Java doesn't run directly on Windows or Mac. First, the compiler turns your source into bytecode — like an international language. Then the JVM — the Java Virtual Machine — translates that bytecode for your system.

Windows has a JVM. Mac has a JVM. Linux has a JVM. Same bytecode. Different translator. Same result. That's Write Once, Run Anywhere — for real. And that's why Java became infrastructure.

Banks need stability, not hype. Android needed a language millions already knew. Large backends needed scale that was battle-tested. Enterprise teams don't switch for trends. They switch when failure costs too much.

Java earned trust — one production system at a time. Alright — your first program. You write a public class. That's the blueprint. Inside it, public static void main — the entry point. The JVM starts here.

Then System.out.println — print a line to the console. Filename must match the class name. Java is case-sensitive. Don't forget that. Hit Run. Compiler to bytecode. JVM loads it. Finds main. Executes println.

Hello, World. Behind the scenes, the JVM did the heavy lifting — not Windows directly. Quick interview question. Why is Java platform independent? Answer like this: we compile to bytecode, not machine code.

Bytecode is platform-neutral. The JVM on each OS turns it into native instructions. Same class files. Windows, Mac, Linux — as long as a compatible JVM is there. So now you know why Java still runs the world.

Safer. Portable. Trusted at scale. But one mystery remains. When people say install Java… what are they actually installing? JDK. JRE. JVM — three names beginners mix up every day. That's Episode Two. I'll see you there.
