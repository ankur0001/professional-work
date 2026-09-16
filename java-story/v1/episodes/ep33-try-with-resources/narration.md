# Episode 33 — try-with-resources

**Cut:** v1 (original)

## Transcript (from captions)

Open a file. Read data. Crash before close. The handle leaks. Resource leaks are silent killers — connections, streams, locks. Manual finally blocks help, but they are easy to get wrong.

Java seven introduced try-with-resources — automatic cleanup. Declare resources in the try header — close happens on the way out. Today — leak-free I/O and the AutoCloseable contract.

Episode Thirty-Three. try-with-resources — automatic resource management. A resource is anything that must be released — files, sockets, JDBC connections. Forgetting close under an exception path leaks OS handles.

Leaks accumulate until the system runs out — then everything fails. finally was the old answer — always call close in finally. But what if close itself throws? Nested try-finally gets ugly fast.

try-with-resources exists to make the right thing the easy thing. The syntax is try with resources in parentheses. Each resource must implement AutoCloseable or Closeable. Resources are closed in reverse order of declaration.

Close runs after the try block — success or exception. You can still use catch and finally alongside the try header. One line of syntax replaces fragile cleanup boilerplate. AutoCloseable defines void close throws Exception.

Most I/O classes already implement it — FileInputStream, BufferedReader, Connection. Your own types can implement AutoCloseable for RAII-style cleanup. close should be idempotent — safe to call more than once.

Document whether your close is thread-safe. Implement AutoCloseable when your object owns a scarce resource. What if the try block throws and close also throws? The primary exception is thrown — close exception is suppressed.

Call getSuppressed on the thrown exception to inspect it. This preserves the original failure while recording cleanup trouble. Before Java seven, the close exception often masked the real one.

Suppressed exceptions are a quiet but important design detail. Declare multiple resources separated by semicolons in one try header. They initialize left to right — close happens right to left.

Typical pattern — open an InputStream and a Reader together. Each resource must be final or effectively final. Nested try-with-resources works but one header is usually clearer. Multiple resources — one cleanup block, zero leaks.

Three common mistakes. One — opening a resource outside try-with-resources and hoping close happens. Two — implementing close that swallows errors without logging. Three — returning from inside the try block before resources finish closing.

Also — forgetting that resources close in reverse declaration order. Let the language close for you — do not fight the pattern. Interview question — how does try-with-resources work?

Resources declared in try are closed automatically via AutoCloseable. Close runs in reverse order after the try block exits. If both try and close throw, primary wins — close is suppressed.

Mention it replaced most hand-written finally cleanup. That answer shows you write leak-resistant Java. Resources close themselves. Next — the modern file API. Episode Thirty-Four — Files and NIO point two.

Paths, walking trees, and reading bytes without the old File class. See you there.
