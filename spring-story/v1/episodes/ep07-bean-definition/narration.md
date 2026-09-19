# Episode 07 — Bean Definition

| Field | Value |
|---|---|
| Episode | 07 |
| Title | Bean Definition |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 7 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The PR title is "register Stripe and Adyen from plugins.yml." The reviewer leaves one comment in red: "We are not scanning `@Component` on vendor jars we do not control. Metadata only." The author wanted to drop annotated classes on the classpath and hope component scan invents beans. The marketplace platform loads payment plugins from YAML that marketing and partnerships can edit without a rebuild of every adapter class.

That fight is about bean definitions. A bean definition is the recipe Spring holds before any instance exists: bean name, class (or factory method), scope, constructor arguments, property values, lazy flag, depends-on, primary, init/destroy method names, and more. Instances are cakes. Definitions are recipes. You can have a recipe with zero cakes baked yet — and you can register a recipe for a class that lives in a jar you must not component-scan.

```yaml
# plugins.yml — marketplace payment adapters
plugins:
  - id: stripeCheckout
    className: com.market.payments.StripeCheckoutPlugin
    apiKeyProp: stripe.api-key
  - id: adyenCheckout
    className: com.market.payments.AdyenCheckoutPlugin
    apiKeyProp: adyen.api-key
```

```java
@Configuration
public class PaymentPluginRegistrar {

    @Bean
    BeanDefinitionRegistryPostProcessor paymentPlugins(Environment env) {
        return registry -> {
            List<PluginSpec> specs = PluginSpec.load("classpath:plugins.yml");
            for (PluginSpec spec : specs) {
                GenericBeanDefinition def = new GenericBeanDefinition();
                def.setBeanClassName(spec.className());
                def.setScope(BeanDefinition.SCOPE_SINGLETON);
                ConstructorArgumentValues args = new ConstructorArgumentValues();
                args.addIndexedArgumentValue(0, env.getRequiredProperty(spec.apiKeyProp()));
                def.setConstructorArgumentValues(args);
                registry.registerBeanDefinition(spec.id(), def);
            }
        };
    }
}
```

Runtime order matters. During context bootstrap, Spring collects bean definitions into a `BeanDefinitionRegistry` — the same `DefaultListableBeanFactory` wears that hat. Sources of definitions include XML readers, `@Configuration` class parsing, component scanning, and programmatic registration. `BeanDefinitionRegistryPostProcessor` beans run early, after the registry exists but before most ordinary beans are instantiated. In this registrar, each YAML row becomes a `GenericBeanDefinition`: `setBeanClassName` stores a string so the class need not be loadable at registration time the way a hard-coded `Class<?>` literal would; `setScope` marks singleton; constructor args capture the resolved API key string from Environment. `registerBeanDefinition(spec.id(), def)` puts the recipe under `stripeCheckout` or `adyenCheckout`. Only later, when something needs those beans — an autowired `List<PaymentPlugin>`, a lookup by name, or singleton pre-instantiation at end of refresh — does the factory read each definition, load the class, invoke the constructor with the indexed argument, and cache the singleton. Change YAML, restart, new recipe set. No `@Component` on Stripe's SDK required; no vendor package added to `@ComponentScan`.

Walk a failure that QA hits when YAML drifts. Typo in `className` → `CannotLoadBeanClassException` or `ClassNotFoundException` wrapped when the definition is first instantiated, not when the YAML was parsed — registration succeeded with a bad string. Missing `stripe.api-key` → `getRequiredProperty` fails inside the post-processor and context refresh aborts before Tomcat accepts traffic; that is the loud failure you want. Duplicate `id` with an existing bean → `BeanDefinitionStoreException` / override behavior depending on `allowBeanDefinitionOverriding`. Registering after ordinary singleton instantiation has already begun is too late for this post-processor contract — wrong extension point, and the new names never appear in early autowiring. Another symptom: partnerships edits YAML to point at a class that exists but whose constructor signature no longer matches the indexed args — `BeanCreationException` naming the plugin id, with a nested constructor mismatch.

Trade-offs. Programmatic definitions give marketplace teams a metadata-driven plugin surface without scanning untrusted jars. You own validation: bad YAML becomes a startup incident unless you schema-check before `registerBeanDefinition`. Component scanning is simpler for first-party code you control; it is the wrong tool when the class lives in a vendor artifact annotated for someone else's product. XML `<bean>` elements are the same metadata idea in a different syntax — the registry does not care how the `BeanDefinition` object was born.

Misconception unique to bean definitions: "The `@Component` class is the bean definition." The annotation is a signal that a scanner should create a definition. The definition is a separate metadata object living in the registry. Two definitions can point at the same class with different names, scopes, or constructor args — `stripeCheckout` and `stripeCheckoutSandbox` might share a class and differ only in property values. Removing the annotation does not remove a definition you registered by hand. Another misconception: "Registering a definition creates the instance." Registration stores the recipe; creation happens on demand or during singleton pre-instantiation.

Partnerships ships a third plugin next week. QA files a nastier bug first: two hotel-booking browsers share one shopping cart bean, and guest A's room selection appears in guest B's checkout. The recipes are fine. The scope on the cart definition is wrong.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 7 (*Bean Definition*).
