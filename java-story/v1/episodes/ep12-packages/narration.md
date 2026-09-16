# Episode 12 — Packages

**Cut:** v1 (original)

## Transcript (from captions)

Access needs a neighborhood. Packages are those neighborhoods. A package is a namespace — and a boundary. It prevents name collisions and shapes who collaborates. On disk and at runtime, package plus class name is identity.

Treat package structure as architecture you can see. Folders tell the truth about ownership — or they should. Episode Twelve. Packages — namespaces, boundaries, and ownership. package com.acme.orders.domain; That line is not decoration — it is part of the binary name.

com.acme.OrderService is not the same as com.other.OrderService. Folders should match the package declaration. Java expects that. Break the mapping and tools get angry fast. Folder path and package declaration must agree.

Packages define package-private visibility. Types in the same package can collaborate quietly. Types outside must use the public API — if you designed one. Good packages make invalid dependencies hard to introduce.

Bad packages — one giant folder — erase ownership. Boundaries only work if the tree reflects them. Organize by capability when you can. api. application. domain. infrastructure. Or by feature — orders, payments, shipping — when teams own features.

Layered-only packages can become anemic and tangled. Pick a structure that mirrors how people own the code. Feature teams and domain packages often fit better than pure layers. Spring Boot tip — scanning starts from the main class package downward.

Put OrdersApplication at a sensible root. Bury it too deep and beans disappear mysteriously. Packages are not only organization — frameworks navigate them. Design the root on purpose.

A wrong root creates mysterious missing beans. Three common mistakes. One — every class in one package called util or common. Two — cyclic dependencies between packages — architecture spaghetti.

Three — main class buried so component scanning misses half the app. Also — package names that lie about contents. Honest names reduce wrong imports and wrong ownership. Interview question — why do packages matter?

Namespace uniqueness. Access boundaries. Ownership. Framework scanning. Runtime identity is package plus class name — plus classloader later. Good structure makes illegal dependencies awkward.

That is architecture you can feel in the folder tree. Boundaries are set. Next — fixed sets of constants with behavior. Episode Thirteen — enums. Type-safe states instead of magic strings.

See you there.
