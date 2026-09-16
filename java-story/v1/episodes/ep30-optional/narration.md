# Episode 30 — Optional

**Cut:** v1 (original)

## Transcript (from captions)

Parallel streams need thread-safe design. Optional handles absence safely. Null references cause bugs that compile fine and fail in production. Optional is a container that may hold a value — or be empty.

It forces callers to acknowledge missing data explicitly. Today — Optional as a design tool, not a silver bullet. Present or empty — choose with intent. Episode Thirty. Optional — modeling absence without null.

Optional.of wraps a non-null value. Optional.ofNullable accepts null — producing an empty Optional. Optional.empty is the canonical empty instance. isPresent and isEmpty test state without unwrapping.

Never call of with a value that might be null — use ofNullable. Creation methods set expectations from the first line. An empty Optional is not null — it is an explicit absence. get throws NoSuchElementException on empty — avoid in production code.

orElse supplies a default when empty. orElseGet takes a supplier — lazy default computation. orElseThrow maps absence to a meaningful exception. Pick the fallback that matches your domain semantics.

Optional chains avoid nested if-not-null checks. ifPresent runs a consumer only when a value exists. filter keeps the value only if a predicate passes. map transforms the inner value if present.

flatMap transforms into another Optional — no nested Optional mess. Chain fluently — stop when empty at any step. map is for simple transformations — String to Integer. flatMap is for operations that themselves return Optional.

Lookup then parse. Find user then fetch profile. flatMap flattens Optional of Optional into one level. Combine with stream flatMap for filtering present values. Readable pipelines replace defensive null ladders.

When Optional shines. Return types where absence is normal — findById, parse attempts. Chaining transformations without null checks at every step. When not to use it. Fields on entities — prefer plain nullability discipline or records.

Method parameters — often clearer as overloads or validation. Optional is for APIs and return types — not everywhere. Three common mistakes. One — Optional.of with a possibly null value.

Two — using get without checking — same as ignoring null. Three — Optional fields in JSON entities — serialization pain. Also — orElse with expensive work — use orElseGet instead. Optional clarifies intent — misuse adds noise.

Interview question — why Optional instead of null? Forces explicit handling — isPresent, orElse, map chains. Documents that absence is expected in the return type. Mention ofNullable versus of — null safety at creation.

Note it is mainly for return values, not fields. That answer shows modern Java API design awareness. Absence handled. Next — dates and times done right. Episode Thirty-One — java.time.

Instant, LocalDate, ZonedDateTime — without Calendar pain. See you there.
