# Episode 51 — Class Loading

| Field | Value |
|---|---|
| Episode | 51 |
| Title | Class Loading |
| Catalog handbook column | 51 |
| Narration source script | `make_episode_51.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty showed virtual threads running your code.
2. But how does the JVM find and load that code in the first place?
3. Every class file travels through loading, linking, and initialization.
4. ClassLoader hierarchy — bootstrap, platform, application — delegates upward.
5. Linkage verifies bytecode and prepares static fields.
6. Today — class loading basics, the loader tree, and initialization traps.

### Scene `title` (renderer: `title`)

1. Episode Fifty-One.
2. Class Loading Basics.

### Scene `classloader_hierarchy` (renderer: `classloader_hierarchy`)

1. Three built-in loaders in the JDK class-loading hierarchy.
2. Bootstrap ClassLoader — loads core JDK classes from modules and rt.jar legacy.
3. Written in native code — returns null from getClassLoader on its classes.
4. Platform ClassLoader — JDK modules not on the boot path.
5. Application ClassLoader — loads classes from the classpath and module path.
6. Default context loader for app code — Thread.currentThread getContextClassLoader.

### Scene `loading` (renderer: `loading`)

1. Loading — find the bytecode and define the Class object.
2. findClass reads bytes — defineClass creates the runtime Class metadata.
3. Parent delegation — child asks parent first before loading itself.
4. Prevents duplicate class definitions across loaders.
5. Custom ClassLoader — override findClass for hot reload or plugin jars.
6. Class.forName triggers loading — does not initialize by default.

### Scene `linking` (renderer: `linking`)

1. Linking has three sub-phases — verification, preparation, resolution.
2. Verification — bytecode safety checks — stack map tables, type rules.
3. Preparation — allocate static field memory, set primitives to zero, refs to null.
4. Resolution — replace symbolic references with direct references — often lazy.
5. Linking happens after loading, before initialization.
6. Failed verification throws VerifyError — class never runs.

### Scene `initialization` (renderer: `initialization`)

1. Initialization — run the static initializer and assign static fields.
2. Triggered on first active use — new, static field access, static method call.
3. Class.forName with initialize true runs clinit.
4. JVM guarantees clinit runs exactly once per class per loader.
5. Parent classes initialize before children.
6. Deadlocks possible if static blocks acquire locks in circular order.

### Scene `delegation_model` (renderer: `delegation_model`)

1. The delegation model in practice.
2. Application loader asks platform — platform asks bootstrap.
3. Only if parent cannot find the class does the child attempt loadClass.
4. SPI pattern breaks delegation — Thread context class loader.
5. ServiceLoader uses context loader to find provider implementations.
6. Understand which loader owns a class — affects visibility and casting.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — Class.forName in static blocks causing initialization cycles.
3. Two — assuming custom loaders without parent delegation — security risk.
4. Three — mixing classes from different loaders — ClassCastException at runtime.
5. Also — leaking ClassLoader references — PermGen or metaspace leaks in old apps.
6. Class loading is infrastructure — get the loader boundaries right.

### Scene `interview` (renderer: `interview`)

1. Interview question — explain class loading phases?
2. Loading — find bytes, define Class. Linking — verify, prepare, resolve.
3. Initialization — run static initializer on first active use.
4. Bootstrap, platform, application — parent delegation model.
5. Custom ClassLoader for plugins — override findClass, delegate to parent.
6. Mention Class.forName versus ClassLoader loadClass initialize flag.

### Scene `teaser` (renderer: `teaser`)

1. Classes load from bytecode — but what is inside those class files?
2. Episode Fifty-Two — Bytecode Basics.
3. Opcodes, constant pool, and reading javap output.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **56** — *Class Loading*.
- **Series catalog mapping:** Episode 51 / catalog column `51` / published title *Class Loading*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 56 → episode 51). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty showed virtual threads running your code._
- **`title`** — starts from: _Episode Fifty-One._
- **`classloader_hierarchy`** — starts from: _Three built-in loaders in the JDK class-loading hierarchy._
- **`loading`** — starts from: _Loading — find the bytecode and define the Class object._
- **`linking`** — starts from: _Linking has three sub-phases — verification, preparation, resolution._
- **`initialization`** — starts from: _Initialization — run the static initializer and assign static fields._
- **`delegation_model`** — starts from: _The delegation model in practice._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — explain class loading phases?_
- **`teaser`** — starts from: _Classes load from bytecode — but what is inside those class files?_
