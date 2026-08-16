# Episode 63 — Object Layout

| Field | Value |
|---|---|
| Episode | 63 |
| Title | Object Layout |
| Catalog handbook column | 63 |
| Narration source script | `make_episode_63.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Sixty-Two covered JVM flags and a measurement-first tuning mindset.
2. Flags control runtime behavior — object layout controls per-instance memory cost.
3. A million small objects can dominate heap even when each field is tiny.
4. Every Java object carries a header, alignment padding, and reference fields.
5. On 64-bit JVMs, compressed oops shrink pointer overhead dramatically.
6. Today — object headers, field layout, padding, and UseCompressedOops.

### Scene `title` (renderer: `title`)

1. Episode Sixty-Three.
2. Object Layout and Compressed Oops.

### Scene `object_headers` (renderer: `object_headers`)

1. Every heap object starts with a header — metadata the JVM needs.
2. Mark word — stores hash code, GC age, lock state, and identity bits.
3. Klass pointer — points to class metadata in metaspace.
4. On 64-bit HotSpot, the header is typically twelve bytes with compressed class pointers.
5. Arrays add a length field — four bytes — before element data.
6. Headers are invisible in source code but count toward heap footprint.

### Scene `field_layout` (renderer: `field_layout`)

1. Instance fields are laid out by the JVM — not in source declaration order.
2. HotSpot reorders fields to minimize padding — widest fields first.
3. long and double take eight bytes — int and references take four.
4. boolean and byte pack into remaining slots when alignment allows.
5. Subclass fields append after superclass layout — inheritance affects size.
6. Use jol-core or JVM object layout tools to inspect real instance sizes.

### Scene `padding_alignment` (renderer: `padding_alignment`)

1. Objects align to eight-byte boundaries on 64-bit JVMs.
2. If fields leave three bytes free, the JVM may add five bytes of padding.
3. An object with one boolean field can still cost sixteen bytes total.
4. Padding is why micro-optimizing field order rarely beats fewer objects.
5. Array of small objects multiplies header cost — consider primitive arrays.
6. Alignment rules apply per object — not per field in isolation.

### Scene `compressed_oops` (renderer: `compressed_oops`)

1. Compressed Oops — compressed ordinary object pointers — save heap space.
2. Flag -XX:+UseCompressedOops — enabled by default on most 64-bit heaps under 32 GB.
3. References stored as 32-bit offsets from a base address instead of full 64-bit pointers.
4. Cuts reference field size in half — huge savings for reference-heavy structures.
5. Heap base must fit in 32 GB for compression — larger heaps use uncompressed oops.
6. Compressed class pointers — UseCompressedClassPointers — shrink klass pointers too.

### Scene `sizing_impact` (renderer: `sizing_impact`)

1. Layout knowledge informs real design decisions.
2. Linked lists of boxed Integers — header plus box plus pointer per element.
3. int[] stores primitives densely — one header, four bytes per int.
4. Records and value-oriented designs reduce pointer chasing and header overhead.
5. Cache-friendly layouts matter more than saving one byte per field.
6. Profile allocation rate — layout explains why some structures cost more.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — assuming declared field order equals memory layout.
3. Two — disabling compressed oops on heaps under 32 GB — wastes memory.
4. Three — optimizing field order before reducing object count.
5. Also — ignoring boxing overhead — Integer costs far more than int.
6. Measure with JOL or heap dumps — do not guess object sizes.

### Scene `interview` (renderer: `interview`)

1. Interview question — how is a Java object laid out in memory?
2. Header — mark word plus klass pointer — typically twelve bytes on 64-bit.
3. Fields reordered by JVM for alignment — not source order.
4. Eight-byte alignment adds padding — small objects can be surprisingly large.
5. Compressed oops store 32-bit offsets — default under 32 GB heap.
6. Arrays add length field — primitive arrays avoid per-element headers.

### Scene `teaser` (renderer: `teaser`)

1. Object layout explains memory cost — safepoints explain when the JVM pauses.
2. Episode Sixty-Four — Safepoints.
3. Stop-the-world coordination, polling, and safepoint bias.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **63** — *Object Layout*.
- **Series catalog:** Episode 63 ↔ handbook lesson 63 — *Object Layout*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Sixty-Two covered JVM flags and a measurement-first tuning mindset._
- **`title`** — starts from: _Episode Sixty-Three._
- **`object_headers`** — starts from: _Every heap object starts with a header — metadata the JVM needs._
- **`field_layout`** — starts from: _Instance fields are laid out by the JVM — not in source declaration order._
- **`padding_alignment`** — starts from: _Objects align to eight-byte boundaries on 64-bit JVMs._
- **`compressed_oops`** — starts from: _Compressed Oops — compressed ordinary object pointers — save heap space._
- **`sizing_impact`** — starts from: _Layout knowledge informs real design decisions._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how is a Java object laid out in memory?_
- **`teaser`** — starts from: _Object layout explains memory cost — safepoints explain when the JVM pauses._
