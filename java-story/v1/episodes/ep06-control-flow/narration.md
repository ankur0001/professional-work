# Episode 06 — Control Flow

**Cut:** v1 (original)

## Transcript (from captions)

Operators decide values. Control flow decides the path. Which statements run? How often? When do we exit? In production, unclear branching becomes missed edge cases — and messy failures.

Today we make the path visible — and keep it flat. Episode Six. Control Flow — if, switch, loops, and clean exits. Start with if — but prefer guard clauses. Validate early. Reject early. Return early.

Flat code beats a pyramid of nested else blocks. If not valid — return. If not authorized — deny. Then process the happy path. Readable. Testable. Kind to the next engineer. When cases are finite — switch shines.

Modern Java has switch expressions — they produce a value. Arrow labels. No accidental fall-through. Perfect for statuses — PENDING, PAID, CANCELLED. If you are still writing classic switch with missing breaks — upgrade the habit.

Finite states belong in switch. Open-ended rules belong in methods. Loops repeat work. for when you know the bounds. while when you wait on a condition. for-each when you walk a collection cleanly.

break exits. continue skips to the next iteration. Watch unbounded loops — they become production incidents. And avoid allocating heavy objects on every iteration in hot paths. Exceptions are for exceptional paths — not everyday outcomes.

try, catch, finally — and try-with-resources for cleanup. Open a file or connection inside try-with-resources — Java closes it for you. Do not throw exceptions to mean not found on every request. That is control flow wearing a costume.

Reserve exceptions for failures you cannot express as a normal return. Picture a production request. Validate. Authorize. Process. Commit. Respond. On failure — compensate or retry with clear rules.

Good control flow makes normal and failure paths equally obvious. Hidden branches are where incidents hide. Three common mistakes. One — deeply nested branches that hide the real intent.

Two — missing break in legacy switch — fall-through bugs. Three — exceptions for common outcomes. Expensive and confusing. Also — putting whole business workflows inside controllers. Extract the flow.

Interview question — when do you use a switch expression? Answer — finite, clear cases that produce a value. Then add — prefer guard clauses over nesting. And try-with-resources for deterministic cleanup.

That package of answers sounds senior. Paths are clear. Next we package behavior. Episode Seven — methods. Parameters, return types, overloading — how code becomes reusable. See you there.
