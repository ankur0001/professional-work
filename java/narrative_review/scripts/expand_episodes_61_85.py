#!/usr/bin/env python3
"""Generate expanded narration markdown for episodes 61-85."""

from __future__ import annotations

import re
from pathlib import Path

EPISODES_DIR = Path(__file__).resolve().parents[1] / "episodes"

# Each episode: (filename, field_updates, scenes_dict, source_attribution_extra, footer_note)
# scenes_dict maps scene_id -> list of beat strings (full replacement for narration section)

def field_table(ep: int, title: str, col: str, source_note: str = "Expanded review narration (4–15 min target)") -> str:
    return f"""| Field | Value |
|---|---|
| Episode | {ep:02d} |
| Title | {title} |
| Catalog handbook column | {col} |
| Narration source script | {source_note} |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |"""


def render_episode(
    h1: str,
    fields: str,
    scenes: list[tuple[str, str, list[str]]],
    source: str,
    footer: str,
) -> str:
    lines = [f"# {h1}", "", fields, "", "## Full narration (spoken beats)", ""]
    for scene_id, renderer, beats in scenes:
        lines.append(f"### Scene `{scene_id}` (renderer: `{renderer}`)")
        lines.append("")
        for i, beat in enumerate(beats, 1):
            lines.append(f"{i}. {beat}")
        lines.append("")
    total = sum(len(b) for _, _, b in scenes)
    lines.append(footer.format(total=total, scenes=len(scenes)))
    lines.append("")
    lines.append("## Source attribution (reference document)")
    lines.append("")
    lines.append(source)
    return "\n".join(lines)


# --- Episode content definitions ---

EP61 = render_episode(
    "Episode 61 — Reference Types",
    field_table(61, "Reference Types", "61"),
    [
        ("hook", "hook", [
            "Episode Sixty covered metaspace and native memory — the parts of the JVM footprint that live outside your heap objects.",
            "Today we zoom in on a quieter lever: reference types.",
            "Most of the time you hold a strong reference — a normal variable pointing at an object — and the garbage collector leaves that object alone.",
            "But Java gives you weaker reference types with different contracts about when an object may be collected.",
            "Soft, weak, and phantom references are how you build memory-sensitive caches, canonical maps, and native-resource cleanup hooks.",
            "And ReferenceQueue is how you get notified when the referent disappears — if you set up a consumer thread.",
            "Watch this space carefully. Reference types are powerful, subtle, and easy to misuse.",
        ]),
        ("title", "title", [
            "Episode Sixty-One.",
            "Soft, Weak, and Phantom References.",
            "By the end you'll know when each strength helps — and when a proper cache library is the better call.",
        ]),
        ("reference_hierarchy", "reference_hierarchy", [
            "Picture four reference strengths from strongest to weakest.",
            "Strong reference — that's your everyday assignment. `String s = \"hello\"`. While anything strongly reachable can reach the object, GC will not collect it.",
            "Soft reference — the JVM keeps the referent while memory is comfortable, but may clear it when the heap gets tight. That's the classic memory-sensitive cache story.",
            "Weak reference — cleared at the next GC cycle once only weakly reachable. Think canonical keys that should not pin objects forever.",
            "Phantom reference — the referent is effectively unreachable through the reference itself. You use it for post-mortem cleanup — often native handles — via a queue.",
            "Each type extends `Reference<T>` with different enqueue behavior. The hierarchy is about reachability, not magic lifetime control.",
        ]),
        ("soft_weak_use", "soft_weak_use", [
            "Let's walk a soft-reference cache — the pattern people reach for when parsed data is expensive but disposable under pressure.",
            "Here's a minimal shape:",
            "",
        ]),
        ("soft_weak_code", "soft_weak_use", []),  # placeholder - handled below
    ],
    "",
    "",
)

# Script is getting too complex inline. I'll write files directly with Write tool instead.

if __name__ == "__main__":
    print("Use direct file writes for expanded episodes.")
