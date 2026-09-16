# Episode 05 — Operators

**Cut:** v1 (original)

## Transcript (from captions)

In Episode Four, we chose types carefully. Now those values meet operators — plus, equals, and, or. Small symbols. Large consequences. Overflow, equality bugs, and null crashes often start here.

Episode Five. Operators — arithmetic, equality, and short-circuit logic. Three families you use every day. Arithmetic — plus, minus, multiply, divide. Relational — less than, greater than, equals-equals.

Logical — and, or, not — decisions that branch your code. Java evaluates left to right. Parentheses remove guesswork. The classic trap — equality. For primitives, equals-equals compares values. Fine.

For objects, equals-equals compares references — same object in memory? For String content — use equals. Never equals-equals for text you care about. Safer pattern — put the literal first. PAID dot equals status.

That avoids a null pointer if status is null. Short-circuit logic protects you. Double ampersand — and. Double pipe — or. If the left side already decides the answer, the right side never runs.

user not null and user is active — the second call only happens when user exists. Single ampersand does not short-circuit. That difference causes real bugs. Use short-circuit when the second check is expensive — or unsafe.

Arithmetic looks innocent. int can silently wrap on overflow — no exception by default. For money limits and counters, silent wrap is dangerous. Prefer Math dot addExact when overflow must fail loudly.

Or use long — and still think about the upper bound. Payment systems choose exact math for a reason. The ternary operator — question mark colon. condition question result-if-true colon result-if-false.

Great for simple choices. Terrible for nested puzzles. If the expression needs a paragraph of comments — extract a method instead. Architect tip — order can be cancelled beats a pile of operators copied everywhere.

Three common mistakes. One — equals-equals for String content. Two — ignoring integer overflow until production numbers get big. Three — side effects stuffed inside clever expressions. Hard to read. Hard to debug.

Also — trusting operator precedence instead of parentheses. Be kind to the next reader. Interview question — equals-equals versus equals? Answer cleanly. Equals-equals — references for objects. Values for primitives.

Equals — logical equality defined by the type. Then add — short-circuit and protects null. That shows production sense. Operators decide. Next we control the path. Episode Six — control flow.

if, else, switch, loops — how programs choose and repeat. See you there.
