# Episode 52 — Bytecode Basics

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-One showed how the JVM loads class files. But what is actually inside those bytes? Java source compiles to bytecode — a stack-machine instruction set. Opcodes like iload, invokevirtual, and return drive every method.

javap disassembles class files so you can read what the JVM runs. Today — bytecode basics, the constant pool, and the stack machine model. Episode Fifty-Two. Bytecode Basics. A class file is a structured binary format — not human-readable source.

Magic number CA FE BA BE identifies a valid Java class file. Constant pool holds strings, class names, method signatures, and literals. Fields, methods, and attributes describe the class structure.

Code attribute contains the actual bytecode instructions for each method. The JVM never sees your .java file — only verified .class bytecode. javap is the JDK disassembler — your window into bytecode.

javap -c MyClass prints disassembled method bodies. javap -v adds verbose output — constant pool entries and stack maps. javap -p shows private members — useful for debugging generated code.

Compare source to javap output — see what the compiler actually emitted. Every senior Java developer should read javap at least once per project. The JVM is a stack machine — operands live on an operand stack.

Each method frame has its own operand stack and local variable array. Instructions push values, operate, and pop results. iload pushes a local int — iadd pops two ints and pushes the sum.

No general-purpose registers — the stack is the workspace. Think push, operate, pop — that mental model unlocks every opcode. Opcodes are single-byte instructions — some have operands.

Constants — iconst_1, ldc, bipush load values onto the stack. Locals — iload, istore, aload, astore read and write local slots. Fields — getfield, putfield, getstatic access object and class data.

Methods — invokevirtual, invokestatic, invokespecial dispatch calls. Control flow — ifeq, goto, tableswitch branch on stack values. Walk through a simple method bytecode by bytecode.

aload_0 pushes this — getfield reads an instance field. invokevirtual calls a method — return ends the frame. Stack depth must match what verification expects — stack map tables help.

Compiler optimizations change bytecode — loops may unroll or inline. Reading bytecode connects source code to runtime behavior. Three common mistakes. One — assuming bytecode matches source line-for-line — compilers optimize.

Two — ignoring stack depth errors — VerifyError at class load time. Three — confusing invokevirtual with invokestatic — wrong dispatch semantics. Also — editing .class files by hand without understanding verification.

Use javap as a learning tool — not as something to fear. Interview question — what is Java bytecode? Platform-independent instruction set for the JVM stack machine. Compiled from .java by javac into .class files.

Constant pool, fields, methods, and Code attributes per class. javap disassembles bytecode — read opcodes like iload and invokevirtual. Verification ensures type safety and stack consistency before execution.

Bytecode runs on stacks — but where do objects actually live? Episode Fifty-Three — Heap and Stack. Frames, locals, object layout, and metaspace. See you there.
