"""Episode 02-20 expansion data."""

from __future__ import annotations

JAVA_PAYMENT = '''```java
public class PaymentCalculator {
    public static void main(String[] args) {
        System.out.println("Runtime: " + Runtime.version());
        long amountInCents = 12_345L;
        System.out.println("Amount (cents): " + amountInCents);
    }
}
```'''

BASH_EP02 = '''```bash
java -version
javac -version
javac PaymentCalculator.java
java PaymentCalculator
jar --describe-module --file app.jar
jcmd <pid> VM.version
```'''

JAVA_ORDER = '''```java
package com.example.orders.domain;

public final class Order {
    private final String id;
    private final long amountInCents;

    public Order(String id, long amountInCents) {
        if (amountInCents < 0) {
            throw new IllegalArgumentException("amount must be non-negative");
        }
        this.id = id;
        this.amountInCents = amountInCents;
    }

    public boolean isHighValue() {
        return amountInCents >= 100_00;
    }
}
```'''

JAVA_HELLO = '''```java
package com.example.app;

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```'''

JAVA_TYPES = '''```java
long amountInCents = 12_345L;
boolean active = true;
String customerId = "C-1001";
var retryCount = 3; // still int at compile time

public record Money(String currency, long minorUnits) {
    public Money {
        if (currency == null || currency.length() != 3) {
            throw new IllegalArgumentException("currency must be ISO-4217");
        }
    }
}
```'''

JAVA_OPS = '''```java
public class CheckoutGuard {
    static boolean canShip(String orderStatus, String customerId, String requestId) {
        if (orderStatus == null || customerId == null) {
            return false;
        }
        if ("PAID".equals(orderStatus) && customerId.equals(requestId)) {
            return true;
        }
        return false;
    }

    static long addWithOverflowCheck(long existing, long delta) {
        return Math.addExact(existing, delta);
    }
}
```'''

JAVA_FLOW = '''```java
public enum OrderStatus { PENDING, PAID, CANCELLED, SHIPPED }

public class OrderRouter {
    static String nextAction(OrderStatus status) {
        return switch (status) {
            case PENDING -> "await_payment";
            case PAID -> "fulfill";
            case CANCELLED -> "archive";
            case SHIPPED -> "track";
        };
    }
}
```'''

JAVA_METHODS = '''```java
public class OrderService {
    public boolean canBeCancelled(Order order) {
        return order.status() == OrderStatus.PENDING;
    }

    public void cancel(Order order) {
        if (!canBeCancelled(order)) {
            throw new IllegalStateException("cannot cancel");
        }
        order.markCancelled();
    }

    public static int compareByAmount(Order a, Order b) {
        return Long.compare(a.amountInCents(), b.amountInCents());
    }
}
```'''

JAVA_ARRAYS = '''```java
public class ScoreBoard {
    public static void main(String[] args) {
        int[] scores = new int[5];
        scores[0] = 90;
        scores[4] = 88; // last valid index is length - 1

        for (int i = 0; i < scores.length; i++) {
            System.out.println("Index " + i + ": " + scores[i]);
        }
    }
}
```'''

JAVA_STRINGS = '''```java
public class LabelBuilder {
    public static String buildLabels(String[] items) {
        StringBuilder sb = new StringBuilder();
        for (String item : items) {
            sb.append(item).append(", ");
        }
        if (sb.length() >= 2) {
            sb.setLength(sb.length() - 2);
        }
        return sb.toString();
    }

    public static boolean isPaid(String status) {
        return "PAID".equals(status); // content equality, null-safe
    }
}
```'''

JAVA_OOP = '''```java
public class BankAccount {
    private final String id;
    private long balanceInCents;

    public BankAccount(String id, long openingBalance) {
        this.id = id;
        this.balanceInCents = openingBalance;
    }

    public void deposit(long cents) {
        if (cents <= 0) throw new IllegalArgumentException("positive deposit only");
        balanceInCents += cents;
    }

    public long balanceInCents() {
        return balanceInCents;
    }
}
```'''

JAVA_ACCESS = '''```java
public class InvoiceFacade {
    private final TaxCalculator calculator = new TaxCalculator();

    public Money totalWithTax(Money subtotal) {
        return calculator.applyTax(subtotal);
    }
}

class TaxCalculator {
    Money applyTax(Money subtotal) {
        return subtotal; // package-private collaborator
    }
}
```'''

