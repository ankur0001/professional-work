# Episode 31 — java.time

**Cut:** v1 (original)

## Transcript (from captions)

Optional modeled absence. java.time models moments — without Calendar pain. Old java.util.Date and Calendar were mutable, confusing, and error-prone. Java eight introduced java.time — immutable, clear, and ISO-based.

Instant for machine timestamps. LocalDate for birthdays. ZonedDateTime for meetings. Today — the modern date-time toolkit every Java developer needs. Time is hard. Good APIs make it less hard.

Episode Thirty-One. java.time — dates, times, and zones done right. Instant is a point on the UTC timeline. Machine timestamps — logs, events, database instants. Instant.now captures the current moment in UTC.

Compare with isBefore and isAfter — natural ordering. Convert to epoch seconds or millis when legacy APIs require it. Think Instant when the zone does not matter yet. ZonedDateTime ties a local date-time to a time zone.

ZoneId identifies a region — Europe/Paris, America/New_York. Meetings, flight departures, user-facing clocks need zones. withZoneSameInstant converts between zones without shifting the instant.

Daylight saving transitions are handled by the rules in ZoneId. Store Instants in databases — render ZonedDateTime for users. LocalDate is a calendar date without time or zone. LocalTime is a time of day without date or zone.

LocalDateTime combines both — still no zone attached. Birthdays, due dates, business hours templates use local types. Do not attach a zone until you know which zone. Parse and format with consistent patterns — DateTimeFormatter.

DateTimeFormatter replaces SimpleDateFormat for new code. Predefined constants — ISO_LOCAL_DATE, ISO_INSTANT. ofPattern for custom layouts — but prefer ISO when possible. format and parse are symmetric — define once, reuse.

Locale affects human-readable month and day names. Immutable formatters are thread-safe — share them freely. Arithmetic uses clear units — ChronoUnit.DAYS, HOURS, MINUTES. plus and minus on local and zoned types read naturally.

Period covers calendar amounts — two months, three years. Duration covers exact time amounts — ninety minutes. between measures the gap between two points. Pick Period versus Duration based on calendar versus clock semantics.

Three common mistakes. One — mixing legacy Date with java.time without explicit conversion. Two — assuming LocalDateTime has a zone — it does not. Three — storing zoned strings instead of Instant in the database.

Also — ignoring daylight saving when scheduling recurring events. Model instants in UTC. Display in the user zone. Interview question — Instant versus LocalDateTime? Instant — absolute point on the UTC timeline.

LocalDateTime — date and time without zone context. Mention ZonedDateTime when user zones matter. Note immutability and DateTimeFormatter for parsing. That answer shows you escaped the Date era.

Time is typed. Next — when things go wrong. Episode Thirty-Two — Exceptions. Checked, unchecked, and handling failure with intent. See you there.
