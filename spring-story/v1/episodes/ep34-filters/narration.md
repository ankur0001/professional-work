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

At 02:17 the customs API drops a request somewhere between the load balancer and a controller. Ops asks for a correlation id. If that id only appears after `DispatcherServlet` maps a handler, you have already lost the misses — static asset 404s, rejected auth, paths that never matched. Correlation belongs earlier: on the servlet filter chain.

Filters sit on the container’s filter chain, outside Spring MVC’s handler story. The Jakarta Servlet `Filter` API is the standard hook: `doFilter(request, response, chain)`. You wrap, reject, or decorate, then either call `chain.doFilter` to continue or write a response and stop. For a customs API, the classic early job is ensuring every request carries `X-Request-Id` before security and MVC spend time on the call.

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class RequestIdFilter extends OncePerRequestFilter {

    public static final String HEADER = "X-Request-Id";

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {
        String incoming = request.getHeader(HEADER);
        String requestId = (incoming == null || incoming.isBlank())
                ? UUID.randomUUID().toString()
                : incoming.trim();

        response.setHeader(HEADER, requestId);
        MDC.put("requestId", requestId);
        try {
            filterChain.doFilter(request, response);
        } finally {
            MDC.remove("requestId");
        }
    }
}
```

`OncePerRequestFilter` keeps the logic from running twice on forwards. `@Order` with highest precedence puts the filter early so later security filters and `DispatcherServlet` inherit the id on the response and in MDC logs. If the client already sent `X-Request-Id`, honor it; otherwise mint one. Either way, the outbound header is set even when no controller ever runs.

Mental model the chain: incoming request → your filters (in order) → `DispatcherServlet` → … → response unwinds back through filters. Encoding filters, compression filters, and Spring Security’s filter chain all live here. They do not receive a `HandlerMethod`. They do not know whether `/customs/declarations` mapped. That ignorance is a feature when you need work for every HTTP exchange.

Registering filters in Boot is usually `@Component` plus optional `FilterRegistrationBean` when you need URL patterns or an explicit name. Ordering matters: a security filter that rejects before your request-id filter runs will leave ops without the header on 401s — put identity-of-request first when that is the ops contract.

Filters are not interceptors with a different annotation. If you need the chosen handler method, model attributes, or MVC-specific pre/post hooks tied to mapped controllers, you want a `HandlerInterceptor`. Forgetting `filterChain.doFilter` and wondering why controllers never run is another classic. Heavy customs business rules in a filter bypass validation, advice, and the programming model you just built — keep filters thin and mechanical.

You can stamp every customs call with a request id before MVC wakes up. What if you need cross-cutting behavior that *does* know the chosen handler — timing only mapped admin console methods, or rules based on handler annotations? That is interceptor territory.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 34 (*Filters*).
