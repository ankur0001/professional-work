# Episode 03 — Java Program Structure

| Field | Value |
|---|---|
| Episode | 03 |
| Title | Java Program Structure |
| Catalog handbook column | 3 |
| Narration source script | `make_episode_03.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. In Episode Two, we separated JDK, JRE, and JVM.
2. Now look at a real Java file.
3. Every line has a job — package, class, main, statements.
4. Structure is not decoration.
5. It decides how your code is found, loaded, tested, and owned.

### Scene `title` (renderer: `title`)

1. Episode Three.
2. Java Program Structure — packages, classes, and the entry point.

### Scene `anatomy` (renderer: `anatomy`)

1. Here is the shape of a Java program.
2. A package is the folder — the namespace.
3. Inside it — a type. Usually a class. Sometimes an interface, record, or enum.
4. Inside the class — fields for state, constructors to create objects, methods for behavior.
5. That hierarchy is the blueprint Java expects — and tools rely on.

### Scene `hello` (renderer: `hello`)

1. Walk a classic Hello World — line by line.
2. First, optional package — the fully qualified home of the class.
3. Then public class HelloWorld — and yes, the filename must match.
4. Java is case-sensitive. HelloWorld.java means HelloWorld — not helloworld.
5. public static void main — the JVM starts here.
6. System.out.println — a statement that prints a line.
7. Four jobs. Four layers. One program.

### Scene `access` (renderer: `access`)

1. Access is part of structure too.
2. public means other packages can see it.
3. No modifier means package-private — same package only. Perfect for helpers.
4. private fields keep state inside the class.
5. Good structure hides what shouldn't leak — and makes APIs smaller.

### Scene `packages` (renderer: `packages`)

1. In real services, packages mirror ownership.
2. api at the edge — controllers and DTOs.
3. application to orchestrate use-cases.
4. domain for business rules. infrastructure for databases and adapters.
5. Arrows should point inward — not dump everything into one flat folder.
6. That is how teams keep domain code clean as the service grows.

### Scene `flow` (renderer: `flow`)

1. Follow runtime.
2. Load the class. Verify bytecode. Prepare statics.
3. Initialize. Construct objects. Invoke methods.
4. Your package and class names become the identity the JVM loads.
5. Same simple name in two packages? Completely different classes.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — every class in one giant package. Ownership disappears.
3. Two — public fields everywhere — no encapsulation, hard to change later.
4. Three — Spring main class buried too deep, so component scanning misses your beans.
5. Put the main class at a sensible root — and keep infrastructure out of domain.

### Scene `interview` (renderer: `interview`)

1. Interview question — why do packages matter?
2. Answer with four words on screen.
3. Namespacing. Access. Ownership. Framework scanning.
4. Then add — class identity is the name plus the classloader.
5. That answer shows you understand design and runtime — not just syntax.

### Scene `teaser` (renderer: `teaser`)

1. You can now read a Java file like a map.
2. Next — variables and data types.
3. int, long, boolean, String — what lives where in memory.
4. Episode Four. See you there.

_Total beats: **49** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **3** — *Java Program Structure*.
- **Series catalog:** Episode 03 ↔ handbook lesson 3 — *Java Program Structure*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 3 excerpt)

- A Java program is organized into packages, types, fields, methods, constructors, blocks, and statements. Structure is not cosmetic; it affects access control, class loading, dependency boundaries, testability, modularity, and framework scanning.
- Java's structure was built around classes from the beginning. Over time, the platform added annotations, generics, enums, lambdas, records, sealed classes, and modules. Enterprise frameworks such as Spring made annotations and package organization central to a
- Unstructured codebases become hard to test, deploy, and reason about. Poor package boundaries create cyclic dependencies, leaky domain models, unclear ownership, and fragile framework configuration. Senior engineers must design structure that expresses busines
- Java provides packages for namespacing, classes for behavior and state, interfaces for contracts, access modifiers for encapsulation, and annotations for metadata. This lets teams scale code ownership while giving tools enough structure for compilation, refact
- The compiler maps each top-level type to bytecode. Packages become naming conventions in fully qualified class names. Access checks are enforced by the compiler and verified by the JVM. Annotations may be retained in class files and read reflectively by framew
- The JVM loads classes by fully qualified name. Class identity is the combination of class name and defining classloader. This matters in application servers, plugins, test frameworks, hot reload tools, and Spring Boot devtools.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 3).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _In Episode Two, we separated JDK, JRE, and JVM._
- **`title`** — starts from: _Episode Three._
- **`anatomy`** — starts from: _Here is the shape of a Java program._
- **`hello`** — starts from: _Walk a classic Hello World — line by line._
- **`access`** — starts from: _Access is part of structure too._
- **`packages`** — starts from: _In real services, packages mirror ownership._
- **`flow`** — starts from: _Follow runtime._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — why do packages matter?_
- **`teaser`** — starts from: _You can now read a Java file like a map._
