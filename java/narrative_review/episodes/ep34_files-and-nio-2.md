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

Suppose a batch job must write a short status file and read it back later. Older Java pushed you toward `java.io.File` plus streams glued together by hand. It works. It is also noisy, easy to get charset-wrong, and awkward for modern path operations like walking a tree or moving a file atomically. So teams kept asking: what is the modern way Java talks to the filesystem?

NIO.2 answers with `Path` and `Files`. Prefer them for new code. `File` is legacy you will still meet; it is not the model you should reach for first.

```java
Path p = Path.of("data.txt");
Files.writeString(p, "hello");
String s = Files.readString(p);
```

Walk the idea. `Path.of("data.txt")` builds a path value — a location, not the bytes themselves. `Files.writeString` writes text to that location. `Files.readString` reads it back. The helpers hide a lot of boilerplate while still throwing clear I/O exceptions when the world disagrees. Combined with try-with-resources for streams when you need them, this is the everyday filesystem vocabulary.

Charset is the quiet requirement inside those helpers. Text is not "just bytes with letters on them." If you assume the default charset, a machine in another locale — or a container with a different default — can reinterpret your file. Be explicit when the content is text meant to travel. When you drop to stream APIs, carry the same discipline: pick `UTF_8` (or another intentional charset) instead of hoping defaults match production.

Walking and globbing appear as soon as "one file" becomes "a directory of inputs":

```java
try (var paths = Files.walk(Path.of("incoming"))) {
    paths.filter(path -> path.toString().endsWith(".csv"))
         .forEach(path -> System.out.println(path));
}
```

`Files.walk` gives you a stream of paths. Filter to the names you care about. Close the stream — try-with-resources again — because walking can hold directory resources. Glob helpers exist for pattern matching when the pattern is the point. The design goal is the same: express filesystem intent without hand-rolling recursion badly.

Atomic move caveats matter the first time you try to publish a file safely. You write to a temp path, then move into the final name so readers never see a half-written file. On some systems and filesystems, "atomic move" has constraints — especially across storage volumes. The API lets you request options; the operating system still has the last word. Treat atomic rename as a tool with documented limits, not as a spell.

Path traversal is the security sibling of these APIs. If any part of a path comes from user input, a string like `../../etc/passwd` is not a cute edge case — it is an attack. Resolve and normalize against a known root, and reject paths that escape it. NIO.2 makes path math clearer; it does not make untrusted input safe by itself.

Common mistakes line up with those pressures. Assuming default charset corrupts text across environments. Not handling `NoSuchFileException` turns a missing input into an opaque crash. Blindly concatenating user strings into paths invites traversal. None of these are advanced topics. They are the cost of treating the filesystem as a dumb string bag.

So reconnect the chain. We needed a modern filesystem vocabulary. `Path` and `Files` provided it. Charset kept text honest. Walk and glob scaled to directories. Atomic moves and traversal showed production edges. Legacy `File` can wait in maintenance code; new design should start with NIO.2.

And yet reading and writing "strings" still hides a deeper split: sometimes the payload is text, and sometimes it is raw bytes. Bridging those worlds — and doing it efficiently — is the job of readers, writers, and the streams underneath them.

That is Episode Thirty-Five.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 34 (*Files and NIO.2*).

Narration technique: status-file situation → Path/Files as modern answer → charset → walk/glob → atomic move → traversal → mistakes → next natural problem (readers/writers).
