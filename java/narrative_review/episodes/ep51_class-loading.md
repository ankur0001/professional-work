# Episode 51 — Class Loading

| Field | Value |
|---|---|
| Episode | 51 |
| Title | Class Loading |
| Catalog handbook column | 51 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Virtual threads closed a long concurrency arc. A quieter question has been waiting since Episode One: when you run a program, how do classes actually appear inside the JVM? You write source, compile to bytecode, and somehow `main` runs. Between "bytecode on disk" and "code the CPU can execute" sits class loading — lazy, layered, and responsible for a family of mysterious errors.

Classes appear lazily. Understanding loaders explains `ClassNotFoundException` and `NoClassDefFoundError` mysteries that look identical until you know what failed when.

Start from a deliberate load:

```java
Class<?> c = Class.forName("com.ex.App");
System.out.println(c.getClassLoader());
```

Walk it. `Class.forName` asks the JVM to load, link, and initialize the named class if needed, then returns a `Class` object. Printing the class loader shows which loader defined it. That one line makes an invisible process visible: classes are not all dumped into one flat bag at startup. They arrive through loaders with parents and responsibilities.

The usual hierarchy is bootstrap, platform, and application loaders. The bootstrap loader knows the most fundamental JDK classes. The platform loader covers other modular JDK content. The application loader finds your classpath or module path types. Parent delegation is the rule of thumb: ask the parent loader first before loading a class yourself. That keeps core types unique and prevents user code from casually replacing `String` with a rogue version.

```text
Application loader
    ↑ delegates to
Platform loader
    ↑ delegates to
Bootstrap loader
```

Hold the picture lightly. Custom loaders — plugin systems, containers — complicate it, but the delegation instinct remains: prefer parents for shared types so identity stays coherent. Two classes with the same binary name loaded by different loaders are different runtime types. That fact alone explains entire categories of "but they look the same!" cast failures in plugin architectures.

Loading is only one phase. Linking verifies bytecode and prepares memory structures. Verification checks that the bytecode obeys JVM safety rules — stack discipline, type constraints — so the runtime can trust it. Initialization runs static initializers. Forcing eager init everywhere can slow startup and surface static failures earlier than you wanted; lazy init can defer surprises until first use. Neither extreme is always right. Know that `Class.forName` and first active use are moments when initialization can run.

Metaspace holds class metadata — not your ordinary object heap. When you generate or load huge numbers of classes, metaspace pressure can become its own incident story. Dynamic loading has costs and risks: more classes, more metadata, more chances for classpath order surprises. You do not need every metaspace flag today. You need curiosity that "memory" is not only `-Xmx`.

Classpath order surprises are legendary. Two JARs contain different versions of a type; the first one wins. The code compiles against one version and runs against another. Parent delegation and modularization try to tame that chaos; they do not excuse ignoring what your loader graph actually sees. Linkage errors ignored until production — `NoClassDefFoundError` when a class was present at compile time but failed during init or is missing at runtime — are how teams learn loaders the hard way.

What if we treat class loading as "classpath magic" and never look?

Then every loader-related incident becomes folklore. Printing the loader, reading the exception carefully, and knowing delegation give you a map. `ClassNotFoundException` often means a loader could not find the bytes. `NoClassDefFoundError` often means the JVM previously failed to initialize or link a class that the compiler thought existed. The names are not interchangeable.

A container incident makes the loader story concrete. The app JAR expects a library class. The image's classpath omits that JAR version. At compile time on a developer machine everything resolved. At runtime `Class.forName` or first use fails. Printing loaders and examining the layered classpath — or module graph — turns "works on my machine" into a diff you can fix. Class loading is not academic taxonomy. It is how deployment disagreements become exceptions.

Dynamic proxies and generated subclasses multiply classes at runtime. Frameworks do this constantly. Each generated class consumes metaspace and must be loadable under the right loader. When a framework says "add this agent" or "open this module," it is often speaking loader and linkage language. Curiosity about those messages beats pasting flags blindly.

What if two plugins each ship a different `com.google.Guava` and each uses its own loader? Same names, different types, confusing `ClassCastException`. Parent delegation and shared parent loaders exist to reduce that pain for core types; plugin systems still have to design sharing deliberately. Identity is loader plus name, not name alone.

Hold a practical checklist: know which loader owns your application types; treat linkage errors as phase failures, not random noise; watch metaspace when generating classes; make classpath/module contents an explicit deployment concern. Meet those and class loading becomes a map instead of a myth.

Initialization order can also bite: static fields that call code which loads more classes which initialize more statics. Keep static initializers boring. Laziness is not only a performance idea — it is a way to keep startup failure modes local.

Picture a springing application that fails on first request with `NoClassDefFoundError` for a class that "is clearly in the JAR." Often static initialization threw earlier, the JVM marked the class failed, and later use reports `NoClassDefFoundError`. Reading the first failure in the log matters more than staring at the second. Loaders and initialization phases turn that drama into a sequence you can debug.

So reconnect the chain. We asked how classes appear. Loaders and parent delegation answered with a hierarchy. Linking, verification, and initialization showed phases beyond finding bytes. Metaspace and dynamic loading marked costs. Classpath order and linkage errors showed failure modes. The next natural hunger is what those bytes actually contain — the JVM's language itself.

Episode Fifty-Two: bytecode basics.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 51 (*Class Loading*).

Narration technique: how-classes-appear situation → forName/loaders → parent delegation → link/verify/init → metaspace → mistakes → next natural problem (bytecode).
