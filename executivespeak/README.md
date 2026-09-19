# ExecutiveSpeak

**AI Communication Coach for Software Engineers** — speak-first coaching for workplace English, leadership communication, technical explanations, and executive presence.

## Quick start (demo mode)

Demo mode works **without PostgreSQL or API keys**.

```bash
cd executivespeak
cp .env.example .env
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) → **Try demo** → sign in with:

- Email: `demo@executivespeak.app`
- Password: `demo1234`

## Production setup

1. Start PostgreSQL (example):

```bash
docker compose up -d
```

2. Configure `.env`:

- `DEMO_MODE=false`
- `DATABASE_URL=postgresql://executivespeak:executivespeak@localhost:5432/executivespeak`
- `NEXTAUTH_SECRET=` (long random string)
- Optional: `AI_PROVIDER=openai` and `OPENAI_API_KEY`

3. Migrate and seed:

```bash
npm run db:generate
npm run db:migrate
npm run db:seed
```

4. Run:

```bash
npm run build && npm start
```

## Environment variables

See [`.env.example`](./.env.example).

| Variable | Purpose |
|----------|---------|
| `DEMO_MODE` | When `true`, uses in-memory profile + mock AI |
| `DATABASE_URL` | PostgreSQL connection string |
| `NEXTAUTH_URL` / `NEXTAUTH_SECRET` | Auth.js session security |
| `AI_PROVIDER` | `mock` (default) or `openai` |
| `OPENAI_API_KEY` | Required for live LLM analysis |
| `SPEECH_TO_TEXT_PROVIDER` | `browser` (Web Speech API in client) |
| `TEXT_TO_SPEECH_PROVIDER` | `browser` (Speech Synthesis) |

## Architecture

- **Frontend:** Next.js 15 App Router, React 19, Tailwind CSS 4, Radix/shadcn-style components
- **Backend:** Next.js Route Handlers
- **Database:** PostgreSQL + Prisma 7
- **Auth:** NextAuth credentials (+ demo user)
- **AI / Speech:** Provider interfaces in `src/lib/providers/` with mock implementations

Documentation:

- [Architecture](./docs/architecture.md)
- [API](./docs/api.md)
- [AI prompts](./docs/ai-prompts.md)

## Testing

```bash
npm test
```

## Demo vs production

| Feature | Demo mode | Production |
|---------|-----------|------------|
| Sign-in | Demo credentials | Registered users + DB |
| AI analysis | Mock coach JSON | OpenAI (if configured) |
| Speech input | Browser mic / typed text | Same |
| Progress storage | In-memory demo store | PostgreSQL |
| Registration | Disabled | Enabled with DB |

## MVP scope (Phase 1)

Implemented: authentication, onboarding, baseline assessment, dashboard, voice conversation UI, STT (browser), mock/live AI feedback, daily practice plan, session history, progress views, phrase library, module scaffolds.

### Phase 2 (implemented)

- Meeting simulator with multi-participant scripts and response evaluation
- Impromptu speaking (15s think → 30/60/90s speak)
- Email & chat coach (Slack/email/Teams/Jira/PR)
- Vocabulary engine with spaced repetition (demo store)
- Grammar memory drills from recurring mistakes
- Daily leadership challenges + achievements
- Weekly assessment trends (from real session data)

Phase 3+: monthly executive assessment day, advanced pronunciation API, meeting multi-agent AI, full DB-backed SRS.

## License

Private / project use — adjust for your deployment.
