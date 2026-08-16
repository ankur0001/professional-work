# Episode 11 — Access Modifiers

| Field | Value |
|---|---|
| Episode | 11 |
| Title | Access Modifiers |
| Catalog handbook column | 11 |
| Narration source script | `make_episode_11.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Objects need boundaries. Access modifiers draw those lines.
2. Who can see this field? Who can call this method?
3. Visibility is ownership encoded in syntax.
4. Today we map private, package-private, protected, and public.
5. Visibility is a design decision — not an afterthought.

### Scene `title` (renderer: `title`)

1. Episode Eleven.
2. Access Modifiers — private, public, protected, package-private.

### Scene `levels` (renderer: `levels`)

1. Four levels. Narrow to wide.
2. private — only this class.
3. No modifier — package-private — same package only.
4. protected — package plus subclasses.
5. public — anyone. A promise. Use it carefully.
6. Default to the narrowest visibility that still works.
7. Widen only when a real collaborator needs access.

### Scene `private` (renderer: `private`)

1. private is your first encapsulation tool.
2. Fields start private unless you have a reason.
3. Helpers that are not part of the API stay private too.
4. If everything is public, you have no boundary — only hope.
5. Hope is not an architecture.
6. Start private. Widen only with intent.

### Scene `package` (renderer: `package`)

1. Package-private is underrated.
2. Same package collaboration without publishing an API.
3. Great for internal helpers shared by a few types.
4. When a type must leave the package — promote visibility intentionally.
5. Accidental public is how APIs grow barnacles.
6. Package-private keeps the neighborhood tidy.

### Scene `protected_public` (renderer: `protected_public`)

1. protected supports inheritance-aware extension.
2. Subclasses can reach it — so can the same package.
3. public is the stable contract. Every public method is a promise to maintain.
4. In libraries, public surface area is a long-term cost.
5. Architect tip — treat public like a published product.
6. Every public method is a maintenance promise.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — public fields for convenience. Encapsulation dies quietly.
3. Two — making every helper public just in case.
4. Three — protected used as a lazy public for subclasses everywhere.
5. Also — widening visibility to fix a test instead of redesigning.
6. Fix the design — do not dissolve the boundary.

### Scene `interview` (renderer: `interview`)

1. Interview question — default access versus private?
2. Default — package-private — same package sees it.
3. private — only the declaring class.
4. Then — prefer narrowest visibility. Public is a contract.
5. That answer shows API discipline.
6. Visibility choices are architecture in miniature.

### Scene `teaser` (renderer: `teaser`)

1. Visibility needs a home. Next — packages.
2. Episode Twelve — packages.
3. Namespaces, boundaries, and ownership on disk.
4. See you there.

_Total beats: **48** across **9** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **11** — *Access Modifiers*.
- **Series catalog:** Episode 11 ↔ handbook lesson 11 — *Access Modifiers*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

### Handbook concepts reused (from recovered Lesson 11 excerpt)

- Concept: Access modifiers define visibility boundaries for classes, constructors, fields, and methods. Java uses them to encode ownership: private for implementation detail, package-private for module-internal collaboration, protected for inheritance-aware ext

Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` (Lesson 11).

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Objects need boundaries. Access modifiers draw those lines._
- **`title`** — starts from: _Episode Eleven._
- **`levels`** — starts from: _Four levels. Narrow to wide._
- **`private`** — starts from: _private is your first encapsulation tool._
- **`package`** — starts from: _Package-private is underrated._
- **`protected_public`** — starts from: _protected supports inheritance-aware extension._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — default access versus private?_
- **`teaser`** — starts from: _Visibility needs a home. Next — packages._
