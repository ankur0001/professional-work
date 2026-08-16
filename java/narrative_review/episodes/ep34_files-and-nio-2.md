# Episode 34 — Files and NIO.2

| Field | Value |
|---|---|
| Episode | 34 |
| Title | Files and NIO.2 |
| Catalog handbook column | 34 |
| Narration source script | `make_episode_34.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. java.io.File is legacy — platform strings and limited operations.
2. Java seven brought NIO point two — Path, Files, and a modern file API.
3. Paths are immutable value objects — combine, resolve, normalize safely.
4. Files is a static utility class — read, write, copy, delete in one call.
5. Works with try-with-resources for streams when you need more control.
6. Today — filesystem operations without the old File headaches.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Four.
2. Files and NIO point two — the modern filesystem API.

### Scene `paths` (renderer: `paths`)

1. Path replaces File as the primary filesystem reference.
2. Paths.get builds a path from strings — or use Path.of since Java eleven.
3. resolve combines segments. normalize removes dot-dot clutter.
4. getParent, getFileName, startsWith — rich path algebra.
5. Paths are not tied to the default filesystem — use a FileSystem for jars or memory.
6. Think Path for location, Files for operations.

### Scene `readwrite` (renderer: `readwrite`)

1. Files.readAllBytes loads an entire file into a byte array.
2. Files.readString reads text with a charset — UTF eight by default since Java eighteen.
3. Files.writeString and write dump content in one shot — great for small files.
4. For large files, use newInputStream and newOutputStream with try-with-resources.
5. copy, move, and delete are one-liners with sensible options.
6. Choose convenience methods for small files — streams for big data.

### Scene `walk` (renderer: `walk`)

1. Files.walk traverses a directory tree as a Stream of Path.
2. Filter with stream operations — find all dot java files, skip hidden dirs.
3. walk with maxDepth limits how deep you recurse.
4. Files.list is for a single directory — non-recursive.
5. Always close streams from walk and list — or use try-with-resources.
6. Tree walking plus Streams is powerful for build tools and log scanners.

### Scene `attrs` (renderer: `attrs`)

1. Files.readAttributes returns metadata — size, timestamps, permissions.
2. BasicFileAttributes covers the common case across platforms.
3. exists, isDirectory, isRegularFile — quick checks without exceptions.
4. createDirectories creates parent folders as needed.
5. createTempFile and createTempDirectory for scratch space.
6. Metadata queries keep you from reinventing stat calls.

### Scene `copy` (renderer: `copy`)

1. Files.copy transfers data between paths with CopyOption flags.
2. REPLACE_EXISTING overwrites the target if it already exists.
3. Files.move renames or relocates — atomic on the same filesystem.
4. Files.delete and deleteIfExists remove files — IOException if not empty dir.
5. StandardCopyOption and LinkOption control behavior across platforms.
6. One-liner file operations beat hand-rolled stream copying for common cases.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using readAllBytes on multi-gigabyte files — out of memory.
3. Two — forgetting to close walk or list streams — file handle leaks.
4. Three — mixing Path with string concatenation instead of resolve.
5. Also — assuming default charset instead of specifying StandardCharsets.
6. Match the API to file size and encoding needs.

### Scene `interview` (renderer: `interview`)

1. Interview question — Path versus File, and when to use Files?
2. Path is immutable and NIO-based — File is legacy.
3. Files provides static helpers — read, write, copy, walk.
4. Mention try-with-resources for streams on large files.
5. Note walk returns a Stream that must be closed.
6. That answer shows modern filesystem fluency.

### Scene `teaser` (renderer: `teaser`)

1. Bytes and paths are covered. Next — text streams the classic way.
2. Episode Thirty-Five — Readers, Writers, and Text I/O.
3. BufferedReader, PrintWriter, and character encoding done right.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **34** — *Files and NIO.2*.
- **Series catalog:** Episode 34 ↔ handbook lesson 34 — *Files and NIO.2*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _java.io.File is legacy — platform strings and limited operations._
- **`title`** — starts from: _Episode Thirty-Four._
- **`paths`** — starts from: _Path replaces File as the primary filesystem reference._
- **`readwrite`** — starts from: _Files.readAllBytes loads an entire file into a byte array._
- **`walk`** — starts from: _Files.walk traverses a directory tree as a Stream of Path._
- **`attrs`** — starts from: _Files.readAttributes returns metadata — size, timestamps, permissions._
- **`copy`** — starts from: _Files.copy transfers data between paths with CopyOption flags._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — Path versus File, and when to use Files?_
- **`teaser`** — starts from: _Bytes and paths are covered. Next — text streams the classic way._
