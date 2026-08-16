# Laptop setup — professional-work

Use this guide to set up **https://github.com/ankur0001/professional-work** on your personal laptop (Windows, Mac, or Linux).

---

## 1. Prerequisites

Install if you don’t have them:

| Tool | Why | Install |
|------|-----|---------|
| **Git** | Clone and pull updates | https://git-scm.com/downloads |
| **Browser** | LinkedIn, Upwork, GitHub | Chrome / Edge / Firefox |
| **Optional: VS Code / Cursor** | Edit portfolio HTML, read markdown | https://cursor.com or https://code.visualstudio.com |

You do **not** need Java, Docker, or Node for the profile grooming files — they are markdown and HTML only.

---

## 2. Clone the repository

Open **Terminal** (Mac/Linux) or **PowerShell** (Windows):

```bash
cd ~/Documents   # or any folder you prefer
git clone https://github.com/ankur0001/professional-work.git
cd professional-work
```

If you already cloned the old name (`Curser`), update the remote:

```bash
cd Curser   # your existing folder
git remote set-url origin https://github.com/ankur0001/professional-work.git
git pull origin main
```

---

## 3. What to open on your laptop

| Goal | Open this file |
|------|----------------|
| **LinkedIn + Upwork copy (ready)** | `all-work/freelance-profile/10-ANKUR-KUMAR-PROFILE-PACK.md` |
| Full LinkedIn sections | `all-work/freelance-profile/02-linkedin-profile.md` |
| Upwork bio + portfolio entries | `all-work/freelance-profile/03-upwork-profile.md` |
| freelancermap / Truelancer | `all-work/freelance-profile/04-freelancermap-truelancer.md` |
| Portfolio website (HTML) | `all-work/freelance-profile/portfolio/index.html` |
| Checklist | `all-work/freelance-profile/01-profile-audit-checklist.md` |

**Tip:** Open the folder in Cursor/VS Code for easy preview:

```bash
cursor professional-work
# or
code professional-work
```

---

## 4. Update profiles on your laptop (order)

Do this in your **local browser** — no Cloud Agent needed.

### Step A — LinkedIn (~15 min)

1. Go to https://www.linkedin.com/in/ankur-kumar-4801078a/
2. Click **Edit** (intro section)
3. Copy **headline** and **About** from `10-ANKUR-KUMAR-PROFILE-PACK.md`
4. Paste into LinkedIn → **Save**
5. **Me → Open to work** → enable **Contract / Freelance**
6. Post the “open to contract” text from the same file (optional)

### Step B — Upwork (~20 min)

1. Create or log in at https://www.upwork.com
2. **Settings → My Profile**
3. Paste title + overview from `03-upwork-profile.md` or the profile pack
4. Add 3 portfolio entries (templates in `03-upwork-profile.md`)
5. Set hourly rate and availability
6. Complete ID verification

### Step C — GitHub profile (~10 min)

1. Log in at https://github.com/ankur0001
2. Create repo `ankur0001` (same as username) if you want a profile README
3. Copy README from `05-github-portfolio.md` → save as `README.md` in that repo

### Step D — Portfolio site (optional, ~15 min)

**Option 1 — GitHub Pages (recommended)**

1. On GitHub: **professional-work** → **Settings** → **Pages**
2. Source: **Deploy from branch** → branch `main`
3. Folder: `/all-work/freelance-profile/portfolio` (or copy `index.html` to `/docs` if Pages only allows root/docs)
4. Your site: `https://ankur0001.github.io/professional-work/` (path may vary)

**Option 2 — Open locally**

Double-click `all-work/freelance-profile/portfolio/index.html` in your browser.

---

## 5. Keep repo updated

When the agent adds new files:

```bash
cd professional-work
git pull origin main
```

---

## 6. Folder map

```
professional-work/
├── README.md
├── all-work/
│   ├── README.md
│   └── freelance-profile/
│       ├── 10-ANKUR-KUMAR-PROFILE-PACK.md   ← START HERE
│       ├── 02-linkedin-profile.md
│       ├── 03-upwork-profile.md
│       ├── portfolio/index.html
│       └── ...
└── .cursor/
    └── environment.json    ← Cloud Agent only (ignore on laptop)
```

---

## 7. Troubleshooting

| Issue | Fix |
|-------|-----|
| `git clone` asks for password | Use GitHub PAT or SSH: https://docs.github.com/en/authentication |
| Old repo name `Curser` | `git remote set-url origin https://github.com/ankur0001/professional-work.git` |
| Markdown hard to read | Use Cursor/VS Code preview (Cmd/Ctrl + Shift + V) |
| Portfolio Pages not showing | Check Pages settings; may need `docs/` folder — ask agent to add |

---

## 8. What you don’t need on laptop

- Cloud Agent desktop / remote Chrome
- Sending passwords to any agent
- Running the Java learning branches (separate work in same repo)

---

## Quick start (copy-paste)

```bash
git clone https://github.com/ankur0001/professional-work.git
cd professional-work
# Open profile pack in your editor
cursor all-work/freelance-profile/10-ANKUR-KUMAR-PROFILE-PACK.md
```

Then paste into LinkedIn and Upwork from your browser.
