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

`DispatcherServlet` can route only if something exists to route *to*. Controllers are that something: thin Java types whose methods claim URLs and translate HTTP into harbor-domain calls.

Without a convention, every team invents its own router for luggage: a giant servlet with a switch on the path, a hand-rolled map of strings to method handles, or XML that points method names at URLs. Spring MVC’s answer is annotation-driven controllers. You mark a class as a web endpoint. You mark methods with HTTP verbs and path patterns. At startup, `RequestMappingHandlerMapping` reads those annotations and builds the lookup table the dispatcher already uses.

Two stereotypes show up constantly. `@Controller` is the classic stereotype for MVC that often returns a view name. `@RestController` is `@Controller` plus `@ResponseBody` on the type: return values are written to the response body, typically as JSON, not resolved as view names. For a luggage API, `@RestController` is the everyday choice.

```java
@RestController
@RequestMapping("/luggage")
public class LuggageController {

    private final LuggageLookup luggage;

    public LuggageController(LuggageLookup luggage) {
        this.luggage = luggage;
    }

    @GetMapping("/{tag}")
    public LuggageStatusResponse get(@PathVariable String tag) {
        return luggage.statusFor(tag);
    }
}
```

Read that against a live request. Client sends `GET /luggage/TAG-8841`. Mapping matches class path `/luggage` plus method path `/{tag}` with verb GET. The adapter binds path variable `tag` to `TAG-8841`. Your method runs. The return value is serialized. Status defaults to 200 unless you change it. No XML. No manual registration of the method with the servlet.

Method mapping annotations are shortcuts over `@RequestMapping`. `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, and `@DeleteMapping` fix the HTTP method so the declaration reads like the contract. Path variables use `{name}` in the pattern and `@PathVariable` on the parameter. Query parameters use `@RequestParam`. Headers and cookies have their own annotations when you need them. Prefer constructor injection for the lookup collaborator so the controller stays easy to test with a fake `LuggageLookup`.

Keep controllers thin on purpose. The method should bind input, call one use case, and shape the HTTP result. Tag status rules belong in the domain service. Persistence belongs in repositories. When a luggage controller grows `if` trees for customs holds and berth assignments, you are no longer writing a translation layer — you are hiding a service inside a web adapter.

Return types are part of the mapping story. A plain object becomes the response body under `@RestController`. `ResponseEntity<T>` lets you set status and headers — useful when a missing tag should be 404 rather than an empty 200. `void` with a status annotation can work for no-content responses. For HTML MVC, a `String` view name plus a `Model` parameter is still valid — same dispatcher, different adapter outcome. Component scanning must see the controller: put it under the Boot application’s package tree or declare an explicit `@ComponentScan`. If the class is invisible to the context, the mapping never exists, and the dispatcher correctly answers 404.

Testing stays close to the type. A unit test can new up `LuggageController` with a fake lookup and call `get("TAG-8841")`. A slice test with `@WebMvcTest` loads MVC infrastructure without the full Boot context and asserts that `GET /luggage/TAG-8841` returns JSON. Both styles reinforce the same idea: the controller is an adapter, not the harbor domain.

`@RestController` and `@Controller` are not interchangeable "as long as Jackson is on the classpath." A plain `@Controller` method returning an object without `@ResponseBody` is treated as a view name or model dance, not a JSON body. Stuffing every harbor path onto one god controller also hurts: split by resource — luggage, berths, manifests — so mappings stay discoverable. And treating path variables as trusted domain ids without checking existence is how you leak 500s instead of deliberate 404s.

You now know what sits at the end of the dispatcher pipeline: annotated methods that claim verbs and paths, with `/luggage/{tag}` as the mental model. Mapping a method still leaves a bigger contract open — how those methods should speak HTTP as an API: status codes, resource shapes, and content types, rather than merely returning a Java object.

That contract is REST design.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 30 (*Controllers*).
