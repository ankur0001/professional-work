# Episode 16 — Annotations

**Cut:** v1 (original)

## Transcript (from captions)

Generics typed our containers. Annotations label our code. An annotation is metadata — information about the code, attached to the code. Override. Deprecated. Spring markers. Validation rules.

Tiny symbols. Huge framework power. Today we learn what annotations are — and what they are not. Angle brackets were contracts. At-signs are signals. Episode Sixteen. Annotations — metadata that frameworks and compilers read.

An annotation starts with an at-sign. It can mark a class, a method, a field, a parameter — even another annotation. By itself, most annotations do nothing magical at runtime. Something must read them — the compiler, a tool, or a framework.

Think of them as sticky notes with structure. The note matters only if someone looks. Start with built-ins you already use. Override — catch signature mistakes when you think you are overriding.

Deprecated — warn callers that an API is going away. SuppressWarnings — silence a warning you have consciously accepted. FunctionalInterface — document a single abstract method type.

These are small, precise, and compile-time friendly. Retention answers — how long does this annotation live? Source — only in source. Gone after compile. Class — in the class file. Not necessarily visible at runtime.

Runtime — readable through reflection while the program runs. Spring and many frameworks need runtime retention. If retention is wrong, your marker is invisible when it matters. In Spring, annotations drive wiring.

SpringBootApplication. RestController. Service. Autowired. They tell the framework what to scan, create, and inject. That is powerful — and easy to overuse. Prefer clear boundaries. Do not decorate every line into a mystery.

Annotations should clarify intent — not hide architecture. You can define your own annotations. Declare an interface with an at-sign — interface RoleRequired. Add retention and target so tools know where it applies.

Then write a processor or runtime check that enforces it. Without a reader, a custom annotation is just documentation in disguise. Design the annotation and the enforcement together.

Three common mistakes. One — assuming an annotation does work with no processor behind it. Two — wrong retention — runtime framework never sees your marker. Three — annotation soup — so many markers the real flow disappears.

Also — using SuppressWarnings to hide problems instead of fixing types. Annotations amplify discipline. They do not replace it. Interview question — what is an annotation in Java? Structured metadata attached to code elements.

Useful when compilers, tools, or frameworks read it. Mention retention — source, class, runtime. Then give Override versus a Spring stereotype as examples. That answer covers language and ecosystem.

Metadata is clear. Next — looking inside types at runtime. Episode Seventeen — reflection. Inspect classes, call methods, and know the costs. See you there.
