# Episode 51 — Class Loading

| Field | Value |
|---|---|
| Episode | 51 |
| Title | Class Loading |
| Catalog handbook column | 51 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Virtual threads closed a long concurrency arc. A quieter question has been waiting since the beginning: when you run a program, how do classes actually appear inside the JVM? You write source, compile to bytecode, and somehow `main` runs. Between "bytecode on disk" and "code the CPU can execute" sits class loading — lazy, layered, and responsible for a family of mysterious errors.

Classes appear lazily. Understanding loaders explains `ClassNotFoundException` and `NoClassDefFoundError` mysteries that look identical until you know what failed when.

Start from a deliberate load:

```java
Class<?> c = Class.forName("com.ex.App");
System.out.println(c.getClassLoader());
```

`Class.forName` asks the JVM to load, link, and initialize the named class if needed, then returns a `Class` object. Printing the class loader shows which loader defined it. Classes are not all dumped into one flat bag at startup. They arrive through loaders with parents and responsibilities.

The usual hierarchy is bootstrap, platform, and application loaders. The bootstrap loader knows the most fundamental JDK classes. The platform loader covers other modular JDK content. The application loader finds your classpath or module path types. Parent delegation is the rule of thumb: ask the parent loader first before loading a class yourself. That keeps core types unique and prevents user code from casually replacing `String` with a rogue version.

Custom loaders — plugin systems, containers — complicate it, but the delegation instinct remains: prefer parents for shared types so identity stays coherent. Two classes with the same binary name loaded by different loaders are different runtime types. That fact alone explains entire categories of "but they look the same!" cast failures in plugin architectures.

Loading is only one phase. Linking verifies bytecode and prepares memory structures. Verification checks that the bytecode obeys JVM safety rules — stack discipline, type constraints — so the runtime can trust it. Initialization runs static initializers. Forcing eager init everywhere can slow startup; lazy init can defer surprises until first use. Know that `Class.forName` and first active use are moments when initialization can run.

Metaspace holds class metadata — not your ordinary object heap. When you generate or load huge numbers of classes, metaspace pressure can become its own incident story. Dynamic loading has costs: more classes, more metadata, more chances for classpath order surprises. "Memory" is not only `-Xmx`.

Classpath order surprises are legendary. Two JARs contain different versions of a type; the first one wins. The code compiles against one version and runs against another. `ClassNotFoundException` often means a loader could not find the bytes. `NoClassDefFoundError` often means the JVM previously failed to initialize or link a class that the compiler thought existed. The names are not interchangeable.

A container incident makes the loader story concrete. The app JAR expects a library class. The image's classpath omits that JAR version. At compile time on a developer machine everything resolved. At runtime first use fails. Printing loaders and examining the layered classpath turns "works on my machine" into a diff you can fix.

What if two plugins each ship a different version of the same library and each uses its own loader? Same names, different types, confusing `ClassCastException`. Identity is loader plus name, not name alone.

Dynamic proxies and generated subclasses multiply classes at runtime. Frameworks do this constantly. Each generated class consumes metaspace and must be loadable under the right loader. When a framework says "add this agent" or "open this module," it is often speaking loader and linkage language.

Initialization order can also bite: static fields that call code which loads more classes which initialize more statics. Keep static initializers boring. Picture an application that fails on first request with `NoClassDefFoundError` for a class that "is clearly in the JAR." Often static initialization threw earlier, the JVM marked the class failed, and later use reports `NoClassDefFoundError`. Reading the first failure in the log matters more than staring at the second.

Hold a practical checklist: know which loader owns your application types; treat linkage errors as phase failures, not random noise; watch metaspace when generating classes; make classpath contents an explicit deployment concern.

The next natural hunger is what those bytes actually contain — the JVM's instruction language itself.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 51 (*Class Loading*).

Narration technique: how-classes-appear situation → forName/loaders → parent delegation → link/verify/init → metaspace → next natural problem (bytecode).
