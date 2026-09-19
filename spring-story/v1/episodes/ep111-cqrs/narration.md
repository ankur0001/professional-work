# Episode 111 — CQRS

| Field | Value |
|---|---|
| Episode | 111 |
| Title | CQRS |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 111 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Write berth assignments under row locks and overlap rules. The schedule board wants a denormalized view: berth, vessel name, ETA, tide window, billing status — refreshed for operators who refresh every few seconds. One normalized write model serving both jobs creates lock contention and ugly queries. CQRS — Command Query Responsibility Segregation — separates the write path from the read model.

Commands go through the `Berth` aggregate. Queries hit a projection built for the board.

```java
@RestController
@RequestMapping("/berths")
public class BerthCommandController {
    private final ReserveBerthService reserve;

    @PostMapping("/{berthId}/reservations")
    ResponseEntity<Void> reserve(@PathVariable String berthId,
                                 @Valid @RequestBody ReserveRequest body) {
        reserve.reserve(BerthId.of(berthId), body.imo(), body.window());
        return ResponseEntity.accepted().build();
    }
}

@RestController
@RequestMapping("/schedule-board")
public class ScheduleBoardQueryController {
    private final ScheduleBoardQuery query;

    @GetMapping
    List<ScheduleBoardRow> board(@RequestParam String quay) {
        return query.rowsForQuay(quay);
    }
}
```

```java
@Component
public class ScheduleBoardProjector {
    private final JdbcTemplate jdbc;

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void on(BerthReserved event) {
        jdbc.update("""
                insert into schedule_board_view (berth_id, imo, window_start, window_end, status)
                values (?,?,?,?, 'RESERVED')
                on conflict (berth_id) do update
                set imo = excluded.imo,
                    window_start = excluded.window_start,
                    window_end = excluded.window_end,
                    status = 'RESERVED'
                """,
                event.berthId().value(),
                event.imo().value(),
                event.window().start(),
                event.window().end());
    }
}
```

```sql
-- read model tailored to the board
create table schedule_board_view (
  berth_id text primary key,
  imo text,
  vessel_name text,
  window_start timestamptz,
  window_end timestamptz,
  status text,
  billing_state text
);
```

Operators query `schedule_board_view` without touching the write aggregate’s reservation collection. Billing state can update from `BerthReserved` consumers without blocking `reserve`. Observe projection lag — a Micrometer gauge of “seconds behind last write” — so on-call knows when the board lies. Walk a lag incident: write succeeds at T0; projector stalls; board still shows EMPTY; a second scheduler tries to reserve; write model correctly rejects overlap while the board confused the human. The fix is lag alerts and honest UI (“updated 12s ago”), not putting board queries back on the locked aggregate.

CQRS is a spectrum. Mild CQRS is a SQL view or upsert table updated after commit in the same database. Strong CQRS is separate stores and eventual consistency you must explain to operators. Start mild when the schedule board hurts; do not duplicate every entity “for purity.” Projector tests matter: feed `BerthReserved` and `BerthReleased` fixtures and assert row shape — without them, read and write drift until the board invents berths.

Failure symptoms: two models with duplicated business rules (board “validates” overlaps in SQL while `Berth.reserve` also does — they diverge). Commands that query the read model to make decisions — you just coupled consistency to lag. Event sourcing assumed mandatory — you can project from domain events without storing the full event log as source of truth.

Trade-offs: faster, simpler reads and concentrated write invariants versus eventual consistency and more moving parts. For a board that refreshes every few seconds, seconds of lag are often acceptable; for a gate release decision, do not read a stale projection to authorize cargo. Keep authorization and invariants on the command side.

When billing_state on the board updates from a separate consumer, design for partial rows: vessel name may fill in after a lookup, billing_state after invoice open. The UI should render “pending” rather than invent defaults that look like unpaid. Projector idempotency matters here too — replaying `BerthReserved` must upsert, not insert a second board row for B7.

A misconception is equating CQRS with event sourcing — you can project from domain events without storing the full event log as the source of truth. Another is two models that drift with no projector tests. A third is using CQRS as an excuse for duplicate incoherent business rules on both sides; commands own invariants, queries own presentation.

Patterns earn trust when they survive messy production constraints — traffic, people, legacy, and tradeoffs. The last episode synthesizes three harbor postmortems from the whole series. There is no further handbook lesson after that.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 111 (*CQRS*).