JAVA_PACKAGES = '''```java
package com.acme.orders;

import com.acme.orders.domain.Order;
import com.acme.orders.api.OrderController;

public class OrdersApplication {
    public static void main(String[] args) {
        System.out.println("Boot from root package: com.acme.orders");
    }
}
```'''

JAVA_ENUMS = '''```java
public enum OrderStatus {
    PENDING("Awaiting payment"),
    PAID("Ready to ship"),
    SHIPPED("In transit"),
    CANCELLED("Closed");

    private final String label;
    OrderStatus(String label) { this.label = label; }

    public String label() { return label; }

    public boolean canTransitionTo(OrderStatus next) {
        return switch (this) {
            case PENDING -> next == PAID || next == CANCELLED;
            case PAID -> next == SHIPPED;
            default -> false;
        };
    }
}
```'''

JAVA_WRAPPERS = '''```java
import java.util.ArrayList;
import java.util.List;

public class WrapperDemo {
    public static void main(String[] args) {
        int primitive = 42;
        Integer boxed = primitive;       // autobox
        int unboxed = boxed;             // unbox

        List<Integer> counts = new ArrayList<>();
        counts.add(10);                  // autobox on add
        int first = counts.get(0);       // unbox on read
    }
}
```'''

JAVA_GENERICS = '''```java
import java.util.ArrayList;
import java.util.List;

public class GenericBox<T> {
    private T value;

    public void set(T value) { this.value = value; }
    public T get() { return value; }

    public static <E> E first(List<E> items) {
        return items.isEmpty() ? null : items.get(0);
    }
}

class Usage {
    void demo() {
        List<String> names = new ArrayList<>();
        names.add("Ada");
        String first = names.get(0); // no cast needed
    }
}
```'''

JAVA_ANNOTATIONS = '''```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Audited {
    String action();
}

public class PaymentService {
    @Audited(action = "capture")
    public void capturePayment(String id) {
        // framework or processor reads @Audited at runtime
    }

    @Override
    public String toString() {
        return "PaymentService";
    }
}
```'''

JAVA_REFLECTION = '''```java
import java.lang.reflect.Method;

public class ReflectionDemo {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = Class.forName("java.lang.String");
        Method lengthMethod = clazz.getMethod("length");
        Object result = lengthMethod.invoke("hello");
        System.out.println("length = " + result);
    }
}
```'''

JAVA_RECORDS = '''```java
public record Money(String currency, long minorUnits) {
    public Money {
        if (currency == null || currency.length() != 3) {
            throw new IllegalArgumentException("ISO-4217 currency required");
        }
        if (minorUnits < 0) {
            throw new IllegalArgumentException("minorUnits must be non-negative");
        }
    }

    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("currency mismatch");
        }
        return new Money(currency, minorUnits + other.minorUnits);
    }
}
```'''

JAVA_SEALED = '''```java
public sealed interface PaymentResult permits PaymentResult.Ok, PaymentResult.Err {
    record Ok(String transactionId) implements PaymentResult {}
    record Err(String message) implements PaymentResult {}

    static String describe(PaymentResult result) {
        return switch (result) {
            case Ok ok -> "success: " + ok.transactionId();
            case Err err -> "failure: " + err.message();
        };
    }
}
```'''

JAVA_MODULES = '''```java
module com.shop.payments {
    requires java.sql;
    requires com.shop.common;

    exports com.shop.payments.api;

    opens com.shop.payments.api to com.fasterxml.jackson.databind;
}
```'''

EPISODE_DATA: dict[int, dict] = {}

