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

One PostgreSQL database and `@Transactional` feel almost comfortable now. Stretch the same business promise across two systems and the comfort evaporates. Place an order in the orders database. Publish `OrderPlaced` to Kafka so inventory and billing react. If the commit succeeds and the publish never leaves the process, inventory never moves. If the publish succeeds and the database rolls back, consumers act on an order that does not exist. Two resources. One business sentence. No single local transaction can cover both without help.

That help historically meant a distributed transaction: a coordinator, resource managers that speak XA, and a protocol that tries to commit everywhere or nowhere.

The classic protocol is two-phase commit. In phase one, the coordinator asks every participant to prepare — flush, lock, vote yes or no. If all vote yes, phase two tells everyone to commit. If any votes no, everyone rolls back. On paper, atomicity spans databases and JMS brokers. In production, the coordinator can crash between phases, participants can block holding locks, and networks can partition. You trade local simplicity for global coordination cost and operational pain.

```java
// Conceptual: JTA / XA spanning a DataSource and a JMS connection factory
@Configuration
public class XaConfig {

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
public class OrderPlacementService {

    private final OrderRepository orders;
    private final JmsTemplate jms;

    public OrderPlacementService(OrderRepository orders, JmsTemplate jms) {
        this.orders = orders;
        this.jms = jms;
    }

    @Transactional // backed by JtaTransactionManager in an XA setup
    public OrderId place(NewOrder request) {
        Order order = Order.open(request);
        orders.save(order);
        jms.convertAndSend("orders.placed", OrderPlaced.of(order));
        return order.id();
    }
}
```

In a true XA arrangement, that single `@Transactional` is enlisted with a `JtaTransactionManager`. Both the XA datasource and the XA connection factory become participants. Spring’s programming model looks familiar — same annotation — but the runtime is heavier: application server or standalone transaction manager like Atomikos/Narayana, XA drivers, recovery logs, and ops runbooks for in-doubt transactions.

Spring Boot apps today often do not go there. Cloud datastores, managed Kafka, and polyglot stores frequently lack honest XA support. Even when XA works, holding locks across prepare and commit under latency kills throughput. Teams discovered that “just enable two-phase commit” was rarely the product-friendly answer for long workflows.

Still, you should know the vocabulary. Global transaction versus local. Resource manager versus transaction manager. `UserTransaction` begin/commit in raw JTA versus Spring’s declarative boundary on top. Heuristic exceptions when participants disagree after prepare. Those words show up in postmortems even when your team chose not to use XA.

A misconception is assuming `@Transactional` automatically spans every bean interaction — REST calls to other services, Mongo writes, Redis updates. It does not. A local `DataSourceTransactionManager` covers one JDBC resource. Crossing process or technology boundaries without XA means you either accept eventual inconsistency or design for it. Another misconception is treating distributed transactions as “Spring’s fault” when they hurt. The protocol’s cost is inherent; Spring only integrates with it.

So the honest fork in the road appears. Either invest in XA where both resources truly support it and the business demands strict atomicity across them, or stop pretending one ACID transaction can cover a multi-service workflow. The second path needs a different coordination style: a sequence of local transactions plus compensations when a later step fails.

That pattern has a name — saga — and it is the next episode’s problem to solve.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 56 (*Distributed Transactions*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
