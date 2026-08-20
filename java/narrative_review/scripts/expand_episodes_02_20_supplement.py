"""Supplemental beats to reach 1200-1800 words per episode."""

from __future__ import annotations

# Extra beats inserted before 'mistakes' scene in each episode
SUPPLEMENT: dict[int, list[tuple[str, str, list[str]]]] = {
    3: [
        ("imports", "imports", [
            "One more structural piece — imports.",
            "import java.util.List brings a type into scope without fully qualifying every use.",
            "Static imports exist for constants and static methods — use sparingly.",
            "Star imports — import java.util.* — save typing but hide origin in reviews.",
            "Most teams prefer explicit imports — IDE manages them anyway.",
            "Imports are compile-time convenience. Runtime identity is always fully qualified.",
        ]),
    ],
    4: [
        ("deeper", "deeper", [
            "Go deeper on var — local variable type inference since Java 10.",
            "var list = new ArrayList<String>() — compiler infers ArrayList on the right.",
            "var is not var in JavaScript — still statically typed.",
            "Do not use var when the type is unclear from the right-hand side.",
            "var customer = getCustomer() hiding a complex return type hurts readers.",
            "Inference is for locals only — not fields, not parameters, not return types.",
            "Eight primitives quick reference: byte, short, int, long, float, double, char, boolean.",
            "Each has a wrapper except void. char is sixteen-bit UTF-16 code unit — not a full Unicode code point alone.",
            "Reference types include classes, interfaces, arrays, enums, records.",
            "String is a reference type — immutable object, not a primitive.",
            "Choosing long for timestamps in epoch millis avoids Year 2038 int worries on older systems.",
            "Instant from java.time — Episode Thirty-One — is the modern timestamp type for new code.",
        ]),
    ],
    5: [
        ("deeper", "deeper", [
            "Bitwise operators — and, or, xor, shift — still appear in permissions and low-level flags.",
            "Use EnumSet over raw bitmasks when enums define the flags — Episode Thirteen.",
            "instanceof pattern matching — if (obj instanceof String s) — binds s in true branch.",
            "Reduces cast clutter. Modern Java making type checks expressive.",
            "Assignment operators — plus equals, minus equals — read-modify-write in one expression.",
            "Side effects in the right-hand side of assignment still run — order matters.",
            "String concatenation with plus — fine for few pieces, not for loops.",
            "CompareTo for ordering, equals for equality — different contracts on Comparable types.",
            "Never use compareTo for equality checks — inconsistent with equals on some types.",
        ]),
    ],
    6: [
        ("deeper", "deeper", [
            "do-while runs body at least once — rare but useful for retry prompts.",
            "Labeled break and continue exist — avoid unless clarifying nested loops.",
            "Pattern matching in switch — switch (obj) { case String s -> ... } — Java 21+ style.",
            "Combines type check and binding — pairs with sealed types later.",
            "Yield in switch blocks when arrow form needs multiple statements.",
            "InterruptedException in loops — restore interrupt flag or exit cleanly.",
            "Ignoring Thread.interrupted() causes shutdown hooks and pool stops to hang.",
            "Finally runs even when return in try — mind return values overwritten by finally return.",
            "Try-with-resources can suppress secondary exceptions from close — suppressed array on primary.",
        ]),
    ],
    7: [
        ("deeper", "deeper", [
            "Parameters are pass-by-value — always.",
            "For references, the reference value is copied — both point at same object.",
            "Reassigning parameter to new object does not affect caller's variable.",
            "Mutating object through reference is visible to caller — know the difference.",
            "Varargs — public void log(String level, String... messages) — treat as array inside.",
            "Overloading resolution picks most specific match — ambiguity compile error.",
            "Bridge methods and generics — rare interview topic — compiler synthesizes bridges for erasure.",
            "Recursion has stack depth limits — deep recursion risks StackOverflowError.",
            "Tail recursion is not optimized by standard HotSpot — use loops for deep iteration.",
            "Method references — System.out::println — shorthand for lambdas, Episode Twenty-Six area.",
        ]),
    ],
    8: [
        ("deeper", "deeper", [
            "Array initialization shorthand — int[] nums = {1, 2, 3};",
            "Anonymous array for method args — method(new int[]{1,2}) — fine for tests, noisy in production.",
            "Arrays.clone() shallow copy — new array, same element references for objects.",
            "System.arraycopy fast block copy between arrays.",
            "Arrays.equals and Arrays.deepEquals for content comparison — not == on array references.",
            "Sort with Arrays.sort — primitive sorts highly optimized.",
            "Parallel sort for large primitive arrays when order matters.",
            "Covariance trap — Number[] nums = new Integer[10]; nums[0] = 1.0 — ArrayStoreException at runtime.",
            "Generic List avoids that particular footgun.",
        ]),
    ],
    9: [
        ("deeper", "deeper", [
            "String pool — literal strings interned in heap string pool.",
            "new String(\"hello\") creates separate object — usually avoid unnecessary new.",
            "text blocks — triple quotes — multi-line JSON and SQL templates cleanly since Java 15.",
            "formatted and formatted methods — String templates evolving — know your JDK version.",
            "Regular expressions — String.matches, Pattern.compile — powerful, easy to DoS with catastrophic backtracking.",
            "Validate regex complexity on user-supplied patterns.",
            "StringTokenizer legacy — prefer split with limit or Scanner for structured parsing.",
            "Security — never construct SQL with plus on user input — parameterized queries always.",
            "Logging user-controlled strings can be log injection — sanitize or escape.",
        ]),
    ],
    10: [
        ("deeper", "deeper", [
            "this reference — current object inside instance methods.",
            "super — call superclass constructor or method — must be first in constructor if used.",
            "Constructor chaining — this(...) or super(...) — one must be first statement.",
            "Default constructor inserted if none written — only if no other constructors.",
            "Initialization order — static fields, static blocks, instance fields, instance blocks, constructor.",
            "Wrong order assumptions cause subtle null bugs with overridden methods in constructors.",
            "Interfaces define contracts — multiple interfaces on one class — no multiple inheritance of state.",
            "Abstract classes — mix abstract and concrete methods — share code with partial implementation.",
            "final class cannot be extended — String is final — security and immutability.",
            "final methods cannot be overridden — rare in application code.",
            "Object methods — equals, hashCode, toString — override together with consistent contract.",
        ]),
    ],
    11: [
        ("deeper", "deeper", [
            "Top-level classes — only public or package-private.",
            "Nested classes — static nested, inner, local, anonymous — different visibility and this binding.",
            "Inner class holds implicit reference to outer — memory leak risk if outer outlives needed scope.",
            "Static nested class — no outer reference — prefer when nesting is organizational.",
            "Module system adds another layer — exports and opens — Episode Twenty.",
            "public on interface methods is implicit — redundant but readable.",
            "Sealed types restrict who extends — Episode Nineteen — interacts with protected visibility.",
            "Library design — minimize public, document package-private collaborators in module docs.",
            "JPMS exports package — access modifiers still apply inside module.",
        ]),
    ],
    12: [
        ("deeper", "deeper", [
            "Default package — no package declaration — quick demos only, not production.",
            "Package naming convention — reversed domain — com.company.product.layer.",
            "Never use java or javax as your prefix — reserved and confusing.",
            "Split packages — same package name in two JARs — illegal in modules, fragile on classpath.",
            "JPMS forbids split packages — migration pain point.",
            "package-info.java — package level documentation and annotations.",
            "ArchUnit and similar tools test package dependency rules in CI.",
            "Feature folders versus layers — both valid — align with team ownership.",
            "Monorepo multi-module Maven/Gradle — each module maps to deployable or library boundary.",
        ]),
    ],
    13: [
        ("deeper", "deeper", [
            "Enum implements Comparable — natural order is declaration order.",
            "values() and valueOf — parse from string name — IllegalArgumentException if unknown.",
            "Custom constructor on enum must be private — compiler enforces.",
            "Enum singleton pattern — effective single instance — Joshua Bloch recommended.",
            "Switch on enum — compiler knows all constants — add constant, fix switches.",
            "Serialization — readResolve can protect singleton enums — built-in protection.",
            "GraphQL and OpenAPI enums — name strings must match API contract — document mapping.",
        ]),
    ],
    14: [
        ("deeper", "deeper", [
            "ValueOf and parse methods on wrappers — prefer over constructors — caching.",
            "Boolean.TRUE and FALSE instances — use instead of new Boolean.",
            "OptionalInt, OptionalLong, OptionalDouble — avoid boxing in streams — performance.",
            "Primitive streams — IntStream, LongStream — specialized operations without boxing.",
            "Null in Map of Integer — HashMap allows null key once — know your map implementation.",
            "Concurrent collections — never null keys or values on ConcurrentHashMap.",
            "Performance test — boxing one million integers — measurable GC — profile before optimizing.",
        ]),
    ],
    15: [
        ("deeper", "deeper", [
            "Diamond operator — List<String> list = new ArrayList<>(); — infer type args.",
            "Generic methods — Collections.sort(list) — type inferred from argument.",
            "Heap pollution — mixing raw and generic — unchecked warnings are warnings for a reason.",
            "Generic arrays illegal — new List<String>[10] won't compile — erasure again.",
            "List<?> unmodifiable wildcard list — read-only unknown element type.",
            "Capture conversion — compiler magic — rarely hand-write, sometimes see in errors.",
            "Class<T> tokens — Gson, Jackson type references — pattern for runtime generic types.",
            "Reifiable types — can use in instanceof — int not reifiable, String is.",
        ]),
    ],
    16: [
        ("deeper", "deeper", [
            "ElementType — TYPE, METHOD, FIELD, PARAMETER, CONSTRUCTOR, PACKAGE, etc.",
            "Documented annotation — generates javadoc snippet.",
            "Inherited meta-annotation — subclasses inherit annotation if marked @Inherited.",
            "Repeatable annotations — container annotation generated — Java 8+.",
            "Annotation processing at compile time — generate code, fail build on violations.",
            "Lombok, MapStruct, Immutables — compile-time processors — not runtime magic.",
            "Spring's @Configuration and @Bean — runtime plus classpath scanning — startup cost.",
            "Micrometer @Timed — AOP around methods — ties to observability Episode Seventy-Nine.",
        ]),
    ],
    17: [
        ("deeper", "deeper", [
            "getDeclaredMethods versus getMethods — declared includes private, getMethods includes inherited public.",
            "Constructor.newInstance — replaces deprecated Class.newInstance.",
            "Field.get and set — break encapsulation — test utilities sometimes need it.",
            "Proxy.newProxyInstance — dynamic interfaces — JDK proxies limited to interfaces.",
            "MethodHandles — Java 7+ — faster reflective invoke when cached.",
            "VarHandles — atomic access — low-level concurrent field updates.",
            "Stack walking — StackWalker API — who called me without full stack trace cost.",
            "SecurityManager deprecated — modules and strong encapsulation replace some use cases.",
        ]),
    ],
    18: [
        ("deeper", "deeper", [
            "Record implements implicit final — cannot extend other classes — can implement interfaces.",
            "Nested records — allowed — keep small.",
            "Local records — inside methods — Java 16+ — scoped data carriers.",
            "Serialization — records serialize components — define readObject if migration needed.",
            "Jackson and records — constructor properties — configure naming strategy.",
            "JPA — records as DTOs yes, as entities generally no — mutability and proxies.",
            "Defensive copy — List.copyOf in compact constructor for mutable list components.",
            "Compact constructor assigns to this implicitly after validation — no redundancy needed.",
        ]),
    ],
    19: [
        ("deeper", "deeper", [
            "Permitted subclasses in same module — or same package if module unnamed.",
            "Sealed class extends another sealed class — permits chain carefully.",
            "Pattern switch — case Ok(var id) — destructure record components.",
            "Domain modeling — Result, Either, Option variants — algebraic style in Java.",
            "Open sealed hierarchy for library — non-sealed leaf for user extension point.",
            "Compiler error on missing case — better than default that hides new subtype.",
            "IDE quick fixes add cases when sealed family grows — workflow win.",
        ]),
    ],
    20: [
        ("deeper", "deeper", [
            "java.base module — every module implicitly requires it.",
            "Module path versus classpath — module-path for modular JARs.",
            "jlink — build custom runtime — strip unused modules — smaller containers.",
            "Spring Boot 3 — Jakarta namespace — module path still optional for most apps.",
            "IllegalAccessError — calling internal JDK API — modules block strong encapsulation.",
            "--add-opens and --add-exports — migration escape hatches — use temporarily.",
            "ServiceLoader with module provides — explicit provider loading.",
            "Layered configurations — multiple module layers in advanced containers.",
        ]),
    ],
}

