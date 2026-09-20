# Episode 04 — Dependency Injection

| Field | Value |
|---|---|
| Episode | 04 |
| Title | Dependency Injection |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 4 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Knowing that the container owns creation is useful — until you ask the practical question: how do my objects actually receive what they need?

Inversion of Control tells you who is in charge. Dependency Injection is the everyday mechanism. It is how a service gets a repository, how a controller gets a service, how a gateway gets a config object — without each class reaching into a global registry to fetch friends.

Start from a familiar mess. A class constructs collaborators with `new`, or asks a service locator for them, or reaches into static holders. The class now knows too much: which implementation exists, how it is configured, and when it is born. Tests inherit that knowledge. Swapping a real payment client for a fake means editing production construction paths or inventing brittle wrappers.

Dependency Injection flips that. The class declares dependencies. Someone else supplies them. In Spring, that someone is the container during wiring.

There are a few injection styles, and they are not equal in clarity. Constructor injection passes required collaborators when the object is created. Setter injection assigns optional or mutable dependencies after construction. Field injection writes directly into annotated fields. Spring can do all three. Modern Spring style strongly prefers constructor injection for required dependencies, because the object cannot exist in a half-built state and the dependencies are obvious in the signature.

```java
@Service
public class PricingService {
    private final TaxCalculator tax;
    private final DiscountPolicy discounts;

    public PricingService(TaxCalculator tax, DiscountPolicy discounts) {
        this.tax = tax;
        this.discounts = discounts;
    }

    public Money quote(Cart cart) {
        Money base = discounts.apply(cart);
        return tax.apply(base);
    }
}
```

Walk that code with the DI lens. `@Service` is just a stereotype that helps component scanning find the class. The constructor lists what pricing truly needs. Spring looks at the parameter types, finds beans that match, and calls the constructor. Inside `quote`, there is no lookup. There is only collaboration.

Notice what became easy. In a unit test, you can write `new PricingService(new FakeTax(), new NoDiscount())` without starting Spring at all. That is not a side benefit. That is evidence the design is honest. If you cannot construct the object in a test without a container, the object is probably still doing lookup work in disguise.

How does Spring choose which bean to inject when several candidates share a type? It uses type matching first. If more than one bean fits, you narrow with `@Qualifier`, `@Primary`, or more specific types. Ambiguity is not a Spring bug — it is the container refusing to guess when your graph is unclear. Treat that error as design feedback.

Field injection looks shorter, and that brevity is exactly why it tempts beginners.

```java
@Service
public class FragilePricingService {
    @Autowired
    private TaxCalculator tax;
}
```

It works until testing, immutability, or required-dependency clarity matters. The field can remain `null` if something skips the container path. The dependencies are invisible in the constructor. Prefer constructors for required pieces. Use setters when a dependency is truly optional or must change. Keep field injection for legacy code and narrow framework cases, not as your default style.

DI also changes how you think about interfaces. If `PricingService` depends on `TaxCalculator`, you can ship a local rule engine today and a remote tax microservice adapter tomorrow without rewriting callers. Program to interfaces, inject implementations. Spring's type-based wiring makes that natural.

A common misunderstanding is that Dependency Injection means "put `@Autowired` on everything." Autowiring is one way Spring finds candidates. Injection is the design principle. Another misunderstanding is that IoC and DI are interchangeable words. IoC is the broader inversion of control. DI is the specific pattern of supplying dependencies from the outside. Spring's container is an IoC container that performs DI.

So today we moved from "the container creates beans" to "the container supplies collaborators." We preferred constructor injection, saw how type matching works, and named the failure mode of ambiguous beans.

The next natural question is where those beans live at the lowest API level — the factory that can get a bean by name or type.

That is Episode Five — BeanFactory.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 4 (*Dependency Injection*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
