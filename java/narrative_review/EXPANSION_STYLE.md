# Narration technique (quality benchmark)

Use **EP01, EP04, and EP07** as the **narrative quality benchmark**, but do not mechanically copy their sentence patterns, paragraph structures, analogies, or transition phrases.

Extract the underlying teaching technique.

**Approved direction:** make every episode as narratively coherent and example-driven as EP01/04/07, while preserving each episode's own natural flow.

Do **not** ask for "more descriptive" content. Descriptive expansion is already solved. The missing quality is continuous spoken-lesson coherence.

---

## The goal

The goal is not for every episode to sound identical.

The goal is for every episode to have the same level of:

* narrative continuity
* descriptive explanation
* conceptual depth
* practical examples
* code walkthrough
* natural questions
* cause-and-effect reasoning
* learner-oriented explanation

---

## How concepts appear

Every new concept should feel like it became necessary because of something the learner just encountered.

Do not introduce a concept merely because it is the next item in the syllabus.

Create a natural reason for the learner to need it.

The instructor should:

1. Establish a situation
2. Make the learner notice a problem
3. Ask the question that naturally follows
4. Introduce the Java concept as the answer
5. Use examples as part of that reasoning — not pasted after the explanation

The learner should never feel that the instructor switched topics because the syllabus said it was time.

---

## Examples and code

Examples must be integrated into the explanation. Do not append an example after a definition simply to satisfy an "example required" rule.

Code must be introduced with context, explained after it is shown, and connected back to the problem that caused us to write it.

Preferred flow:

**Narrative → explanation → example → code → walkthrough → learner question → deeper explanation → connection → next problem**

Interview checkpoints and practice drills are optional and secondary. Do not interrupt the lesson just to include them.

---

## Depth and pacing

When a concept is complex, slow down and explain it progressively rather than compressing several definitions into one paragraph.

Avoid excessive technical detail when it is not necessary for the current learning objective. If a detail belongs to a later concept, create curiosity and defer the deep explanation rather than dumping it into the current episode.

Runtime guidance: floor **4 minutes**, soft aim **~10–12**, ceiling **15**. Do not pad with syllabus dumps or bolted-on drills.

---

## Descriptive content ≠ narrative content

Adding more sentences, definitions, examples, interview questions, or code does **not** automatically make the narration better.

The narration must have a **continuous chain of thought**.

Every concept should emerge naturally from the previous discussion.

---

## Continuity check (required before finalizing)

Read the episode beginning to end. At every topic change, verify there is a reason for the learner to move forward.

The transition must answer:

> Given what we just learned, what problem or question would naturally make the learner want to learn this next?

If the next concept appears only because it is next in the syllabus, rewrite the transition.

---

## Most important

**The learner should feel that the instructor is thinking through the problem with them, not reading a list of Java facts to them.**

### Final test

> If I remove the headings, does this still sound like one person naturally teaching the learner for 10 minutes?

If yes, the narration is working.

If it sounds like several documentation sections joined together, rewrite it.

---

## Gold standards (approved)

* `episodes/ep01_why-java-exists-introduction-to-java.md` — approve with minor refinement
* `episodes/ep04_variables-and-data-types.md` — approved
* `episodes/ep07_methods.md` — approved
* Narrative methodology — approved

Apply the **technique** (not wording) across EP01–EP85.
