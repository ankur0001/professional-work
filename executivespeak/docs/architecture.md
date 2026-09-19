# Architecture

## Product loop

1. Scenario prompt → user speaks (mic or typed fallback)
2. STT transcript → `POST /api/analyze` → validated JSON feedback
3. Coach shows Natural / Professional / Leadership phrasing
4. User must repeat improved phrasing when `mustRepeatPhrase` is set
5. Session end → `POST /api/sessions` → summary + weakness profile update

## Layers

```
app/                 # Routes & UI
components/          # Speaking session, shell, UI primitives
lib/
  providers/         # AIProvider, STT/TTS/Pronunciation abstractions
  prompts/           # System prompts (not inlined in components)
  schemas/           # Zod validation for AI JSON
  demo/              # In-memory store when DEMO_MODE=true
  data/              # Scenarios, phrases, personalities
prisma/              # PostgreSQL schema
```

## Personalization

`UserProfile.weaknessProfile` (JSON) merges grammar/filler patterns after each session via `mergeWeaknessProfile`.

Levels derive from demonstrated scores (`levelFromScores`) — not from time spent alone.

## Privacy

Audio is processed client-side for Web Speech API; server receives text transcripts only in MVP.
