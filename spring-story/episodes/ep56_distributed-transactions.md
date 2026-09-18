# Episode 56 — Distributed Transactions

| Field | Value |
|---|---|
| Episode | 56 |
| Title | Distributed Transactions |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 56 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Harbor booking wants one sentence to be true: “berth reserved and carrier notified.” The reservation lands in PostgreSQL. The notification leaves on a JMS queue for the carrier gateway. If the database commits and the message never sends, trucks arrive to a berth nobody told them about. If the message sends and the database rolls back, carriers prepare for a booking that does not exist. Two resources. One business promise. A local `@Transactional` on the database alone cannot cover both.

Historically the industry answer was a distributed transaction: a coordinator, XA-capable resource managers, and a protocol that tries to commit everywhere or nowhere.

Two-phase commit is that protocol. Phase one: the coordinator asks every participant to prepare — flush, lock, vote yes or no. If all vote yes, phase two tells everyone to commit. If any votes no, everyone rolls back. On paper, atomicity spans the booking database and the JMS broker. In production, the coordinator can crash between phases, participants can block holding locks, and networks can partition. You trade local simplicity for global coordination cost and operational pain — which is why 2PC hurts even when it “works.”

```java
@Configuration
public class BookingXaConfig {

    @Bean
    public JtaTransactionManager transactionManager(
            UserTransaction userTransaction,
            TransactionManager transactionManager) {
        return new JtaTransactionManager(userTransaction, transactionManager);
    }
}
```

```java
@Service
public class BerthBookingBridge {

    private final BookingRepository bookings;
    private final JmsTemplate jms;

    public BerthBookingBridge(BookingRepository bookings, JmsTemplate jms) {
        this.bookings = bookings;
        this.jms = jms;
    }

    @Transactional // enlisted with JtaTransactionManager in a true XA setup
    public BookingId reserveAndNotify(BerthHold hold) {
        Booking booking = Booking.open(hold);
        bookings.save(booking);
        jms.convertAndSend("harbor.bookings", BookingPlaced.of(booking));
        return booking.id();
    }
}
```

In a true XA arrangement, that single annotation enlists both the XA datasource and the XA connection factory under a `JtaTransactionManager`. The programming model looks familiar. The runtime does not: application server or standalone manager (Atomikos, Narayana), XA drivers, recovery logs, and runbooks for in-doubt transactions after a crash mid-protocol.

Modern Boot services often never go there. Managed Kafka, cloud datastores, and polyglot stores frequently lack honest XA support. Even when XA is available, holding locks across prepare and commit under harbor-scale latency kills throughput. Teams learned that “just enable two-phase commit” for DB plus JMS booking was rarely the product-friendly answer.

Still own the vocabulary. Global versus local transaction. Resource manager versus transaction manager. Raw `UserTransaction` begin/commit versus Spring’s declarative boundary on top. Heuristic exceptions when participants disagree after prepare. Those words appear in postmortems even when your team refused XA.

A misconception is assuming `@Transactional` automatically spans REST calls, Redis, and Mongo because they happen in the same method. A local `DataSourceTransactionManager` covers one JDBC resource. Another misconception is blaming Spring when 2PC hurts. The protocol’s cost is inherent; Spring only integrates with it.

So the fork is honest. Invest in XA where both resources truly support it and the business demands strict atomicity across DB and JMS — or stop pretending one ACID transaction covers a multi-system booking. The second path needs a sequence of local commits plus compensations when a later step fails.

That pattern is the saga.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 56 (*Distributed Transactions*).
