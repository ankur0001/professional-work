# AI prompt modules

Prompts live under `src/lib/prompts/` — not in React components.

| Module | Purpose |
|--------|---------|
| `conversation-coach.ts` | Speech analysis JSON + coaching tone |
| `assessment-coach.ts` | Baseline + session summary JSON |
| `leadershipCoachSystem` | Leadership scenarios (Phase 2 simulators) |
| `technicalCoachSystem` | Audience-aware technical explanations |

OpenAI provider sends these system prompts with `response_format: json_object` and validates responses with Zod schemas in `src/lib/schemas/feedback.ts`.

Mock provider implements the same JSON contract for demo mode and tests.
