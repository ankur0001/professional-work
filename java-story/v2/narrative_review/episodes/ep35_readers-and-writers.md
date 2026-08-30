# Episode 35 — Readers and Writers

| Field | Value |
|---|---|
| Episode | 35 |
| Title | Readers and Writers |
| Catalog handbook column | 35 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

NIO.2 gave us paths and helpers. The helpers are polite enough that you can forget an older, sharper lesson: text is not bytes.

Imagine you open a customer export that contains names with accents or text produced on another operating system. If you read it as raw bytes and casually turn those bytes into a `String` with the wrong encoding, characters break, equality checks fail, and downstream reports look haunted. The bug is not in your business rule. It is in the boundary between byte streams and character streams — a boundary Java models on purpose.

So how does Java force that boundary into the open?

Readers and writers are character streams. Input streams and output streams are byte streams. When you mean text, prefer readers and writers — or higher helpers that still take an explicit charset. When you mean binary — images, compressed payloads, length-prefixed frames — stay with bytes. Mixing the two without an intentional decoder is how mojibake enters a codebase that "only deals with files."

```java
try (var w = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
    w.write("line one\n");
    w.write("line two\n");
}
```

`newBufferedWriter` gives you a buffered `Writer` tied to a path, with UTF-8 named in the call. Try-with-resources closes and flushes according to the resource contract. The charset is not buried in platform defaults — it is part of the method call you can defend in review.

Buffering is not optional for performance once writes happen in a loop. Unbuffered tiny writes — one character at a time straight to a cold OS call — can crush throughput on what looks like a simple export. You still must understand flush: buffering means "not necessarily on disk yet." If another process must see the data before close, flush intentionally. Close also flushes for well-behaved writers, which is another reason try-with-resources matters.

`InputStreamReader` is the bridge when you already have bytes and need characters:

```java
try (var reader = new BufferedReader(
        new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
    String line;
    while ((line = reader.readLine()) != null) {
        process(line);
    }
}
```

Bytes arrive on `inputStream`. `InputStreamReader` decodes them with UTF-8. `BufferedReader` makes line-oriented reading practical. Each layer has one job. Skipping the charset argument invites the default-encoding bug back through a side door — the code looks sophisticated and still depends on whatever the JVM's default happens to be today.

What if we ignore the distinction and read text as raw bytes "because it is simpler"?

```java
byte[] raw = Files.readAllBytes(path);
String s = new String(raw); // default charset — portable programs regret this
```

It looks small. Prefer `Files.readString(path, StandardCharsets.UTF_8)` or an explicit decoding path. The rule is how text survives the trip between machines, containers, and developer laptops.

Flush and close semantics close the lesson. Writers may hold data in memory. Streams may hold native resources. Neither flush nor close, and another reader sees a truncated file. Flush obsessively after every character, and you may be correct and still slow. Buffer by default, flush when a checkpoint is required, close with try-with-resources.

Another pressure appears in loops that write many lines. People sometimes reopen the file in append mode for each line. The character-stream model is not only about encoding — it is about owning one writer for the lifetime of the export, buffering it, and closing it once.

What if the file is binary after all — a compressed archive or an image? Then a `Writer` is the wrong abstraction. Match the stream family to the payload, and when the payload is text, name the charset out loud.

Once encoding is explicit, many "random" production text bugs stop looking random. They become missing charset arguments you can find in review. The same bridge shows up for network sockets: bytes arrive from the wire; characters leave into a log or CSV. Prefer explicit charset in every text boundary you own — files, sockets, and batch stdout. Defaults are convenient until they become an incident.

Until now, our programs have mostly walked one path of execution from `main` downward. Real systems often need more than one path at once — a background worker, a concurrent request, a timer — and that is where threads enter the story.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 35 (*Readers and Writers*).

Narration technique: encoding-corruption situation → readers/writers vs bytes → buffered writer → InputStreamReader → default charset trap → flush/close → next natural problem (threads).
