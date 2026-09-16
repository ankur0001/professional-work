# Episode 51 — Class Loading

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty showed virtual threads running your code. But how does the JVM find and load that code in the first place? Every class file travels through loading, linking, and initialization.

ClassLoader hierarchy — bootstrap, platform, application — delegates upward. Linkage verifies bytecode and prepares static fields. Today — class loading basics, the loader tree, and initialization traps.

Episode Fifty-One. Class Loading Basics. Three built-in loaders in the JDK class-loading hierarchy. Bootstrap ClassLoader — loads core JDK classes from modules and rt.jar legacy. Written in native code — returns null from getClassLoader on its classes.

Platform ClassLoader — JDK modules not on the boot path. Application ClassLoader — loads classes from the classpath and module path. Default context loader for app code — Thread.currentThread getContextClassLoader.

Loading — find the bytecode and define the Class object. findClass reads bytes — defineClass creates the runtime Class metadata. Parent delegation — child asks parent first before loading itself.

Prevents duplicate class definitions across loaders. Custom ClassLoader — override findClass for hot reload or plugin jars. Class.forName triggers loading — does not initialize by default.

Linking has three sub-phases — verification, preparation, resolution. Verification — bytecode safety checks — stack map tables, type rules. Preparation — allocate static field memory, set primitives to zero, refs to null.

Resolution — replace symbolic references with direct references — often lazy. Linking happens after loading, before initialization. Failed verification throws VerifyError — class never runs.

Initialization — run the static initializer and assign static fields. Triggered on first active use — new, static field access, static method call. Class.forName with initialize true runs clinit.

JVM guarantees clinit runs exactly once per class per loader. Parent classes initialize before children. Deadlocks possible if static blocks acquire locks in circular order. The delegation model in practice.

Application loader asks platform — platform asks bootstrap. Only if parent cannot find the class does the child attempt loadClass. SPI pattern breaks delegation — Thread context class loader.

ServiceLoader uses context loader to find provider implementations. Understand which loader owns a class — affects visibility and casting. Three common mistakes. One — Class.forName in static blocks causing initialization cycles.

Two — assuming custom loaders without parent delegation — security risk. Three — mixing classes from different loaders — ClassCastException at runtime. Also — leaking ClassLoader references — PermGen or metaspace leaks in old apps.

Class loading is infrastructure — get the loader boundaries right. Interview question — explain class loading phases? Loading — find bytes, define Class. Linking — verify, prepare, resolve.

Initialization — run static initializer on first active use. Bootstrap, platform, application — parent delegation model. Custom ClassLoader for plugins — override findClass, delegate to parent.

Mention Class.forName versus ClassLoader loadClass initialize flag. Classes load from bytecode — but what is inside those class files? Episode Fifty-Two — Bytecode Basics. Opcodes, constant pool, and reading javap output.

See you there.
