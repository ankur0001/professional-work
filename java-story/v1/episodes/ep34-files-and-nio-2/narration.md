# Episode 34 — Files and NIO.2

**Cut:** v1 (original)

## Transcript (from captions)

java.io.File is legacy — platform strings and limited operations. Java seven brought NIO point two — Path, Files, and a modern file API. Paths are immutable value objects — combine, resolve, normalize safely.

Files is a static utility class — read, write, copy, delete in one call. Works with try-with-resources for streams when you need more control. Today — filesystem operations without the old File headaches.

Episode Thirty-Four. Files and NIO point two — the modern filesystem API. Path replaces File as the primary filesystem reference. Paths.get builds a path from strings — or use Path.of since Java eleven.

resolve combines segments. normalize removes dot-dot clutter. getParent, getFileName, startsWith — rich path algebra. Paths are not tied to the default filesystem — use a FileSystem for jars or memory.

Think Path for location, Files for operations. Files.readAllBytes loads an entire file into a byte array. Files.readString reads text with a charset — UTF eight by default since Java eighteen.

Files.writeString and write dump content in one shot — great for small files. For large files, use newInputStream and newOutputStream with try-with-resources. copy, move, and delete are one-liners with sensible options.

Choose convenience methods for small files — streams for big data. Files.walk traverses a directory tree as a Stream of Path. Filter with stream operations — find all dot java files, skip hidden dirs.

walk with maxDepth limits how deep you recurse. Files.list is for a single directory — non-recursive. Always close streams from walk and list — or use try-with-resources. Tree walking plus Streams is powerful for build tools and log scanners.

Files.readAttributes returns metadata — size, timestamps, permissions. BasicFileAttributes covers the common case across platforms. exists, isDirectory, isRegularFile — quick checks without exceptions.

createDirectories creates parent folders as needed. createTempFile and createTempDirectory for scratch space. Metadata queries keep you from reinventing stat calls. Files.copy transfers data between paths with CopyOption flags.

REPLACE_EXISTING overwrites the target if it already exists. Files.move renames or relocates — atomic on the same filesystem. Files.delete and deleteIfExists remove files — IOException if not empty dir.

StandardCopyOption and LinkOption control behavior across platforms. One-liner file operations beat hand-rolled stream copying for common cases. Three common mistakes. One — using readAllBytes on multi-gigabyte files — out of memory.

Two — forgetting to close walk or list streams — file handle leaks. Three — mixing Path with string concatenation instead of resolve. Also — assuming default charset instead of specifying StandardCharsets.

Match the API to file size and encoding needs. Interview question — Path versus File, and when to use Files? Path is immutable and NIO-based — File is legacy. Files provides static helpers — read, write, copy, walk.

Mention try-with-resources for streams on large files. Note walk returns a Stream that must be closed. That answer shows modern filesystem fluency. Bytes and paths are covered. Next — text streams the classic way.

Episode Thirty-Five — Readers, Writers, and Text I/O. BufferedReader, PrintWriter, and character encoding done right. See you there.
