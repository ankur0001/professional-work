# Episode 34 — Filters

| Field | Value |
|---|---|
| Episode | 34 |
| Title | Filters |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 34 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Some work must run before Spring MVC wakes up — and sometimes after the response is committed. Servlet filters sit on the container’s filter chain for exactly that reason.

Imagine you need a correlation id on every request, including static asset misses and calls that never reach a controller. Or you need to reject an unauthenticated call before `DispatcherServlet` spends time on mapping. Or you must wrap the request to enforce UTF-8 encoding. Those concerns are not controller problems. They are servlet-pipeline problems. The Jakarta Servlet `Filter` API is the standard hook: `doFilter(request, response, chain)`.

The chain is literal. The container holds an ordered list of filters, then the target servlet — in our case usually `DispatcherServlet`. Filter A calls `chain.doFilter`, which enters Filter B, which eventually reaches the servlet, which produces a response, then the stack unwinds back through the filters. That means a filter can work on the way in, on the way out, or both. It can also short-circuit by not calling `chain.doFilter` and writing its own response.

```java
@Component
@Order(1)
public class CorrelationIdFilter extends OncePerRequestFilter {

    public static final String HEADER = "X-Correlation-Id";

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {

        String cid = request.getHeader(HEADER);
        if (cid == null || cid.isBlank()) {
            cid = UUID.randomUUID().toString();
        }
        response.setHeader(HEADER, cid);
        request.setAttribute(HEADER, cid);

        filterChain.doFilter(request, response);
    }
}
```

Prefer `OncePerRequestFilter` in Spring apps when you want the body to run once per request dispatch and avoid double work on forwards. Registering as a `@Component` lets Boot pick it up; `@Order` influences relative order among Spring-registered filters. For security, Spring Security installs its own filter chain — another reminder that filters are the native place for authentication gates that must wrap the dispatcher.

Contrast this carefully with what comes next. Filters do not know which controller method will run. They see `HttpServletRequest` and `HttpServletResponse`. They run for any servlet mapping they are attached to, including paths that later 404 inside MVC. They are the right tool for raw HTTP concerns: compression wrappers, CORS at the edge, TLS-related headers, early rejects, request logging that must include non-MVC traffic.

Ordering bugs are common. If Filter A wraps the response for metrics and Filter B short-circuits auth, metrics may miss denied calls — or count them twice — depending on order. Draw the chain on paper when behavior surprises you: container filters, Spring Security’s filter chain, your `OncePerRequestFilter` beans, then `DispatcherServlet`. Boot’s `FilterRegistrationBean` gives explicit control when `@Order` alone is not enough.

Request wrapping is another filter specialty. Need to read the body twice — once for a signature check, once for MVC binding? A wrapping filter that caches the input stream is the servlet-native approach. Controllers and interceptors should not invent that mechanism.

A topic-specific misconception is using filters as a substitute for Spring MVC interceptors because "they feel the same." They are not the same layer. If you need the handler method, model attributes, or MVC-specific pre/post hooks tied to mapped controllers, you want a `HandlerInterceptor`, not a servlet filter. Another misconception is forgetting to call `filterChain.doFilter` and wondering why controllers never run. A third is doing heavy business logic in filters — you bypass the programming model of controllers, validation, and advice.

So today we placed filters on the servlet chain, walked in-and-out behavior, and built a correlation-id filter as a concrete early-pipeline example that does not depend on controller mapping.

That leaves a gap. What if you need cross-cutting behavior that *does* know the chosen handler — timing only mapped controller calls, adding model attributes for views, or applying rules based on handler annotations? That is interceptor territory.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 34 (*Filters*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
