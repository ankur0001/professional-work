# Episode 17 — Reflection

**Cut:** v1 (original)

## Transcript (from captions)

Annotations are metadata. Reflection is how code reads the structure of types at runtime. Ask a class for its methods. Read fields. Create instances by name. Frameworks do this constantly — Spring, serializers, test tools.

Powerful. Flexible. Easy to misuse. Today we open the hood — carefully. Know the tool. Respect the cost. Episode Seventeen. Reflection — inspect and invoke types at runtime. Start with Class.

Order.class or order.getClass — you get a Class object. From there — getMethods, getFields, getConstructors. You can discover what a type offers without hardcoding every name. That discovery is the heart of reflective programming.

Dynamic systems are built on this doorway. Reflection can call methods too. Lookup a Method. Invoke it with arguments. You can even reach private members — with setAccessible. That breaks encapsulation walls — use it only with clear cause.

Libraries may need it. Business code usually should not. If you reach for private access daily — redesign the API. Why frameworks love reflection. Dependency injection scans annotations and constructs beans.

JSON mappers bind properties without hand-written glue for every class. ORMs inspect entities and map tables. You get productivity — the platform pays with complexity. Understanding reflection makes those magic layers less magical.

Reflection is not free. Lookups are slower than direct calls. Security managers and modules can restrict access. Native images and Graal may need extra config for reflective use. Cache Method handles if you must reflect in a hot path.

Prefer normal calls when the type is known at compile time. Safety rules of thumb. Validate names and inputs — reflective calls can become injection surfaces. Do not suppress access checks casually in application code.

Log clearly when reflective fallbacks run — they hide bugs. If a feature needs reflection, quarantine it behind a small module. Power without boundaries becomes an incident. Three common mistakes.

One — using reflection where an interface would do. Two — calling setAccessible everywhere and calling it fine. Three — ignoring performance until the profiler screams. Also — assuming field names are a stable public API.

Reflect on purpose — not as a default style. Interview question — what is reflection in Java? Runtime inspection and interaction with classes, methods, and fields. Used heavily by frameworks for wiring and mapping.

Tradeoffs — flexibility versus speed, safety, and clarity. Mention modules and native-image constraints for senior signal. That answer balances power and caution. We can inspect types. Next — a cleaner way to carry data.

Episode Eighteen — records. Transparent data carriers with less boilerplate. See you there.
