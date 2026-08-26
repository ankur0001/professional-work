# Episode 34 — Files and NIO.2

| Field | Value |
|---|---|
| Episode | 34 |
| Title | Files and NIO.2 |
| Catalog handbook column | 34 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Try-with-resources made opening and closing honest. The next question is what we open when the thing we care about is a path on disk.

Suppose a batch job must write a short status file after each run and read yesterday's status at startup. Older Java pushed you toward `java.io.File` plus streams glued together by hand. It works. It is also noisy, easy to get charset-wrong, and awkward for walking a tree or moving a file into place atomically. What is the modern way Java talks to the filesystem?

NIO.2 answers with `Path` and `Files`. Prefer them for new code. `File` is legacy you will still meet in maintenance; it is not the model you should reach for first.

```java
Path p = Path.of("data", "status.txt");
Files.createDirectories(p.getParent());
Files.writeString(p, "ok\n");
String s = Files.readString(p);
```

`Path.of(...)` builds a location, not the bytes themselves. Creating parent directories makes the write robust when the folder structure is part of the job. `Files.writeString` and `Files.readString` hide boilerplate while still throwing clear I/O exceptions when the world disagrees. Combined with try-with-resources for streams when you need finer control, this is the everyday filesystem vocabulary.

Charset is the quiet requirement inside those helpers. Text is not "just bytes with letters on them." Assume the default charset, and a machine in another locale — or a container with a different default — can reinterpret your file:

```java
Files.writeString(p, "café\n", StandardCharsets.UTF_8);
String again = Files.readString(p, StandardCharsets.UTF_8);
```

When you drop to stream APIs, carry the same discipline: pick an intentional charset instead of hoping defaults match production.

Walking appears as soon as "one file" becomes "a directory of inputs":

```java
try (var paths = Files.walk(Path.of("incoming"))) {
    paths.filter(path -> path.toString().endsWith(".csv"))
         .forEach(path -> System.out.println(path));
}
```

`Files.walk` gives you a stream of paths. Close the stream — try-with-resources again — because walking can hold directory resources. Express filesystem intent without hand-rolling recursion badly.

Atomic move matters the first time you publish a file safely. Write to a temporary sibling, then move into the final name so readers never see a half-written file:

```java
Path tmp = Path.of("data", "status.txt.tmp");
Path finalPath = Path.of("data", "status.txt");
Files.writeString(tmp, "ok\n", StandardCharsets.UTF_8);
Files.move(tmp, finalPath, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);
```

On some filesystems, "atomic move" has constraints — especially across storage volumes. Treat atomic rename as a tool with documented limits, not as a spell that always works the way your laptop's disk did in development.

Path traversal is the security sibling. If any part of a path comes from user input, `../../etc/passwd` is not a cute edge case — it is an attack. Resolve and normalize against a known root, and reject paths that escape it. NIO.2 makes path math clearer; it does not make untrusted input safe by itself.

Common mistakes line up with those pressures. Default charset corrupts text across environments. Not handling `NoSuchFileException` turns a missing input into an opaque crash at the wrong layer. Blindly concatenating user strings into paths invites traversal.

What if we keep using `new File("data.txt")` and manual streams for every new feature? You can ship. You will also keep re-solving charset, recursive listing, and move semantics with one-off utilities that disagree with each other. `Path` and `Files` concentrate those answers in one modern vocabulary.

Existence checks, size, and copy read as ordinary operations — and that readability is part of correctness, because reviewers can see intent without decoding a ritual of streams for a simple copy. Prefer NIO.2 for new code even when a teammate reaches for `File` out of habit. Translation layers between `Path` and `File` should be boundaries, not the center of new design.

One more habit: `Files.deleteIfExists` is intentionally forgiving; `Files.delete` is not. Choosing between them is a product decision about whether absence is normal. NIO.2 gives you the verbs — your domain decides which verb matches the invariant.

And yet reading and writing "strings" still hides a deeper split: sometimes the payload is text, and sometimes it is raw bytes. Bridging those worlds — and doing it efficiently — is the next pressure.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 34 (*Files and NIO.2*).

Narration technique: status-file situation → Path/Files → charset → walk → atomic move → traversal → next natural problem (readers/writers).
