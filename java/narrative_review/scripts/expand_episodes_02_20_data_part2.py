"""Episode 04-20 expansion data (part 2)."""

from __future__ import annotations

from expand_episodes_02_20_data import (
    JAVA_ANNOTATIONS,
    JAVA_ARRAYS,
    JAVA_ENUMS,
    JAVA_FLOW,
    JAVA_GENERICS,
    JAVA_HELLO,
    JAVA_METHODS,
    JAVA_MODULES,
    JAVA_OOP,
    JAVA_OPS,
    JAVA_PACKAGES,
    JAVA_RECORDS,
    JAVA_REFLECTION,
    JAVA_SEALED,
    JAVA_STRINGS,
    JAVA_TYPES,
    JAVA_WRAPPERS,
    JAVA_ACCESS,
)

EPISODE_DATA_PART2: dict[int, dict] = {}

EPISODE_DATA_PART2[4] = {
    "slug": "variables-and-data-types",
    "title": "Variables and Data Types",
    "scenes": [
        ("hook", "hook", [
            "Episode Three mapped packages and classes.",
            "Now — what actually lives inside those fields, parameters, and locals?",
            "Variables name values. Types decide what is valid and how operations behave.",
            "Pick the wrong type and production pays — overflow, null crashes, rounding bugs on money.",
            "Java's type system is strict on purpose. Today we learn to use it as a design tool.",
        ]),
        ("title", "title", [
            "Episode Four.",
            "Variables and Data Types — primitives, references, and real production choices.",
        ]),
        ("families", "families", [
            "Two families — keep this picture in your head forever.",
            "Primitives — raw values stored inline. Eight of them. Never null.",
            "References — variables that point to objects on the heap. Can be null.",
            "Assignment copies primitive values. Assignment copies reference values — not the whole object.",
            "That difference drives memory layout, equality, collections, and API contracts.",
            "Confusing the families causes half the NullPointerExceptions in brownfield code.",
        ]),
        ("primitives", "primitives", [
            "Eight primitives — learn the common four first.",
            "int for everyday integers. long for IDs, timestamps, money in minor units.",
            "boolean for flags. double for scientific floats — not for currency.",
            "byte, short, char, float exist for specialized cases — binary protocols, graphics, legacy APIs.",
            "Primitives are fast and compact — no object header, no indirection.",
            "They cannot hold null — which eliminates a whole failure class for counters and flags.",
        ]),
        ("memory", "memory", [
            "Picture memory while you declare variables.",
            "int count = 10 — the ten lives in the stack frame as a value.",
            "Order order = new Order(...) — order holds a reference; the Order object lives on the heap.",
            "final prevents reassigning the variable — not mutating the object it points at.",
            "final Order o = ... then o.setStatus(...) may still be legal if the type allows mutation.",
            "Deep immutability requires immutable types — records help, coming in Episode Eighteen.",
        ]),
        ("example", "example", [
            "Walk types you'd see in a payment service.",
            ("code", JAVA_TYPES),
            "long amountInCents — store money as integer minor units when rounding rules are simple.",
            "boolean active — compact flag, no null unless you choose Boolean wrapper.",
            "String customerId — reference type, immutable text, lives on heap.",
            "var retryCount = 3 — local type inference. Still statically typed as int — not dynamic typing.",
            "record Money — domain type with validation in compact constructor. Currency must be three letters.",
            "Types are contracts — especially across APIs, databases, and event payloads.",
        ]),
        ("money", "money", [
            "Production gotcha — money.",
            "Never store currency in double for ledger logic.",
            "Binary floating point cannot represent many decimal fractions exactly — 0.1 plus 0.2 drama.",
            "Prefer long minor units — cents, paise — or a Money value object.",
            "Use BigDecimal when you need explicit decimal scale and rounding modes.",
            "Architects standardize this early — fixing money types across services is expensive surgery.",
            "Interviewers ask this because teams still ship rounding bugs.",
        ]),
        ("wrappers", "wrappers", [
            "Wrappers — Integer, Long, Boolean — box primitives into objects.",
            "Nullable. Heap allocated. Autoboxing hides conversions.",
            "List<Integer> needs objects — autobox on add, unbox on read.",
            "A hot loop boxing every int allocates constantly — GC pressure.",
            "Prefer primitives in numeric hot paths. Use wrappers when null carries meaning.",
            "Episode Fourteen goes deeper on autoboxing traps — today know the cost exists.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes burned into memory.",
            "One — double for money.",
            "Two — ignoring integer overflow on counters and limits — silent wrap on int.",
            "Three — assuming final means deep immutability.",
            "Bonus — overusing String for every domain concept — CustomerId as a type beats naked strings.",
        ]),
        ("interview", "interview", [
            "Interview question — primitive versus wrapper?",
            "Primitive — value, non-null, compact, fast arithmetic.",
            "Wrapper — object, nullable, overhead, autoboxing and unboxing risk.",
            "Why avoid double for money — binary precision and rounding.",
            "What does final mean — no reassignment, not deep immutability.",
            "Calm, specific answers beat memorized lists.",
        ]),
        ("summary", "summary", [
            "Land the plane.",
            "Two type families — primitives and references.",
            "Choose types for correctness, memory, and API stability.",
            "Money belongs in long minor units, BigDecimal, or value objects — not double.",
            "final guards variables, not necessarily object contents.",
            "Types are contracts — treat them that way across service boundaries.",
        ]),
        ("teaser", "teaser", [
            "Values have types. Next — operators act on them.",
            "Episode Five — Operators.",
            "Equality, short-circuit logic, overflow — small symbols, large consequences.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[5] = {
    "slug": "operators",
    "title": "Operators",
    "scenes": [
        ("hook", "hook", [
            "Episode Four chose types carefully.",
            "Now those values meet operators — plus, minus, equals, and, or.",
            "Small symbols. Enormous consequences.",
            "Overflow, equality bugs, and null crashes often start here.",
            "Operators look like math class. In production they are correctness and security.",
        ]),
        ("title", "title", [
            "Episode Five.",
            "Operators — arithmetic, equality, and short-circuit logic.",
        ]),
        ("families", "families", [
            "Three families you touch daily.",
            "Arithmetic — plus, minus, multiply, divide, remainder.",
            "Relational — less than, greater than, equals-equals.",
            "Logical — double ampersand and, double pipe or, exclamation not.",
            "Java evaluates left to right. Parentheses remove precedence guesswork.",
            "Compound assignment — plus equals — reads, computes, writes back.",
        ]),
        ("equality", "equality", [
            "The classic trap — equality.",
            "For primitives, equals-equals compares values.",
            "For objects, equals-equals compares references — same object in memory?",
            "For String content — use equals. Never equals-equals for text you care about.",
            "Safer pattern — literal first: PAID.equals(status) avoids null pointer if status is null.",
            "Objects.equals(a, b) handles nulls on both sides — use it in utility code.",
        ]),
        ("shortcircuit", "shortcircuit", [
            "Short-circuit logic protects you.",
            "Double ampersand — if left is false, right never runs.",
            "Double pipe — if left is true, right never runs.",
            "user != null && user.isActive() — second call only when user exists.",
            "Single ampersand does not short-circuit — both sides always evaluate.",
            "Use short-circuit when the second check is expensive or unsafe on null.",
        ]),
        ("example", "example", [
            "Walk guard logic you would ship.",
            ("code", JAVA_OPS),
            "canShip checks null first — short-circuit prevents calling equals on null status.",
            "PAID.equals(orderStatus) — literal-first idiom for String equality.",
            "customerId.equals(requestId) — only reached when both sides passed null guards.",
            "Math.addExact — overflow throws ArithmeticException instead of silent int wrap.",
            "Payment limits and ledger deltas need exact arithmetic discipline.",
        ]),
        ("overflow", "overflow", [
            "Arithmetic looks innocent until counters hit two billion.",
            "int overflow wraps silently — no exception by default.",
            "Math.addExact, multiplyExact — fail loud when range exceeded.",
            "Or promote to long and still think about upper bounds.",
            "Ternary operator — condition question trueValue colon falseValue — great for simple choices.",
            "Nested ternaries become unreadable — extract a method instead.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "One — equals-equals for String content.",
            "Two — ignoring integer overflow until production numbers get big.",
            "Three — side effects inside clever expressions — hard to debug.",
            "Also — trusting precedence instead of parentheses. Be kind to the next reader.",
        ]),
        ("interview", "interview", [
            "Interview — equals-equals versus equals?",
            "Equals-equals — references for objects, values for primitives.",
            "Equals — logical equality defined by the type.",
            "Short-circuit and protects null and skips expensive checks.",
            "Detect overflow with Math.addExact or domain validation.",
            "That package sounds like daily Java, not trivia.",
        ]),
        ("summary", "summary", [
            "Operators decide and combine values.",
            "Use equals for object content. Use short-circuit for safety.",
            "Watch overflow on int. Use exact math for money paths.",
            "Keep expressions readable — methods beat nested ternaries.",
            "Small syntax — large production impact.",
        ]),
        ("teaser", "teaser", [
            "Operators decide values. Next — control the path.",
            "Episode Six — Control Flow.",
            "if, switch, loops, and clean exits.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[6] = {
    "slug": "control-flow",
    "title": "Control Flow",
    "scenes": [
        ("hook", "hook", [
            "Operators decide values. Control flow decides which statements run.",
            "Which path executes? How often? When do we exit?",
            "In production, unclear branching becomes missed edge cases and messy failures.",
            "Distributed systems amplify bad flow — duplicate processing, retry storms, swallowed errors.",
            "Today we make paths visible — flat, explicit, testable.",
        ]),
        ("title", "title", [
            "Episode Six.",
            "Control Flow — if, switch, loops, and clean exits.",
        ]),
        ("guards", "guards", [
            "Start with if — but prefer guard clauses.",
            "Validate early. Reject early. Return early.",
            "Flat code beats a pyramid of nested else blocks.",
            "if not valid — return bad request. if not authorized — return forbidden.",
            "Then process the happy path at low indentation.",
            "Readable. Testable. Kind to the next engineer at three a.m.",
        ]),
        ("switch", "switch", [
            "When cases are finite — switch shines.",
            "Modern switch expressions produce a value — arrow labels, no fall-through.",
            "Perfect for statuses — PENDING, PAID, CANCELLED, SHIPPED.",
            "Classic switch without break caused decades of bugs — upgrade the habit.",
            "Pattern matching plus sealed types later make switches exhaustive — Episodes Eighteen and Nineteen.",
            "Finite states belong in switch. Open-ended rules belong in methods.",
        ]),
        ("loops", "loops", [
            "Loops repeat work.",
            "for when you know bounds. while when waiting on a condition.",
            "Enhanced for-each when walking collections cleanly.",
            "break exits. continue skips to next iteration.",
            "Unbounded loops become incidents. Off-by-one loops become ArrayIndexOutOfBounds.",
            "Avoid heavy allocation every iteration in hot paths.",
        ]),
        ("example", "example", [
            "Walk a switch expression routing order status.",
            ("code", JAVA_FLOW),
            "OrderStatus enum — finite set of states.",
            "switch expression returns a String action — each case an arrow label.",
            "Compiler checks exhaustiveness when all enum constants covered.",
            "No break needed — arrow form does not fall through.",
            "This is readable control flow — status to action in one place.",
        ]),
        ("exceptions", "exceptions", [
            "Exceptions are for exceptional paths — not everyday outcomes.",
            "try, catch, finally — and try-with-resources for deterministic cleanup.",
            "Open JDBC connection or InputStream in try-with-resources — close called automatically.",
            "Do not throw exceptions to mean not found on every request — that is expensive control flow.",
            "Reserve exceptions for failures you cannot express as a normal return.",
            "Episode Thirty-Two goes deep on exception design — today know the boundary.",
        ]),
        ("pipeline", "pipeline", [
            "Picture a production request pipeline.",
            "Validate. Authorize. Process. Commit. Respond.",
            "On failure — compensate or retry with idempotency keys and clear rules.",
            "Good flow makes normal and failure paths equally obvious.",
            "Hidden branches are where incidents hide — log and test both paths.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "One — deeply nested branches hiding intent.",
            "Two — missing break in legacy switch — fall-through bugs.",
            "Three — exceptions for common outcomes.",
            "Also — entire business workflows stuffed in controllers — extract services.",
        ]),
        ("interview", "interview", [
            "Interview — when use switch expression?",
            "Finite, clear cases that produce a value.",
            "Prefer guard clauses over nesting.",
            "try-with-resources for deterministic cleanup.",
            "Do not use exceptions for normal control flow — cost and clarity.",
            "That package sounds senior.",
        ]),
        ("summary", "summary", [
            "Control flow shapes reliability.",
            "Guard clauses flatten code. Switch handles finite states.",
            "Loops need bounds and allocation discipline.",
            "Exceptions for failures — not regular branches.",
            "Make failure paths as visible as happy paths.",
        ]),
        ("teaser", "teaser", [
            "Paths are clear. Next — package behavior.",
            "Episode Seven — Methods.",
            "Parameters, returns, overloading — reusable named work.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[7] = {
    "slug": "methods",
    "title": "Methods",
    "scenes": [
        ("hook", "hook", [
            "Control flow chooses the path. Methods package the work.",
            "A method is named behavior — inputs, outputs, side effects, visibility.",
            "Good methods make APIs clear. Bad methods hide bugs in long routines.",
            "Senior Java is mostly method design — domain language at the right boundaries.",
        ]),
        ("title", "title", [
            "Episode Seven.",
            "Methods — parameters, returns, and clean contracts.",
        ]),
        ("anatomy", "anatomy", [
            "Anatomy of a method.",
            "Access modifier. Return type. Name. Parameter list. Body.",
            "Name says what it does. Parameters say what it needs.",
            "Return type says what you get — void if it only acts.",
            "Read a signature like a sentence — that is the contract callers depend on.",
        ]),
        ("signature", "signature", [
            "The signature is the contract.",
            "Same name, different parameter types — overloading. Compiler picks at compile time.",
            "Override — subclass replaces parent method — runtime polymorphism. Different idea.",
            "Keep overloads obvious. If callers guess wrong, rename instead.",
            "Varargs — String... parts — sparingly. Lists often clearer.",
        ]),
        ("example", "example", [
            "Walk domain methods on an order service.",
            ("code", JAVA_METHODS),
            "canBeCancelled encodes a rule — better than five comparisons copied in controllers.",
            "cancel validates then mutates — guard clause inside method.",
            "compareByAmount static — utility on type, no instance needed.",
            "Methods should express domain intent — not just mechanical steps.",
        ]),
        ("design", "design", [
            "Design tips that scale.",
            "One job per method. Short enough to scan in a code review.",
            "Avoid boolean flag parameters that fork behavior — split into two methods.",
            "Prefer clear return types over returning null without contract — Optional later in Episode Thirty.",
            "Do not swallow exceptions in helpers — callers need failure signals.",
            "Hide helpers as private unless they are real API.",
        ]),
        ("static", "static", [
            "Instance methods need an object. Static methods belong to the class.",
            "Static utilities fine for pure functions — parsing, math.",
            "Static mutable state is global — concurrency and test pollution.",
            "In Spring, this.method() from same class may skip transactional proxy — know AOP boundaries.",
            "Prefer instance behavior for domain rules.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "One — screen-long methods doing five jobs.",
            "Two — names like processData or handleStuff.",
            "Three — swallowing exceptions so callers never learn failure.",
            "Also — every helper public — no encapsulation left.",
        ]),
        ("interview", "interview", [
            "Interview — overload versus override?",
            "Overload — same name, different parameters, compile time.",
            "Override — subclass replaces inherited method, runtime dispatch.",
            "Methods should express domain intent.",
            "Boolean flag parameters are a design smell — split methods.",
        ]),
        ("summary", "summary", [
            "Methods package behavior with contracts.",
            "Signatures are API promises. Overload carefully. Override for polymorphism.",
            "Domain methods beat scattered operator soup.",
            "Static for utilities — not mutable global state.",
            "Name and size methods for the reader who arrives at three a.m.",
        ]),
        ("teaser", "teaser", [
            "Behavior is packaged. Next — hold many values.",
            "Episode Eight — Arrays.",
            "Fixed size, indexed access, off-by-one traps.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[8] = {
    "slug": "arrays",
    "title": "Arrays",
    "scenes": [
        ("hook", "hook", [
            "Methods package behavior. Arrays package many values.",
            "Fixed size. Indexed. Homogeneous — one type per slot.",
            "Arrays are objects in Java — special syntax, fast access.",
            "Collections build on this foundation — but arrays never go away.",
        ]),
        ("title", "title", [
            "Episode Eight.",
            "Arrays — fixed size, indexed access, and off-by-one traps.",
        ]),
        ("declare", "declare", [
            "Declaration — int[] scores = new int[5];",
            "Length five. Valid indices zero through four.",
            "Zero-based indexing — last index is length minus one.",
            "Length fixed at creation — no push like ArrayList.",
            "Default values — zero for numeric, false for boolean, null for references.",
        ]),
        ("access", "access", [
            "Access by index — constant time read and write.",
            "scores[0] = 90. scores[4] = 88.",
            "scores[5] throws ArrayIndexOutOfBoundsException.",
            "Off-by-one — loop with i <= length instead of i < length — classic bug.",
            "Say length minus one out loud until it is reflex.",
        ]),
        ("example", "example", [
            "Walk a small scoreboard loop.",
            ("code", JAVA_ARRAYS),
            "new int[5] allocates array object on heap — reference in scores variable.",
            "Fill index zero and four — middle slots still default zero.",
            "Loop uses i < scores.length — correct upper bound.",
            "Print index and value — see zero-based layout clearly.",
        ]),
        ("multi", "multi", [
            "Multidimensional — arrays of arrays.",
            "int[][] grid — rows can differ in length — jagged.",
            "Not one flat C-style block — know what you allocated.",
            "For heavy matrix math — use libraries designed for it.",
        ]),
        ("vs_list", "vs_list", [
            "Arrays versus ArrayList?",
            "Arrays — fixed, simple, fast index, can hold primitives with int[].",
            "ArrayList — grows, rich API, objects only — autoboxing for int.",
            "Prefer lists for most application code intent.",
            "Prefer arrays for buffers, interop, and primitive-heavy performance paths.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "One — off-by-one loops.",
            "Two — returning internal array from getter — callers mutate your internals.",
            "Three — huge arrays over the wire when pagination would do.",
            "Defensive copy on getters when exposing array fields.",
        ]),
        ("interview", "interview", [
            "Interview — are arrays objects?",
            "Yes — heap allocated with length field.",
            "Special bracket syntax. length property — not size().",
            "Zero-based indexing always.",
            "ArrayList wraps arrays internally for growable storage.",
        ]),
        ("summary", "summary", [
            "Arrays — fixed homogeneous indexed storage.",
            "Zero-based, length minus one for last index.",
            "Objects on heap. Fast access. No resize.",
            "Choose arrays or lists based on size behavior and primitives.",
            "Respect bounds — exceptions are loud for a reason.",
        ]),
        ("teaser", "teaser", [
            "Many values in fixed slots. Next — text.",
            "Episode Nine — Strings.",
            "Immutability, equality, careful building.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[9] = {
    "slug": "strings",
    "title": "Strings",
    "scenes": [
        ("hook", "hook", [
            "Arrays hold many values. Strings hold text — everywhere in Java.",
            "APIs, logs, JSON, SQL, HTTP headers, configuration.",
            "String is immutable — powerful safety, easy misuse.",
            "Small String mistakes become security and performance incidents.",
        ]),
        ("title", "title", [
            "Episode Nine.",
            "Strings — immutability, equality, and careful construction.",
        ]),
        ("immutable", "immutable", [
            "Immutable — characters do not change after creation.",
            "s = s + world creates new String — old s unchanged.",
            "Enables sharing, caching, safe concurrency for read-only text.",
            "Careless concatenation in loops allocates repeatedly.",
            "Understand create versus mutate — String only creates.",
        ]),
        ("equality", "equality", [
            "Equality trap again — equals-equals versus equals.",
            "Equals-equals — reference identity for objects.",
            "Equals — character content comparison.",
            "PAID.equals(status) — null-safe literal-first pattern.",
            "Make equals your default reflex for text comparison.",
        ]),
        ("example", "example", [
            "Walk building labels and checking status.",
            ("code", JAVA_STRINGS),
            "StringBuilder append in loop — mutates builder, not immutable strings.",
            "toString once at end — single allocation burst versus many intermediate strings.",
            "isPaid uses PAID.equals(status) — content equality, null-safe.",
            "Hot paths need builders. Simple plus is fine for two or three pieces.",
        ]),
        ("build", "build", [
            "Never plus in tight loops for many pieces.",
            "StringBuilder — append, then toString.",
            "String.join and String.format for structured assembly.",
            "Compilers optimize some simple cases — do not rely on that in hot loops.",
        ]),
        ("charset", "charset", [
            "Bytes are not characters without charset.",
            "StandardCharsets.UTF_8 explicitly when encoding.",
            "toLowerCase without Locale can break Turkish I.",
            "Never assume platform default charset matches production Linux containers.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "One — equals-equals for text.",
            "Two — logging secrets in strings.",
            "Three — unbounded input strings until OOM.",
            "Prefer typed IDs over raw strings twelve layers deep.",
        ]),
        ("interview", "interview", [
            "Interview — why String immutable?",
            "Safety, sharing, stable hash codes for hash maps, simpler concurrency.",
            "Use StringBuilder for repeated mutation.",
            "Never compare text with equals-equals.",
        ]),
        ("summary", "summary", [
            "Strings — immutable UTF-16 text objects.",
            "equals for content. StringBuilder for loops.",
            "Explicit charset. Careful logging.",
            "Text is a production type — treat it seriously.",
        ]),
        ("teaser", "teaser", [
            "Text under control. Next — model the world.",
            "Episode Ten — Object-Oriented Programming.",
            "Classes, objects, encapsulation.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[10] = {
    "slug": "object-oriented-programming",
    "title": "Object-Oriented Programming",
    "scenes": [
        ("hook", "hook", [
            "Strings and arrays hold data. Objects model the world.",
            "State, behavior, identity — working together.",
            "OOP in Java is how teams manage domain complexity — not just a syntax style.",
            "Classes are blueprints. Objects are living instances on the heap.",
        ]),
        ("title", "title", [
            "Episode Ten.",
            "Object-Oriented Programming — classes, objects, and encapsulation.",
        ]),
        ("class_obj", "class_obj", [
            "Class — blueprint. Fields hold state. Methods hold behavior.",
            "new BankAccount creates an object — unique identity.",
            "Two objects same class — different instances, different identity.",
            "== compares identity for objects. equals compares value when overridden.",
        ]),
        ("encaps", "encaps", [
            "Encapsulation — hide internals, expose intention.",
            "private fields. public methods enforcing invariants.",
            "Callers should not set balanceInCents directly if rules apply.",
            "Methods like deposit express domain language.",
            "Encapsulation is protection — not ceremony.",
        ]),
        ("example", "example", [
            "Walk a small account type.",
            ("code", JAVA_OOP),
            "private fields — state hidden.",
            "Constructor sets initial state.",
            "deposit validates positive amount — invariant enforced at boundary.",
            "balanceInCents accessor — read without exposing mutation path.",
        ]),
        ("pillars", "pillars", [
            "Four pillars people cite.",
            "Encapsulation — hide details.",
            "Abstraction — show what matters.",
            "Inheritance — share and specialize — carefully.",
            "Polymorphism — one interface, many implementations.",
            "Prefer composition — has-a — when inheritance trees get deep.",
        ]),
        ("compose", "compose", [
            "Composition — Order has Money, Customer has Address.",
            "Small collaborating objects beat god classes.",
            "Anemic model — data only in entities, all logic in services — loses clarity.",
            "Put behavior next to data it protects.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "One — god services doing every use case.",
            "Two — deep fragile inheritance.",
            "Three — public mutable fields.",
            "Leaking JPA entities through REST APIs — coupling nightmare.",
        ]),
        ("interview", "interview", [
            "Interview — class versus object?",
            "Class blueprint. Object instance with identity and state.",
            "Encapsulation — hide fields, expose behavior.",
            "Composition over deep inheritance.",
        ]),
        ("summary", "summary", [
            "OOP models collaborating objects.",
            "Encapsulate state. Express domain in methods.",
            "Composition often beats inheritance depth.",
            "Identity and equality are distinct concepts.",
            "Design for change at object boundaries.",
        ]),
        ("teaser", "teaser", [
            "Objects need boundaries. Next — who can see what.",
            "Episode Eleven — Access Modifiers.",
            "private, public, protected, package-private.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[11] = {
    "slug": "access-modifiers",
    "title": "Access Modifiers",
    "scenes": [
        ("hook", "hook", [
            "Objects need boundaries. Access modifiers draw the lines.",
            "Who sees this field? Who calls this method?",
            "Visibility is ownership encoded in syntax.",
            "Not an afterthought — an architecture decision in miniature.",
        ]),
        ("title", "title", [
            "Episode Eleven.",
            "Access Modifiers — private, public, protected, package-private.",
        ]),
        ("levels", "levels", [
            "Four levels — narrow to wide.",
            "private — declaring class only.",
            "package-private — no modifier — same package.",
            "protected — package plus subclasses.",
            "public — everyone. A promise.",
            "Default to narrowest that works. Widen with intent.",
        ]),
        ("private", "private", [
            "private first — fields and helpers.",
            "If everything is public — no boundary, only hope.",
            "Tests can use package-private collaborators in same package test sources.",
        ]),
        ("package", "package", [
            "Package-private underrated.",
            "Internal collaboration without publishing API.",
            "Accidental public grows compatibility obligations forever.",
        ]),
        ("example", "example", [
            "Walk facade hiding calculator.",
            ("code", JAVA_ACCESS),
            "InvoiceFacade public — stable entry.",
            "TaxCalculator package-private — internal to billing package.",
            "Only facade crosses package boundary in public API.",
        ]),
        ("protected_public", "protected_public", [
            "protected for extension points in inheritance hierarchies.",
            "public is published contract — every method maintained across releases.",
            "Libraries minimize public surface. Applications too.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "One — public fields.",
            "Two — public everything just in case.",
            "Three — widening visibility to fix tests instead of redesign.",
        ]),
        ("interview", "interview", [
            "Interview — default versus private?",
            "Default package-private — same package sees it.",
            "private — declaring class only.",
            "Prefer narrowest visibility. public is contract.",
        ]),
        ("summary", "summary", [
            "Access modifiers encode ownership.",
            "Start private. Use package for internal neighbors.",
            "public is long-term promise.",
            "Visibility shapes API evolution and test design.",
        ]),
        ("teaser", "teaser", [
            "Visibility needs a home. Next — packages.",
            "Episode Twelve — Packages.",
            "Namespaces, boundaries, ownership on disk.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[12] = {
    "slug": "packages",
    "title": "Packages",
    "scenes": [
        ("hook", "hook", [
            "Access needs neighborhoods. Packages are those neighborhoods.",
            "Namespace and boundary — on disk and at runtime.",
            "Prevent name collisions. Shape collaboration.",
            "Folder tree should tell the truth about ownership.",
        ]),
        ("title", "title", [
            "Episode Twelve.",
            "Packages — namespaces, boundaries, and ownership.",
        ]),
        ("namespace", "namespace", [
            "package com.acme.orders.domain — part of binary class name.",
            "com.acme.OrderService distinct from com.other.OrderService.",
            "Directory path must match package declaration.",
            "Break mapping — IDE and compiler angry.",
        ]),
        ("boundary", "boundary", [
            "Package-private visibility scoped to package.",
            "External code uses public API types only.",
            "Good packages make illegal dependencies awkward.",
            "One giant util package erases boundaries.",
        ]),
        ("structure", "structure", [
            "Organize by capability — api, application, domain, infrastructure.",
            "Or by feature when teams own features end to end.",
            "Pure layers alone can become anemic and tangled.",
            "Pick structure matching ownership and dependency direction.",
        ]),
        ("example", "example", [
            "Walk application root placement.",
            ("code", JAVA_PACKAGES),
            "OrdersApplication at com.acme.orders — root for scanning.",
            "Imports show dependency direction toward domain types.",
            "Main at sensible root — frameworks scan downward from here.",
        ]),
        ("spring", "spring", [
            "Spring Boot scans from main class package down.",
            "Too deep main — beans missed mysteriously.",
            "Packages are navigation paths for frameworks.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "One — everything in util.",
            "Two — cyclic package dependencies.",
            "Three — buried main class.",
            "Package names that lie about contents.",
        ]),
        ("interview", "interview", [
            "Interview — why packages matter?",
            "Namespace. Access. Ownership. Framework scanning.",
            "Runtime identity — fully qualified name plus classloader.",
            "Structure enforces architecture when done honestly.",
        ]),
        ("summary", "summary", [
            "Packages group types under namespace.",
            "Match folders. Control access. Express ownership.",
            "Root package is framework anchor in Spring.",
            "Honest tree beats clever naming.",
        ]),
        ("teaser", "teaser", [
            "Boundaries set. Next — type-safe fixed constants.",
            "Episode Thirteen — Enums.",
            "States instead of magic strings.",
            "See you there.",
        ]),
    ],
}

# Episodes 13-20
EPISODE_DATA_PART2[13] = {
    "slug": "enums",
    "title": "Enums",
    "scenes": [
        ("hook", "hook", [
            "Packages organize types. Enums organize fixed choices.",
            "PENDING, PAID, CANCELLED — not free-form strings drifting across services.",
            "Type-safe constants with behavior attached.",
            "Replace magic strings with domain vocabulary the compiler knows.",
        ]),
        ("title", "title", ["Episode Thirteen.", "Enums — type-safe states instead of magic strings."]),
        ("basics", "basics", [
            "enum OrderStatus — each constant is singleton instance.",
            "Compare with == safely — identity stable.",
            "Switch expressions love enums — finite exhaustive cases.",
            "Compiler helps when you add a new constant — update switches.",
        ]),
        ("behavior", "behavior", [
            "Enums can have fields, constructors, methods.",
            "Attach labels and transition rules next to constants.",
            "Better than String.equals scattered in five services.",
        ]),
        ("example", "example", [
            "Walk status enum with transitions.",
            ("code", JAVA_ENUMS),
            "Each constant calls constructor with display label.",
            "canTransitionTo encodes allowed moves — domain rule on the type.",
            "Switch on enum elsewhere stays readable and finite.",
        ]),
        ("vs_string", "vs_string", [
            "String status = PAID — typos compile. Invalid states sneak in.",
            "Enums reject invalid assignments at compile time.",
            "Persistence — prefer name over ordinal. Ordinal reorder breaks databases.",
        ]),
        ("enumset", "enumset", [
            "EnumSet for enum flag combinations — fast and compact.",
            "Better than raw int bitmasks unless you truly need bits.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes.",
            "Stringly typed statuses.",
            "ordinal in database columns.",
            "Enums for volatile business catalogs that change weekly.",
        ]),
        ("interview", "interview", [
            "Interview — enums versus strings?",
            "Type safety. Exhaustive switches. Behavior on constants.",
            "Persist name not ordinal.",
        ]),
        ("summary", "summary", [
            "Enums model fixed vocabularies.",
            "Constants are objects — can carry logic.",
            "Prefer over magic strings for states and categories.",
        ]),
        ("teaser", "teaser", [
            "Fixed states clear. Next — primitives as objects.",
            "Episode Fourteen — Wrappers and Autoboxing.",
            "Integer, nullability, hidden allocations.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[14] = {
    "slug": "wrappers-and-autoboxing",
    "title": "Wrappers and Autoboxing",
    "scenes": [
        ("hook", "hook", [
            "Enums gave type-safe states. Now numbers as objects.",
            "int primitive. Integer wrapper — nullable object.",
            "Autoboxing hides conversion — and hides costs and crashes.",
            "Collections need objects — wrappers bridge the gap.",
        ]),
        ("title", "title", ["Episode Fourteen.", "Wrappers and Autoboxing — objects around primitives."]),
        ("pairs", "pairs", [
            "Eight primitives. Eight wrappers.",
            "Wrappers on heap — identity, null allowed.",
            "Default to primitives unless nullability required.",
        ]),
        ("autobox", "autobox", [
            "Integer x = 10 boxes int.",
            "int y = x unboxes.",
            "Null Integer unboxed — NullPointerException.",
            "Silent conversion plus null is production trap.",
        ]),
        ("example", "example", [
            "Walk list of integers.",
            ("code", JAVA_WRAPPERS),
            "counts.add(10) autoboxes.",
            "get(0) unboxes to int.",
            "Hot loops through boxed lists allocate heavily.",
        ]),
        ("cost", "cost", [
            "Object header and indirection versus raw int.",
            "List<Integer> versus int[] in hot numeric code.",
            "Measure before boxing every number.",
        ]),
        ("cache", "cache", [
            "Integer caches small values — == may appear to work.",
            "Always use equals for wrapper comparison.",
        ]),
        ("mistakes", "mistakes", [
            "Unboxing null.",
            "Wrappers in hot loops without need.",
            "== on wrappers.",
            "Nullable Boolean in conditions without null check.",
        ]),
        ("interview", "interview", [
            "Primitive versus wrapper — value, null, overhead, autoboxing NPE.",
        ]),
        ("summary", "summary", [
            "Wrappers enable null and collections.",
            "Autoboxing convenient — not free.",
            "Prefer primitives in hot paths.",
        ]),
        ("teaser", "teaser", [
            "Objects around values. Next — type-safe containers.",
            "Episode Fifteen — Generics.",
            "List of Order without casts.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[15] = {
    "slug": "generics",
    "title": "Generics",
    "scenes": [
        ("hook", "hook", [
            "Wrappers made objects from values. Generics make containers type-safe.",
            "List of Order — not raw List with casts everywhere.",
            "Mistakes move from runtime ClassCastException to compile time.",
        ]),
        ("title", "title", ["Episode Fifteen.", "Generics — type parameters without the cast tax."]),
        ("why", "why", [
            "Raw List held anything — cast on exit — fail at runtime.",
            "List<String> documents and enforces intent.",
            "Compiler is first reviewer.",
        ]),
        ("declare", "declare", [
            "GenericBox<T> — T placeholder for type.",
            "Methods can be generic too — static <E> E first(List<E> items).",
            "Name parameters clearly — E element, K key, V value.",
        ]),
        ("example", "example", [
            "Walk generic box and typed list.",
            ("code", JAVA_GENERICS),
            "Box<String> and usage with ArrayList<String>.",
            "get returns String without cast.",
            "Type safety at compile time.",
        ]),
        ("bounds", "bounds", [
            "<T extends Number> limits type argument.",
            "Wildcards for flexible APIs — PECS when you go deeper.",
            "Prefer concrete type args at call sites when possible.",
        ]),
        ("erasure", "erasure", [
            "Generics mostly compile-time — type erasure at runtime.",
            "List<String> largely List at runtime.",
            "Cannot new T(). Cannot instanceof List<String>.",
            "Design with erasure limits in mind.",
        ]),
        ("mistakes", "mistakes", [
            "Raw types.",
            "Ignoring unchecked warnings.",
            "Overcomplicated wildcards.",
        ]),
        ("interview", "interview", [
            "Type erasure — compile-time checks, erased runtime for compatibility.",
            "Prefer parameterized types always.",
        ]),
        ("summary", "summary", [
            "Generics add compile-time type safety to APIs and collections.",
            "Erasure limits runtime type introspection.",
            "No raw types in new code.",
        ]),
        ("teaser", "teaser", [
            "Containers type-safe. Next — metadata on code.",
            "Episode Sixteen — Annotations.",
            "Override, Spring markers, retention.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[16] = {
    "slug": "annotations",
    "title": "Annotations",
    "scenes": [
        ("hook", "hook", [
            "Generics typed containers. Annotations label code.",
            "Metadata attached to classes, methods, fields.",
            "Override. Deprecated. Spring stereotypes.",
            "Tiny symbols — huge framework power when something reads them.",
        ]),
        ("title", "title", ["Episode Sixteen.", "Annotations — metadata compilers and frameworks read."]),
        ("what", "what", [
            "At-sign on declarations.",
            "Does nothing alone — compiler, tool, or framework must process.",
            "Structured sticky notes on code.",
        ]),
        ("builtin", "builtin", [
            "Override catches signature mistakes.",
            "Deprecated signals migration.",
            "FunctionalInterface documents SAM types.",
        ]),
        ("retention", "retention", [
            "RetentionPolicy — SOURCE, CLASS, RUNTIME.",
            "Spring needs RUNTIME to see markers while app runs.",
            "Wrong retention — invisible when needed.",
        ]),
        ("example", "example", [
            "Walk custom audited annotation.",
            ("code", JAVA_ANNOTATIONS),
            "RUNTIME retention and METHOD target.",
            "capturePayment marked — processor can enforce audit trail.",
            "Override on toString — compile-time check.",
        ]),
        ("spring", "spring", [
            "SpringBootApplication, RestController, Service — wiring instructions.",
            "Powerful — avoid annotation soup hiding architecture.",
        ]),
        ("custom", "custom", [
            "Define @interface with retention and target.",
            "Must pair with processor or runtime enforcement.",
        ]),
        ("mistakes", "mistakes", [
            "Assuming annotation works without reader.",
            "Wrong retention.",
            "SuppressWarnings to hide real issues.",
        ]),
        ("interview", "interview", [
            "Annotation — structured metadata on code elements.",
            "Retention and examples — Override vs RestController.",
        ]),
        ("summary", "summary", [
            "Annotations are metadata contracts.",
            "Retention and targets matter.",
            "Frameworks consume RUNTIME markers.",
        ]),
        ("teaser", "teaser", [
            "Metadata clear. Next — inspect types at runtime.",
            "Episode Seventeen — Reflection.",
            "Classes, methods, costs.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[17] = {
    "slug": "reflection",
    "title": "Reflection",
    "scenes": [
        ("hook", "hook", [
            "Annotations are metadata. Reflection reads type structure at runtime.",
            "Discover methods. Invoke by name. Frameworks live here.",
            "Powerful — expensive — easy to misuse.",
        ]),
        ("title", "title", ["Episode Seventeen.", "Reflection — inspect and invoke at runtime."]),
        ("basics", "basics", [
            "Class<?> clazz = String.class or obj.getClass().",
            "getMethod, getField, getConstructor — discovery API.",
        ]),
        ("invoke", "invoke", [
            "Method.invoke target with args.",
            "setAccessible breaks encapsulation — use rarely.",
        ]),
        ("example", "example", [
            "Walk invoking String.length reflectively.",
            ("code", JAVA_REFLECTION),
            "Class.forName loads by name.",
            "getMethod and invoke — dynamic call slower than direct.",
        ]),
        ("frameworks", "frameworks", [
            "Spring DI, JSON mappers, ORMs — reflection-heavy.",
            "Productivity trade for complexity and startup cost.",
        ]),
        ("cost", "cost", [
            "Slower than direct calls. Module restrictions. Native image config.",
            "Cache MethodHandles in hot paths if unavoidable.",
        ]),
        ("safety", "safety", [
            "Validate inputs — reflective surfaces can be injection points.",
            "Quarantine reflection behind small modules.",
        ]),
        ("mistakes", "mistakes", [
            "Reflection instead of interfaces.",
            "setAccessible everywhere.",
            "Field names as stable API.",
        ]),
        ("interview", "interview", [
            "Reflection — runtime inspection and invocation.",
            "Framework use. Trade flexibility for speed and clarity.",
        ]),
        ("summary", "summary", [
            "Reflection enables frameworks.",
            "Prefer normal calls when types known.",
            "Understand cost and encapsulation risks.",
        ]),
        ("teaser", "teaser", [
            "Inspect types. Next — cleaner data carriers.",
            "Episode Eighteen — Records.",
            "Less boilerplate, immutable data.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[18] = {
    "slug": "records",
    "title": "Records",
    "scenes": [
        ("hook", "hook", [
            "Reflection digs into types. Records make data honest.",
            "Getters, equals, hashCode, toString — generated for transparent carriers.",
            "Less boilerplate. Clearer intent.",
        ]),
        ("title", "title", ["Episode Eighteen.", "Records — compact immutable data carriers."]),
        ("declare", "declare", [
            "record Money(String currency, long minorUnits) — components final.",
            "Canonical constructor, accessors, equals, hashCode, toString generated.",
        ]),
        ("accessors", "accessors", [
            "currency() not getCurrency — intentional style.",
            "Not classic JavaBeans — libraries adapting.",
        ]),
        ("example", "example", [
            "Walk Money record with validation and add.",
            ("code", JAVA_RECORDS),
            "Compact constructor validates currency and non-negative minorUnits.",
            "add returns new record — immutability preserved.",
        ]),
        ("validation", "validation", [
            "Compact constructor enforces invariants at creation.",
            "Invalid money cannot exist.",
        ]),
        ("when", "when", [
            "DTOs, events, value objects — yes.",
            "Mutable JPA entities with proxies — often no.",
        ]),
        ("limits", "limits", [
            "Records implicitly final. Can implement interfaces and add methods.",
            "Do not turn records into services.",
        ]),
        ("mistakes", "mistakes", [
            "Mutable list components without defensive copy.",
            "Records as JPA entities expecting mutation.",
            "Skipping validation in compact constructor.",
        ]),
        ("interview", "interview", [
            "Record — immutable data carrier with generated members.",
            "Great for DTOs and values. Compact constructor for rules.",
        ]),
        ("summary", "summary", [
            "Records reduce boilerplate for immutable data.",
            "Validate at construction. Mind component mutability.",
            "Not replacement for all classes.",
        ]),
        ("teaser", "teaser", [
            "Data carriers clean. Next — restrict hierarchies.",
            "Episode Nineteen — Sealed Classes.",
            "Controlled subclasses, exhaustive switches.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[19] = {
    "slug": "sealed-classes",
    "title": "Sealed Classes",
    "scenes": [
        ("hook", "hook", [
            "Records cleaned data. Hierarchies still sprawl.",
            "Anyone could subclass — switches incomplete.",
            "Sealed types close the permitted family.",
        ]),
        ("title", "title", ["Episode Nineteen.", "Sealed Classes — controlled hierarchies."]),
        ("idea", "idea", [
            "sealed interface or class lists permits.",
            "Subtypes must be final, sealed, or non-sealed.",
            "Compiler enforces guest list.",
        ]),
        ("syntax", "syntax", [
            "sealed interface Shape permits Circle, Rectangle.",
            "non-sealed reopens one branch deliberately.",
        ]),
        ("example", "example", [
            "Walk payment result variants.",
            ("code", JAVA_SEALED),
            "Ok and Err records implement sealed PaymentResult.",
            "describe switch covers all cases — no default needed.",
        ]),
        ("switch", "switch", [
            "Exhaustive switch — compiler forces updates when family grows.",
            "Pairs with pattern matching.",
        ]),
        ("when", "when", [
            "Closed domain variants — events, AST nodes, results.",
            "Not for open plugin ecosystems.",
        ]),
        ("records", "records", [
            "Sealed plus records — compact closed ADTs in Java.",
        ]),
        ("mistakes", "mistakes", [
            "Sealing too early.",
            "Wrong package for permitted types.",
            "Default case hiding missing cases.",
        ]),
        ("interview", "interview", [
            "Sealed restricts extenders — enables exhaustive switches.",
            "permits and final/non-sealed subtypes.",
        ]),
        ("summary", "summary", [
            "Sealed types model closed families.",
            "Exhaustive switches catch evolution.",
            "Pair with records for modern modeling.",
        ]),
        ("teaser", "teaser", [
            "Hierarchies closed. Next — module boundaries.",
            "Episode Twenty — Modules and JPMS.",
            "requires, exports, strong encapsulation.",
            "See you there.",
        ]),
    ],
}

EPISODE_DATA_PART2[20] = {
    "slug": "modules-and-jpms",
    "title": "Modules and JPMS",
    "scenes": [
        ("hook", "hook", [
            "Sealed types close inheritance. Modules close the classpath.",
            "JPMS — Java Platform Module System — explicit boundaries since Java 9.",
            "What you require. What you export. What stays internal.",
        ]),
        ("title", "title", ["Episode Twenty.", "Modules and JPMS — strong encapsulation."]),
        ("why", "why", [
            "Flat classpath — accidental access to public types everywhere.",
            "Split packages. Leaky internals. Classpath order roulette.",
            "Modules declare graph upfront — JVM enforces.",
        ]),
        ("info", "info", [
            "module-info.java — requires and exports.",
            "Internal packages hidden even if types are public.",
        ]),
        ("example", "example", [
            "Walk payments module descriptor.",
            ("code", JAVA_MODULES),
            "requires java.sql and com.shop.common.",
            "exports com.shop.payments.api only.",
            "opens for reflection frameworks like Jackson when needed.",
        ]),
        ("directives", "directives", [
            "requires transitive for re-exported dependencies.",
            "exports to for narrow API consumers.",
            "provides/uses for service loading.",
        ]),
        ("unnamed", "unnamed", [
            "Classpath JARs — unnamed module.",
            "Migration incremental — automatic modules from JAR names.",
        ]),
        ("when", "when", [
            "Platform libraries, jlink images, strong encapsulation.",
            "Many Spring Boot apps stay classpath-first unless boundary is product feature.",
        ]),
        ("mistakes", "mistakes", [
            "Export everything.",
            "opens forever instead of narrowing.",
            "Split packages across modules.",
        ]),
        ("interview", "interview", [
            "JPMS adds explicit dependencies and exports beyond packages.",
            "public not enough — module must export package.",
            "Unnamed module and jlink mention.",
        ]),
        ("summary", "summary", [
            "Modules enforce encapsulation at build and runtime.",
            "module-info is contract. Plan migration.",
            "Classpath still valid — modules when boundaries matter.",
        ]),
        ("teaser", "teaser", [
            "Language foundations in place. Next — everyday collections.",
            "Episode Twenty-One — Lists.",
            "Ordered sequences and choosing implementations.",
            "See you there.",
        ]),
    ],
}
