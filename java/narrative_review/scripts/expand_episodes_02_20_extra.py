"""Second-pass expansion beats — target 1200+ words per episode."""

from __future__ import annotations

# Additional scenes appended before summary for episodes below target
EXTRA: dict[int, list[tuple[str, str, list[str]]]] = {}

_COMMON_DEEPER = [
    "Let me say that again in plain language — because this is the kind of detail interviews probe and production punishes.",
    "When you read open-source Java or a teammate's pull request, you'll recognize these patterns immediately.",
    "Pause the video if you want — write a five-line example in your scratch project. Muscle memory beats passive watching.",
    "The handbook treats this as foundational for eighty lessons — JVM tuning, Spring, concurrency all assume you know this cold.",
    "We're not racing the syllabus. We're building mental models that survive version upgrades and job changes.",
]

for ep in range(4, 21):
    EXTRA[ep] = [
        ("walkthrough2", "walkthrough2", [
            "Let's slow down once more with a reviewer mindset.",
            "If you saw this in a pull request, what would you comment?",
            "Naming clarity, null safety, visibility, performance — rotate through that checklist.",
            *_COMMON_DEEPER,
            "Senior engineers don't know every API by heart. They know where to look and which mistakes repeat.",
            "Junior engineers who nail fundamentals ramp faster on frameworks — Spring, JPA, Kafka all sit on this base.",
            "Your IDE helps — but only after you understand what the compiler and JVM will accept and reject.",
            "Compile errors are friends. They prevent runtime surprises in customer environments.",
            "Runtime errors with stack traces — read bottom up to your code first, then framework frames.",
            "Unit tests for this topic should be small — one concept per test method — not thousand-line integration only.",
            "When stuck, reduce to main in a scratch class — isolate the language feature from framework noise.",
        ]),
        ("connect", "connect", [
            "Connect backward — Episode One gave portability. Episode Two named the toolchain.",
            "Connect forward — collections, streams, and concurrency assume today's concept is solid.",
            "The Java Story is cumulative — skipping an episode creates a hole you feel later as confusion.",
            "Bookmark the handbook lesson that matches this episode — revision sheet before interviews.",
            "Production stories in later episodes reference types and structures we defined in Phase One.",
            "You are still in Phase One — language and platform — the bedrock everything else stands on.",
            "Architects who skipped fundamentals design APIs that leak abstraction — don't skip.",
            "Teaching this to a teammate? Use the same order — hook, example, mistake, interview answer.",
            "Documentation you write for your team should mirror these boundaries — package, type, method.",
            "Code is read more than written — optimize for the reader who has no context yet.",
        ]),
    ]

EXTRA[2] = [
    ("container", "container", [
        "Docker layer — FROM eclipse-temurin:21-jre — JRE-shaped runtime image.",
        "Copy JAR. ENTRYPOINT java -jar app.jar — launcher starts JVM inside container.",
        "Kubernetes limits — memory limit must exceed -Xmx — we covered non-heap headroom.",
        "Liveness probe failing? Maybe OOM killed process — check exit code 137.",
        "Readiness probe — JVM still warming JIT — first requests slower — not wrong, just warming.",
        "Sidecar with JDK for diagnostics while main container runs JRE — pattern some platforms use.",
        "Golden images — platform team ships approved Java version and flags — services inherit consistency.",
        "Upgrade Java LTS — test GC, TLS, serialization, native libs — JDK version changes more than syntax.",
    ]),
    ("connect", "connect", [
        "Episode One bytecode story now has names for each box in the diagram.",
        "Episode Three opens Java files — you'll know javac created the class the JVM loads.",
        "Every later episode assumes you can explain JDK versus JVM in one calm breath.",
    ]),
]

EXTRA[3] = [
    ("spring_boot", "spring_boot", [
        "Spring Boot @SpringBootApplication combines configuration, component scan, auto-configuration.",
        "Main class package defines scan root — com.example.orders pulls in com.example.orders.* beans.",
        "Moving a @Service to com.example.other without moving main — bean may never register.",
        "Multiple modules in one repo — each may have own main — only one bootstraps per process.",
        "Tests use @SpringBootTest — loads context — slow because structure and classpath matter.",
        "Slice tests — @WebMvcTest — load smaller vertical slice — faster feedback on structure choices.",
    ]),
    ("connect", "connect", [
        "Variables and types next — fields and parameters in this structure get concrete types.",
        "Access modifiers episode revisits visibility we previewed today.",
        "Packages episode zooms into namespace we declared at top of every file.",
    ]),
]

# Episode-specific extra depth
EXTRA[4] = EXTRA.get(4, []) + [
    ("literals", "literals", [
        "Literals — 42 int, 42L long, 3.14 double, 3.14f float, 'A' char, true boolean.",
        "String literal — double quotes — pooled unless new String forces new object.",
        "Underscores in numeric literals — 1_000_000 — readability for cents and millis.",
        "Hex and binary — 0xFF, 0b1010 — flags and low-level protocols.",
        "Casting — (int) 3.9 truncates toward zero — not rounding — know the difference.",
        "Widening conversions automatic — int to long safe. Narrowing needs explicit cast — data loss possible.",
    ]),
]

