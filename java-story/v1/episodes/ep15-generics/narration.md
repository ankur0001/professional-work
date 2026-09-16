# Episode 15 — Generics

**Cut:** v1 (original)

## Transcript (from captions)

Wrappers made objects from values. Generics make containers type-safe. List of Order — not List of Object with casts everywhere. Generics move mistakes from runtime ClassCastException to compile time.

Today we read angle brackets with confidence. This is how modern Java APIs stay both flexible and safe. Angle brackets are not ceremony — they are contracts. Episode Fifteen. Generics — type parameters without the cast tax.

Before generics — a raw List held anything. You cast on the way out. Wrong cast — boom at runtime. List angle Order documents intent and enforces it. The compiler becomes your first code reviewer.

That alone earns generics a permanent place in your toolkit. Catch type mistakes before they ship. Type parameters look like this. class Box angle T — T is a placeholder for a type.

Box angle String holds strings. Box angle Order holds orders. Methods can be generic too — static angle T T first of List angle T. Name type parameters clearly — T for type, E for element, K V for maps.

Sometimes T needs limits. angle T extends Number — only numeric types. Wildcards — question mark extends — for flexible consumers. PECS — producer extends, consumer super — when you dig deeper.

For now — prefer concrete type args at call sites when you can. Important JVM truth — type erasure. Generics are mainly a compile-time tool. At runtime, List angle Order is largely a List.

You cannot new T easily. You cannot check instanceof List angle Order. Design with erasure in mind — do not fight the platform. Know the limits so you use the strengths. Three common mistakes.

One — raw types — List without angle brackets — undoing the safety. Two — ignoring unchecked warnings until ClassCastExceptions return. Three — overcomplicated wildcards where a simple type parameter would do.

Also — using Object when a generic method would express intent. Interview question — what is type erasure? Generics checked at compile time; type args are largely erased at runtime.

Why — backward compatibility with older bytecode. Then — prefer parameterized types over raw types always. That answer shows language history and daily discipline. Containers are type-safe. Next — metadata on code.

Episode Sixteen — annotations. Override, Spring markers, and what retention means. See you there.
