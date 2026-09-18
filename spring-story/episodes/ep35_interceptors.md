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

Filters speak Servlet. Interceptors speak Spring MVC: handlers, handler mappings, and the lifecycle around controller invocation.

Recall the dispatcher pipeline. After `HandlerMapping` resolves a `HandlerExecutionChain`, that chain includes interceptors. `DispatcherServlet` calls `preHandle` on each interceptor before the `HandlerAdapter` invokes the controller. After a successful invocation it calls `postHandle`. After completion — including when an exception was thrown — it calls `afterCompletion`. That is a different timeline from the servlet filter chain, and a different example set.

Use interceptors when the cross-cutting concern needs MVC context. Examples: measure how long a mapped controller method took; reject requests to handlers missing a custom annotation; add common model attributes for view controllers; enforce tenancy rules based on the chosen handler type. Do not use them to replace servlet-level authentication that must run even when no handler exists — that remains filter work.

```java
public class HandlerTimingInterceptor implements HandlerInterceptor {

    private static final String START = "timing.start";

    @Override
    public boolean preHandle(
            HttpServletRequest request,
            HttpServletResponse response,
            Object handler) {
        request.setAttribute(START, System.nanoTime());
        return true; // false would abort the chain before the controller
    }

    @Override
    public void afterCompletion(
            HttpServletRequest request,
            HttpServletResponse response,
            Object handler,
            Exception ex) {
        Long start = (Long) request.getAttribute(START);
        if (start == null) {
            return;
        }
        long tookMs = (System.nanoTime() - start) / 1_000_000;
        String handlerName = (handler instanceof HandlerMethod hm)
                ? hm.getBeanType().getSimpleName() + "#" + hm.getMethod().getName()
                : String.valueOf(handler);
        // log: handlerName, tookMs, status, ex
    }
}

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new HandlerTimingInterceptor())
                .addPathPatterns("/orders/**")
                .excludePathPatterns("/orders/health");
    }
}
```

Notice what this example knows that the correlation-id filter did not: the `handler` object, often a `HandlerMethod` naming the controller type and method. Path patterns are MVC path patterns, not servlet filter URL mappings. Returning `false` from `preHandle` stops the controller from running and skips later interceptors’ `preHandle` — you become responsible for the response.

`postHandle` runs only after a successful controller return, before the view is rendered (for view-based MVC). For `@RestController` APIs, `afterCompletion` is often the more useful hook because there is no view phase in the classic sense. Always treat `afterCompletion` as the place to clean up thread-locals or timing state, because it runs on the exceptional path too when the dispatcher triggers it.

A second interceptor example clarifies annotation-driven gates. Suppose only methods marked `@Audited` should emit domain audit events. In `preHandle`, cast `handler` to `HandlerMethod`, look for the annotation, and stash a flag. In `afterCompletion`, if the flag is set and `ex` is null, write the audit record. That logic cannot live cleanly in a servlet filter because the filter never receives the handler method metadata. Path patterns on the registry still help: apply the interceptor only under `/orders/**` so unrelated actuators stay quiet.

Keep interceptors light. Database work in `preHandle` on every request becomes a latency tax. Prefer reading request attributes set by an earlier filter — for example a correlation id — rather than recomputing them.

A topic-specific misconception is registering a "filter-like" interceptor and expecting it to see 404s for unmapped URLs. If no handler was mapped, your interceptor never entered the chain. Another is stuffing security authentication solely into an interceptor and leaving non-dispatcher routes unprotected. A third is mutating the response body in `postHandle` for REST controllers and fighting message converters — prefer controller advice or filters for raw body wrapping.

So today we separated layers with different examples: servlet filters for early HTTP wrapping, MVC interceptors for handler-aware hooks, with timing around `/orders/**` as the concrete interceptor case.

One more request shape still sits outside ordinary JSON bodies. Clients upload files — invoices, images, CSVs — as multipart streams with size limits and different binding rules. How does Spring expose that without making you parse MIME by hand?

File upload is that story.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 35 (*Interceptors*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