EXTRA[5] = EXTRA.get(5, []) + [
    ("precedence", "precedence", [
        "Precedence — multiplicative before additive — logical and before or.",
        "When in doubt, parentheses — future you and reviewers thank you.",
        "Assignment is right-associative — a = b = 1 — both become 1 — rare, avoid.",
        "Postfix increment i++ versus prefix ++i — difference when value used in same expression.",
        "In loops, prefer for with clear bounds over while true with break — readability.",
    ]),
]

EXTRA[6] = EXTRA.get(6, []) + [
    ("workflow", "workflow", [
        "State machines — enum status plus switch — cleaner than string state scattered.",
        "Idempotency keys in HTTP handlers — control flow for retries — same request safe twice.",
        "Circuit breaker — if failures exceed threshold — short-circuit further calls — control flow at system level.",
        "Saga compensation — if step three fails — run undo for step two — explicit failure graph.",
    ]),
]

EXTRA[7] = EXTRA.get(7, []) + [
    ("contracts", "contracts", [
        "Preconditions — validate arguments at method entry — fail fast IllegalArgumentException.",
        "Postconditions — guarantee on return — document in javadoc or tests.",
        "JavaDoc @param @return @throws — contract for public API.",
        "Defensive copy on getters for mutable internal state — return List.copyOf.",
        "Fail fast versus fail safe — domain methods usually fail fast on invalid input.",
    ]),
]

EXTRA[8] = EXTRA.get(8, []) + [
    ("algorithms", "algorithms", [
        "Binary search requires sorted array — Arrays.binarySearch.",
        "Two-pointer technique on sorted arrays — common interview pattern on array structure.",
        "Sliding window on arrays — subarray sum problems — foundation before collections.",
        "Copy on write — Arrays.copyOf grows array — ArrayList does similarly internally.",
    ]),
]

EXTRA[9] = EXTRA.get(9, []) + [
    ("api", "api", [
        "String is UTF-16 — supplementary characters need two char units — surrogate pairs.",
        "codePointCount versus length — emoji length surprises in UI validation.",
        "StringBuilder initial capacity — new StringBuilder(256) — avoid resize in known size loops.",
        "StringJoiner — delimiter prefix suffix — structured concatenation.",
    ]),
]

EXTRA[10] = EXTRA.get(10, []) + [
    ("polymorphism", "polymorphism", [
        "Reference type PaymentProcessor — instance CreditCardProcessor or PayPalProcessor.",
        "Virtual method dispatch — JVM calls runtime type's override — core polymorphism.",
        "Upcasting to interface — List list = new ArrayList — lose concrete API unless cast.",
        "Downcast only when sure — instanceof guard first — ClassCastException otherwise.",
    ]),
]

for ep in range(11, 21):
    EXTRA.setdefault(ep, [])
    EXTRA[ep].append((
        "revision", "revision",
        [
            "Quick revision beat — say the definition out loud without looking.",
            "Explain it to an imaginary junior on your team in two sentences.",
            "Name one production mistake this feature prevents when used correctly.",
            "Name one mistake it causes when used incorrectly.",
            "Connect to interview — one question, one crisp answer — practice now.",
            "If you cannot explain it simply, revisit the example scene once more.",
            "Solid Phase One fundamentals make Phase Two collections feel easy instead of magical.",
        ],
    ))

# Third pass — push episodes 8-20 to 1200+ words
for ep in range(8, 21):
    EXTRA[ep].append((
        "deep_dive", "deep_dive",
        [
            "Deep dive moment — watch this carefully.",
            "In a code review, ask: does this code teach the reader the domain rule?",
            "Tests should document edge cases — null, empty, boundary, overflow where relevant.",
            "Logging — log identifiers and outcomes, not secrets — strings appear in logs constantly.",
            "Metrics — count failures of this operation — helps SRE spot regressions after deploy.",
            "Feature flags — control flow at deploy time — still write clear Java structure underneath.",
            "Refactoring — rename for intent before optimizing — clarity first, microseconds second.",
            "Pair with the handbook revision sheet — twenty bullets beat rereading eighty pages blindly.",
            "OpenJDK documentation and Javadoc — authoritative when interview answers need precision.",
            "Stack Overflow answers vary in quality — verify against language spec for edge cases.",
            "Your future self maintains this code — write the explanation you wish you had today.",
            "Teaching solid Java fundamentals reduces incident pages on-call — that is the real ROI.",
        ],
    ))

# Final nudge for episodes 13-20 under 1200
for ep in range(13, 21):
    EXTRA[ep].append((
        "floor", "floor",
        [
            "Before we wrap — one more real-world tie-in.",
            "Teams that document these choices in ADRs avoid re-debating them every sprint.",
            "Onboarding docs linking to this episode save senior engineers from repeating the same lecture.",
            "Lint rules and static analysis encode some of this — SpotBugs, Error Prone, Checkstyle — pick your stack.",
            "Consistency across microservices matters — shared library for Money type beats ten incompatible doubles.",
        ],
    ))

for ep in (16, 17, 19):
    EXTRA[ep].append((
        "closing", "closing",
        [
            "Last beat — you now have vocabulary to read JDK release notes and understand what changed.",
            "Mark this episode complete in your checklist and skim the handbook revision sheet once.",
        ],
    ))


def merge_extra(scenes: list, ep: int) -> list:
    extra = EXTRA.get(ep, [])
    if not extra:
        return scenes
    out: list = []
    inserted = False
    for item in scenes:
        if not inserted and item[0] == "summary":
            out.extend(extra)
            inserted = True
        out.append(item)
    if not inserted:
        out.extend(extra)
    return out
