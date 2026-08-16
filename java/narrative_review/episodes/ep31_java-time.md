# Episode 31 — java.time

| Field | Value |
|---|---|
| Episode | 31 |
| Title | java.time |
| Catalog handbook column | 31 |
| Narration source script | `make_episode_31.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Optional modeled absence. java.time models moments — without Calendar pain.
2. Old java.util.Date and Calendar were mutable, confusing, and error-prone.
3. Java eight introduced java.time — immutable, clear, and ISO-based.
4. Instant for machine timestamps. LocalDate for birthdays. ZonedDateTime for meetings.
5. Today — the modern date-time toolkit every Java developer needs.
6. Time is hard. Good APIs make it less hard.

### Scene `title` (renderer: `title`)

1. Episode Thirty-One.
2. java.time — dates, times, and zones done right.

### Scene `instant` (renderer: `instant`)

1. Instant is a point on the UTC timeline.
2. Machine timestamps — logs, events, database instants.
3. Instant.now captures the current moment in UTC.
4. Compare with isBefore and isAfter — natural ordering.
5. Convert to epoch seconds or millis when legacy APIs require it.
6. Think Instant when the zone does not matter yet.

### Scene `zoned` (renderer: `zoned`)

1. ZonedDateTime ties a local date-time to a time zone.
2. ZoneId identifies a region — Europe/Paris, America/New_York.
3. Meetings, flight departures, user-facing clocks need zones.
4. withZoneSameInstant converts between zones without shifting the instant.
5. Daylight saving transitions are handled by the rules in ZoneId.
6. Store Instants in databases — render ZonedDateTime for users.

### Scene `local` (renderer: `local`)

1. LocalDate is a calendar date without time or zone.
2. LocalTime is a time of day without date or zone.
3. LocalDateTime combines both — still no zone attached.
4. Birthdays, due dates, business hours templates use local types.
5. Do not attach a zone until you know which zone.
6. Parse and format with consistent patterns — DateTimeFormatter.

### Scene `formatting` (renderer: `formatting`)

1. DateTimeFormatter replaces SimpleDateFormat for new code.
2. Predefined constants — ISO_LOCAL_DATE, ISO_INSTANT.
3. ofPattern for custom layouts — but prefer ISO when possible.
4. format and parse are symmetric — define once, reuse.
5. Locale affects human-readable month and day names.
6. Immutable formatters are thread-safe — share them freely.

### Scene `chrono` (renderer: `chrono`)

1. Arithmetic uses clear units — ChronoUnit.DAYS, HOURS, MINUTES.
2. plus and minus on local and zoned types read naturally.
3. Period covers calendar amounts — two months, three years.
4. Duration covers exact time amounts — ninety minutes.
5. between measures the gap between two points.
6. Pick Period versus Duration based on calendar versus clock semantics.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — mixing legacy Date with java.time without explicit conversion.
3. Two — assuming LocalDateTime has a zone — it does not.
4. Three — storing zoned strings instead of Instant in the database.
5. Also — ignoring daylight saving when scheduling recurring events.
6. Model instants in UTC. Display in the user zone.

### Scene `interview` (renderer: `interview`)

1. Interview question — Instant versus LocalDateTime?
2. Instant — absolute point on the UTC timeline.
3. LocalDateTime — date and time without zone context.
4. Mention ZonedDateTime when user zones matter.
5. Note immutability and DateTimeFormatter for parsing.
6. That answer shows you escaped the Date era.

### Scene `teaser` (renderer: `teaser`)

1. Time is typed. Next — when things go wrong.
2. Episode Thirty-Two — Exceptions.
3. Checked, unchecked, and handling failure with intent.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **31** — *java.time*.
- **Series catalog:** Episode 31 ↔ handbook lesson 31 — *java.time*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Optional modeled absence. java.time models moments — without Calendar pain._
- **`title`** — starts from: _Episode Thirty-One._
- **`instant`** — starts from: _Instant is a point on the UTC timeline._
- **`zoned`** — starts from: _ZonedDateTime ties a local date-time to a time zone._
- **`local`** — starts from: _LocalDate is a calendar date without time or zone._
- **`formatting`** — starts from: _DateTimeFormatter replaces SimpleDateFormat for new code._
- **`chrono`** — starts from: _Arithmetic uses clear units — ChronoUnit.DAYS, HOURS, MINUTES._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — Instant versus LocalDateTime?_
- **`teaser`** — starts from: _Time is typed. Next — when things go wrong._
