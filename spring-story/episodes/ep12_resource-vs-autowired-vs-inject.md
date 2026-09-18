# Episode 12 — @Resource vs @Autowired vs @Inject

| Field | Value |
|---|---|
| Episode | 12 |
| Title | @Resource vs @Autowired vs @Inject |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 12 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Component scanning filled the context with candidates. Then a wiring error appears that looks like a riddle: two beans implement `NotifyClient`, and three different annotations on the field all claim to inject "the" client.

A notification facade declares `@Autowired NotifyClient client` and fails with `NoUniqueBeanDefinitionException` because both `EmailNotifyClient` and `SmsNotifyClient` match by type. A teammate "fixes" it by switching to `@Resource` without changing names — and suddenly email wins because the field is named `emailNotifyClient` in another branch, or fails because the field name matches nothing. A third engineer brings `@Inject` from Jakarta and expects qualifier semantics that Spring's `@Autowired` taught them. Same injection goal; different matching rules; confused reviews.

What goes wrong is treating the annotations as synonyms. They are not. The engineer asks: when I have multiple candidates, which annotation matches how — and which should this codebase standardize on?

Spring understands all three. `@Autowired` is Spring's annotation: primary matching is by type, then qualifiers, with `@Primary` as a tie-breaker; `required` defaults to true. `@Inject` is the Jakarta/JSR-330 standard: also type-driven, with `@Named` for qualification; no `required` attribute like Spring's. `@Resource` is JSR-250: name-first matching — the field or setter name, or the `name` attribute — then type if needed. That name-first behavior is why `@Resource` feels magical or broken depending on whether your field name equals a bean name.

```java
@Service
public class NotificationFacade {
    private final NotifyClient email;
    private final NotifyClient sms;

    public NotificationFacade(
            @Autowired @Qualifier("emailNotifyClient") NotifyClient email,
            @Resource(name = "smsNotifyClient") NotifyClient sms) {
        this.email = email;
        this.sms = sms;
    }

    public void push(User user, String body) {
        email.send(user.email(), body);
        sms.send(user.phone(), body);
    }
}

@Component("emailNotifyClient")
public class EmailNotifyClient implements NotifyClient { /* ... */ }

@Component("smsNotifyClient")
public class SmsNotifyClient implements NotifyClient { /* ... */ }
```

At wiring time, Spring resolves the first constructor parameter by type `NotifyClient` narrowed by `@Qualifier("emailNotifyClient")`. The second uses `@Resource(name = "smsNotifyClient")`, which looks up that bean name directly. Both end as injected collaborators. If you dropped the qualifier on an `@Autowired` parameter, startup would fail on ambiguity. If you renamed the `@Resource` target bean without updating `name`, lookup would fail even though a compatible type still exists — name-first means the name matters.

For modern Spring style, prefer constructor injection without field annotations when there is a single candidate. When you must disambiguate, `@Autowired` with `@Qualifier` (or `@Primary` on the default bean) keeps the rules obvious. Use `@Resource` when you intentionally want name-based lookup, especially bridging older Java EE style. Use `@Inject` when you want a standards annotation for portability across DI containers — knowing Spring still performs the injection underneath.

The misconception to kill is "they all do the same thing, pick any." Matching order differs, attribute sets differ, and mixing them without a team rule makes failures harder to read. Another misconception: putting `@Autowired` on every constructor parameter "for clarity" when a single constructor already implies autowiring in modern Spring.

Stereotypes and injection annotations cover types you own. They do not help when you must assemble a `RestTemplate`, an `ObjectMapper`, or a vendor SDK you cannot annotate. That gap is why `@Configuration` classes exist as the home for explicit factory methods — which is where we go next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 12 (*@Resource vs @Autowired vs @Inject*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
