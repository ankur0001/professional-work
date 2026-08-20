# Episode 03 — Java Program Structure

| Field | Value |
|---|---|
| Episode | 03 |
| Title | Java Program Structure |
| Catalog handbook column | 3 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Two named the platform layers — JDK, JRE, JVM.
2. Now open any Java file in your editor.
3. Every line has a job — package, imports, class, fields, methods, statements.
4. Structure is not decoration.
5. It decides how code is found, compiled, loaded, tested, scanned by frameworks, and owned by teams.
6. Today we read a Java program like a map — slowly, line by line.

### Scene `title` (renderer: `title`)

1. Episode Three.
2. Java Program Structure — packages, classes, and the entry point.
3. By the end you'll see hierarchy, access, and runtime identity in one picture.

### Scene `anatomy` (renderer: `anatomy`)

1. Here is the shape Java expects.
2. At the top — optional package declaration. That is your namespace on disk and in bytecode.
3. Then imports — shortcuts to types defined elsewhere.
4. A top-level type — usually a public class. One public class per file, filename must match.
5. Inside the class — fields for state, constructors to create valid objects, methods for behavior, nested types when needed.
6. Below that — blocks and statements inside methods.
7. Think tree: package, then type, then members, then statements.
8. Tools — compilers, IDEs, Spring — all assume this hierarchy.

### Scene `hello` (renderer: `hello`)

1. Walk a classic program — slowly, because every piece maps to a real rule.
```java
package com.example.app;

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

2. Line one: package com.example.app — this type's fully qualified name starts here.
3. Folders under src/main/java should mirror that path — com/example/app/HelloWorld.java.
4. public class HelloWorld — the public class name and filename must match. Java is case-sensitive.
5. public static void main(String[] args) — the JVM entry point. public so the launcher sees it. static so it runs without constructing an object first.
6. String[] args — command-line arguments as an array of strings.
7. System.out.println — one statement, terminated by semicolon, printing a line to standard output.
8. Tiny file. Four layers of structure. One runnable program.

### Scene `access` (renderer: `access`)

1. Access is part of structure — not a later topic.
2. public — visible everywhere. Use for intentional API surface.
3. No modifier — package-private. Same package only. Perfect for internal collaborators.
4. private — only this class. Default for fields.
5. protected — package plus subclasses — we'll deepen that in Episode Eleven.
6. Good structure hides what should not leak — and keeps public APIs small.
7. If everything is public, you have no boundary — only hope.

### Scene `packages` (renderer: `packages`)

1. In real services, packages mirror ownership.
2. api — controllers, DTOs, public HTTP contracts.
3. application — use-case orchestration.
4. domain — business rules and entities.
5. infrastructure — databases, messaging, external adapters.
6. Dependency arrows should point inward — domain should not import JDBC types.
7. Flat util packages with two hundred classes erase ownership — and make cyclic imports inevitable.
8. Structure expresses who owns what — and what must not depend on what.

### Scene `flow` (renderer: `flow`)

1. Follow runtime with structure in mind.
2. Load class by fully qualified name. Verify bytecode. Prepare static fields. Run static initializers. Construct objects. Invoke methods.
3. Your package and class names become the identity the classloader loads.
4. com.example.orders.Order and com.other.orders.Order are different types — even if both are called Order.
5. Class identity is name plus classloader — matters in app servers, plugins, and Spring devtools.
6. Static fields live with class metadata. Instance fields live in heap objects. Locals live in stack frames.
7. Structure you write becomes layout and lifecycle at runtime — indirectly but reliably.

### Scene `deeper` (renderer: `deeper`)

1. Go one level deeper — domain example with validation in the constructor.
```java
package com.example.orders.domain;

public final class Order {
    private final String id;
    private final long amountInCents;

    public Order(String id, long amountInCents) {
        if (amountInCents < 0) {
            throw new IllegalArgumentException("amount must be non-negative");
        }
        this.id = id;
        this.amountInCents = amountInCents;
    }

