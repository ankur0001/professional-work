# Episode 03 — Java Program Structure

| Field | Value |
|---|---|
| Episode | 03 |
| Title | Java Program Structure |
| Catalog handbook column | 3 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Two ended on a frustration that arrives the moment the tools work. You write a class, name a file, maybe add a package — and the compiler or the launcher refuses until those pieces agree with each other.

That refusal is not Java being petty. It is Java answering a practical question: when you type `java Something`, how does the runtime find the right bytecode, and when you type `javac`, how does the compiler know what belongs together?

Start with the smallest piece: a single source file.

A `.java` file is a compilation unit. The rule that trips almost everyone first is this: if a top-level class is `public`, its name must match the filename, including case. `App` lives in `App.java`. Not `app.java`. Not `Application.java`. Filenames are how tools locate the public type you asked them to compile.

```java
public class App {
    public static void main(String[] args) {
        System.out.println("ready");
    }
}
```

Save that as `App.java`, compile it, run it. Now rename the file to `Demo.java` without renaming the class and compile again. The error is teaching you the contract: public top-level type and filename are one identity.

But a real project is not one lonely class in the current folder. Names collide. Two teams invent `User`. Two libraries invent `Util`. So the next natural question is: how do we give types an address so the same short name can exist in different places without chaos?

Packages are that address. A package is a namespace, and on disk it maps to directories. `package com.example.demo;` is not a comment. It claims that this type lives under folders that mirror those segments. If the declaration says `com.example.demo` and the file sits in the wrong tree, the tools lose the trail.

```java
package com.example.demo;

public class App {
    public static void main(String[] args) {
        System.out.println("args length = " + args.length);
    }
}
```

Walk the pieces. The package line places `App` in `com.example.demo`. The public class still matches `App.java`. Inside it, `public static void main(String[] args)` is the classic launcher entry point — the door the JVM knocks on. `args` is how command-line words arrive. Printing `args.length` is a tiny proof that the entry point was found and executed.

Once types live in packages, how does one file talk about a type from another package without writing the full address every time?

Imports bring types into scope. An import does not copy code into your file. It tells the compiler which fully qualified name you mean when you write the short name. Behind that sits the classpath — and later the module path — which tells the tools where to look for already-compiled classes. If the type is not on that path, the import cannot save you.

```java
package com.example.demo;

import java.util.ArrayList;

public class App {
    public static void main(String[] args) {
        ArrayList<String> names = new ArrayList<>();
        names.add("Ada");
        System.out.println(names);
    }
}
```

`import java.util.ArrayList;` means: when I say `ArrayList`, I mean that type from the standard library. Without the import, you could still write `java.util.ArrayList` in full. The import is convenience with a clear cost — you are declaring a dependency on a specific type.

These rules feel expensive until you need them. A public class that does not match its filename stops at compile time — cheaper than a runtime hunt. A package that does not match its folders may compile in one layout and fail to launch from another. Assuming the working directory alone finds classes works for tiny demos, then a second jar appears and "it worked on my machine" becomes a classpath story. Structure is how tools search. If the search path is wrong, perfect source still fails at launch.

Episode Two named the layers that build and run bytecode. Today we answered why those layers care so much about agreement: a compilation unit binds public type to filename, packages bind names to directories, `main` is the launcher door, and imports plus classpath tell the tools which types you mean and where they live.

Once a program has a home and an entry point, a more basic need appears. Before the program can do useful work, it must remember information — an age, a name, a flag — with meaning attached, not as anonymous literals scattered through `main`.

That need is what variables and data types exist to solve.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 3 (*Java Program Structure*).

Narration technique: structural-stubbornness situation → filename/public-class contract → packages as addresses → main as entry → imports/classpath → mismatch failures → next natural problem (remembering values). Continuity-checked transitions.
