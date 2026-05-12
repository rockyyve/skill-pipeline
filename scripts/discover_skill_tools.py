#!/usr/bin/env python3
"""Discover local skill generation and optimization tools."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


COMMANDS = ["skill-seekers", "skill-create", "skill-creator", "claude", "codex"]
SEARCH_ROOTS = [
    Path.home() / ".codex" / "skills",
    Path.home() / ".agents" / "skills",
    Path.home() / ".skills-manager" / "skills",
    Path.home() / "work",
]
NAME_HINTS = ("skill-seek", "skill-seeker", "skill-seekers", "skill-create", "skill-creator")


def safe_walk(root: Path, max_matches: int = 80) -> list[str]:
    matches: list[str] = []
    if not root.exists():
        return matches

    for dirpath, dirnames, filenames in os.walk(root):
        path = Path(dirpath)
        parts = set(path.parts)
        if {".git", "node_modules", "__pycache__"} & parts:
            dirnames[:] = []
            continue

        haystack = " ".join([path.name, *dirnames, *filenames]).lower()
        if any(hint in haystack for hint in NAME_HINTS):
            matches.append(str(path))
            if len(matches) >= max_matches:
                break

        depth = len(path.relative_to(root).parts) if path != root else 0
        if depth >= 5:
            dirnames[:] = []

    return matches


def skill_seekers_commands(path: str | None) -> list[str]:
    if not path:
        return []
    try:
        completed = subprocess.run(
            [path, "--help"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return []

    text = completed.stdout + "\n" + completed.stderr
    known = [
        "create", "config", "scrape", "github", "package", "upload", "analyze",
        "enhance", "pdf", "word", "epub", "video", "unified", "estimate",
        "install", "jupyter", "html", "openapi", "asciidoc", "pptx", "rss",
        "manpage", "confluence", "notion", "chat",
    ]
    return [command for command in known if command in text]


def main() -> None:
    commands = {command: shutil.which(command) for command in COMMANDS}
    result = {
        "commands": commands,
        "skill_seekers_supported_commands": skill_seekers_commands(commands.get("skill-seekers")),
        "candidate_paths": {},
        "recommended_path": "",
        "missing_optional_tools": [],
    }

    for root in SEARCH_ROOTS:
        result["candidate_paths"][str(root)] = safe_walk(root)

    has_seekers = bool(commands.get("skill-seekers"))
    has_create = bool(commands.get("skill-create"))
    result["missing_optional_tools"] = [
        name for name, present in (("skill-seekers", has_seekers), ("skill-create", has_create)) if not present
    ]

    if has_seekers and has_create:
        result["recommended_path"] = "full automated pipeline: skill-seekers draft, then skill-create optimization"
    elif has_seekers:
        result["recommended_path"] = "hybrid pipeline: skill-seekers draft, then skill-creator/manual optimization"
    elif has_create:
        result["recommended_path"] = "hybrid pipeline: manual repository draft, then skill-create optimization"
    else:
        result["recommended_path"] = "fallback pipeline: manual repository inspection, skill-creator-style optimization, validation, and packaging"

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
