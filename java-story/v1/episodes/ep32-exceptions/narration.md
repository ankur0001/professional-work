# Episode 32 — Exceptions

**Cut:** v1 (original)

## Transcript (from captions)

Programs fail. Networks drop. Files vanish. Users type nonsense. Exceptions are Java way of signaling that something went wrong. Not every error is a crash — some are expected and recoverable.

Checked exceptions force you to acknowledge risk at compile time. Unchecked exceptions flag programming bugs and broken assumptions. Today — how Java models failure, and how to handle it with intent.

Episode Thirty-Two. Exceptions — checked, unchecked, and handling failure. Throwable sits at the root of the error hierarchy. Error is for serious JVM problems — you rarely catch these.

Exception is what application code usually deals with. RuntimeException and its subclasses are unchecked. Everything else under Exception is checked — the compiler enforces handling.

Know the hierarchy before you catch broadly. try wraps code that might throw. catch handles a specific exception type — order matters, most specific first. You can catch multiple types in one block since Java seven.

Handle what you can recover from — log, retry, or return a safe default. Swallowing exceptions silently is almost always wrong. A narrow catch beats catch Exception everywhere. throws declares that a method may propagate an exception.

Callers must handle checked exceptions — try-catch or declare throws. Unchecked exceptions do not require a throws clause. Document what can go wrong — throws is part of the contract.

Do not use throws to push problems up without a plan. Sometimes wrapping a checked exception in an unchecked one is cleaner. finally runs whether the try block succeeds or throws. Classic use — release resources in a finally block.

Modern code prefers try-with-resources — we cover that next episode. Do not return from finally — it can mask the real exception. finally is for cleanup that must happen no matter what.

Keep finally blocks short and predictable. Define custom exceptions when domain errors need clear names. Extend Exception for checked, RuntimeException for unchecked. Provide meaningful constructors — message, cause, both.

BankAccountOverdrawnException beats a generic IllegalStateException. Do not create an exception class for every trivial case. Good exception names read like answers to what went wrong.

Three common mistakes. One — catching Exception or Throwable and doing nothing useful. Two — using exceptions for normal control flow — they are expensive. Three — throwing generic RuntimeException without context or cause.

Also — empty catch blocks that hide production bugs. Fail loudly in development. Handle deliberately in production. Interview question — checked versus unchecked exceptions? Checked — compiler requires handling or declaring throws.

Unchecked — extends RuntimeException, no compile-time enforcement. Checked for recoverable conditions callers should know about. Unchecked for programming errors and broken invariants.

Mention try-with-resources for cleanup — that shows modern Java. You know how to catch failure. Next — how to close resources safely. Episode Thirty-Three — try-with-resources. AutoCloseable, suppressed exceptions, and leak-free I/O.

See you there.
