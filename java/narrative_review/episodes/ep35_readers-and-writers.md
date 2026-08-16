# Episode 35 — Readers and Writers

| Field | Value |
|---|---|
| Episode | 35 |
| Title | Readers and Writers |
| Catalog handbook column | 35 |
| Narration source script | `make_episode_35.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Bytes are raw. Text is encoded — characters mapped to bytes by a charset.
2. Reader and Writer are the character-stream abstractions in java.io.
3. InputStreamReader bridges bytes to characters. OutputStreamWriter the reverse.
4. Always specify a charset — never rely on the platform default silently.
5. BufferedReader adds readLine — the workhorse for line-oriented text.
6. Today — reading and writing text the classic, still-relevant way.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Five.
2. Readers, Writers, and Text I/O.

### Scene `reader` (renderer: `reader`)

1. Reader reads characters — abstract base for text input.
2. InputStreamReader wraps an InputStream with a Charset decoder.
3. FileReader is a convenience shortcut — but hides charset choice.
4. Prefer Files.newBufferedReader with StandardCharsets.UTF_8.
5. read returns an int — minus one means end of stream.
6. Character streams handle encoding — byte streams do not.

### Scene `buffered` (renderer: `buffered`)

1. BufferedReader wraps any Reader with an internal buffer.
2. readLine returns one line without the newline — null at end of file.
3. lines since Java eight returns a Stream of lines — lazy and closeable.
4. Buffering reduces system calls — essential for file and network reads.
5. Process line by line for log files and CSV — not readAll at once.
6. Always use try-with-resources with BufferedReader.

### Scene `printwriter` (renderer: `printwriter`)

1. PrintWriter is a character-output wrapper with print and println.
2. It can auto-flush on println — useful for interactive output.
3. Wrap a FileWriter or OutputStreamWriter with explicit charset.
4. Files.newBufferedWriter is the NIO convenience — UTF eight default.
5. printf-style formatting is available but String.format is often clearer.
6. Flush before close when downstream consumers need immediate data.

### Scene `files` (renderer: `files`)

1. Files.readAllLines loads every line into a List — fine for small files.
2. Files.lines returns a Stream — better for large text with lazy processing.
3. write with a charset writes a collection of lines with a newline separator.
4. Combine NIO Path with classic Reader and Writer when you need flexibility.
5. For config and data files, UTF eight is the modern default.
6. Pick the API level that matches file size and processing style.

### Scene `charset` (renderer: `charset`)

1. A charset maps characters to bytes — UTF eight is the universal default.
2. StandardCharsets.UTF_8 is a constant — never rely on defaultCharset blindly.
3. InputStreamReader and OutputStreamWriter require an explicit Charset.
4. Mojibake happens when reader and writer disagree on encoding.
5. Files methods accept a Charset parameter — pass it every time.
6. Explicit encoding prevents bugs that only appear in production.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using platform default charset — breaks across environments.
3. Two — readAllLines on huge files — memory explosion.
4. Three — forgetting to close Reader or Writer — handle leaks.
5. Also — mixing byte and character APIs on the same stream.
6. Explicit charset, buffering, and try-with-resources every time.

### Scene `interview` (renderer: `interview`)

1. Interview question — Reader versus InputStream?
2. InputStream reads raw bytes — Reader reads decoded characters.
3. Bridge with InputStreamReader and a specified Charset.
4. BufferedReader adds readLine and buffering for efficiency.
5. Mention UTF eight and try-with-resources.
6. That answer shows text I/O literacy.

### Scene `teaser` (renderer: `teaser`)

1. Text I/O is sorted. Next — doing work in parallel.
2. Episode Thirty-Six — Threads Introduction.
3. Runnable, thread lifecycle, and why concurrency is hard.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **35** — *Readers and Writers*.
- **Series catalog:** Episode 35 ↔ handbook lesson 35 — *Readers and Writers*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Bytes are raw. Text is encoded — characters mapped to bytes by a charset._
- **`title`** — starts from: _Episode Thirty-Five._
- **`reader`** — starts from: _Reader reads characters — abstract base for text input._
- **`buffered`** — starts from: _BufferedReader wraps any Reader with an internal buffer._
- **`printwriter`** — starts from: _PrintWriter is a character-output wrapper with print and println._
- **`files`** — starts from: _Files.readAllLines loads every line into a List — fine for small files._
- **`charset`** — starts from: _A charset maps characters to bytes — UTF eight is the universal default._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — Reader versus InputStream?_
- **`teaser`** — starts from: _Text I/O is sorted. Next — doing work in parallel._
