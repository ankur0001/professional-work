# Episode 19 — Sealed Classes

**Cut:** v1 (original)

## Transcript (from captions)

Records cleaned up data carriers. Hierarchies still sprawl. Anyone can subclass. Switches stay incomplete. Domain rules leak. Sealed classes close the set of permitted subtypes. You design the family. The compiler enforces the guest list.

Today — sealed types, permits, and exhaustive switches that finally trust you. Controlled inheritance — not inheritance theater. Episode Nineteen. Sealed Classes — controlled hierarchies.

A sealed class or interface restricts who may extend or implement it. You list permitted subtypes with permits. Those subtypes must be in the same module — or the same package if unnamed.

Final, sealed, or non-sealed — each child declares how open it remains. The hierarchy becomes a deliberate design artifact. Open by accident is the bug sealed types fix. Look at the shape.

sealed interface Shape permits Circle, Rectangle, Triangle. Circle can be final. Rectangle can be sealed further. Triangle can be non-sealed. non-sealed reopens extension for that branch only.

You keep control at the root and choose where flexibility returns. That is intentional polymorphism — not a free-for-all. Exhaustive switch is the payoff. Switch on a sealed Shape — cover Circle, Rectangle, Triangle.

No default required when every permitted type is handled. Add a new subtype later — the compiler forces you to update the switches. That is safer evolution than hoping teams remember every if-else.

Pattern matching and sealed types were built to work together. When sealed types shine. Domain models with a closed set of variants — payments, events, AST nodes. APIs where third parties should not invent new subtypes.

When not — frameworks that need open extension points, or libraries that invite plugins. Sealed is a design decision, not a default for every interface. Close the hierarchy when completeness matters more than openness.

Records and sealed types pair beautifully. sealed interface Result permits Ok, Err. record Ok of value. record Err of message. Compact data plus a closed variant set. Your switch becomes documentation that the compiler checks.

That is modern Java modeling — small, explicit, enforceable. Three common mistakes. One — sealing too early, then fighting every new legitimate subtype. Two — forgetting non-sealed when a branch truly needs open extension.

Three — relying on default in switches and losing exhaustiveness warnings. Also — putting permitted types in the wrong package or module. Sealed types reward careful package and module boundaries.

Interview question — what problem do sealed classes solve? They restrict which types may extend a hierarchy. That enables exhaustive switches and safer domain modeling. Mention permits, and final versus sealed versus non-sealed subtypes.

Tie it to pattern matching for a modern answer. That shows language design awareness — not just syntax. Hierarchies can be closed. Next — how code is packaged for the JVM. Episode Twenty — modules and JPMS.

Requires, exports, and strong encapsulation. See you there.
