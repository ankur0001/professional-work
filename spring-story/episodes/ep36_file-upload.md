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

A shipping clerk attaches a bill of lading — a PDF — to a cargo booking. The browser does not send JSON. It sends `multipart/form-data`: fields plus a binary part. If your controller still expects `@RequestBody`, the adapter will not bind what you think.

Spring MVC treats multipart as a first-class request shape on the dispatcher path. Before handler invocation, `DispatcherServlet` can resolve a multipart request into a wrapped request the adapter understands. Boot auto-configures a `MultipartResolver` when servlet multipart support is enabled. You bind parts with `MultipartFile` (or `Part`) alongside ordinary form fields.

```java
@RestController
@RequestMapping("/cargo/bookings")
public class BillOfLadingController {

    private final BillOfLadingStore store;

    public BillOfLadingController(BillOfLadingStore store) {
        this.store = store;
    }

    @PostMapping(path = "/{bookingId}/bill-of-lading", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<BolUploadResponse> upload(
            @PathVariable String bookingId,
            @RequestPart("document") MultipartFile document,
            @RequestPart(value = "notes", required = false) String notes) throws IOException {

        if (document.isEmpty()) {
            throw new IllegalArgumentException("bill of lading PDF is required");
        }
        String original = document.getOriginalFilename();
        if (original == null || !original.toLowerCase(Locale.ROOT).endsWith(".pdf")) {
            throw new IllegalArgumentException("only PDF bills of lading are accepted");
        }

        BolUploadResponse saved = store.save(bookingId, document.getBytes(), original, notes);
        return ResponseEntity.accepted().body(saved);
    }
}
```

`@RequestPart` names the multipart field. `MultipartFile` gives you bytes, size, content type, and the client-supplied filename. Treat that filename as hostile metadata — never concatenate it straight into a filesystem path. Prefer generated storage keys and store the original name as data.

Size limits are production essentials, not afterthoughts:

```yaml
spring:
  servlet:
    multipart:
      max-file-size: 5MB
      max-request-size: 6MB
```

When a clerk uploads a 40MB scan, the container should reject early with a clear error rather than buffering until the heap suffers. Align gateway limits, Boot multipart limits, and reverse-proxy body sizes so the failure mode is intentional.

Streaming large files through `getBytes()` is fine for small PDFs and wrong for multi-hundred-megabyte transfers — use `getInputStream()` and stream to object storage. Virus scanning and content-type sniffing belong in the store or a dedicated pipeline; trusting `Content-Type` from the client alone is not enough.

On the dispatcher path, multipart resolution happens before the adapter invokes your method — remember the early step in `doDispatch`. If resolution fails because the body is not multipart or exceeds limits, your controller never runs; advice and error handling still should return a JSON problem, not an HTML container page.

People bind multipart with `@RequestBody` and blame Jackson. Others disable size limits "temporarily" for a demo and leave them off. A third trap is writing uploads into a directory inside the fat JAR’s working tree without cleanup — disks fill, pods restart, bookings look fine until storage fails.

Uploads now fit the MVC model. The broader craft around the stack you already have — resource-oriented URLs, disciplined statuses, paginated collections, DTO boundaries, and idempotent creates for parcels — is REST best practice, not another annotation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 36 (*File Upload*).
