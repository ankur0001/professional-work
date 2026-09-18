# Episode 05 — BeanFactory

| Field | Value |
|---|---|
| Episode | 05 |
| Title | BeanFactory |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 5 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Dependency Injection told us collaborators arrive from the outside. That sentence still hides a machine. Somewhere, Spring must store bean recipes and hand back instances when asked. At the lowest public API, that machine is `BeanFactory`.

Imagine you are debugging a CLI tool that embeds Spring only for wiring. You do not need HTTP events or message bundles yet. You need one honest question answered: given a name or a type, can the container produce the object? Without a factory abstraction, every module invents its own registry — static maps, service locators, thread-local holders. Those registries drift. Tests fight globals. Shutdown order becomes folklore.

What breaks without a bean factory is consistency. Two libraries register "the" `Clock` differently. Lookups disagree on lazy versus eager. You cannot ask a single API "do you have this bean?" across the process.

So the engineer asks: what is the minimal Spring interface that can create and retrieve managed objects?

`BeanFactory` is that interface. It is the root of the Spring container hierarchy. You register bean definitions with it — or load them through a reader — then call `getBean`. Implementations such as `DefaultListableBeanFactory` hold the definition map, resolve dependencies, and cache singletons. Historically, a raw `BeanFactory` is lazy: it does not create singletons until something requests them. That laziness is useful for constrained environments and for understanding the plumbing without the full application runtime.

```java
DefaultListableBeanFactory factory = new DefaultListableBeanFactory();

GenericBeanDefinition paymentDef = new GenericBeanDefinition();
paymentDef.setBeanClass(StripePaymentClient.class);
factory.registerBeanDefinition("paymentClient", paymentDef);

GenericBeanDefinition checkoutDef = new GenericBeanDefinition();
checkoutDef.setBeanClass(CheckoutService.class);
checkoutDef.getConstructorArgumentValues()
        .addIndexedArgumentValue(0, new RuntimeBeanReference("paymentClient"));
factory.registerBeanDefinition("checkoutService", checkoutDef);

CheckoutService checkout = factory.getBean("checkoutService", CheckoutService.class);
checkout.checkout(Cart.sample());
```

Step through the run. First the factory only holds metadata — two definitions, no instances. The `getBean` call for `checkoutService` forces instantiation. Spring sees the constructor needs `paymentClient`, creates that bean, injects it, returns `CheckoutService`. A second `getBean("checkoutService")` returns the same singleton instance from the singleton cache. You just watched the factory's core contract: define, resolve, cache, return.

Most applications never touch `DefaultListableBeanFactory` directly. They use `ApplicationContext`, which builds on this foundation. Still, when logs say "bean factory" or you read container source, this is the floor. Misread it as "the class I inject into services." You almost never inject `BeanFactory` into domain code; doing so recreates the service-locator smell DI was meant to erase. Reach for it in infrastructure, bootstrapping, or learning the model — not inside `OrderService`.

Another misconception: thinking `getBean` by string name is the normal application style. Names matter inside the container, but application code should prefer type-safe injection. String lookups are for the container's internals and for rare dynamic cases.

`BeanFactory` can create beans. Production systems usually want more on day one: environment abstraction, event publication, internationalization, and eager failure if a singleton cannot start. That richer runtime is `ApplicationContext` — and it is the natural next layer above this factory floor.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 5 (*BeanFactory*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
