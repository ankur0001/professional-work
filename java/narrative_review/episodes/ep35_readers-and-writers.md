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

Imagine you open a customer export that contains names with accents, currency symbols, or text produced on another operating system. If you read it as raw bytes and casually turn those bytes into a `String` with the wrong encoding, the data is not "mostly fine." Characters break. Equality checks fail. Downstream reports look haunted. The bug is not in your business rule. It is in the boundary between byte streams and character streams — a boundary Java models on purpose.

So the question becomes: how does Java force that boundary into the open?

Readers and writers are character streams. Input streams and output streams are byte streams. When you mean text, prefer readers and writers — or higher helpers that still take an explicit charset. When you mean binary — images, compressed payloads, length-prefixed frames — stay with bytes. Mixing the two without an intentional decoder is how mojibake enters a codebase that "only deals with files."

```java
try (var w = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
    w.write("line one\n");
    w.write("line two\n");
}
```

Walk it. `newBufferedWriter` gives you a `Writer` already buffered, tied to a path, with UTF-8 named in the call. You write lines of text. Try-with-resources closes and flushes according to the resource contract. The charset is not an afterthought buried in platform defaults. It is part of the method call you can read in review and defend in a code review.

Buffering is not optional for performance once writes or reads happen in a loop. Unbuffered tiny writes — one character at a time straight to a cold OS call — can crush throughput on what looks like a simple export. Buffered readers and writers batch the expensive boundary crossing. You still must understand flush: buffering means "not necessarily on disk yet." If another process must see the data before close, flush intentionally. Close also flushes for well-behaved writers, which is another reason try-with-resources matters more than a casually forgotten `close()` at the bottom of a method.

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

Bytes arrive on `inputStream`. `InputStreamReader` decodes them with UTF-8 into characters. `BufferedReader` makes line-oriented reading practical. Each layer has one job. Skipping the charset argument is how you invite the default-encoding bug back in through a side door — the code looks sophisticated and still depends on whatever the JVM's default happens to be today.

What if we ignore the distinction and read text as raw bytes "because it is simpler"?

```java
byte[] raw = Files.readAllBytes(path);
String s = new String(raw); // default charset — portable programs regret this
```

It looks small. It is one of the classic portability traps. Prefer `Files.readString(path, StandardCharsets.UTF_8)` or an explicit decoding path. The rule is not ceremony. It is how text survives the trip between machines, containers, and developer laptops.

Flush and close semantics close the lesson. Writers may hold data in memory. Streams may hold native resources. If you neither flush nor close, another reader can see a truncated file, and the process can leak handles. If you flush obsessively after every character, you may be correct and still slow. Intention beats habit: buffer by default, flush when a checkpoint is required, close with try-with-resources.

Another pressure appears in loops that write many lines. People sometimes open a writer, then call a helper that opens another writer to the same file for each line — or they reopen the file in append mode thousands of times. The character-stream model is not only about encoding. It is about owning one writer for the lifetime of the export, buffering it, and closing it once. Performance and correctness travel together here.

What if the file is binary after all — a compressed archive or an image? Then a `Writer` is the wrong abstraction. You want `InputStream`/`OutputStream` or channel APIs, and you should not force binary through character decoders. The lesson is not "always use readers." The lesson is "match the stream family to the payload," and when the payload is text, name the charset out loud.

Once encoding is explicit, many "random" production text bugs stop looking random. They become missing charset arguments you can find in review.

Readers and writers also show up when bridging network sockets and files. Bytes arrive from the wire; characters leave into a log or CSV. The bridge is still an `InputStreamReader` or an explicit charset decode. Once you see that pattern, "we had encoding issues in production" becomes a missing bridge, not a mysterious platform curse.

 Prefer explicit charset in every text boundary you own — files, sockets, and stdout redirects in batch jobs. Defaults are convenient until they become an incident.

So reconnect the chain. Filesystem helpers made paths easy. Character versus byte streams made encoding visible. Buffering made the boundary affordable. Explicit charset made text portable. Bridges like `InputStreamReader` connected the two worlds without pretending they are the same.

Until now, our programs have mostly walked one path of execution from `main` downward. Real systems often need more than one path at once — a background worker, a concurrent request, a timer — and that is where threads enter the story.

Episode Thirty-Six begins there.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 35 (*Readers and Writers*).

Narration technique: encoding-corruption situation → readers/writers vs bytes → buffered writer walkthrough → InputStreamReader bridge → default charset trap → flush/close → next natural problem (threads).
