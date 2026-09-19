# Episode 35 — Interceptors

| Field | Value |
|---|---|
| Episode | 35 |
| Title | Interceptors |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 35 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Filters speak Servlet. Interceptors speak Spring MVC: handlers, handler mappings, and the lifecycle around controller invocation. The port operations console makes that distinction concrete — you want timing on `/admin/**` handler methods, not on every static asset and health ping.

Recall the dispatcher pipeline. After `HandlerMapping` resolves a `HandlerExecutionChain`, that chain includes interceptors. `DispatcherServlet` calls `preHandle` on each interceptor before the `HandlerAdapter` invokes the controller. After a successful invocation it calls `postHandle`. After completion — including when an exception was thrown — it calls `afterCompletion`. That timeline is inside MVC, after a handler was chosen.

```java
public class AdminTimingInterceptor implements HandlerInterceptor {

    private static final Logger log = LoggerFactory.getLogger(AdminTimingInterceptor.class);
    private static final String START = AdminTimingInterceptor.class.getName() + ".start";

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
                             Object handler) {
        request.setAttribute(START, System.nanoTime());
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
                                Object handler, Exception ex) {
        Object start = request.getAttribute(START);
        if (start instanceof Long nanos) {
            long tookMs = (System.nanoTime() - nanos) / 1_000_000;
            String handlerLabel = handler instanceof HandlerMethod hm
                    ? hm.getBeanType().getSimpleName() + "#" + hm.getMethod().getName()
                    : String.valueOf(handler);
            log.info("admin handler={} status={} tookMs={} error={}",
                    handlerLabel, response.getStatus(), tookMs, ex != null);
        }
    }
}
```

```java
@Configuration
public class PortConsoleWebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new AdminTimingInterceptor())
                .addPathPatterns("/admin/**")
                .excludePathPatterns("/admin/health");
    }
}
```

Path patterns on the registry are the point of this lesson’s scenario: only `/admin/**` pays the timing tax. Berth boards and public parcel GETs stay quiet. Returning `false` from `preHandle` aborts the chain — useful for annotation-driven gates, dangerous if you forget to write a response.

A second interceptor pattern clarifies why filters cannot replace this layer. Suppose only methods marked `@Audited` should emit console audit events. In `preHandle`, cast `handler` to `HandlerMethod`, look for the annotation, and stash a flag. In `afterCompletion`, if the flag is set and `ex` is null, write the audit record. A servlet filter never receives that handler method metadata.

`postHandle` runs only after a successful handler return and before the view is rendered — less useful for pure `@RestController` JSON, still useful for adding model attributes on view controllers. Prefer `afterCompletion` for timing and cleanup because it runs on success and failure.

Registering the same logic as both a filter and an interceptor "just in case" doubles work and muddies logs. Putting security authentication solely in an interceptor also fails closed paths that never map — authentication that must run even when no handler exists remains filter work. And measuring every path under `/**` recreates the noise you avoided by scoping to `/admin/**`.

Servlet filters cover early HTTP wrapping; MVC interceptors cover handler-aware hooks. One request shape still sits outside ordinary JSON bodies: clients upload files — bill-of-lading PDFs — as multipart streams with size limits and different binding rules. How Spring exposes that without hand-parsing MIME is next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 35 (*Interceptors*).
