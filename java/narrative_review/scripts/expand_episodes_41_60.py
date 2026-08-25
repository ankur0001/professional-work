#!/usr/bin/env python3
"""Generate expanded 4-15 min narration for episodes 41-60."""

from __future__ import annotations

import re
from pathlib import Path

EPISODES_DIR = Path(__file__).resolve().parents[1] / "episodes"

# Episode key -> scenes dict (scene_id -> list of beat strings)
# Use empty string "" for blank lines before/after code blocks
EXPANSIONS: dict[str, dict[str, list[str]]] = {}

PLACEHOLDER = "__PLACEHOLDER__"
