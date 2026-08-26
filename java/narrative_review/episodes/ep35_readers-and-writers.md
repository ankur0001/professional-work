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

Imagine you open a file that contains names with accents, or currency symbols, or text produced on another operating system. If you read it as raw bytes and casually turn those bytes into a `String` with the wrong encoding, the data is not "mostly fine." Characters break. Comparisons fail. Logs look haunted. The bug is not in your business rule. It is in the boundary between byte streams and character streams.

So the question becomes: how does Java force that boundary into the open?

Readers and writers are character streams. Input streams and output streams are byte streams. When you mean text, prefer readers and writers — or higher helpers that still take an explicit charset. When you mean binary — images, compressed payloads, protobuf — stay with bytes.

```java
try (var w = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
    w.write("line\n");
}
```

Walk it. `newBufferedWriter` gives you a `Writer` already buffered, tied to a path, with UTF-8 named in the call. You write a line of text. Try-with-resources closes and flushes according to the resource contract. The charset is not an afterthought buried in platform defaults. It is part of the method call you can read in review.

Buffering is not optional for performance once writes or reads happen in a loop. Unbuffered tiny writes — one character at a time to a cold OS call — can crush throughput. Buffered readers and writers batch the expensive boundary crossing. You still must understand flush: buffering means "not necessarily on disk yet." If another process must see the data before close, flush intentionally. Close also flushes for well-behaved writers, which is another reason try-with-resources matters.

`InputStreamReader` is the bridge when you already have bytes and need characters:

```java
try (var reader = new BufferedReader(
        new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
    String line = reader.readLine();
}
```

Bytes arrive on `inputStream`. `InputStreamReader` decodes them with UTF-8 into characters. `BufferedReader` makes line-oriented reading practical. Each layer has one job. Skipping the charset argument is how you invite the default-encoding bug back in through a side door.

What if we ignore the distinction and read text as raw bytes "because it is simpler"?

```java
byte[] raw = Files.readAllBytes(path);
String s = new String(raw); // default charset — portable programs regret this
```

It looks small. It is one of the classic portability traps. Prefer `Files.readString(path, StandardCharsets.UTF_8)` or an explicit decoding path. The rule is not ceremony. It is how text survives the trip between machines.

Flush and close semantics close the lesson. Writers may hold data in memory. Streams may hold native resources. If you neither flush nor close, another reader can see a truncated file, and the process can leak handles. If you flush obsessively after every character, you may be correct and still slow. Intention beats habit: buffer by default, flush when a checkpoint is required, close with try-with-resources.

So reconnect the chain. Filesystem helpers made paths easy. Character versus byte streams made encoding visible. Buffering made the boundary affordable. Explicit charset made text portable. Bridges like `InputStreamReader` connected the two worlds without pretending they are the same.

Until now, our programs have mostly walked one path of execution from `main` downward. Real systems often need more than one path at once — a background worker, a concurrent request, a timer — and that is where threads enter the story.

Episode Thirty-Six begins there.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 35 (*Readers and Writers*).

Narration technique: encoding-corruption situation → readers/writers vs bytes → buffered writer walkthrough → InputStreamReader bridge → default charset trap → flush/close → next natural problem (threads).
