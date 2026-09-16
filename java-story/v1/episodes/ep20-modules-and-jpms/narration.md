# Episode 20 — Modules and JPMS

**Cut:** v1 (original)

## Transcript (from captions)

Sealed types close hierarchies. Modules close the classpath. For years, every public type was fair game if the JAR was on the path. JPMS — the Java Platform Module System — adds explicit boundaries.

What you require. What you export. What stays internal. Today — module-info, strong encapsulation, and when modules earn their keep. Packages organize names. Modules organize trust.

Episode Twenty. Modules and JPMS — strong encapsulation. Why modules exist. The classpath is flat — order and accidents decide visibility. Split packages, accidental API leakage, brittle shading wars.

Modules declare dependencies and exported packages up front. The JVM can refuse illegal access instead of hoping conventions hold. Reliability beats classpath folklore. module-info.java is the contract.

module com.shop.payments. requires java.sql. requires com.shop.common. exports com.shop.payments.api. Internal packages stay hidden even if types are public. Public no longer means globally reachable.

Know the key directives. requires — and requires transitive when consumers need your dependency too. exports — and exports to specific modules when the API is narrow. opens — for reflection frameworks that need deep access at runtime.

provides and uses — for service loading with clear providers. Each keyword is a deliberate encapsulation choice. Reality check — the unnamed module. Classic classpath JARs still run. They become the unnamed module.

They can read everything, but modular code cannot require them by name. Migration is often incremental — modularize libraries you own first. Automatic modules bridge JARs with a derived module name.

Plan the boundary. Do not flip a monolith overnight. When modules help. Platform libraries. Large multi-JAR systems. Clear API versus internal split. When you need reliable encapsulation and smaller runtime images with jlink.

When not — tiny apps where classpath simplicity wins and tooling friction hurts. Spring Boot apps often stay on the classpath path unless you have a reason. Use JPMS when boundaries are a product feature — not a fashion statement.

Three common mistakes. One — exporting everything — encapsulation theater with no teeth. Two — opens for convenience forever instead of narrowing reflective needs. Three — split packages across modules — the JVM will not forgive that.

Also — ignoring transitive requires until consumers break at compile time. Module graphs should be boring and intentional. Interview question — what does JPMS add over packages and JARs?

Explicit module dependencies and exported packages. Strong encapsulation — public is not enough to be accessible. Mention module-info, requires, exports, and the unnamed module. Bonus — jlink for custom runtimes.

That answer separates classpath history from modular design. Language features are in place. Next — the collections you use every day. Episode Twenty-One — Lists, and the java.util foundation.

Interfaces, implementations, and choosing the right structure. See you there.