    public boolean isHighValue() {
        return amountInCents >= 100_00;
    }
}
```

2. private final fields — state encapsulated, reassignment blocked on the reference.
3. Constructor validates amountInCents — invalid objects cannot exist.
4. isHighValue encodes a domain rule next to the data it protects — better than scattered comparisons in controllers.
5. This is structure serving design — not ceremony.
6. Spring Boot later scans from your main class package downward — root package choice is architectural.

### Scene `imports` (renderer: `imports`)

1. One more structural piece — imports.
2. import java.util.List brings a type into scope without fully qualifying every use.
3. Static imports exist for constants and static methods — use sparingly.
4. Star imports — import java.util.* — save typing but hide origin in reviews.
5. Most teams prefer explicit imports — IDE manages them anyway.
6. Imports are compile-time convenience. Runtime identity is always fully qualified.

### Scene `blocks` (renderer: `blocks`)

1. Static initializer block — static { ... } — runs once when class loaded.
2. Instance initializer block — { ... } — runs before constructor body every new.
3. Use static blocks sparingly — hard to test, hide I/O — prefer static factory methods.
4. Single-class demos skip package — production code always declares package.
5. Multiple top-level classes in one file — only one public, rest package-private — rare style.
6. Text blocks for multi-line strings in main — JSON fixtures in tutorials — Java 15+.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — every class in one giant package. Ownership and test boundaries disappear.
3. Two — public mutable fields — encapsulation dies, invariants impossible.
4. Three — burying @SpringBootApplication too deep so component scanning misses half your beans.
5. Also — hiding I/O inside constructors — hard to test, surprising side effects on new.
6. Fix structure early — refactors across package boundaries hurt later.

### Scene `interview` (renderer: `interview`)

1. Interview question — why do packages matter?
2. Namespacing — avoid class name collisions.
3. Access control — package-private collaboration.
4. Ownership — teams and modules align to packages.
5. Framework scanning — Spring Boot starts from the application class package.
6. Add — class identity is fully qualified name plus defining classloader.
7. That answer connects syntax to architecture — interviewers notice.

### Scene `spring_boot` (renderer: `spring_boot`)

1. Spring Boot @SpringBootApplication combines configuration, component scan, auto-configuration.
2. Main class package defines scan root — com.example.orders pulls in com.example.orders.* beans.
3. Moving a @Service to com.example.other without moving main — bean may never register.
4. Multiple modules in one repo — each may have own main — only one bootstraps per process.
5. Tests use @SpringBootTest — loads context — slow because structure and classpath matter.
6. Slice tests — @WebMvcTest — load smaller vertical slice — faster feedback on structure choices.

### Scene `connect` (renderer: `connect`)

1. Variables and types next — fields and parameters in this structure get concrete types.
2. Access modifiers episode revisits visibility we previewed today.
3. Packages episode zooms into namespace we declared at top of every file.

### Scene `summary` (renderer: `summary`)

1. Let's land the plane.
2. Java programs organize as packages, types, members, and statements.
3. Filename matches public class. main is the conventional entry.
4. Access modifiers encode boundaries. Package layout encodes ownership.
5. Runtime loads by fully qualified names — structure is not cosmetic.
6. You can read a Java file as a map now — not a wall of keywords.

### Scene `teaser` (renderer: `teaser`)

1. You can read the skeleton. Next — what lives inside those fields and methods.
2. Episode Four — Variables and Data Types.
3. Primitives, references, money traps, and memory shape.
4. See you there.
_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

(reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **3** — *Java Program Structure*.
- **Series catalog:** Episode 03 ↔ handbook lesson 3 — *Java Program Structure*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- **Narration expansion:** Spoken lines expanded for **4–15 minute** conversational runtime; handbook still used as topic reference.

### Handbook concepts reused (from recovered Lesson 3 excerpt)

- A Java program is organized into packages, types, fields, methods, constructors, blocks, and statements. Structure is not cosmetic; it affects access control, class loading, dependency boundaries, testability, modularity, and framework scanning.
- Java's structure was built around classes from the beginning. Over time, the platform added annotations, generics, enums, lambdas, records, sealed classes, and modules. Enterprise frameworks such as Spring made annotations and package organization central to a
- Unstructured codebases become hard to test, deploy, and reason about. Poor package boundaries create cyclic dependencies, leaky domain models, unclear ownership, and fragile framework configuration. Senior engineers must design structure that expresses busines
- Java provides packages for namespacing, classes for behavior and state, interfaces for contracts, access modifiers for encapsulation, and annotations for metadata. This lets teams scale code ownership while giving tools enough structure for compilation, refact
- The compiler maps each top-level type to bytecode. Packages become naming conventions in fully qualified class names. Access checks are enforced by the compiler and verified by the JVM. Annotations may be retained in class files and read reflectively by framew
- The JVM loads classes by fully qualified name. Class identity is the combination of class name and defining classloader. This matters in application servers, plugins, test frameworks, hot reload tools, and Spring Boot devtools.

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 3).

### Scene ↔ curriculum intent

- **`hook`** — continuity from JDK layers
- **`title`** — episode promise
- **`anatomy`** — program hierarchy
- **`hello`** — HelloWorld line-by-line
- **`access`** — access modifiers primer
- **`packages`** — production package layout
- **`flow`** — load-init-invoke runtime
- **`deeper`** — domain Order example
- **`mistakes`** — common mistakes
- **`interview`** — packages interview
- **`summary`** — revision
- **`teaser`** — bridge to Episode 04

- **Runtime note:** Narration expanded for a **4–15 minute** conversational lesson (aim ~8–12) with a worked example — not the ultra-short headline cut.
