# Descriptive narration style (required)

The narration must be **descriptive and explanatory**, not a sequence of short statements.

Do not assume that mentioning a concept means the learner understands it.

## For every important concept

1. Introduce the idea in a natural context.
2. Explain **why we need it**.
3. Explain the idea in simple language.
4. Give a relatable real-world example or analogy when it genuinely helps.
5. Show a Java example.
6. Walk through the example and explain what is happening.
7. Explain the result or behavior.
8. Point out an important detail or common misunderstanding.
9. Connect the concept back to the previous discussion.
10. Naturally lead into the next concept.

The learner should think: *"I understand why this exists, how it works, and where I would use it."*

## Pattern for examples

**Concept → Situation → Example → Code → Explanation → Variation**

Examples evolve with the explanation. Do not dump code at the end.

For hard concepts, use:

- **Example 1 — Simple**
- **Example 2 — Practical**
- **Example 3 — Edge case / common mistake** (only when it teaches something)

Never place a code block without explaining why it is there and what each important line does.

## Preferred depth

**Introduce → Explain → Illustrate → Code → Walk Through → Question → Extend → Connect**

Do not rush. If the source has five related statements, turn them into one coherent explanation with context, examples, and transitions.

## Voice

Write like an experienced instructor sitting beside the learner:

> Let's start with a problem. Here's what we have. Notice where it gets difficult. Here's why. Here's how Java helps. Let's write code. Let's understand exactly what that code is doing. Now here's the next challenge...

## Runtime

- Floor **4 minutes**, soft aim **8–12**, ceiling **15**
- Prefer continuous prose paragraphs under scene headings (not telegram-style one-liners)
- Numbered beats are allowed only when each item is a full spoken sentence or short paragraph

## Forbidden

- Definition dumps: "X is Y. Java supports Z. `int` stores integers."
- Code with no walkthrough
- Analogy paragraphs that never return to Java
- Padding that does not teach
