# Episode 29 — DispatcherServlet

| Field | Value |
|---|---|
| Episode | 29 |
| Title | DispatcherServlet |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 29 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A luggage scanner at the harbor gate pings your Boot process: `GET /luggage/TAG-8841`. Tomcat accepted the socket. Something inside the JVM still has to decide which Java method owns that tag, call it, and write JSON back. That center of gravity is not "Spring magic." It is `DispatcherServlet`.

Harbor teams used to register a servlet per concern — one for luggage tags, one for berth boards, one for customs forms. Each copy-pasted encoding, error pages, and content-type negotiation. Change the error shape in luggage and forget customs. The front-controller pattern collapses that duplication: one servlet owns the HTTP pipeline; handlers answer one kind of request.

In a Boot web app you rarely declare `DispatcherServlet` by hand. `DispatcherServletAutoConfiguration` registers it, usually mapped to `/`. Underneath it remains a servlet. Every request that reaches it runs `doDispatch`. If you can narrate `doDispatch`, you can debug a 404 without a slide deck.

Walk `GET /luggage/TAG-8841` through the chain. The HTTP request arrives at the servlet container. The container hands it to `DispatcherServlet`. The servlet asks a `HandlerMapping`: given this URL, verb, and headers, which handler should run? The mapping returns a `HandlerExecutionChain` — typically a controller method plus any interceptors. Next the servlet asks a `HandlerAdapter`: can you invoke this kind of handler? Annotated controllers are not called by raw reflection from the servlet. An adapter binds parameters, invokes the method, and wraps the return value. The adapter calls the controller. The controller returns a body — for luggage, a tag status payload — and the servlet finishes the response. The client sees status, headers, and bytes.

Say the pipeline once without ornament: HTTP request → `DispatcherServlet` → `HandlerMapping` → `HandlerAdapter` → controller → response. If you keep only one diagram from this lesson, keep that.

Here is the handler the mapping will find for that luggage tag — ordinary Spring MVC code, not a call you make into `doDispatch` yourself:

```java
@RestController
@RequestMapping("/luggage")
public class LuggageTagController {

    private final LuggageLookup lookup;

    public LuggageTagController(LuggageLookup lookup) {
        this.lookup = lookup;
    }

    @GetMapping("/{tag}")
    public LuggageStatus byTag(@PathVariable String tag) {
        return lookup.statusFor(tag)
                .orElseThrow(() -> new TagNotFoundException(tag));
    }
}
```

At startup, a `RequestMappingHandlerMapping` reads `@GetMapping("/{tag}")` and records that `GET /luggage/TAG-8841` belongs to `byTag`. At request time, `DispatcherServlet` asks that mapping “which handler?” and gets back this method (plus interceptors). Separately, a `RequestMappingHandlerAdapter` answers “how do I call it?” — bind `{tag}` from the path, invoke `byTag`, write the returned `LuggageStatus` as JSON via message conversion. Mapping chooses; adapting invokes. That split is why the same servlet can drive a Thymeleaf berth board and this luggage JSON endpoint without becoming a god class.

```java
// Conceptual shape of doDispatch — not an API you call yourself
// 1. resolve multipart if needed
// 2. mappedHandler = getHandler(request)          // HandlerMapping → LuggageTagController#byTag
// 3. ha = getHandlerAdapter(mappedHandler.getHandler())
// 4. interceptors preHandle...
// 5. mv = ha.handle(request, response, handler)   // adapter invokes byTag
// 6. processDispatchResult(...)                   // @ResponseBody JSON write
// 7. interceptors postHandle / afterCompletion
```

Operationally, Boot’s default is one dispatcher for the app. Filters still sit outside this story on the servlet filter chain. Interceptors sit inside the handler execution chain. Those layers get their own lessons. The center holds either way: almost every Spring MVC request you care about passes through `doDispatch`.

People sometimes treat `DispatcherServlet` as the thing that wires collaborators or as a synonym for the application context. Wrong layer. The servlet uses the web application context to find mappings and adapters. It does not assemble your luggage lookup graph. Another trap: assuming every controller annotation is interpreted at request time by the servlet itself. Mapping metadata is read at startup into handler mappings; invocation is delegated to an adapter when traffic arrives. Memorizing "Boot auto-configures a dispatcher" will not help you when `GET /luggage/TAG-8841` returns 404 — that usually means no `HandlerMapping` claimed the path. A 415 or binding failure usually means the adapter and converters disagreed with the client. Those failures live on this pipeline.

We named the front door and watched one luggage GET move through mapping and adaptation into `LuggageTagController`. Controllers are no longer a mystery shape — but the annotations that claim verbs, paths, and payloads still deserve their own slow look: how `@GetMapping` and `@PathVariable` become mapping metadata, what happens when two methods compete for the same pattern, and how a return type becomes a status and a body.

That is where controller design starts.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 29 (*DispatcherServlet*).
