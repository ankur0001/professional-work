# Episode 35 — Readers and Writers

**Cut:** v1 (original)

## Transcript (from captions)

Bytes are raw. Text is encoded — characters mapped to bytes by a charset. Reader and Writer are the character-stream abstractions in java.io. InputStreamReader bridges bytes to characters. OutputStreamWriter the reverse.

Always specify a charset — never rely on the platform default silently. BufferedReader adds readLine — the workhorse for line-oriented text. Today — reading and writing text the classic, still-relevant way.

Episode Thirty-Five. Readers, Writers, and Text I/O. Reader reads characters — abstract base for text input. InputStreamReader wraps an InputStream with a Charset decoder. FileReader is a convenience shortcut — but hides charset choice.

Prefer Files.newBufferedReader with StandardCharsets.UTF_8. read returns an int — minus one means end of stream. Character streams handle encoding — byte streams do not. BufferedReader wraps any Reader with an internal buffer.

readLine returns one line without the newline — null at end of file. lines since Java eight returns a Stream of lines — lazy and closeable. Buffering reduces system calls — essential for file and network reads.

Process line by line for log files and CSV — not readAll at once. Always use try-with-resources with BufferedReader. PrintWriter is a character-output wrapper with print and println.

It can auto-flush on println — useful for interactive output. Wrap a FileWriter or OutputStreamWriter with explicit charset. Files.newBufferedWriter is the NIO convenience — UTF eight default.

printf-style formatting is available but String.format is often clearer. Flush before close when downstream consumers need immediate data. Files.readAllLines loads every line into a List — fine for small files.

Files.lines returns a Stream — better for large text with lazy processing. write with a charset writes a collection of lines with a newline separator. Combine NIO Path with classic Reader and Writer when you need flexibility.

For config and data files, UTF eight is the modern default. Pick the API level that matches file size and processing style. A charset maps characters to bytes — UTF eight is the universal default.

StandardCharsets.UTF_8 is a constant — never rely on defaultCharset blindly. InputStreamReader and OutputStreamWriter require an explicit Charset. Mojibake happens when reader and writer disagree on encoding.

Files methods accept a Charset parameter — pass it every time. Explicit encoding prevents bugs that only appear in production. Three common mistakes. One — using platform default charset — breaks across environments.

Two — readAllLines on huge files — memory explosion. Three — forgetting to close Reader or Writer — handle leaks. Also — mixing byte and character APIs on the same stream. Explicit charset, buffering, and try-with-resources every time.

Interview question — Reader versus InputStream? InputStream reads raw bytes — Reader reads decoded characters. Bridge with InputStreamReader and a specified Charset. BufferedReader adds readLine and buffering for efficiency.

Mention UTF eight and try-with-resources. That answer shows text I/O literacy. Text I/O is sorted. Next — doing work in parallel. Episode Thirty-Six — Threads Introduction. Runnable, thread lifecycle, and why concurrency is hard.

See you there.
