# Rename GitHub repository (required)

**Current:** https://github.com/ankur0001/Curser  
**Target:** https://github.com/ankur0001/all-work

The Cloud Agent **cannot** rename your GitHub repo automatically. GitHub returns `403 Resource not accessible by integration` — only you (repo owner) can rename it in Settings.

---

## Steps on GitHub (2 minutes)

1. Open **https://github.com/ankur0001/Curser/settings**
2. Under **General → Repository name**, replace `Curser` with:

   **`all-work`**

   Other realistic names if you prefer:
   - `professional-work`
   - `career-hub`
   - `ankur-work`

3. **Description (optional):**
   `Personal professional work hub — career assets, freelance profiles, and project resources`

4. Click **Rename**

5. Confirm — old links like `github.com/ankur0001/Curser` will redirect to `all-work`.

---

## After you rename — update git remote

On any machine where you clone this repo:

```bash
git remote set-url origin https://github.com/ankur0001/all-work.git
git remote -v
```

For SSH:

```bash
git remote set-url origin git@github.com:ankur0001/all-work.git
```

---

## What this does NOT change

- Folder `all-work/` inside the repo is separate from the **repository name** on GitHub.
- Repo name = `ankur0001/all-work` on GitHub.
- Folder = `all-work/` directory holding freelance-profile files.

Both use the same name for consistency.

---

## Tell the agent

Reply **"Repo renamed to all-work"** after you complete the GitHub Settings step.
