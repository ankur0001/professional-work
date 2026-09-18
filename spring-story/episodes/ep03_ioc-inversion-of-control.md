# Episode 03 — IoC (Inversion of Control)

| Field | Value |
|---|---|
| Episode | 03 |
| Title | IoC (Inversion of Control) |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 3 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Breakpoint on line 41 of `AppointmentScheduler.book`. The hospital's outpatient desk is stuck on a flaky integration test, so you step into the constructor chain. `new DoctorDirectory(...)`, then `new RoomBoard(...)`, then `new SmsNotifier(new TwilioClient(System.getenv("TWILIO_KEY")))`. Three frames later you are configuring a vendor SDK inside a domain type that was supposed to be about appointment slots.

That stack trace is Inversion of Control explained by its absence. Control of creation still lives in the business class. Every collaborator birth, every config lookup, every concrete type choice is decided by `AppointmentScheduler` itself.

IoC flips the ownership. The scheduler stops being the composer. It declares what it needs — a directory of doctors, a room board, a notifier — and something outside constructs and supplies those parts. In Spring, that outside force is the container. Your code becomes a musician with a clear part; the container runs the orchestra.

Before IoC, the hospital code looked like this in spirit: the scheduler knew Twilio existed, knew which environment variable held the key, and knew that rooms were backed by a JDBC board. Tests could not book a slot without standing up SMS. Swapping the notifier for an in-memory stub meant editing production construction paths.

```java
public class AppointmentScheduler {
    private final DoctorDirectory doctors;
    private final RoomBoard rooms;
    private final AppointmentNotifier notifier;

    public AppointmentScheduler(
            DoctorDirectory doctors,
            RoomBoard rooms,
            AppointmentNotifier notifier) {
        this.doctors = doctors;
        this.rooms = rooms;
        this.notifier = notifier;
    }

    public Booking book(PatientId patient, Specialty specialty, LocalDate day) {
        Doctor doctor = doctors.findAvailable(specialty, day);
        Room room = rooms.allocate(doctor, day);
        Booking booking = Booking.of(patient, doctor, room, day);
        notifier.confirm(booking);
        return booking;
    }
}
```

Read the runtime story carefully. When the container starts, it creates `DoctorDirectory`, `RoomBoard`, and an `AppointmentNotifier` implementation first (or on demand, depending on laziness). Then it invokes the scheduler constructor with those instances. `book` never calls `new` on its collaborators. If a test passes a fake notifier, confirmation becomes a list append. If production passes an SMS adapter, patients get texts. Same scheduler bytecode either way.

Misconception unique to IoC: "IoC means I must never write `new` anywhere." No. Domain values — `Booking`, `PatientId`, a temporary `ArrayList` inside an algorithm — are still yours to construct. IoC targets the wiring of long-lived collaborators and infrastructure, not every object that exists for three lines.

The hospital team can finally unit-test slot logic without Twilio. What they still argue about in code review is the how of supply: constructor parameters versus setters versus field injection, and who decides which notifier implementation lands in that constructor. That mechanism has a name of its own.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 3 (*IoC (Inversion of Control)*).
