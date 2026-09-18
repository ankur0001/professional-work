# Narration technique (Spring Story)

Use **EP01, EP04, and EP17** as the **narrative quality benchmark**, but do **not** copy their sentence patterns, analogies, or transition phrases.

The gold standard is **natural, topic-specific, example-driven teaching** — not a shared outline with the topic name swapped in.

---

## Final tests (required)

1. Remove the headings. Read the episode aloud.  
   Does it sound like an experienced Spring instructor teaching **this** concept, or like a template with a different topic inserted?

2. Replace the topic name with another Spring concept.  
   Would most of the narration still work? If **yes**, rewrite — it is too generic.

3. Delete the code sample.  
   Does the surrounding story still mention runtime details that only make sense for **this** mechanism? If not, the example is ornamental.

---

## What every episode must determine

1. What real application situation makes **this exact** Spring mechanism necessary?
2. What goes wrong or becomes difficult without it?
3. What question would an engineer naturally ask at that moment?
4. How does Spring solve **that** specific problem?
5. What concrete example demonstrates it (domain chosen for this episode — see `SCENARIO_MAP.md`)?
6. What Java/Spring (or YAML/PromQL/HTTP) artifact demonstrates it?
7. What happens when that artifact runs?
8. What misconception is most likely for **this** concept?
9. What new problem naturally leads to the next episode?

---

## Anti-template rules

**Forbidden as a recurring skeleton** (occasional natural use of similar English is fine; cloning the same spine across episodes is not):

* "Here is the pain this lesson exists to remove."
* "So the natural question becomes..."
* "At a practical level..."
* "Spring's design choice is deliberate."
* "Once you accept the feature..."
* "As you practice..."
* "A common misunderstanding is to memorize..."
* "Today we walked through..."
* "The next natural question is waiting in Episode N — Title."
* Identical "Narration technique: situation → problem → ..." footers on every file

**Do not** end with a mechanical episode announcement. Create an unresolved engineering problem instead.

**Do not** reuse OrderService / CheckoutService / generic DI examples unless the episode *is* about DI and `SCENARIO_MAP.md` assigns that domain.

**Do** vary openings (incident, failing test, PR review, debugger, cold-start log, pager) so consecutive episodes do not sound the same.

---

## Examples must be topic-specific

| Concept | Example must show |
|---|---|
| DispatcherServlet | HTTP request → mapping → adapter → controller → response |
| @Transactional | Multi-step DB work + rollback boundary |
| Authentication | Request with credentials/token → SecurityContext |
| JUnit 5 | Real test discovery, execution, reporting |
| JPA / N+1 | Entity/repository/SQL — not bean wiring |
| Feign | Declarative HTTP client interface to a named service |

If you could paste the same `OrderService` constructor-injection snippet into five different episodes, none of them is done.

---

## Depth and pacing

Runtime guidance: floor **~4 minutes**, soft aim **~8–12**, ceiling **~15**.

Complex topics: spend time on runtime behavior, failure modes, and trade-offs.  
Simple topics: stay concise.  
**Never pad** to hit a word count — but never ship a definition stub either.

---

## Continuity

The beginning should connect to what the learner already knows.  
The ending should create a genuine problem that makes the next episode necessary.

---

## Goal

Same *level* of continuity, depth, integrated examples, code walkthrough, and cause-and-effect reasoning as EP01 / EP04 / EP17 — **not** the same sound.