# --- Episode 02 ---
EPISODE_DATA[2] = {
    "slug": "jdk-jre-and-jvm",
    "title": "JDK, JRE, and JVM",
    "scenes": [
        ("hook", "hook", [
            "Quick continuity from Episode One.",
            "We learned why Java survives — bytecode, the JVM, Write Once Run Anywhere.",
            "But on day one, beginners slam into three names that sound interchangeable.",
            "JDK. JRE. JVM.",
            "Install Java — which one did you actually install?",
            "Today we separate those layers clearly — with a diagram in your head and commands on screen.",
            "Once this clicks, Docker images, CI builds, and production incidents make more sense.",
        ]),
        ("title", "title", [
            "Episode Two.",
            "JDK, JRE, and JVM — the three layers of the Java platform.",
            "By the end you'll know who compiles, who launches, and who executes.",
        ]),
        ("layers", "layers", [
            "Picture three nested boxes.",
            "At the bottom — the JVM. The engine. It executes bytecode.",
            "Wrap that with the JRE idea — runtime libraries, launchers, the standard APIs your app calls at run time.",
            "On top — the JDK. Everything in the runtime plus developer tools.",
            "javac to compile. jar to package. jlink to trim runtimes. jcmd, jmap, jfr for diagnostics.",
            "Mnemonic that actually helps: JDK for develop. JRE for run. JVM is the engine inside.",
            "Modern distributions often ship a JDK by default — but the conceptual split still matters in containers and CI.",
        ]),
        ("jdk_tools", "jdk_tools", [
            "Zoom into the JDK — this is your developer toolkit.",
            "javac turns .java source into .class bytecode.",
            "jar bundles classes and resources. jdeps analyzes dependencies.",
            "jlink builds custom runtimes — smaller than shipping a full JDK when you only need java.base plus a few modules.",
            "jcmd attaches to running processes. jmap and jfr help you debug memory and latency in production.",
            "If you write code — or troubleshoot live services — you want JDK tools available somewhere in your pipeline.",
            "Production containers sometimes carry only a runtime image — but then you need another path for thread dumps and flight recordings.",
        ]),
        ("jre_run", "jre_run", [
            "The JRE is the runtime layer — what you need to launch a Java process.",
            "Standard libraries. The java launcher. Core APIs like java.lang and java.util.",
            "Historically you could install a standalone JRE without compilers.",
            "Today many teams ship a JDK everywhere for consistency — or a slim jlink image that is runtime-shaped.",
            "The JRE concept still explains why a container might omit javac — and why missing diagnostics hurts at three a.m.",
            "Runtime-only packaging saves disk — until you need jcmd and it is not there.",
        ]),
        ("jvm_engine", "jvm_engine", [
            "And here is the JVM — where bytecode becomes behavior.",
            "It loads class files, verifies bytecode safety, allocates heap and stacks, runs garbage collection.",
            "HotSpot is the common implementation — interpreter first, then JIT for hot methods.",
            "Class loaders, bytecode verifier, linker, interpreter, C1 and C2 compilers — the pipeline from Episode One, now with names.",
            "Other JVMs exist — OpenJ9, GraalVM — with different tradeoffs for startup, memory, and native image.",
            "Same bytecode contract. Different engines. That is why we say JVM as specification and HotSpot as one implementation.",
        ]),
        ("flow", "flow", [
            "Follow the arrows from source to running process.",
            "Your .java file goes to javac — a JDK tool.",
            "Out comes HelloWorld.class — platform-neutral bytecode.",
            "The java launcher starts a JVM process, creates runtime data areas, loads the main class, calls main.",
            "Behind the scenes: class loading, static initialization, then your println.",
            "Build systems compile with a JDK. Deployment platforms launch a JVM with your artifact and flags.",
            "Spring Boot fat JARs add a launcher layer — but the story ends the same way: JVM executes bytecode.",
            "Let's make that concrete with commands you'd run every day.",
            ("code", BASH_EP02),
            "java -version tells you what runtime you're holding — vendor, version, sometimes LTS.",
            "javac -version should match your build JDK — mismatch is a classic incident seed.",
            "Compile, then run — notice you pass the class name to java, not the .class filename.",
            "jar --describe-module inspects modular JARs. jcmd VM.version attaches to a live PID when serviceability tools are present.",
        ]),
        ("memory", "memory", [
            "Now the production gotcha nobody warns you about on day one.",
            "When ops says set heap to four gigabytes — that is not the whole process.",
            "The JVM also allocates metaspace for class metadata, thread stacks, code cache for JIT code, direct memory for NIO, native structures for GC.",
            "Container limit equals -Xmx is a famous failure mode.",
            "You starve metaspace, threads, or direct buffers — and the process dies with errors that blame the wrong layer.",
            "Always leave headroom beyond heap. Account for total RSS, not just -Xmx on a slide.",
            "Episode One showed stack versus heap — today add non-heap as first-class in your mental model.",
        ]),
        ("mistakes", "mistakes", [
            "Three mistakes I want burned into your brain.",
            "Mistake one — shipping a full JDK into every tiny container when a jlink runtime would suffice — image bloat and attack surface.",
            "Mistake two — CI compiles with Java twenty-one, production runs seventeen — subtle bytecode or API differences, or worse, silent assumptions.",
            "Mistake three — treating the JVM as a black box until GC pauses or OOM kills the pod.",
            "Bonus trap — assuming public types on the classpath are all equally reachable once modules enter — preview of Episode Twenty.",
            "Know your layers. Version them together. Instrument the engine.",
        ]),
        ("interview", "interview", [
            "Interview time — say this like someone who ships Java services.",
            "Question: What's the difference between JDK, JRE, and JVM?",
            "JVM executes bytecode — class loading, verification, JIT, GC.",
            "JRE is the runtime environment — libraries and launcher to run applications.",
            "JDK is the development kit — JRE plus compilers and diagnostic tools like javac, jar, jcmd.",
            "Bonus line: container memory must include heap and non-heap; -Xmx alone is not the process budget.",
            "If you can point to the three boxes while you answer — you're ahead of candidates who only memorized acronyms.",
        ]),
        ("summary", "summary", [
            "Let's land the plane.",
            "JDK develops. JRE runs. JVM executes bytecode.",
            "javac and java are different doors into the same platform story.",
            "HotSpot is the engine most of us run — with real memory areas beyond heap.",
            "Match JDK versions across build and runtime. Leave container headroom.",
            "Episode One gave you why Java is portable — Episode Two names the machinery you install.",
        ]),
        ("teaser", "teaser", [
            "The three names finally line up with the picture.",
            "Next — open a Java file and read it like a map.",
            "Episode Three — Java Program Structure.",
            "Packages, classes, main — what every line is doing.",
            "See you there.",
        ]),
    ],
    "scene_intent": {
        "hook": "continuity + three-name confusion",
        "title": "episode promise",
        "layers": "JDK/JRE/JVM nested model",
        "jdk_tools": "developer toolchain",
        "jre_run": "runtime layer",
        "jvm_engine": "bytecode execution engine",
        "flow": "compile-run pipeline + bash walkthrough",
        "memory": "heap vs non-heap in containers",
        "mistakes": "common mistakes",
        "interview": "JDK vs JRE vs JVM interview",
        "summary": "revision",
        "teaser": "bridge to Episode 03",
    },
}

