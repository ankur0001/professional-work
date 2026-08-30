# Episode 31 — java.time

| Field | Value |
|---|---|
| Episode | 31 |
| Title | java.time |
| Catalog handbook column | 31 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Optional made absence explicit at API boundaries. Time is the next place older Java APIs hid too much — and punished you for guessing.

Imagine a deadline feature: a task is due seven days from today. Older tutorials still reach for `java.util.Date` or `Calendar`. They compile. Then a teammate in another city sees a different calendar day, or a daylight-saving shift moves what you thought was Tuesday afternoon. The arithmetic looked fine. The type was lying about what it meant.

So the question is not "how do I add seven?" It is: what types keep "a calendar day," "a local date-time," and "a moment on the timeline" from sharing one blurry class?

That is why `java.time` exists. `Date` and `Calendar` are legacy. Modern Java splits the meanings that used to collide.

Start with a calendar date that does not pretend to be a universal instant:

```java
LocalDate today = LocalDate.now();
LocalDate due = today.plusDays(7);
```

`LocalDate` is year, month, day — no time-of-day, no zone. Adding seven days is calendar arithmetic. Notice also: `plusDays` does not mutate `today`; it returns a new value. Immutability is not decoration. Shared date values stop surprising you because some other method called `setMonth` on an object you thought you still owned.

Sometimes you need "two-thirty this afternoon" without claiming which city that afternoon belongs to — that is `LocalDateTime`. Useful for zone-free civil date-times; dangerous if you treat it as a portable moment.

When you need a true point on the timeline — audit logs, cross-system records — use `Instant`:

```java
Instant createdAt = Instant.now();
Instant deadline = createdAt.plus(Duration.ofHours(48));
```

`Instant.now()` captures a UTC timeline moment. A forty-eight-hour `Duration` moves along that timeline. `LocalDateTime` has no zone; treat it as a wall-clock reading without a city, not as something you can safely compare across machines without more context.

Zones are where production bugs live. `ZonedDateTime` attaches a zone — and zones change with politics and daylight saving:

```java
ZonedDateTime meeting = ZonedDateTime.of(
    LocalDateTime.of(2026, 3, 8, 9, 0),
    ZoneId.of("America/New_York"));
ZonedDateTime inTokyo = meeting.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));
```

The same instant prints as different local clock times in New York and Tokyo. Hardcoding a zone because "the server is here" works until the product expands or the cloud region moves. Store an `Instant` for moments; convert with a zone only for display.

Formatting closes the loop for humans and files:

```java
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String text = due.format(fmt);
LocalDate parsed = LocalDate.parse(text, fmt);
```

Prefer explicit formatters over hoping `toString` stays stable across versions and locales.

Put it together the way a booking system might. Check-in and check-out are `LocalDate` values in the property's civil calendar. Confirmation time is an `Instant` in the database. Email formats those local dates for the guest and converts the confirmation instant into their zone only at display time. Each type earns its keep by refusing to pretend it is the others.

Collapse that into one `Date` field "for simplicity," and every feature inherits ambiguity. Is this a day? A local afternoon? A moment? The next developer will guess — and guessing is how daylight-saving bugs and off-by-one checkouts are born.

Once we can represent time cleanly, another pressure appears: what happens when an operation cannot finish successfully? A missing file, garbage text, a downed service — success is not the only path a method can take.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 31 (*java.time*).

Narration technique: deadline situation → Date/Calendar confusion → typed java.time answers → Instant vs local → zones → formatter → next natural problem (exceptions).
