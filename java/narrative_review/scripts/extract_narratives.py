#!/usr/bin/env python3
"""Extract per-episode narration markdown for narrative-review PR.

Reads make_episode_XX.py SCENES lists via AST (no runtime imports) and writes
one markdown file per episode under java/narrative_review/episodes/.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP_DIR = ROOT / "episodes"
SCRIPT_DIR = Path("/tmp/ep_scripts")
CATALOG = ROOT / "reference" / "EPISODE_CATALOG.md"
EXCERPTS = ROOT / "reference" / "handbook_lessons_1-12_excerpts.md"
HANDBOOK_TOC = ROOT / "reference" / "handbook_toc_recovered.md"

# Handbook-authoritative titles recovered from the attached HTML
# (Java_JVM_Handbook_GPT55__1_.html). Gaps filled from episode catalog with a note.
HANDBOOK_TITLES: dict[int, str] = {
    1: "Introduction to Java",
    2: "JDK, JRE, and JVM",
    3: "Java Program Structure",
    4: "Variables and Data Types",
    5: "Operators",
    6: "Control Flow",
    7: "Methods",
    8: "Arrays",
    9: "Strings",
    10: "Object-Oriented Programming",
    11: "Access Modifiers",
    12: "Packages",
    13: "Enums",
    14: "Wrappers and Autoboxing",
    15: "Generics",
    16: "Annotations",
    17: "Reflection",
    18: "Records",
    19: "Sealed Classes",
    20: "Modules and JPMS",
    21: "Collection Framework Overview",
    22: "List",
    23: "Set",
    24: "Queue & Deque",
    25: "Map",
    48: "Atomic Classes",
    56: "Class Loading",
    57: "Bytecode",
    60: "JVM Memory Areas",
    61: "Heap",
    62: "Stack",
    65: "GC Algorithms",
    66: "G1GC",
    67: "ZGC & Shenandoah",
    68: "JVM Tuning",
    70: "JVM Troubleshooting",
}

# Known remaps: episode number -> handbook lesson number that best matches the topic.
# When absent, default is episode N ↔ lesson N (early curriculum) or topic-title match.
EPISODE_TO_HANDBOOK_LESSON: dict[int, int | None] = {
    # Ep 21–25: handbook L21 was Collection Framework Overview; List/Set/Map shifted.
    21: 22,  # Lists ← handbook List
    22: 23,  # Sets ← handbook Set
    23: 25,  # Maps ← handbook Map
    24: 24,  # Queues/Deques ← handbook Queue & Deque
    25: None,  # Sorting — video pacing insert; no recovered handbook title
    # JVM block: catalog titles vs recovered handbook nav (see toc divergences)
    43: 48,  # Atomics ← handbook Atomic Classes
    51: 56,  # Class Loading
    52: 57,  # Bytecode Basics
    53: 61,  # Heap and Stack (primarily Heap; Stack is L62)
    54: 65,  # Garbage Collection ← GC Algorithms family
    56: 66,  # GC Collectors ← G1GC / collector family (also L67)
    62: 68,  # JVM Flags and Tuning ← JVM Tuning
    58: 70,  # Diagnostic Tools ← JVM Troubleshooting family
    # Season 2 bonus — not in the 80-lesson handbook
    81: None,
    82: None,
    83: None,
    84: None,
    85: None,
}


def parse_catalog() -> dict[int, tuple[str, str]]:
    """ep -> (handbook_col_or_track, title)"""
    text = CATALOG.read_text()
    out: dict[int, tuple[str, str]] = {}
    for line in text.splitlines():
        m = re.match(
            r"\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|",
            line.strip(),
        )
        if not m:
            continue
        ep = int(m.group(1))
        if ep < 1 or ep > 85:
            continue
        out[ep] = (m.group(2).strip(), m.group(3).strip())
    return out


def load_excerpt_snippets() -> dict[int, list[str]]:
    """Pull short concept bullets from recovered handbook excerpts for L1–12."""
    if not EXCERPTS.exists():
        return {}
    text = EXCERPTS.read_text()
    by_lesson: dict[int, list[str]] = {}
    current: int | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^##\s+Lesson\s+(\d+)\b", line)
        if m:
            if current is not None and buf:
                by_lesson[current] = buf[:50]
            current = int(m.group(1))
            buf = []
            continue
        if current is None:
            continue
        s = line.strip()
        if not s or s.startswith("```") or s.startswith("---") or s.startswith("="):
            continue
        if s.startswith("###"):
            continue
        # Prefer definitional / concept lines
        if len(s) > 60 or s.startswith(("Java ", "The ", "A ", "Bytecode", "JVM", "JDK", "JRE")):
            s = re.sub(r"^\d+:\s*", "", s)
            buf.append(s[:260])
    if current is not None and buf:
        by_lesson[current] = buf[:50]
    return by_lesson


def extract_scenes_ast(path: Path) -> list[tuple[str, str, list[str]]]:
    tree = ast.parse(path.read_text())
    scenes_node = None
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "SCENES":
                scenes_node = node.value
                break
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "SCENES":
                    scenes_node = node.value
                    break
    if scenes_node is None:
        raise RuntimeError(f"No SCENES in {path}")
    raw = ast.literal_eval(scenes_node)
    out = []
    for item in raw:
        if len(item) != 3:
            raise RuntimeError(f"Bad scene tuple in {path}: {item!r}")
        sid, renderer, beats = item
        out.append((str(sid), str(renderer), [str(b) for b in beats]))
    return out


def ep01_scenes() -> list[tuple[str, str, list[str]]]:
    return extract_scenes_ast(SCRIPT_DIR / "make_episode_01_short.py")


def source_section(
    ep: int,
    title: str,
    catalog_lesson: str,
    scenes: list[tuple[str, str, list[str]]],
    excerpts: dict[int, list[str]],
) -> str:
    lines: list[str] = []
    lines.append("## Source attribution (reference document)")
    lines.append("")
    lines.append(
        "Reference document (user attachment): "
        "**`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*."
    )
    lines.append("")

    if ep >= 81:
        lines.append(
            f"- **Episode {ep:02d}** is a **Season 2 production-systems bonus** track. "
            "It is **not** one of the handbook’s 80 lessons."
        )
        lines.append(
            f"- Topic framing for the video: **{title}** "
            "(continuity after Episode 80’s architecture interview wrap)."
        )
        lines.append(
            "- Narration was **original written for the video** (scene-synced beats), "
            "not copied verbatim from the handbook."
        )
        return "\n".join(lines)

    hb_lesson = EPISODE_TO_HANDBOOK_LESSON.get(ep, ep)
    catalog_says = catalog_lesson

    if hb_lesson is None:
        lines.append(
            f"- Series catalog lists this episode under handbook column **{catalog_says}** "
            f"with title **{title}**."
        )
        lines.append(
            "- Recovered handbook TOC does **not** contain a matching lesson title for this "
            "slot (curriculum was remapped for 4–5 minute YouTube pacing)."
        )
        lines.append(
            "- Narration was **authored for on-screen visuals** using the episode topic as "
            "the outline; concepts reflect standard Java curriculum covered by the handbook’s "
            "surrounding lessons, not a verbatim paste."
        )
        return "\n".join(lines)

    hb_title = HANDBOOK_TITLES.get(hb_lesson, title)
    lines.append(f"- **Primary handbook lesson:** Lesson **{hb_lesson}** — *{hb_title}*.")
    if hb_lesson != ep or (hb_title and hb_title.lower() not in title.lower() and title.lower() not in hb_title.lower()):
        lines.append(
            f"- **Series catalog mapping:** Episode {ep:02d} / catalog column `{catalog_says}` "
            f"/ published title *{title}*."
        )
        if hb_lesson != ep:
            lines.append(
                f"- **Note:** Episode number and handbook lesson number are **not 1:1** here "
                f"(handbook lesson {hb_lesson} → episode {ep:02d}). See "
                "`../reference/handbook_toc_recovered.md` for documented divergences."
            )
    else:
        lines.append(
            f"- **Series catalog:** Episode {ep:02d} ↔ handbook lesson {catalog_says} — *{title}*."
        )

    lines.append(
        "- **How content was used:** The handbook provided the **topic outline and teaching "
        "points**. Spoken lines were **rewritten** into short documentary beats matched to "
        "motion-graphics scenes (per user guidance: own narration synced to presentation; "
        "handbook as reference, not a script to read aloud)."
    )

    # Concept overlap from recovered excerpts when available
    snips = excerpts.get(hb_lesson) or excerpts.get(ep) or []
    if snips:
        lines.append("")
        lines.append(
            f"### Handbook concepts reused (from recovered Lesson {hb_lesson} excerpt)"
        )
        lines.append("")
        # Pick a few distinctive phrases that also appear in narration
        narr = " ".join(b for _, _, beats in scenes for b in beats).lower()
        hits = []
        for s in snips:
            key = re.sub(r"[^a-z0-9 ]", "", s.lower())
            words = [w for w in key.split() if len(w) > 5][:6]
            if words and sum(1 for w in words if w in narr) >= min(2, len(words)):
                hits.append(s)
            if len(hits) >= 6:
                break
        if not hits:
            hits = snips[:5]
        for h in hits:
            lines.append(f"- {h}")
        lines.append("")
        lines.append(
            f"Full recovered excerpt: `../reference/handbook_lessons_1-12_excerpts.md` "
            f"(Lesson {hb_lesson})."
        )
    else:
        lines.append("")
        lines.append(
            "- Full handbook HTML is **not checked into git** (original upload was ephemeral). "
            "Attribution for this episode is by **lesson title / topic** from the recovered TOC "
            "and the series catalog."
        )

    # Scene-level mapping hint
    lines.append("")
    lines.append("### Scene ↔ curriculum intent")
    lines.append("")
    for sid, _r, beats in scenes:
        intent = beats[0] if beats else sid
        lines.append(f"- **`{sid}`** — starts from: _{intent}_")
    return "\n".join(lines)


def render_episode_md(
    ep: int,
    title: str,
    catalog_lesson: str,
    scenes: list[tuple[str, str, list[str]]],
    script_name: str,
    excerpts: dict[int, list[str]],
) -> str:
    parts: list[str] = []
    parts.append(f"# Episode {ep:02d} — {title}")
    parts.append("")
    parts.append("| Field | Value |")
    parts.append("|---|---|")
    parts.append(f"| Episode | {ep:02d} |")
    parts.append(f"| Title | {title} |")
    parts.append(f"| Catalog handbook column | {catalog_lesson} |")
    parts.append(f"| Narration source script | `{script_name}` |")
    parts.append("| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |")
    parts.append("")
    parts.append("## Full narration (spoken beats)")
    parts.append("")
    n = 0
    for sid, renderer, beats in scenes:
        parts.append(f"### Scene `{sid}` (renderer: `{renderer}`)")
        parts.append("")
        for i, beat in enumerate(beats, 1):
            n += 1
            parts.append(f"{i}. {beat}")
        parts.append("")
    parts.append(f"_Total beats: **{n}** across **{len(scenes)}** scenes._")
    parts.append("")
    parts.append(source_section(ep, title, catalog_lesson, scenes, excerpts))
    parts.append("")
    return "\n".join(parts)


def slugify(title: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", title.strip().lower()).strip("-")
    return s[:60] or "episode"


def main():
    EP_DIR.mkdir(parents=True, exist_ok=True)
    catalog = parse_catalog()
    excerpts = load_excerpt_snippets()
    index_rows = []

    # Episode 01 from short cut
    scenes01 = ep01_scenes()
    title01 = catalog.get(1, ("1", "Why Java Exists / Introduction to Java"))[1]
    lesson01 = catalog.get(1, ("1", title01))[0]
    md = render_episode_md(
        1, title01, lesson01, scenes01, "make_short_episode_chatterbox.py / make_episode_01_short.py", excerpts
    )
    name01 = f"ep01_{slugify(title01)}.md"
    (EP_DIR / name01).write_text(md)
    index_rows.append((1, title01, name01, len(scenes01), sum(len(b) for *_, b in scenes01)))

    for path in sorted(SCRIPT_DIR.glob("make_episode_*.py")):
        m = re.fullmatch(r"make_episode_(\d+)\.py", path.name)
        if not m:
            continue
        ep = int(m.group(1))
        if ep < 2:
            continue
        scenes = extract_scenes_ast(path)
        lesson, title = catalog.get(ep, (str(ep), f"Episode {ep}"))
        # Prefer docstring title if catalog missing
        if ep not in catalog:
            doc = ast.get_docstring(ast.parse(path.read_text())) or ""
            dm = re.search(r"Episode\s+\d+\s*[—-]\s*(.+)", doc)
            if dm:
                title = dm.group(1).split("\n")[0].strip()
        fname = f"ep{ep:02d}_{slugify(title)}.md"
        (EP_DIR / fname).write_text(
            render_episode_md(ep, title, lesson, scenes, path.name, excerpts)
        )
        index_rows.append(
            (ep, title, fname, len(scenes), sum(len(b) for *_, b in scenes))
        )

    # README index
    lines = [
        "# The Java Story — Narrative Review Pack",
        "",
        "One markdown file per rendered video with the **full spoken narration** and an",
        "explanation of **what was taken from the reference handbook**.",
        "",
        "## Reference document",
        "",
        "- **User attachment:** `Java_JVM_Handbook_GPT55__1_.html`",
        "- **Title:** Java & JVM Handbook — 80 Lessons",
        "- The full HTML was **not committed** to git (ephemeral upload). Recovered TOC +",
        "  Lessons 1–12 excerpts are under [`reference/`](reference/).",
        "",
        "## How to review",
        "",
        "1. Open any `episodes/epXX_*.md`.",
        "2. Read **Full narration** (exact beats used in the video).",
        "3. Read **Source attribution** for the handbook lesson / remapping notes.",
        "",
        "## Episode index",
        "",
        "| Ep | Title | Beats | Scenes | File |",
        "|---:|---|---:|---:|---|",
    ]
    for ep, title, fname, nscenes, nbeats in index_rows:
        lines.append(f"| {ep:02d} | {title} | {nbeats} | {nscenes} | [`{fname}`](episodes/{fname}) |")
    lines += [
        "",
        f"**Total episodes in this pack:** {len(index_rows)}",
        "",
        "## Related docs",
        "",
        "- [`SOURCE_MAPPING.md`](SOURCE_MAPPING.md) — handbook ↔ episode mapping rules",
        "- [`reference/EPISODE_CATALOG.md`](reference/EPISODE_CATALOG.md)",
        "- [`reference/handbook_toc_recovered.md`](reference/handbook_toc_recovered.md)",
        "- [`reference/handbook_lessons_1-12_excerpts.md`](reference/handbook_lessons_1-12_excerpts.md)",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(lines))

    meta = {
        "episodes": len(index_rows),
        "files": [r[2] for r in index_rows],
    }
    (ROOT / "manifest.json").write_text(json.dumps(meta, indent=2))
    print(f"Wrote {len(index_rows)} episode narrative files")


if __name__ == "__main__":
    main()
