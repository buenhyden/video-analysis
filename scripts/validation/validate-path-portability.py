#!/usr/bin/env python3
"""Warn about paths that may be painful on Windows or cloned deep paths.

This check is intentionally warning-only. The template already contains
reviewed maintenance history, and path portability should guide future names
without breaking existing valid releases.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RELATIVE_WARNING_BUDGET = 140
ABSOLUTE_WARNING_BUDGET = 220
SEGMENT_WARNING_BUDGET = 80
RESERVED_CHARS = set('<>:"|?*')


def repository_paths() -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def path_warnings(rel_path: str) -> list[str]:
    warnings: list[str] = []
    abs_path = str(ROOT / rel_path)
    segments = rel_path.split("/")

    if len(rel_path) > RELATIVE_WARNING_BUDGET:
        warnings.append(
            f"relative length {len(rel_path)} > {RELATIVE_WARNING_BUDGET}"
        )
    if len(abs_path) > ABSOLUTE_WARNING_BUDGET:
        warnings.append(
            f"current absolute length {len(abs_path)} > {ABSOLUTE_WARNING_BUDGET}"
        )

    for segment in segments:
        if len(segment) > SEGMENT_WARNING_BUDGET:
            warnings.append(
                f"segment `{segment}` length {len(segment)} > {SEGMENT_WARNING_BUDGET}"
            )
        if any(char in RESERVED_CHARS for char in segment):
            warnings.append(
                f"segment `{segment}` contains a Windows-reserved character"
            )
        if " " in segment:
            warnings.append(f"segment `{segment}` contains a space")

    return warnings


def main() -> int:
    warnings: list[str] = []
    for rel_path in repository_paths():
        for warning in path_warnings(rel_path):
            warnings.append(f"{rel_path}: {warning}")

    print("=== Path Portability Validation ===")
    if not warnings:
        print("✅ No path portability warnings.")
        return 0

    for warning in warnings:
        print(f"⚠️  {warning}")
    print(
        "⚠️  Path portability warnings are advisory. Keep new file names short, "
        "lowercase, slug-like, and Windows-safe."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
