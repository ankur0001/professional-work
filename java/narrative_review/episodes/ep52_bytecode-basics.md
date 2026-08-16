# Episode 52 — Bytecode Basics

| Field | Value |
|---|---|
| Episode | 52 |
| Title | Bytecode Basics |
| Catalog handbook column | 52 |
| Narration source script | `make_episode_52.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-One showed how the JVM loads class files.
2. But what is actually inside those bytes?
3. Java source compiles to bytecode — a stack-machine instruction set.
4. Opcodes like iload, invokevirtual, and return drive every method.
5. javap disassembles class files so you can read what the JVM runs.
6. Today — bytecode basics, the constant pool, and the stack machine model.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Two.
2. Bytecode Basics.

### Scene `class_file` (renderer: `class_file`)

1. A class file is a structured binary format — not human-readable source.
2. Magic number CA FE BA BE identifies a valid Java class file.
3. Constant pool holds strings, class names, method signatures, and literals.
4. Fields, methods, and attributes describe the class structure.
5. Code attribute contains the actual bytecode instructions for each method.
6. The JVM never sees your .java file — only verified .class bytecode.

### Scene `javap` (renderer: `javap`)

1. javap is the JDK disassembler — your window into bytecode.
2. javap -c MyClass prints disassembled method bodies.
3. javap -v adds verbose output — constant pool entries and stack maps.
4. javap -p shows private members — useful for debugging generated code.
5. Compare source to javap output — see what the compiler actually emitted.
6. Every senior Java developer should read javap at least once per project.

### Scene `stack_machine` (renderer: `stack_machine`)

1. The JVM is a stack machine — operands live on an operand stack.
2. Each method frame has its own operand stack and local variable array.
3. Instructions push values, operate, and pop results.
4. iload pushes a local int — iadd pops two ints and pushes the sum.
5. No general-purpose registers — the stack is the workspace.
6. Think push, operate, pop — that mental model unlocks every opcode.

### Scene `opcodes` (renderer: `opcodes`)

1. Opcodes are single-byte instructions — some have operands.
2. Constants — iconst_1, ldc, bipush load values onto the stack.
3. Locals — iload, istore, aload, astore read and write local slots.
4. Fields — getfield, putfield, getstatic access object and class data.
5. Methods — invokevirtual, invokestatic, invokespecial dispatch calls.
6. Control flow — ifeq, goto, tableswitch branch on stack values.

### Scene `reading_bytecode` (renderer: `reading_bytecode`)

1. Walk through a simple method bytecode by bytecode.
2. aload_0 pushes this — getfield reads an instance field.
3. invokevirtual calls a method — return ends the frame.
4. Stack depth must match what verification expects — stack map tables help.
5. Compiler optimizations change bytecode — loops may unroll or inline.
6. Reading bytecode connects source code to runtime behavior.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — assuming bytecode matches source line-for-line — compilers optimize.
3. Two — ignoring stack depth errors — VerifyError at class load time.
4. Three — confusing invokevirtual with invokestatic — wrong dispatch semantics.
5. Also — editing .class files by hand without understanding verification.
6. Use javap as a learning tool — not as something to fear.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is Java bytecode?
2. Platform-independent instruction set for the JVM stack machine.
3. Compiled from .java by javac into .class files.
4. Constant pool, fields, methods, and Code attributes per class.
5. javap disassembles bytecode — read opcodes like iload and invokevirtual.
6. Verification ensures type safety and stack consistency before execution.

### Scene `teaser` (renderer: `teaser`)

1. Bytecode runs on stacks — but where do objects actually live?
2. Episode Fifty-Three — Heap and Stack.
3. Frames, locals, object layout, and metaspace.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **57** — *Bytecode*.
- **Series catalog mapping:** Episode 52 / catalog column `52` / published title *Bytecode Basics*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 57 → episode 52). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-One showed how the JVM loads class files._
- **`title`** — starts from: _Episode Fifty-Two._
- **`class_file`** — starts from: _A class file is a structured binary format — not human-readable source._
- **`javap`** — starts from: _javap is the JDK disassembler — your window into bytecode._
- **`stack_machine`** — starts from: _The JVM is a stack machine — operands live on an operand stack._
- **`opcodes`** — starts from: _Opcodes are single-byte instructions — some have operands._
- **`reading_bytecode`** — starts from: _Walk through a simple method bytecode by bytecode._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is Java bytecode?_
- **`teaser`** — starts from: _Bytecode runs on stacks — but where do objects actually live?_
