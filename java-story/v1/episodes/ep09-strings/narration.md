# Episode 09 — Strings

**Cut:** v1 (original)

## Transcript (from captions)

Arrays hold many values. Strings hold text — and text is everywhere. APIs, logs, JSON, HTTP, configuration, identifiers. String is immutable. That safety is powerful — and easy to misuse.

Today we treat String like the production type it is. Small mistakes here show up in security and performance. Episode Nine. Strings — immutability, equality, and careful construction.

Immutability means the characters never change after creation. s equals s plus world does not edit s — it creates a new String. That sharing and safety help concurrency and caching.

But careless concatenation can allocate again and again. Understand create versus modify — String only creates. That one idea prevents a whole class of confusion. Equality is the classic trap.

Equals-equals compares references — same String object? For text content — use equals. Safer pattern — literal first. PAID dot equals status. Null-safe and clear. Interviewers listen for this.

Make equals your default reflex for text. Building strings in a loop? Do not use plus repeatedly in hot loops. Use StringBuilder — append in place, then toString once. Modern compilers help simple cases — but builders win when you loop.

Measure hot paths. Clarity first — then allocation discipline. Builders are the boring correct tool — use them. Bytes are not characters without a charset. Prefer UTF-8 explicitly when encoding or decoding.

toLowerCase without a locale can surprise you in Turkish and beyond. For identifiers, be explicit about case rules. Never assume the platform default will match production. Be explicit — always.

Three common mistakes. One — equals-equals for text content. Two — logging secrets inside strings — tokens, passwords, cards. Three — accepting unbounded string input until memory cries.

Also — pushing raw strings deep into domain code. Prefer typed values. A CustomerId type beats a naked string passed twelve layers deep. Interview question — why is String immutable?

Safety, sharing, hash stability for maps, and simpler concurrency reasoning. Then add — use StringBuilder when you mutate often. And never compare text with equals-equals. That trio covers language design and daily practice.

Text is under control. Next we model the world. Episode Ten — object-oriented programming. Classes, objects, encapsulation — how Java scales design. See you there.
