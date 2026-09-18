# Episode 62 — Advice

| Field | Value |
|---|---|
| Episode | 62 |
| Title | Advice |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 62 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A proxy gives you a place to stand. Advice is what you do while standing there. Before the real method? After it returns? Only when it throws? Wrapped around it so you control whether it runs at all? Each of those is a different advice kind, and choosing the wrong one creates either missed cleanup or tangled control flow.

Spring’s annotation model maps cleanly onto spoken intent.

```java
@Aspect
@Component
public class PaymentAdviceExample {

    private static final Logger log = LoggerFactory.getLogger(PaymentAdviceExample.class);

    @Before("execution(* com.example.pay.PaymentService.capture(..))")
    public void denyIfMaintenance(JoinPoint jp) {
        if (MaintenanceWindow.active()) {
            throw new PaymentsFrozenException("maintenance");
        }
        log.debug("capturing via {}", jp.getSignature().toShortString());
    }

    @AfterReturning(
            pointcut = "execution(* com.example.pay.PaymentService.capture(..))",
            returning = "receipt")
    public void publishSuccess(JoinPoint jp, Receipt receipt) {
        Events.publish(PaymentCaptured.of(receipt));
    }

    @AfterThrowing(
            pointcut = "execution(* com.example.pay.PaymentService.capture(..))",
            throwing = "ex")
    public void publishFailure(JoinPoint jp, PaymentFailedException ex) {
        Events.publish(PaymentFailed.of(ex.getCode()));
    }

    @After("execution(* com.example.pay.PaymentService.capture(..))")
    public void clearThreadLocals() {
        PaymentContext.clear();
    }

    @Around("execution(* com.example.pay.PaymentService.capture(..))")
    public Object withDeadline(ProceedingJoinPoint pjp) throws Throwable {
        Deadline deadline = Deadline.after(Duration.ofSeconds(2));
        try {
            return pjp.proceed();
        } finally {
            deadline.close();
        }
    }
}
```

Walk each kind. `@Before` runs before the target. It can throw and stop the call — here, maintenance freezes captures. It cannot change the return value because the target has not returned yet. `@AfterReturning` runs only on success and can bind the returned `receipt`. `@AfterThrowing` runs only when the target throws, and can bind the exception type you care about. `@After` is the finally analog — success or failure — good for clearing thread state. `@Around` is the power tool: you receive a `ProceedingJoinPoint`, choose whether to call `proceed`, call it multiple times, replace arguments, replace the return value, or wrap exceptions.

Transaction management is around-style advice in spirit: begin before proceed, commit or roll back after. Security checks are often before or around. Timing and metrics are naturally around. Prefer the weakest advice that expresses your intent. If you only need to log a return value, `@AfterReturning` is clearer than an `@Around` that always proceeds and ignores half its power.

Order among advice kinds on the same join point follows Spring’s rules, and when multiple aspects apply you will need explicit aspect ordering — a later episode. Inside one `@Around`, your code’s structure is the order: whatever you write before `proceed` is before; whatever you write after is after.

Misuse patterns are familiar. Calling `proceed` twice by accident doubles side effects. Forgetting `proceed` silently skips business logic. Doing heavy work in `@Before` that belongs in the domain muddies the aspect. Catching exceptions inside `@Around` and swallowing them without rethrow can bypass `@AfterThrowing` listeners and transactional rollback behavior you thought you had.

Advice answers “what happens at the join point.” It does not answer “which join points.” Without a precise selector, the same advice might attach to every public method in the app — or to nothing, if the expression is wrong.

Aiming the advice is the job of pointcuts — next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 62 (*Advice*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