# --- Episode 03 ---
EPISODE_DATA[3] = {
    "slug": "java-program-structure",
    "title": "Java Program Structure",
    "scenes": [
        ("hook", "hook", [
            "Episode Two named the platform layers — JDK, JRE, JVM.",
            "Now open any Java file in your editor.",
            "Every line has a job — package, imports, class, fields, methods, statements.",
            "Structure is not decoration.",
            "It decides how code is found, compiled, loaded, tested, scanned by frameworks, and owned by teams.",
            "Today we read a Java program like a map — slowly, line by line.",
        ]),
        ("title", "title", [
            "Episode Three.",
            "Java Program Structure — packages, classes, and the entry point.",
            "By the end you'll see hierarchy, access, and runtime identity in one picture.",
        ]),
        ("anatomy", "anatomy", [
            "Here is the shape Java expects.",
            "At the top — optional package declaration. That is your namespace on disk and in bytecode.",
            "Then imports — shortcuts to types defined elsewhere.",
            "A top-level type — usually a public class. One public class per file, filename must match.",
            "Inside the class — fields for state, constructors to create valid objects, methods for behavior, nested types when needed.",
            "Below that — blocks and statements inside methods.",
            "Think tree: package, then type, then members, then statements.",
            "Tools — compilers, IDEs, Spring — all assume this hierarchy.",
        ]),
        ("hello", "hello", [
            "Walk a classic program — slowly, because every piece maps to a real rule.",
            ("code", JAVA_HELLO),
            "Line one: package com.example.app — this type's fully qualified name starts here.",
            "Folders under src/main/java should mirror that path — com/example/app/HelloWorld.java.",
            "public class HelloWorld — the public class name and filename must match. Java is case-sensitive.",
            "public static void main(String[] args) — the JVM entry point. public so the launcher sees it. static so it runs without constructing an object first.",
            "String[] args — command-line arguments as an array of strings.",
            "System.out.println — one statement, terminated by semicolon, printing a line to standard output.",
            "Tiny file. Four layers of structure. One runnable program.",
        ]),
        ("access", "access", [
            "Access is part of structure — not a later topic.",
            "public — visible everywhere. Use for intentional API surface.",
            "No modifier — package-private. Same package only. Perfect for internal collaborators.",
            "private — only this class. Default for fields.",
            "protected — package plus subclasses — we'll deepen that in Episode Eleven.",
            "Good structure hides what should not leak — and keeps public APIs small.",
            "If everything is public, you have no boundary — only hope.",
        ]),
        ("packages", "packages", [
            "In real services, packages mirror ownership.",
            "api — controllers, DTOs, public HTTP contracts.",
            "application — use-case orchestration.",
            "domain — business rules and entities.",
            "infrastructure — databases, messaging, external adapters.",
            "Dependency arrows should point inward — domain should not import JDBC types.",
            "Flat util packages with two hundred classes erase ownership — and make cyclic imports inevitable.",
            "Structure expresses who owns what — and what must not depend on what.",
        ]),
        ("flow", "flow", [
            "Follow runtime with structure in mind.",
            "Load class by fully qualified name. Verify bytecode. Prepare static fields. Run static initializers. Construct objects. Invoke methods.",
            "Your package and class names become the identity the classloader loads.",
            "com.example.orders.Order and com.other.orders.Order are different types — even if both are called Order.",
            "Class identity is name plus classloader — matters in app servers, plugins, and Spring devtools.",
            "Static fields live with class metadata. Instance fields live in heap objects. Locals live in stack frames.",
            "Structure you write becomes layout and lifecycle at runtime — indirectly but reliably.",
        ]),
        ("deeper", "deeper", [
            "Go one level deeper — domain example with validation in the constructor.",
            ("code", JAVA_ORDER),
            "private final fields — state encapsulated, reassignment blocked on the reference.",
            "Constructor validates amountInCents — invalid objects cannot exist.",
            "isHighValue encodes a domain rule next to the data it protects — better than scattered comparisons in controllers.",
            "This is structure serving design — not ceremony.",
            "Spring Boot later scans from your main class package downward — root package choice is architectural.",
        ]),
        ("mistakes", "mistakes", [
            "Three common mistakes.",
            "One — every class in one giant package. Ownership and test boundaries disappear.",
            "Two — public mutable fields — encapsulation dies, invariants impossible.",
            "Three — burying @SpringBootApplication too deep so component scanning misses half your beans.",
            "Also — hiding I/O inside constructors — hard to test, surprising side effects on new.",
            "Fix structure early — refactors across package boundaries hurt later.",
        ]),
        ("interview", "interview", [
            "Interview question — why do packages matter?",
            "Namespacing — avoid class name collisions.",
            "Access control — package-private collaboration.",
            "Ownership — teams and modules align to packages.",
            "Framework scanning — Spring Boot starts from the application class package.",
            "Add — class identity is fully qualified name plus defining classloader.",
            "That answer connects syntax to architecture — interviewers notice.",
        ]),
        ("summary", "summary", [
            "Let's land the plane.",
            "Java programs organize as packages, types, members, and statements.",
            "Filename matches public class. main is the conventional entry.",
            "Access modifiers encode boundaries. Package layout encodes ownership.",
            "Runtime loads by fully qualified names — structure is not cosmetic.",
            "You can read a Java file as a map now — not a wall of keywords.",
        ]),
        ("teaser", "teaser", [
            "You can read the skeleton. Next — what lives inside those fields and methods.",
            "Episode Four — Variables and Data Types.",
            "Primitives, references, money traps, and memory shape.",
            "See you there.",
        ]),
    ],
    "scene_intent": {
        "hook": "continuity from JDK layers",
        "title": "episode promise",
        "anatomy": "program hierarchy",
        "hello": "HelloWorld line-by-line",
        "access": "access modifiers primer",
        "packages": "production package layout",
        "flow": "load-init-invoke runtime",
        "deeper": "domain Order example",
        "mistakes": "common mistakes",
        "interview": "packages interview",
        "summary": "revision",
        "teaser": "bridge to Episode 04",
    },
}

# Episodes 04-20 continue in part 2
from expand_episodes_02_20_data_part2 import EPISODE_DATA_PART2  # noqa: E402

EPISODE_DATA.update(EPISODE_DATA_PART2)
