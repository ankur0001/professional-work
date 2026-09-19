# Episode 27 — Profiles (Boot)

| Field | Value |
|---|---|
| Episode | 27 |
| Title | Profiles |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 27 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Staging ferry checkout fails a payment smoke test — or rather, succeeds against the wrong place. The charge appears on the production merchant dashboard. Root cause: `application-prod.yml` held `payment.merchant-id: ferry_live_9f3`, and the staging Deployment set `SPRING_PROFILES_ACTIVE` empty. Only `application.yml` loaded, and someone had "temporarily" put the live merchant id in the default file during a firefight. Boot profiles were supposed to keep merchant IDs apart. Defaults betrayed them.

Boot builds on Framework profiles with file conventions: `application.yml` plus `application-{profile}.yml`, multi-document YAML with `spring.config.activate.on-profile`, and profile groups. Active profiles select which documents join the Environment. The same artifact carries every profile's config; activation chooses the slice. Filename alone never means "we are in prod."

```yaml
# application.yml — safe defaults only
payment:
  merchant-id: ferry_dev_local
  connect-timeout: 2s

---
# application-staging.yml
spring:
  config:
    activate:
      on-profile: staging
payment:
  merchant-id: ferry_staging_4a1

---
# application-prod.yml
spring:
  config:
    activate:
      on-profile: prod
payment:
  merchant-id: ferry_live_9f3
```

```java
@ConfigurationProperties(prefix = "payment")
public record PaymentProperties(String merchantId, Duration connectTimeout) {}

@Service
public class FerryPaymentClient {
    private final PaymentGateway gateway;
    private final PaymentProperties props;

    public FerryPaymentClient(PaymentGateway gateway, PaymentProperties props) {
        this.gateway = gateway;
        this.props = props;
    }

    public ChargeResult charge(Booking booking) {
        return gateway.charge(props.merchantId(), booking.total());
    }
}
```

Walk the documents. Default `application.yml` holds only safe local values — never live merchant IDs. The staging document activates only when profile `staging` is on and overlays `payment.merchant-id`. Prod document likewise. `PaymentProperties` binds whatever won in the Environment after activation. `FerryPaymentClient.charge` passes `props.merchantId()` to the gateway — one code path, environment-selected credentials. Scrubbing defaults after the incident is as important as setting `SPRING_PROFILES_ACTIVE=staging` on the Deployment.

Runtime with `SPRING_PROFILES_ACTIVE=staging`. Boot loads default documents, then staging overlays `payment.merchant-id` → `ferry_staging_4a1`. `PaymentProperties` binds that value at context refresh. Empty active profiles leave `ferry_dev_local` — or whatever unsafe value you left in defaults, which is how live ids leaked. Profile-specific beans (`@Profile("prod")` payment circuit breakers) register only when that profile is on. Groups like `spring.profiles.group.production=prod,metrics` activate a bundle with one name so ops sets a single token.

Failure mode symptoms: staging smoke test charge appears on prod merchant dashboard; `payment.merchant-id` in a secured env dump shows `ferry_live_9f3` while hostname is staging; `Environment.getActiveProfiles()` empty or unexpectedly `prod`. Another failure: both `staging` and `prod` active by misconfiguration — last-wins overlay rules and document order decide the merchant id; do not rely on "both" as a feature for payments. CI that never asserts active profiles on a staging deploy will miss this class of bug until money moves.

Trade-offs. Boot profile documents keep one JAR for all environments and pair cleanly with `@ConfigurationProperties`; they concentrate risk in activation and default hygiene. Separate artifacts per environment avoid activation mistakes and multiply build pipelines. Prefer safe defaults + mandatory profile in non-local envs (fail startup if `prod`/`staging` missing when a property `app.require-profile=true`) over clever multi-profile bags for payment config.

Compare Framework `@Profile` on beans with Boot's document overlays: both honor `spring.profiles.active`, but Boot adds the file/document convention so merchant IDs can live in YAML without alternate `@Bean` methods. The ferry bug was a document problem — wrong values in the default file — not a missing `@Profile` on a class. When both exist, activation still gates everything; Boot does not invent a profile from a hostname. Put live secrets and merchant IDs only in profile-specific documents or external mounts, and keep defaults harmless enough that an empty `SPRING_PROFILES_ACTIVE` cannot charge real cards. A staging smoke test that asserts `payment.merchant-id` starts with `ferry_staging_` catches this class of bug before money moves.

Misconception unique to Boot profiles: "`application-prod.yml` is used automatically in production because the filename contains prod." Filename alone does nothing. Something must activate `prod` — env var, config server, or argument. Filename is a convention for which document binds when that profile is active.

Merchant IDs stay in the right environments after defaults are scrubbed. Platform still ships a 180MB fat jar into every tram-timetable container layer, and image pulls dominate deploy time. How Boot packages that jar — fat versus layered — is the remaining deploy-shape problem.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 27 (*Profiles*).
