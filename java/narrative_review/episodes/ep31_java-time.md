# Episode 31 — java.time

| Field | Value |
|---|---|
| Episode | 31 |
| Title | java.time |
| Catalog handbook column | 31 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Optional taught us to make absence explicit. Time is the next place Java APIs used to hide too much — and punish you for guessing.

Imagine you are building a deadline feature. A task is due seven days from today. You might reach for `java.util.Date` or `Calendar` because older tutorials still show them. They compile. They even seem to work on your laptop. Then a teammate in another city opens the same record and sees a different calendar day. Or a daylight-saving transition shifts a "local afternoon" by an hour. Suddenly the bug is not in your arithmetic — it is in the type you chose to mean "a day" versus "a moment on the timeline."

So the natural question is: what types does modern Java give us so those meanings stop colliding?

That is why `java.time` exists. `Date` and `Calendar` are legacy. The modern contract with time lives in `java.time`, and it splits meanings that used to share one blurry class.

Start with a calendar date that does not claim to be a universal instant:

```java
LocalDate today = LocalDate.now();
LocalDate due = today.plusDays(7);
```

`LocalDate` is a date without a time-of-day and without a zone — year, month, day. Adding seven days is calendar arithmetic on that date. If your product rule is "due in seven calendar days," this is the right shape. Notice something else: `plusDays` does not mutate `today`. It returns a new value. The API is immutable. That is not decoration. Shared date values stop surprising you mid-request because some other method called `setMonth` on the same object.

But deadlines are not the only story. Sometimes you need "two-thirty in the afternoon on this calendar day" without claiming which city that afternoon belongs to. That is `LocalDateTime`. Sometimes you need a true point on the timeline — something you can store as "this event happened then," independent of how a wall clock labels it. That is `Instant`.

```java
Instant ts = Instant.now();
```

`Instant` is a timestamp on the UTC timeline. Prefer it when you mean "a moment," especially for logging, auditing, and cross-system records. The interview question "Instant versus LocalDateTime?" is really this design question in disguise: does this value have a zone, or is it only a local civil date-time with no zone attached? `LocalDateTime` has no zone. Treat it as a wall-clock reading without a city, not as a portable moment.

Zones are where production bugs live. `ZonedDateTime` attaches a time zone — and time zones change with politics and daylight-saving rules. Hardcoding a zone string because "the server is in one place" works until the product expands, the cloud region moves, or a user travels. When you need local civil time in a place, make the zone intentional. When you need a moment, store an `Instant` and convert for display.

Formatting and parsing close the loop for humans and APIs:

```java
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String text = due.format(fmt);
LocalDate parsed = LocalDate.parse(text, fmt);
```

Walk that carefully. You define how a date should look as text, format the due date into that shape, and parse it back. Prefer explicit formatters over hoping default `toString` shapes stay stable across versions and locales. Parsing without a clear formatter is how silent mismatches sneak into imports and reports.

What goes wrong if we ignore these distinctions?

Storing a `LocalDateTime` as if it were a moment — then converting later with an assumed zone — recreates the teammate-in-another-city bug. Mixing `Date` and `java.time` in the same module without a clear boundary creates two mental models for one domain. Hardcoding zones hides the real dependency until the first outage that is not a code bug but a calendar rule.

So reconnect the chain. We started with a seven-day deadline and watched legacy date types blur "day," "local date-time," and "instant." `java.time` answers with separate types, immutability, intentional zones, `Instant` for timestamps, and `DateTimeFormatter` for text. The types are the design.

Once we can represent time cleanly, another pressure appears: what happens when an operation cannot finish successfully? Reading a file that is missing, parsing text that is garbage, calling a service that is down — success is not the only path a method can take.

That pressure is Episode Thirty-Two: exceptions.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 31 (*java.time*).

Narration technique: deadline situation → Date/Calendar confusion → typed java.time answers → immutability → Instant vs local → zones → formatter walkthrough → failure modes → next natural problem (exceptions).
