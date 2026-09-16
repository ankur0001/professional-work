# Episode 63 — Object Layout

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty-Two covered JVM flags and a measurement-first tuning mindset. Flags control runtime behavior — object layout controls per-instance memory cost. A million small objects can dominate heap even when each field is tiny.

Every Java object carries a header, alignment padding, and reference fields. On 64-bit JVMs, compressed oops shrink pointer overhead dramatically. Today — object headers, field layout, padding, and UseCompressedOops.

Episode Sixty-Three. Object Layout and Compressed Oops. Every heap object starts with a header — metadata the JVM needs. Mark word — stores hash code, GC age, lock state, and identity bits.

Klass pointer — points to class metadata in metaspace. On 64-bit HotSpot, the header is typically twelve bytes with compressed class pointers. Arrays add a length field — four bytes — before element data.

Headers are invisible in source code but count toward heap footprint. Instance fields are laid out by the JVM — not in source declaration order. HotSpot reorders fields to minimize padding — widest fields first.

long and double take eight bytes — int and references take four. boolean and byte pack into remaining slots when alignment allows. Subclass fields append after superclass layout — inheritance affects size.

Use jol-core or JVM object layout tools to inspect real instance sizes. Objects align to eight-byte boundaries on 64-bit JVMs. If fields leave three bytes free, the JVM may add five bytes of padding.

An object with one boolean field can still cost sixteen bytes total. Padding is why micro-optimizing field order rarely beats fewer objects. Array of small objects multiplies header cost — consider primitive arrays.

Alignment rules apply per object — not per field in isolation. Compressed Oops — compressed ordinary object pointers — save heap space. Flag -XX:+UseCompressedOops — enabled by default on most 64-bit heaps under 32 GB.

References stored as 32-bit offsets from a base address instead of full 64-bit pointers. Cuts reference field size in half — huge savings for reference-heavy structures. Heap base must fit in 32 GB for compression — larger heaps use uncompressed oops.

Compressed class pointers — UseCompressedClassPointers — shrink klass pointers too. Layout knowledge informs real design decisions. Linked lists of boxed Integers — header plus box plus pointer per element.

int[] stores primitives densely — one header, four bytes per int. Records and value-oriented designs reduce pointer chasing and header overhead. Cache-friendly layouts matter more than saving one byte per field.

Profile allocation rate — layout explains why some structures cost more. Three common mistakes. One — assuming declared field order equals memory layout. Two — disabling compressed oops on heaps under 32 GB — wastes memory.

Three — optimizing field order before reducing object count. Also — ignoring boxing overhead — Integer costs far more than int. Measure with JOL or heap dumps — do not guess object sizes.

Interview question — how is a Java object laid out in memory? Header — mark word plus klass pointer — typically twelve bytes on 64-bit. Fields reordered by JVM for alignment — not source order.

Eight-byte alignment adds padding — small objects can be surprisingly large. Compressed oops store 32-bit offsets — default under 32 GB heap. Arrays add length field — primitive arrays avoid per-element headers.

Object layout explains memory cost — safepoints explain when the JVM pauses. Episode Sixty-Four — Safepoints. Stop-the-world coordination, polling, and safepoint bias. See you there.
