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

Imagine you are building a deadline feature for a task tracker. Product says a task is due seven days from today. On your laptop you reach for `java.util.Date` or `Calendar` because older tutorials still show them. They compile. They even seem to work. Then a teammate in another city opens the same record and sees a different calendar day. Or a daylight-saving transition shifts what you thought was "Tuesday afternoon" by an hour. The arithmetic looked fine. The type you chose was lying about what it meant.

So the natural question is not "how do I add seven to a date object?" It is: what types does modern Java give us so "a calendar day," "a local date-time," and "a moment on the timeline" stop sharing one blurry class?

That is why `java.time` exists. `Date` and `Calendar` are legacy. The modern contract with time lives in `java.time`, and it splits meanings that used to collide.

Start with a calendar date that does not pretend to be a universal instant:

```java
LocalDate today = LocalDate.now();
LocalDate due = today.plusDays(7);
System.out.println("Due on " + due);
```

`LocalDate` is a date without a time-of-day and without a zone — year, month, day. Adding seven days is calendar arithmetic on that date. If your product rule is "due in seven calendar days," this is the right shape. Notice something else: `plusDays` does not mutate `today`. It returns a new value. The API is immutable. That is not decoration. Shared date values stop surprising you mid-request because some other method called `setMonth` on the same mutable object you thought you still owned.

But deadlines are not the only story. Sometimes you need "two-thirty in the afternoon on this calendar day" without claiming which city that afternoon belongs to. That is `LocalDateTime`. It is useful for civil date-times that are intentionally zone-free — and dangerous if you treat it as a portable moment.

Sometimes you need a true point on the timeline — something you can store as "this event happened then," independent of how a wall clock labels it in Mumbai or Berlin. That is `Instant`.

```java
Instant createdAt = Instant.now();
Instant deadline = createdAt.plus(Duration.ofHours(48));
```

Walk that. `Instant.now()` captures a timestamp on the UTC timeline. Adding a forty-eight-hour `Duration` moves along that timeline. Prefer `Instant` when you mean "a moment," especially for logging, auditing, and cross-system records. The interview question "Instant versus LocalDateTime?" is really a design question: does this value have a zone, or is it only a local civil date-time with no zone attached? `LocalDateTime` has no zone. Treat it as a wall-clock reading without a city, not as something you can safely compare across machines without more context.

Zones are where production bugs live. `ZonedDateTime` attaches a time zone — and time zones change with politics and daylight-saving rules.

```java
ZonedDateTime meeting = ZonedDateTime.of(
    LocalDateTime.of(2026, 3, 8, 9, 0),
    ZoneId.of("America/New_York"));
ZonedDateTime inTokyo = meeting.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));
```

The same instant can print as different local clock times in New York and Tokyo. Hardcoding a zone because "the server is in one place" works until the product expands, the cloud region moves, or a user travels. When you need local civil time in a place, make the zone intentional. When you need a moment, store an `Instant` and convert for display.

Formatting and parsing close the loop for humans and file formats:

```java
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String text = due.format(fmt);
LocalDate parsed = LocalDate.parse(text, fmt);
```

You define how a date should look as text, format the due date into that shape, and parse it back. Prefer explicit formatters over hoping default `toString` shapes stay stable across versions and locales. Parsing without a clear formatter is how silent mismatches sneak into imports and reports.

What goes wrong if we ignore these distinctions? Storing a `LocalDateTime` as if it were a moment — then converting later with an assumed zone — recreates the teammate-in-another-city bug. Mixing `Date` and `java.time` in the same module without a clear boundary creates two mental models for one domain. Hardcoding zones hides the real dependency until the first outage that is not a code bug but a calendar rule.

Let's put the pieces together the way a booking system might. A hotel stay has a check-in `LocalDate` and check-out `LocalDate` — calendar dates in the property's civil calendar. The instant the reservation was confirmed is an `Instant` stored in the database. When you email the guest, you format those local dates with a `DateTimeFormatter` in their language, and you convert the confirmation instant into their zone only at display time. Each type earns its keep by refusing to pretend it is the others.

If you collapse that design into one `Date` field "for simplicity," every feature that touches time inherits ambiguity. Is this field a day? A local afternoon? A moment? The next developer will guess — and guessing is how daylight-saving bugs and off-by-one checkouts are born. `java.time` is not more classes for their own sake. It is fewer meanings smashed into one class.

So reconnect the chain. We started with a seven-day deadline and watched legacy date types blur "day," "local date-time," and "instant." `java.time` answers with separate types, immutability, intentional zones, `Instant` for timestamps, and `DateTimeFormatter` for text. The types are the design.

Once we can represent time cleanly, another pressure appears: what happens when an operation cannot finish successfully? Reading a file that is missing, parsing text that is garbage, calling a service that is down — success is not the only path a method can take.

That pressure is Episode Thirty-Two: exceptions.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 31 (*java.time*).

Narration technique: deadline situation → Date/Calendar confusion → typed java.time answers → immutability → Instant vs local → zones → formatter walkthrough → failure modes → next natural problem (exceptions).
