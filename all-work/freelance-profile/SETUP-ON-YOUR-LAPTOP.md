# Setup on your personal laptop (Browser B)

Use **your laptop** and **your browser** — no Cloud Agent desktop required.

**Repo:** https://github.com/ankur0001/professional-work

---

## Step 1 — Get the files on laptop B (5 min)

### Option A — Clone (recommended)

```bash
cd ~/Documents   # or any folder you like
git clone https://github.com/ankur0001/professional-work.git
cd professional-work
```

### Option B — Download only the profile folder

1. Open https://github.com/ankur0001/professional-work/tree/main/all-work/freelance-profile
2. Download or open files in browser

### Open the main file locally

| Tool | Path |
|------|------|
| VS Code / Cursor | `all-work/freelance-profile/10-ANKUR-KUMAR-PROFILE-PACK.md` |
| Any editor | same path after clone |

Keep this file open — you will copy-paste from it into each website.

---

## Step 2 — LinkedIn (15–20 min)

**URL:** https://www.linkedin.com/in/ankur-kumar-4801078a/

1. Log in in **your browser** on laptop B.
2. Click your profile photo → **View profile**.
3. Click **pencil (Edit)** on the intro section.

### Headline

Copy from `10-ANKUR-KUMAR-PROFILE-PACK.md` → section **LinkedIn headline**:

```
Senior Technical Lead → Solution Architect | Java, Spring Boot, Kafka, AWS | Banking, Logistics & Rail | Open to Contract
```

4. Paste into **Headline** → Save.

### About

5. Click **Edit** on About / Summary.
6. Copy the full **LinkedIn About** block from the same file → Paste → Save.

### Experience (optional polish)

7. For each role (HCL, Mphasis, Standard Chartered), click **Edit** → replace bullets with the enhanced bullets in the profile pack.

### Open to Work

8. Go to https://www.linkedin.com/jobs/preferences/
9. Turn on **Open to work**.
10. Select: **Contract**, **Freelance** (and full-time if you want).
11. Set visibility (recruiters only or all LinkedIn members).

### Announcement post

12. Copy **Open to contract LinkedIn post** from profile pack → **Start a post** → Paste → Post.

---

## Step 3 — GitHub profile (10 min)

**URL:** https://github.com/ankur0001

1. Log in on laptop B.

### Profile README

2. Create repo named exactly: `ankur0001` (if you don’t have it).
3. Add `README.md` — copy from profile pack section **GitHub profile README**.
4. Commit & push.

### Portfolio site (optional)

5. On GitHub: **New repository** → name `portfolio` (or use existing).
6. Upload `all-work/freelance-profile/portfolio/index.html` from your clone.
7. **Settings → Pages** → Source: `main` branch → Save.
8. Your site: `https://ankur0001.github.io/portfolio/` (if repo name is `portfolio`).

Or copy `index.html` into repo root of `professional-work` and enable Pages on that repo.

---

## Step 4 — Upwork (20–30 min)

**URL:** https://www.upwork.com

1. Sign up or log in.
2. **Settings → My Profile**.

| Field | Copy from |
|-------|-----------|
| Professional title | `03-upwork-profile.md` or profile pack |
| Overview / bio | Upwork overview section |
| Hourly rate | Your target (e.g. $75–90/hr to start) |
| Skills | List in `03-upwork-profile.md` |

3. **Portfolio** → Add 3 entries — text in profile pack / `03-upwork-profile.md`.
4. Upload **professional photo** (same as LinkedIn).
5. Complete **ID verification** (Upwork only — on your laptop).

---

## Step 5 — freelancermap (EU contracts, 15 min)

**URL:** https://www.freelancermap.com

1. Register / log in.
2. Paste pitch from `04-freelancermap-truelancer.md`.
3. Fill skills: Java, Spring Boot, Kafka, AWS, Microservices, Banking.
4. Set: **100% remote**, **freelance**, **B2B** if applicable.

---

## Step 6 — Truelancer (10 min)

**URL:** https://www.truelancer.com

1. Register / log in.
2. Paste bio from `04-freelancermap-truelancer.md`.

---

## Files cheat sheet

| Platform | File on your laptop |
|----------|---------------------|
| LinkedIn | `10-ANKUR-KUMAR-PROFILE-PACK.md` |
| Upwork | `03-upwork-profile.md` + profile pack |
| GitHub | `05-github-portfolio.md` + `portfolio/index.html` |
| freelancermap / Truelancer | `04-freelancermap-truelancer.md` |
| Checklist | `01-profile-audit-checklist.md` |

---

## Suggested order (one evening)

| Order | Platform | Time |
|-------|----------|------|
| 1 | Clone repo | 5 min |
| 2 | LinkedIn | 20 min |
| 3 | GitHub | 10 min |
| 4 | Upwork | 25 min |
| 5 | freelancermap + Truelancer | 15 min |

**Total ~75 min**

---

## After setup

1. Add portfolio URL to LinkedIn **Featured** section.
2. Add GitHub + LinkedIn links on Upwork.
3. Message the Cloud Agent: **“Profiles live on laptop — start hunting”**.

---

## Pull updates later

```bash
cd professional-work
git pull origin main
```

New profile text from agent sessions will appear under `all-work/`.
