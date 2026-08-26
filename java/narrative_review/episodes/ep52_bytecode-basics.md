# Episode 52 — Bytecode Basics

| Field | Value |
|---|---|
| Episode | 52 |
| Title | Bytecode Basics |
| Catalog handbook column | 52 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Class loading finds and prepares types. Once a class is in, the JVM does not execute your Java source. It executes bytecode — the platform-neutral instructions we first mentioned in Episode One. For a long time that statement stays abstract. Then a performance surprise or a language-sugar question appears, and suddenly you want to see the instructions.

Bytecode is the JVM's language. `javap` turns mystery into mechanism.

```bash
javap -c -p App
# look for invokevirtual / getfield / ifeq
```

Walk the habit. `javap -c` disassembles methods. `-p` includes private members. You will see an operand stack and local variables as the abstract machine model: instructions push and pop values on a stack, and locals hold slots for parameters and variables. A constant pool stores symbolic references — class names, method names, string literals — that instructions refer to by index. Reading a little bytecode demystifies what `javac` emitted before any JIT optimization happens.

```java
int abs(int x) {
    if (x >= 0) return x;
    return -x;
}
```

Mentally, that becomes loads, a comparison, branches, negation, returns. One Java line is not one machine instruction — and often not even one bytecode. Assuming a one-to-one map is how people "optimize" the wrong thing. Source lines are for humans. Bytecode is what the interpreter and JIT see.

`javac` emits; the JIT optimizes later. Early calls may run interpreted. Hot methods get compiled to native code with aggressive optimizations. Deoptimization can undo speculation when assumptions fail. You will deepen JIT soon. Today, notice the pipeline: source → bytecode → (maybe) native. Looking only at source when diagnosing a hot path is sometimes enough — and sometimes blind.

Reading bytecode explains language sugar. Enhanced for-loops, try-with-resources, string concatenation, and enums all leave distinctive instruction patterns. When someone asks "is this allocation free?" or "does this capture create an object?", `javap` is a faster truth than debate. Fear of `javap` is mostly unfamiliarity. Ten minutes of reading a small method builds confidence.

```bash
javap -c -p -v App | less
```

`-v` adds verbose details including constant pool entries. You do not need to memorize every opcode. Learn to recognize `invokevirtual`, `invokestatic`, `getfield`, `ifeq`, `new`, `areturn`. Those landmarks tell stories about calls, fields, branches, allocation, and returns.

What if we optimize without looking at bytecode or understanding JIT?

We rearrange source for aesthetics and call it performance. Sometimes we accidentally help. Often we do nothing measurable. Bytecode literacy is not about writing bytecode by hand. It is about seeing the program the JVM sees, so later conversations about escape analysis, inlining, and GC pressure have a concrete substrate.

Do not confuse source lines with native instructions either. Profilers may attribute time to lines after JIT has inlined and reshaped code. Bytecode is a middle lens — more honest than source for "what was emitted," less final than native for "what the CPU ran after warmup."

Try a tiny experiment after this episode. Write a class with string concatenation in a loop and one with `StringBuilder`. Run `javap -c` on both. See how modern `javac` often emits similar efficient patterns for simple cases — and how older intuitions about concatenation can be outdated. The point is not the micro-win. The point is verifying claims against bytecode instead of tribal memory.

Opcodes for allocation (`new`, `newarray`) and boxing patterns also jump out when you chase GC pressure. If a hot method's bytecode shows repeated boxing, you have a lead before you open a profiler. Bytecode is a map; profilers are the terrain. Use both.

What if a teammate claims a stream pipeline "has no allocations"? Disassemble. Captures and boxing often disagree. Fear of `javap` fades when it settles arguments in two minutes.

Hold a practical checklist: use `javap` when sugar or allocation claims disagree; recognize invoke/getfield/branch/new landmarks; remember bytecode precedes JIT; do not equate one source line with one native instruction. Meet those and you are ready for heap, GC, and JIT conversations without hand-waving.

Constant pool entries also explain why renaming a method breaks binary compatibility differently than recompiling callers. Symbolic references are part of the class file's contract with the loader and linker.

Picture an argument about whether a lambda allocates. Disassemble the call site and the synthetic methods. Sometimes you see a singleton in a static field; sometimes you see a new instance capturing locals. The bytecode settles it for that JDK version. Then remember JIT may still inline and elide further — another reason steady-state measurement sits above static argument.

Opcodes will feel less alien each time you return. Literacy compounds. You are not studying for a trivia night; you are building a habit of looking when claims get absolute.

 Prefer evidence over lore: when a performance claim sounds absolute, spend two minutes with `javap` before spending two hours rewriting. Bytecode literacy pays rent quickly.

 That habit — look once, then argue — is the entire skill this episode is trying to install.

Come back to `javap` whenever a language feature feels like magic — sugar leaves footprints, and footprints are teachable.

Those footprints are the curriculum.

So reconnect the chain. Loaders brought classes in. Bytecode showed the instruction language inside. Operand stack, locals, and constant pool sketched the machine model. `javap` made it readable. Sugar and optimization humility followed. The next natural split is where values live while those instructions run — stack frames versus heap objects.

Episode Fifty-Three: heap and stack.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 52 (*Bytecode Basics*).

Narration technique: see-the-instructions situation → javap → stack/locals/pool → sugar → JIT foreshadow → mistakes → next natural problem (heap/stack).
