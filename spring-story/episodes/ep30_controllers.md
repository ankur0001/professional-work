# Episode 30 — Controllers

| Field | Value |
|---|---|
| Episode | 30 |
| Title | Controllers |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 30 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`DispatcherServlet` can route, but it needs something to route *to*. Controllers are that something: thin Java types whose methods claim URLs and translate HTTP into domain calls.

Picture the moment after you understand the front controller. You still have to write the handler for `GET /orders/42`. Without a convention, every team invents its own: a giant servlet with a switch on the path, a hand-rolled router map, or XML that points method names at URLs. Spring MVC’s answer is annotation-driven controllers. You mark a class as a web endpoint. You mark methods with HTTP verbs and path patterns. At startup, `RequestMappingHandlerMapping` reads those annotations and builds the lookup table the dispatcher already uses.

Two stereotypes show up constantly. `@Controller` is the classic stereotype for MVC that often returns a view name. `@RestController` is `@Controller` plus `@ResponseBody` on the type: return values are written to the response body, typically as JSON, not resolved as view names. For APIs, `@RestController` is the everyday choice.

```java
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService orders;

    public OrderController(OrderService orders) {
        this.orders = orders;
    }

    @GetMapping("/{id}")
    public OrderResponse get(@PathVariable long id) {
        return orders.findById(id);
    }
}
```

Read that against a real request. Client sends `GET /orders/42`. Mapping matches class path `/orders` plus method path `/{id}` with verb GET. The adapter binds path variable `id` to `42`. Your method runs. The return value is serialized. Status defaults to 200 unless you change it. No XML. No manual registration of the method with the servlet.

Method mapping annotations are shortcuts over `@RequestMapping`. `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, and `@DeleteMapping` fix the HTTP method so the declaration reads like the contract. Path variables use `{name}` in the pattern and `@PathVariable` on the parameter. Query parameters use `@RequestParam`. Headers and cookies have their own annotations when you need them. Prefer constructor injection for the service dependency so the controller stays easy to test with a fake `OrderService`.

Keep controllers thin on purpose. The method should bind input, call one use case, and shape the HTTP result. Business rules belong in services. Persistence belongs in repositories. When a controller grows `if` trees for pricing and inventory, you are no longer writing a translation layer — you are hiding a service inside a web adapter.

Return types are part of the mapping story. A plain object becomes the response body under `@RestController`. `ResponseEntity<T>` lets you set status and headers. `void` with a status annotation can work for no-content responses. For HTML MVC, a `String` view name plus a `Model` parameter is still valid — same dispatcher, different adapter outcome. Component scanning must see the controller: put it under the Boot application’s package tree or declare an explicit `@ComponentScan`. If the class is invisible to the context, the mapping never exists, and the dispatcher correctly answers 404.

Testing stays close to the type. A unit test can new up `OrderController` with a fake service and call `get(42)`. A slice test with `@WebMvcTest` loads MVC infrastructure without the full Boot context and asserts that `GET /orders/42` returns JSON. Both styles reinforce the same idea: the controller is an adapter, not the domain.

A topic-specific misconception is that `@RestController` and `@Controller` are interchangeable "as long as Jackson is on the classpath." They are not. A plain `@Controller` method returning an object without `@ResponseBody` is treated as a view name or model dance, not a JSON body. Another misconception is stuffing every path onto one god controller. Split by resource or bounded context so mappings stay discoverable. A third is treating path variables as trusted domain IDs without checking existence — that is how you leak 500s instead of deliberate 404s, a problem exception handling will own soon.

So today we answered what sits at the end of the dispatcher pipeline: annotated controller methods that claim verbs and paths, with `@RestController` as the API default and a concrete `/orders/42` handler as the mental model.

Knowing how to map a method still leaves a bigger contract question open. How should those methods speak HTTP as an API — status codes, resource shapes, content types — rather than merely returning a Java object?

That is the REST conversation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 30 (*Controllers*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
