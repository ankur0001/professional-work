# Episode 36 — File Upload

| Field | Value |
|---|---|
| Episode | 36 |
| Title | File Upload |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 36 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Binary uploads are not another string field. Multipart requests carry file parts, size limits, and streaming concerns that ordinary `@RequestBody` JSON does not.

Teams hit the pain quickly. A client sends `multipart/form-data` with a file and a few text fields. A naive servlet reads the whole body into memory and collapses under a large PDF. Or the developer expects `@RequestBody byte[]` and wonders why binding fails. Spring MVC integrates multipart resolving so controller methods can declare `MultipartFile` parameters and keep the rest of the MVC model — validation, advice, interceptors — intact.

In Boot, multipart support is on by default for servlet apps. Properties such as `spring.servlet.multipart.max-file-size` and `spring.servlet.multipart.max-request-size` define ceilings. When a request’s content type is multipart, `DispatcherServlet` uses a `MultipartResolver` early in `doDispatch` so the request becomes a multipart-aware wrapper before handler binding.

```java
@RestController
@RequestMapping("/orders")
public class OrderAttachmentController {

    private final AttachmentStorage storage;

    public OrderAttachmentController(AttachmentStorage storage) {
        this.storage = storage;
    }

    @PostMapping(path = "/{id}/attachments", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<AttachmentMeta> upload(
            @PathVariable long id,
            @RequestPart("file") MultipartFile file,
            @RequestPart(value = "note", required = false) String note) throws IOException {

        if (file.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        String storedKey = storage.store(
                id,
                file.getOriginalFilename(),
                file.getContentType(),
                file.getInputStream());

        return ResponseEntity.accepted()
                .body(new AttachmentMeta(storedKey, file.getSize(), note));
    }
}

public record AttachmentMeta(String key, long size, String note) {}
```

Read the method as a contract. The path identifies the order. The part named `file` is the binary. An optional text part `note` rides along. `MultipartFile` gives you the original filename, content type, size, and an `InputStream`. Prefer streaming into storage over `file.getBytes()` when files can be large. Return `202 Accepted` or `201 Created` depending on whether processing is async or the resource is immediately addressable.

Security and hygiene are part of the lesson, not optional footnotes. Never trust `getOriginalFilename()` as a filesystem path — sanitize or discard it and invent your own object key. Validate content types against an allow-list when the product requires it. Virus scanning and async processing often belong behind the API, not inside the controller thread. Empty files and missing parts should become 400s, not 500s.

When limits are exceeded, resolvers throw multipart exceptions that your exception advice can translate into clear 413-style responses. Configure limits deliberately per environment: local demos can be generous; production edges should match CDN or gateway limits so failures happen at a predictable layer.

Multiple files use either repeated parts or `List<MultipartFile>`. Mixed forms combine text fields and files in one request — useful for "upload plus metadata" without a second round trip. For very large objects, consider direct-to-object-storage uploads with pre-signed URLs so the app server never sees the bytes; your Spring endpoint then only records metadata. That architecture is still "file upload" from the product view, even when `MultipartFile` is not on the hot path.

Temporary storage location matters under load. Boot can spill multipart data to disk; ensure the temp directory has space and is cleaned. Streaming to S3 or similar while the request is open reduces local disk pressure but needs careful timeout settings.

A topic-specific misconception is treating uploads as Base64 fields inside JSON "to keep one content type." That inflates payloads and often hides size problems until memory fails. Another is writing temp files to a shared disk without cleanup and calling it a storage strategy. A third is binding `MultipartFile` on a `@RequestBody` method — parts use `@RequestPart` or `@RequestParam`, not JSON body binding.

So today we wired a multipart endpoint with `MultipartFile`, named the resolver step on the dispatcher path, and called out size limits and filename distrust as production essentials.

You can now map controllers, speak REST, validate, handle errors, wrap with filters and interceptors, and accept files. The remaining craft is less "which annotation" and more "which habits keep an API livable for years."

REST best practices close that gap.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 36 (*File Upload*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
