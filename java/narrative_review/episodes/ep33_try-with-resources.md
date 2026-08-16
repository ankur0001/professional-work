# Episode 33 — try-with-resources

| Field | Value |
|---|---|
| Episode | 33 |
| Title | try-with-resources |
| Catalog handbook column | 33 |
| Narration source script | `make_episode_33.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Open a file. Read data. Crash before close. The handle leaks.
2. Resource leaks are silent killers — connections, streams, locks.
3. Manual finally blocks help, but they are easy to get wrong.
4. Java seven introduced try-with-resources — automatic cleanup.
5. Declare resources in the try header — close happens on the way out.
6. Today — leak-free I/O and the AutoCloseable contract.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Three.
2. try-with-resources — automatic resource management.

### Scene `leak` (renderer: `leak`)

1. A resource is anything that must be released — files, sockets, JDBC connections.
2. Forgetting close under an exception path leaks OS handles.
3. Leaks accumulate until the system runs out — then everything fails.
4. finally was the old answer — always call close in finally.
5. But what if close itself throws? Nested try-finally gets ugly fast.
6. try-with-resources exists to make the right thing the easy thing.

### Scene `syntax` (renderer: `syntax`)

1. The syntax is try with resources in parentheses.
2. Each resource must implement AutoCloseable or Closeable.
3. Resources are closed in reverse order of declaration.
4. Close runs after the try block — success or exception.
5. You can still use catch and finally alongside the try header.
6. One line of syntax replaces fragile cleanup boilerplate.

### Scene `autoclose` (renderer: `autoclose`)

1. AutoCloseable defines void close throws Exception.
2. Most I/O classes already implement it — FileInputStream, BufferedReader, Connection.
3. Your own types can implement AutoCloseable for RAII-style cleanup.
4. close should be idempotent — safe to call more than once.
5. Document whether your close is thread-safe.
6. Implement AutoCloseable when your object owns a scarce resource.

### Scene `suppressed` (renderer: `suppressed`)

1. What if the try block throws and close also throws?
2. The primary exception is thrown — close exception is suppressed.
3. Call getSuppressed on the thrown exception to inspect it.
4. This preserves the original failure while recording cleanup trouble.
5. Before Java seven, the close exception often masked the real one.
6. Suppressed exceptions are a quiet but important design detail.

### Scene `multi` (renderer: `multi`)

1. Declare multiple resources separated by semicolons in one try header.
2. They initialize left to right — close happens right to left.
3. Typical pattern — open an InputStream and a Reader together.
4. Each resource must be final or effectively final.
5. Nested try-with-resources works but one header is usually clearer.
6. Multiple resources — one cleanup block, zero leaks.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — opening a resource outside try-with-resources and hoping close happens.
3. Two — implementing close that swallows errors without logging.
4. Three — returning from inside the try block before resources finish closing.
5. Also — forgetting that resources close in reverse declaration order.
6. Let the language close for you — do not fight the pattern.

### Scene `interview` (renderer: `interview`)

1. Interview question — how does try-with-resources work?
2. Resources declared in try are closed automatically via AutoCloseable.
3. Close runs in reverse order after the try block exits.
4. If both try and close throw, primary wins — close is suppressed.
5. Mention it replaced most hand-written finally cleanup.
6. That answer shows you write leak-resistant Java.

### Scene `teaser` (renderer: `teaser`)

1. Resources close themselves. Next — the modern file API.
2. Episode Thirty-Four — Files and NIO point two.
3. Paths, walking trees, and reading bytes without the old File class.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **33** — *try-with-resources*.
- **Series catalog:** Episode 33 ↔ handbook lesson 33 — *try-with-resources*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Open a file. Read data. Crash before close. The handle leaks._
- **`title`** — starts from: _Episode Thirty-Three._
- **`leak`** — starts from: _A resource is anything that must be released — files, sockets, JDBC connections._
- **`syntax`** — starts from: _The syntax is try with resources in parentheses._
- **`autoclose`** — starts from: _AutoCloseable defines void close throws Exception._
- **`suppressed`** — starts from: _What if the try block throws and close also throws?_
- **`multi`** — starts from: _Declare multiple resources separated by semicolons in one try header._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how does try-with-resources work?_
- **`teaser`** — starts from: _Resources close themselves. Next — the modern file API._
