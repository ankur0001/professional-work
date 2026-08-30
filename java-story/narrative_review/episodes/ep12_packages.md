# Episode 12 — Packages

| Field | Value |
|---|---|
| Episode | 12 |
| Title | Packages |
| Catalog handbook column | 12 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Access modifiers taught us who may touch a member. Package-private visibility only makes sense if "same package" is a real neighborhood, not an accident of whatever folder someone happened to click. As a project grows, another problem appears beside visibility: names collide, and the filesystem stops matching what the source claims.

Two libraries can both invent `Utils`. Two features can both invent `Order`. Without namespaces, short names become a fight. Onboarding suffers too: a newcomer opens `src` and finds fifty classes in one flat pile with no hint which ones form the checkout story.

So the natural question is: how does Java give types an address space large enough for a company, honest enough for the compiler, and useful enough for access boundaries?

Packages are that geography — names, folders, and boundaries together.

Java's common convention is reverse-DNS style naming: `com.shop.order`, `org.example.tools`. The point is uniqueness and hierarchy, not fashion. You own a domain, you flip it, you nest features underneath. `order` alone is a fight waiting to happen. `com.shop.order` is an address.

```java
package com.shop.order;

import com.shop.user.User;

public class OrderService {
    private final User user;

    public OrderService(User user) {
        this.user = user;
    }
}
```

The first line claims a package. On disk, this file should live under folders that mirror `com/shop/order`. The import brings `User` from another package into short-name scope. Because the packages differ, package-private members of `User` stay hidden. Packages and access modifiers combine into real boundaries, not just folder cosmetics.

Episode Three already introduced packages as addresses for the compiler. Today the stakes are higher: packages are how a growing product stays navigable, and how "same package" remains a meaningful friendship for package-private types. If everything sits in one package, package-private collapses into "visible to the whole app," and Episode Eleven's careful ladder loses a rung.

That directory rule is the one that burns beginners. The package declaration must match the directory tree. If the file says `com.shop.order` but sits in `com/shop/orders` or directly under `src`, tools will fail to resolve types, or you will compile one layout and run another. Build tools like Maven and Gradle assume this layout; fighting it means fighting every tutorial and every teammate's muscle memory.

Once packages exist, you choose how to name foreign types: import the short name, or write the fully qualified name at the use site.

```java
com.shop.user.User u = new com.shop.user.User("ada");
// or
import com.shop.user.User;
User u = new User("ada");
```

Fully qualified names are clear when two types share a simple name — `java.util.Date` versus `java.sql.Date`. Imports keep ordinary code readable. Star imports — `import com.shop.user.*;` — hide dependencies. A reader cannot see which types you actually use, and a new class added to that package can create ambiguous references later. Prefer explicit imports; let the IDE manage the list.

What if the project ignores packaging discipline? Giant catch-all packages appear — `com.shop.util`, `com.shop.misc` — where everything is package-private friends with everything else. Access modifiers stop meaning "module interior." Folder structure drifts from declarations. Onboarding becomes archaeology.

A healthier shape groups types that change together and hide together:

```java
package com.shop.order;

class OrderLine {             // package-private type
    private final String sku;
    private final int qty;

    OrderLine(String sku, int qty) {
        this.sku = sku;
        this.qty = qty;
    }
}

public class Order {          // public seam
    private final java.util.List<OrderLine> lines = new java.util.ArrayList<>();

    public void add(String sku, int qty) {
        lines.add(new OrderLine(sku, qty));
    }
}
```

Outside `com.shop.order`, callers see `Order` and its public methods. They do not see `OrderLine`. That split is packages doing product work — the same access ideas from Episode Eleven, now with neighborhoods that make those ideas enforceable.

Access control needed neighborhoods. Packages provide namespaces, map them to directories, and give imports a way to name foreign types. Combined with modifiers, packages become boundaries — and catch-all packages dissolve those boundaries again.

Once types are organized, another modeling need shows up for values that are not free-form strings but a known set of named constants — order status, ticket priority, direction of a move. You can fake that with magic ints and string literals, and then every typo becomes a runtime surprise the compiler never saw.

That pressure leads to enums.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 12 (*Packages*).

Narration technique: colliding-names / neighborhood situation → reverse-DNS packages → directory match → import vs FQN → star-import cost → packages + access boundaries → next natural problem (fixed constant sets / enums). Continuity-checked transitions.
