# API

All authenticated routes require a NextAuth session cookie.

## `GET /api/config`

Public. Returns `{ demoMode, aiProvider, sttProvider, ttsProvider }`.

## `GET/PATCH /api/profile`

User coaching profile. PATCH accepts onboarding fields and `communicationScores`.

## `POST /api/analyze`

Body:

```json
{
  "transcript": "string",
  "scenario": "string",
  "personality": "executive_coach",
  "mustEvaluateRepeat": "optional leadership phrase"
}
```

Returns `FeedbackAnalysis` JSON (Zod-validated).

## `POST /api/baseline`

Body: `{ "transcripts": ["..."] }` → baseline dimension scores.

## `GET/POST /api/sessions`

GET: recent sessions. POST: finalize session with transcripts + analyses → summary.

## `POST /api/auth/register`

Disabled when `DEMO_MODE=true`. Creates user + profile in PostgreSQL.

## `GET/POST /api/auth/[...nextauth]`

NextAuth handlers.
