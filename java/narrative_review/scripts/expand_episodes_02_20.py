#!/usr/bin/env python3
"""Expand episodes 02-20 to 4-15 min conversational narration."""

from __future__ import annotations

import re
from pathlib import Path

EPISODES_DIR = Path(__file__).resolve().parents[1] / "episodes"

NEXT_TITLES = {
    2: "Java Program Structure",
    3: "Variables and Data Types",
    4: "Operators",
    5: "Control Flow",
    6: "Methods",
    7: "Arrays",
    8: "Strings",
    9: "Object-Oriented Programming",
    10: "Access Modifiers",
    11: "Packages",
    12: "Enums",
    13: "Wrappers and Autoboxing",
    14: "Generics",
    15: "Annotations",
    16: "Reflection",
    17: "Records",
    18: "Sealed Classes",
    19: "Modules and JPMS",
    20: "Lists",
}


def field_table(ep: int, title: str, col: int) -> str:
    return f"""| Field | Value |
|---|---|
| Episode | {ep:02d} |
| Title | {title} |
| Catalog handbook column | {col} |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~8–12) |"""


def extract_source_attribution(text: str) -> str:
    m = re.search(r"(## Source attribution \(reference document\)\n\n.*)", text, re.DOTALL)
    if not m:
        raise ValueError("Missing source attribution section")
    src = m.group(1).rstrip()
    bullet = (
        "- **Narration expansion:** Spoken lines expanded for **4–15 minute** "
        "conversational runtime; handbook still used as topic reference."
    )
    if bullet not in src:
        # insert after "How content was used" bullet block — append before ### Handbook
        if "### Handbook concepts reused" in src:
            src = src.replace(
                "### Handbook concepts reused",
                f"{bullet}\n\n### Handbook concepts reused",
                1,
            )
        elif "### Scene ↔ curriculum intent" in src:
            src = src.replace(
                "### Scene ↔ curriculum intent",
                f"{bullet}\n\n### Scene ↔ curriculum intent",
                1,
            )
        else:
            src = src + f"\n\n{bullet}"
    return src


def render_scenes(scenes: list[tuple[str, str, list[str | tuple[str, str]]]]) -> str:
    lines: list[str] = []
    beat_num = 0
    for scene_id, renderer, beats in scenes:
        lines.append(f"### Scene `{scene_id}` (renderer: `{renderer}`)")
        lines.append("")
        n = 1
        for beat in beats:
            if isinstance(beat, tuple) and beat[0] == "code":
                lines.append(beat[1])
                lines.append("")
            else:
                lines.append(f"{n}. {beat}")
                n += 1
                beat_num += 1
        lines.append("")
    return "\n".join(lines), beat_num, len(scenes)


def write_episode(
    ep: int,
    slug: str,
    title: str,
    scenes: list[tuple[str, str, list[str | tuple[str, str]]]],
    scene_intent: dict[str, str] | None = None,
) -> int:
    path = EPISODES_DIR / f"ep{ep:02d}_{slug}.md"
    existing = path.read_text(encoding="utf-8")
    source = extract_source_attribution(existing)
    body, total_beats, n_scenes = render_scenes(scenes)
    if scene_intent and "### Scene ↔ curriculum intent" in source:
        intent_lines = ["### Scene ↔ curriculum intent", ""]
        for sid, desc in scene_intent.items():
            intent_lines.append(f"- **`{sid}`** — {desc}")
        new_intent = "\n".join(intent_lines)
        source = re.sub(
            r"### Scene ↔ curriculum intent\n\n(?:- \*\*`[^`]+`\*\*.*\n)+",
            new_intent + "\n",
            source,
        )
    md = f"""# Episode {ep:02d} — {title}

{field_table(ep, title, ep)}

## Full narration (spoken beats)

{body}_Total beats: expanded for ~8–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

{source}
"""
    path.write_text(md, encoding="utf-8")
    words = len(re.findall(r"\b[\w']+\b", body))
    return words


# Episode definitions loaded from expand_episodes_02_20_data.py
from expand_episodes_02_20_data import EPISODE_DATA  # noqa: E402
from expand_episodes_02_20_supplement import merge_supplement  # noqa: E402
from expand_episodes_02_20_extra import merge_extra  # noqa: E402


def main() -> None:
    counts: dict[int, int] = {}
    for ep, data in sorted(EPISODE_DATA.items()):
        scenes = merge_supplement(data["scenes"], ep)
        scenes = merge_extra(scenes, ep)
        w = write_episode(ep, data["slug"], data["title"], scenes, data.get("scene_intent"))
        counts[ep] = w
        print(f"Episode {ep:02d}: {w} words")
    print("---")
    for ep, w in sorted(counts.items()):
        print(f"ep{ep:02d}: {w}")


if __name__ == "__main__":
    main()