# Extra beats for ep02 and ep03
SUPPLEMENT[2] = [
    ("deeper", "deeper", [
        "Spring Boot executable JAR — nested loader — still ends at JVM executing bytecode.",
        "CI pipeline — compile stage needs JDK. Run stage may use slimmer runtime if diagnostics elsewhere.",
        "Eclipse Temurin, Amazon Corretto, Azul Zulu — distributions share specification, differ in support and patches.",
        "LTS versions — eleven, seventeen, twenty-one — enterprises standardize on LTS for support windows.",
        "javac release flag — compile to older bytecode version while using newer JDK — backward compatibility.",
        "Toolchain in Gradle and Maven — enforce JDK version across team — no more works on my machine Java version drift.",
        "Flight Recorder — jcmd JFR.start — low overhead profiling in production when JDK present.",
        "Native memory tracking — NMT — diagnose direct buffer leaks beyond heap dumps.",
    ]),
]

SUPPLEMENT[3] = SUPPLEMENT.get(3, []) + [
    ("blocks", "blocks", [
        "Static initializer block — static { ... } — runs once when class loaded.",
        "Instance initializer block — { ... } — runs before constructor body every new.",
        "Use static blocks sparingly — hard to test, hide I/O — prefer static factory methods.",
        "Single-class demos skip package — production code always declares package.",
        "Multiple top-level classes in one file — only one public, rest package-private — rare style.",
        "Text blocks for multi-line strings in main — JSON fixtures in tutorials — Java 15+.",
    ]),
]

# Broad expansion for episodes 05-20 — add production_context scene
for ep in range(5, 21):
    SUPPLEMENT.setdefault(ep, []).append((
        "production", "production",
        [
            "Production context — why this topic stops incidents.",
            "Code review checklist item — catch misuse before merge.",
            "Observability — logs and metrics should name concepts clearly — not mystery abbreviations.",
            "Tests should encode the contracts we discussed — one failing test beats ten slides.",
            "Refactor toward clarity — juniors read this code six months from now.",
            "Interview answers map directly to daily choices — not trivia for trivia's sake.",
            "Connect to handbook lesson themes — JVM, structure, types, concurrency later in series.",
            "Next episodes build on this — skipping fundamentals creates gaps that show in system design.",
        ],
    ))


def merge_supplement(scenes: list, ep: int) -> list:
    """Insert supplement scenes before mistakes if present."""
    extra = SUPPLEMENT.get(ep, [])
    if not extra:
        return scenes
    out: list = []
    inserted = False
    for item in scenes:
        if not inserted and item[0] == "mistakes":
            out.extend(extra)
            inserted = True
        out.append(item)
    if not inserted:
        out.extend(extra)
    return out
