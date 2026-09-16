# Episode 11 — Access Modifiers

**Cut:** v1 (original)

## Transcript (from captions)

Objects need boundaries. Access modifiers draw those lines. Who can see this field? Who can call this method? Visibility is ownership encoded in syntax. Today we map private, package-private, protected, and public.

Visibility is a design decision — not an afterthought. Episode Eleven. Access Modifiers — private, public, protected, package-private. Four levels. Narrow to wide. private — only this class.

No modifier — package-private — same package only. protected — package plus subclasses. public — anyone. A promise. Use it carefully. Default to the narrowest visibility that still works.

Widen only when a real collaborator needs access. private is your first encapsulation tool. Fields start private unless you have a reason. Helpers that are not part of the API stay private too.

If everything is public, you have no boundary — only hope. Hope is not an architecture. Start private. Widen only with intent. Package-private is underrated. Same package collaboration without publishing an API.

Great for internal helpers shared by a few types. When a type must leave the package — promote visibility intentionally. Accidental public is how APIs grow barnacles. Package-private keeps the neighborhood tidy.

protected supports inheritance-aware extension. Subclasses can reach it — so can the same package. public is the stable contract. Every public method is a promise to maintain. In libraries, public surface area is a long-term cost.

Architect tip — treat public like a published product. Every public method is a maintenance promise. Three common mistakes. One — public fields for convenience. Encapsulation dies quietly.

Two — making every helper public just in case. Three — protected used as a lazy public for subclasses everywhere. Also — widening visibility to fix a test instead of redesigning. Fix the design — do not dissolve the boundary.

Interview question — default access versus private? Default — package-private — same package sees it. private — only the declaring class. Then — prefer narrowest visibility. Public is a contract.

That answer shows API discipline. Visibility choices are architecture in miniature. Visibility needs a home. Next — packages. Episode Twelve — packages. Namespaces, boundaries, and ownership on disk.

See you there.
