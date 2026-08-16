# AGENTS.md

## Cursor Cloud specific instructions

### What this repository is
This is a **documentation-only repository**. It contains no application code, build
system, package manifest, tests, or services. The tracked content is:

- `README.md` — one-line title.
- `java-episode-01-production-bible.md` — the production script/"bible" for Episode 1
  of a YouTube documentary series ("The Java Story"): narration, storyboard, animation
  and audio direction, code-animation spec, captions, and YouTube metadata.

### Dependencies / setup
- There is **nothing to install or build**. The update script is effectively a no-op.
- The base VM already provides everything used to exercise the repo's subject matter:
  OpenJDK 21 (`java`/`javac`), Node 22 (`node`/`npx`), Python 3.12, and git. Do not add
  a package manager or build tooling to this repo unless a task explicitly asks for it.

### "Running" the content
- There is no service to start. The only executable artifact described anywhere is the
  Java `HelloWorld` program taught in the bible (Scenes 18–20). To reproduce the on-screen
  demo, write that snippet to a scratch dir (keep the repo unmodified) and run:
  `javac HelloWorld.java && java HelloWorld` → prints `Hello, World!`.

### Lint / test / build
- No repo-defined lint, test, or build commands exist.
- For authoring hygiene you can lint the Markdown with
  `npx --yes markdownlint-cli2 "*.md"`. Note: the bible currently reports pre-existing
  style warnings (line length, table spacing, multiple H1s). These are intentional
  content-formatting choices — do not "fix" them unless a task explicitly requests it,
  since editing the production content is normally out of scope.
