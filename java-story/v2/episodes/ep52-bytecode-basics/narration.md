# Episode 52 — Bytecode Basics

| Field | Value |
|---|---|
| Episode | 52 |
| Title | Bytecode Basics |
| Catalog handbook column | 52 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Class loading finds and prepares types. Once a class is in, the JVM does not execute your Java source. It executes bytecode — the platform-neutral instructions we first mentioned when Java's portability story began. For a long time that statement stays abstract. Then a performance surprise or a language-sugar question appears, and suddenly you want to see the instructions.

Bytecode is the JVM's language. `javap` turns mystery into mechanism.

```bash
javap -c -p App
# look for invokevirtual / getfield / ifeq
```

`javap -c` disassembles methods. `-p` includes private members. You will see an operand stack and local variables as the abstract machine model: instructions push and pop values on a stack, and locals hold slots for parameters and variables. A constant pool stores symbolic references — class names, method names, string literals — that instructions refer to by index. Reading a little bytecode demystifies what `javac` emitted before any JIT optimization happens.

```java
int abs(int x) {
    if (x >= 0) return x;
    return -x;
}
```

Mentally, that becomes loads, a comparison, branches, negation, returns. One Java line is not one machine instruction — and often not even one bytecode. Assuming a one-to-one map is how people "optimize" the wrong thing. Source lines are for humans. Bytecode is what the interpreter and JIT see.

`javac` emits; the JIT optimizes later. Early calls may run interpreted. Hot methods get compiled to native code. Looking only at source when diagnosing a hot path is sometimes enough — and sometimes blind.

Reading bytecode explains language sugar. Enhanced for-loops, try-with-resources, string concatenation, and enums all leave distinctive instruction patterns. When someone asks "is this allocation free?" or "does this capture create an object?", `javap` is a faster truth than debate.

```bash
javap -c -p -v App | less
```

`-v` adds verbose details including constant pool entries. You do not need to memorize every opcode. Learn to recognize `invokevirtual`, `invokestatic`, `getfield`, `ifeq`, `new`, `areturn`. Those landmarks tell stories about calls, fields, branches, allocation, and returns.

What if we optimize without looking at bytecode or understanding JIT? We rearrange source for aesthetics and call it performance. Sometimes we accidentally help. Often we do nothing measurable. Bytecode literacy is not about writing bytecode by hand. It is about seeing the program the JVM sees.

Try a tiny experiment. Write a class with string concatenation in a loop and one with `StringBuilder`. Run `javap -c` on both. See how modern `javac` often emits similar efficient patterns for simple cases — and how older intuitions about concatenation can be outdated. The point is verifying claims against bytecode instead of tribal memory.

Opcodes for allocation (`new`, `newarray`) and boxing patterns also jump out when you chase GC pressure. If a hot method's bytecode shows repeated boxing, you have a lead before you open a profiler. Bytecode is a map; profilers are the terrain. Use both.

What if a teammate claims a stream pipeline "has no allocations"? Disassemble. Captures and boxing often disagree.

Picture an argument about whether a lambda allocates. Disassemble the call site and the synthetic methods. Sometimes you see a singleton in a static field; sometimes you see a new instance capturing locals. The bytecode settles it for that JDK version. Then remember JIT may still inline and elide further — another reason steady-state measurement sits above static argument.

Hold a practical checklist: use `javap` when sugar or allocation claims disagree; recognize invoke/getfield/branch/new landmarks; remember bytecode precedes JIT; do not equate one source line with one native instruction. Prefer evidence over lore: when a performance claim sounds absolute, spend two minutes with `javap` before spending two hours rewriting.

The next natural split is where values live while those instructions run — stack frames versus heap objects.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 52 (*Bytecode Basics*).

Narration technique: see-the-instructions situation → javap → stack/locals/pool → sugar → next natural problem (heap/stack).
