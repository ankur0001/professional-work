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

The tide API flakes. Not always — just enough that berth planners see timeouts on calm mornings. You do not want every caller to invent its own retry loop. You want one place that says: around tide fetches, retry a couple of times, then surface the failure. That “around” is advice. A proxy gives you a place to stand; advice is what you do while standing there.

Spring’s annotation model maps cleanly onto spoken intent: before, after returning, after throwing, after finally, and around.

```java
@Aspect
@Component
public class TideAdviceExample {

    private static final Logger log = LoggerFactory.getLogger(TideAdviceExample.class);

    private final TideClient tides;

    public TideAdviceExample(TideClient tides) {
        this.tides = tides;
    }

    @Before("execution(* com.harbor.tide.TideService.forecast(..))")
    public void denyIfStationDown(JoinPoint jp) {
        if (StationBoard.isRed()) {
            throw new TideStationOfflineException("station red");
        }
        log.debug("forecast via {}", jp.getSignature().toShortString());
    }

    @AfterReturning(
            pointcut = "execution(* com.harbor.tide.TideService.forecast(..))",
            returning = "window")
    public void publishOk(JoinPoint jp, TideWindow window) {
        Events.publish(TideForecastReady.of(window));
    }

    @AfterThrowing(
            pointcut = "execution(* com.harbor.tide.TideService.forecast(..))",
            throwing = "ex")
    public void publishFail(JoinPoint jp, TideTimeoutException ex) {
        Events.publish(TideForecastFailed.of(ex.getStationId()));
    }

    @After("execution(* com.harbor.tide.TideService.forecast(..))")
    public void clearThreadLocals() {
        TideContext.clear();
    }

    @Around("execution(* com.harbor.tide.TideService.forecast(..))")
    public Object retryFlakyTide(ProceedingJoinPoint pjp) throws Throwable {
        int attempts = 0;
        while (true) {
            try {
                attempts++;
                return pjp.proceed();
            } catch (TideTimeoutException ex) {
                if (attempts >= 3) {
                    throw ex;
                }
                log.warn("tide timeout, retry {}", attempts);
            }
        }
    }
}
```

Walk each kind. `@Before` runs before the target; it can throw and stop the call — here a red station board freezes forecasts. `@AfterReturning` runs only on success and can bind the returned `TideWindow`. `@AfterThrowing` runs only when the target throws, binding the exception type you care about. `@After` is the finally analog — good for clearing thread state. `@Around` is the power tool: receive a `ProceedingJoinPoint`, choose whether to call `proceed`, call it multiple times for retry, replace arguments, replace the return value, or wrap exceptions. The flaky tide retry lives naturally here.

Transaction management is around-style in spirit: begin before proceed, commit or roll back after. Security checks are often before or around. Timing is naturally around. Prefer the weakest advice that expresses intent. If you only need to log a return value, `@AfterReturning` is clearer than an `@Around` that always proceeds.

Order among advice kinds on the same join point follows Spring’s rules; when multiple aspects apply you need explicit aspect ordering later. Inside one `@Around`, your code’s structure is the order: before `proceed` is before; after is after.

Misuse patterns are familiar. Calling `proceed` twice by accident doubles side effects — fine for deliberate retry, disastrous for a charge. Forgetting `proceed` silently skips business logic. Heavy domain work in `@Before` muddies the aspect. Swallowing exceptions inside `@Around` without rethrow can bypass `@AfterThrowing` and transactional rollback you thought you had.

Advice answers “what happens at the join point.” It does not answer “which join points.” Without a precise selector, the same advice might attach to every public method — or to nothing.

Aiming the advice is the job of pointcuts.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 62 (*Advice*).
