# Handbook Recovery Notes

## Summary

- Handbook-authoritative titles: **36 / 80**
- Lessons with body excerpts: **12** → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
- Series catalog titles available: **80 / 80** (remapped; see divergences)
- Missing handbook titles: 44 → [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 54, 55, 58, 59, 63, 64, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]

### Largest excerpts

- Lesson 3 (Java Program Structure): **22213** chars
- Lesson 5 (Operators): **12503** chars
- Lesson 4 (Variables and Data Types): **11538** chars
- Lesson 1 (Introduction to Java): **4762** chars
- Lesson 2 (JDK, JRE, and JVM): **4146** chars
- Lesson 6 (Control Flow): **4126** chars
- Lesson 9 (Strings): **890** chars
- Lesson 12 (Packages): **621** chars
- Lesson 10 (Object-Oriented Programming): **587** chars
- Lesson 8 (Arrays): **535** chars
- Lesson 7 (Methods): **526** chars
- Lesson 11 (Access Modifiers): **364** chars

## Recovered vs missing

### Recovered handbook titles

- 1. Introduction to Java (`h3@msg347`)
- 2. JDK, JRE, and JVM (`nav@msg347`)
- 3. Java Program Structure (`LESSONS-dump@msg350`)
- 4. Variables and Data Types (`LESSONS-dump@msg350`)
- 5. Operators (`LESSONS-dump@msg350`)
- 6. Control Flow (`LESSONS-dump@msg350`)
- 7. Methods (`LESSONS-dump@msg350`)
- 8. Arrays (`LESSONS-dump@msg350`)
- 9. Strings (`LESSONS-dump@msg350`)
- 10. Object-Oriented Programming (`LESSONS-dump@msg350`)
- 11. Access Modifiers (`LESSONS-dump@msg350`)
- 12. Packages (`LESSONS-dump@msg350`)
- 13. Enums (`LESSONS-dump@msg350`)
- 14. Wrappers and Autoboxing (`LESSONS-dump@msg350`)
- 15. Generics (`LESSONS-dump@msg350`)
- 16. Annotations (`LESSONS-dump@msg350`)
- 17. Reflection (`LESSONS-dump@msg350`)
- 18. Records (`LESSONS-dump@msg350`)
- 19. Sealed Classes (`nav@msg347`)
- 20. Modules and JPMS (`LESSONS-dump@msg350`)
- 21. Collection Framework Overview (`LESSONS-dump@msg350`)
- 22. List (`LESSONS-dump@msg350`)
- 23. Set (`LESSONS-dump@msg350`)
- 24. Queue & Deque (`LESSONS-dump@msg350`)
- 25. Map (`LESSONS-dump@msg350`)
- 48. Atomic Classes (`nav@msg347`)
- 56. Class Loading (`nav@msg347`)
- 57. Bytecode (`nav@msg347`)
- 60. JVM Memory Areas (`nav@msg347`)
- 61. Heap (`nav@msg347`)
- 62. Stack (`nav@msg347`)
- 65. GC Algorithms (`nav@msg347`)
- 66. G1GC (`nav@msg347`)
- 67. ZGC & Shenandoah (`nav@msg347`)
- 68. JVM Tuning (`nav@msg347`)
- 70. JVM Troubleshooting (`nav@msg347`)

### Missing handbook titles

Never printed in tool output. Msg 350 only dumped `titles[:25]` then ellipsis; msg 347 grepped a sparse nav subset.
Missing: [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 54, 55, 58, 59, 63, 64, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]

## Source artifacts in transcript

| Msg | Content |
|---:|---|
| 345 | Handbook HTML head/CSS (`read_file`) |
| 347 | Partial nav + Phase 1/6 + Lesson 1 header |
| 350 | `LESSONS 80` + titles 1–25 |
| 353 | Lesson 2 HTML + cleaned paragraph bullets |
| 588 | HTML articles for lessons 2–4 (and fragments) |
| 590 | Cleaned Lesson 3 parts; byte offsets into L30–39 |
| 593 | Large Lesson 3 dump (~22k) |
| 657 | Lesson 4 dump (~11k) |
| 686 | Lesson 5 dump (~12k) |
| 717 | Lesson 6 part text |
| 744 | Lessons 7–9 Concept/Mistakes |
| 814 | Lessons 10–12 Concept snippets |

## Not recoverable here

- Original HTML upload file (deleted; not in git)
- Full bodies for lessons ≥13
- Handbook titles for most of 26–80 (except sparse nav hits: 48,56,57,60–62,65–68,70)
- Complete phase map beyond Phase 1 and Phase 6 names

## Method

Loaded transcript JSON as structured messages (~5.1MB), then extracted `tool_result` outputs without regex-scanning the file as one undifferentiated string for content assembly.
Ripgrep used for discovery; Python used for precise extraction and file writing.
