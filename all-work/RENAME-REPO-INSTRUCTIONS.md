# Repository rename: Curser → all-work

The agent reorganized files under `all-work/` but **could not rename the GitHub repo** (API 403 — integration lacks admin permission).

## You need to do this manually (2 minutes)

1. Go to: https://github.com/ankur0001/Curser/settings
2. **Repository name:** `all-work`
3. **Description (optional):** `Personal work hub — freelance profiles, career assets, project resources`
4. Click **Rename**

GitHub will redirect `ankur0001/Curser` → `ankur0001/all-work`.

## After rename — update local remote

```bash
git remote set-url origin https://github.com/ankur0001/all-work.git
git remote -v
```

## What was reorganized

All conversation files moved from repo root:

```
freelance-profile/   →   all-work/freelance-profile/
```

Nothing was deleted — only folder structure changed.
