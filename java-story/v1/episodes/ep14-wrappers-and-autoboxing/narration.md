# Episode 14 — Wrappers and Autoboxing

**Cut:** v1 (original)

## Transcript (from captions)

Enums gave us type-safe states. Now look at numbers as objects. int is a primitive. Integer is a wrapper — an object that can be null. Autoboxing hides the conversion — and can hide costs and crashes.

Today we make that invisible work visible. Get this mental model right — collections depend on it. Lists and maps need objects — wrappers bridge that gap. Episode Fourteen. Wrappers and Autoboxing — objects around primitives.

Eight primitives. Eight wrappers. int and Integer. long and Long. boolean and Boolean. Wrappers live on the heap. They have identity. They can be null. Primitives cannot be null — and that alone prevents many bugs.

Choose intentionally — do not default to wrappers everywhere. Default to primitives unless nullability is required. Autoboxing converts automatically. Integer x equals ten — boxes the int.

int y equals x — unboxes the Integer. Convenient in Lists and Maps that need objects. Dangerous when x is null — unboxing throws NullPointerException. Null plus silent conversion is a classic production trap.

Wrappers cost more than primitives. Object header. Indirection. Extra allocations. A List of Integer can thrash the heap versus an int array. Hot loops that box every iteration pay a quiet tax.

Prefer primitives in hot paths. Use wrappers when null is a real signal. Measure before you box every number in a tight loop. One more quirk — Integer caching. Small values are often cached — so equals-equals may look true by accident.

Do not rely on that. Compare wrappers with equals. Autoboxing is not a reason to forget object equality rules. Be explicit — always. Three common mistakes. One — unboxing a null wrapper into a primitive.

Two — using wrappers in hot numeric loops without need. Three — comparing wrappers with equals-equals. Also — Boolean in conditions without null checks. Nullability is a feature — treat it like one.

Interview question — primitive versus wrapper? Primitive — value, non-null, compact, fast. Wrapper — object, nullable, overhead, autoboxing risk. Then mention NullPointerException on unboxing.

That lands the production-level detail. Interviewers listen for null and allocation awareness. Objects around values. Next — type-safe containers. Episode Fifteen — generics. List of Order — compile-time safety without casts.

See you there.
