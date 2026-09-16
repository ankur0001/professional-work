# Episode 03 — Java Program Structure

**Cut:** v1 (original)

## Transcript (from captions)

In Episode Two, we separated JDK, JRE, and JVM. Now look at a real Java file. Every line has a job — package, class, main, statements. Structure is not decoration. It decides how your code is found, loaded, tested, and owned.

Episode Three. Java Program Structure — packages, classes, and the entry point. Here is the shape of a Java program. A package is the folder — the namespace. Inside it — a type. Usually a class. Sometimes an interface, record, or enum.

Inside the class — fields for state, constructors to create objects, methods for behavior. That hierarchy is the blueprint Java expects — and tools rely on. Walk a classic Hello World — line by line.

First, optional package — the fully qualified home of the class. Then public class HelloWorld — and yes, the filename must match. Java is case-sensitive. HelloWorld.java means HelloWorld — not helloworld.

public static void main — the JVM starts here. System.out.println — a statement that prints a line. Four jobs. Four layers. One program. Access is part of structure too. public means other packages can see it.

No modifier means package-private — same package only. Perfect for helpers. private fields keep state inside the class. Good structure hides what shouldn't leak — and makes APIs smaller.

In real services, packages mirror ownership. api at the edge — controllers and DTOs. application to orchestrate use-cases. domain for business rules. infrastructure for databases and adapters.

Arrows should point inward — not dump everything into one flat folder. That is how teams keep domain code clean as the service grows. Follow runtime. Load the class. Verify bytecode. Prepare statics.

Initialize. Construct objects. Invoke methods. Your package and class names become the identity the JVM loads. Same simple name in two packages? Completely different classes. Three common mistakes.

One — every class in one giant package. Ownership disappears. Two — public fields everywhere — no encapsulation, hard to change later. Three — Spring main class buried too deep, so component scanning misses your beans.

Put the main class at a sensible root — and keep infrastructure out of domain. Interview question — why do packages matter? Answer with four words on screen. Namespacing. Access. Ownership. Framework scanning.

Then add — class identity is the name plus the classloader. That answer shows you understand design and runtime — not just syntax. You can now read a Java file like a map. Next — variables and data types.

int, long, boolean, String — what lives where in memory. Episode Four. See you there.
