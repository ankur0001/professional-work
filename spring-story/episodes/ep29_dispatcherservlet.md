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

You have a Boot app that starts. An embedded Tomcat is listening. A client fires `GET /orders/42`. Something in your process has to catch that request, decide which Java method should run, call it, and turn the result into bytes on the wire. That something is not "Spring magic." It has a name: `DispatcherServlet`.

Before a front controller, teams often registered many servlets — one for orders, one for payments, one for admin pages. Each servlet reinvented the same chores: character encoding, security checks, exception pages, content-type negotiation. Change the error format in one place and forget another. That duplication is the pain the front-controller pattern removes. One servlet owns the HTTP pipeline. Handlers focus on the request they were meant to answer.

Spring MVC’s front controller is `DispatcherServlet`. In a Boot web app you rarely declare it by hand. `DispatcherServletAutoConfiguration` registers it, maps it (often to `/`), and gives it an order. Underneath, it is still a servlet. On every request it runs `doDispatch`. That method is the story you should be able to narrate without looking at a slide.

Walk the path out loud. An HTTP request arrives at the servlet container. The container hands it to `DispatcherServlet`. The servlet asks a `HandlerMapping`: given this URL, method, and headers, which handler should run? The mapping returns a `HandlerExecutionChain` — typically a controller method plus any interceptors. Next the servlet asks a `HandlerAdapter`: can you invoke this kind of handler? Controllers annotated with `@RequestMapping` are not called by raw reflection from the servlet. An adapter knows how to bind parameters, call the method, and wrap the return value. The adapter invokes the controller. The controller returns a view name, a `ModelAndView`, or — for REST — a body that will be written as JSON. The servlet finishes the response and the client sees status, headers, and body.

That chain again, slower: HTTP request → `DispatcherServlet` → `HandlerMapping` → `HandlerAdapter` → controller → response. If you remember only one diagram from this episode, remember that.

```java
// Conceptual shape of doDispatch — not something you call yourself
// 1. resolve multipart if needed
// 2. mappedHandler = getHandler(request)          // HandlerMapping
// 3. ha = getHandlerAdapter(mappedHandler.getHandler())
// 4. interceptors preHandle...
// 5. mv = ha.handle(request, response, handler)   // invokes @Controller/@RestController
// 6. processDispatchResult(...)                   // view render or @ResponseBody write
// 7. interceptors postHandle / afterCompletion
```

Notice the strategy split. `HandlerMapping` answers "which handler?" `HandlerAdapter` answers "how do I call it?" That is why the same servlet can drive a Thymeleaf page controller and a `@RestController` without becoming a god class. Pluggable strategies keep the core stable while the handler styles evolve.

Boot’s registration matters operationally. You can have more than one dispatcher for different URL prefixes, but the default is one dispatcher for the app. Filters still sit outside this story on the servlet filter chain. Interceptors sit inside the handler execution chain. We will separate those layers in later lessons. Today the point is the center of gravity: almost every Spring MVC request you care about passes through `doDispatch`.

A topic-specific misconception here is treating `DispatcherServlet` as "the thing that does dependency injection" or confusing it with the application context itself. The servlet uses the web application context to find mappings and adapters. It does not create your `OrderService` graph. Another misconception is thinking every annotation on a controller is processed by the servlet directly. Mapping metadata is read at startup into handler mappings; invocation is delegated to an adapter at request time. If you only memorize "Boot auto-configures a dispatcher," you still cannot debug a 404. A 404 usually means no `HandlerMapping` claimed the request. A 415 or binding failure usually means the adapter and converters disagreed with the client. Those failures live on this pipeline.

So today we named the front door, walked the request path through mapping and adaptation into a controller, and saw why strategies keep MVC extensible. We did not yet ask how you author the handler methods themselves — what annotations turn a plain class into something `HandlerMapping` can find, and how a method claims `/orders/42`.

That unresolved question is where controllers begin.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 29 (*DispatcherServlet*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
