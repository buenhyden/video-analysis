#!/usr/bin/env python3
"""Generate deterministic offline repository intelligence artifacts."""

from __future__ import annotations

import json
import shutil
import subprocess  # nosec B404: fixed git invocation, no shell, no user input
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "_workspace" / "intelligence"
EXCLUDED_PREFIXES = (
    ".git/",
    ".history/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".venv/",
    "node_modules/",
    "dist/",
    "coverage/",
    "storybook-static/",
    "graphify-out/cache/",
)
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".sh",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".css",
    ".html",
    ".txt",
}
TOP_LEVEL_ORDER = [
    ".github",
    ".claude",
    "docs",
    "scripts",
    "web",
    "server",
    "app",
    "tests",
    "monitoring",
]


def git_ls_files() -> list[Path]:
    git_bin = shutil.which("git")
    if git_bin is None:
        raise RuntimeError("git executable not found on PATH")
    result = subprocess.run(
        [git_bin, "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )  # nosec B603: command arguments are static and shell=False by default
    files: list[Path] = []
    for line in result.stdout.splitlines():
        if not line or line.startswith(EXCLUDED_PREFIXES):
            continue
        files.append(Path(line))
    return sorted(files, key=lambda p: p.as_posix())


def classify(path: Path) -> str:
    parts = path.parts
    if not parts:
        return "root"
    first = parts[0]
    if first == ".github" and len(parts) > 1:
        return ".github/" + parts[1]
    if first == "docs" and len(parts) > 1:
        return "docs/" + parts[1]
    return first


def count_lines(path: Path) -> int:
    full = REPO_ROOT / path
    if path.suffix not in TEXT_SUFFIXES:
        return 0
    try:
        return len(full.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return 0


def build_repo_map(files: list[Path]) -> dict[str, object]:
    groups: dict[str, dict[str, object]] = defaultdict(
        lambda: {"files": 0, "lines": 0, "examples": []}
    )
    suffixes: dict[str, int] = defaultdict(int)
    for path in files:
        group = groups[classify(path)]
        group["files"] = int(group["files"]) + 1
        group["lines"] = int(group["lines"]) + count_lines(path)
        examples = group["examples"]
        if isinstance(examples, list) and len(examples) < 8:
            examples.append(path.as_posix())
        suffixes[path.suffix or "[none]"] += 1

    return {
        "schema_version": "1.0.0",
        "source": "git ls-files",
        "file_count": len(files),
        "groups": {key: groups[key] for key in sorted(groups)},
        "suffixes": dict(sorted(suffixes.items())),
    }


def write_mermaid(repo_map: dict[str, object]) -> None:
    groups = repo_map["groups"]
    assert isinstance(groups, dict)
    lines = ["flowchart TD", "  repo[Project-Template]"]
    for name in TOP_LEVEL_ORDER:
        matching = [key for key in groups if key == name or key.startswith(name + "/")]
        if not matching:
            continue
        node = name.replace(".", "dot").replace("/", "_").replace("-", "_")
        total = sum(int(groups[key]["files"]) for key in matching)  # type: ignore[index]
        lines.append(f"  repo --> {node}[{name}: {total} files]")
    OUT_DIR.joinpath("architecture.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_summary(repo_map: dict[str, object]) -> None:
    groups = repo_map["groups"]
    assert isinstance(groups, dict)
    lines = [
        "# Repository Intelligence Summary",
        "",
        f"Schema version: {repo_map['schema_version']}",
        f"Tracked files scanned: {repo_map['file_count']}",
        "",
        "## Top Groups",
        "",
    ]
    ranked = sorted(
        groups.items(),
        key=lambda item: (-int(item[1]["files"]), item[0]),  # type: ignore[index]
    )[:12]
    for name, info in ranked:
        lines.append(f"- `{name}`: {info['files']} files, {info['lines']} text lines")
    lines.extend([
        "",
        "## Generated Artifacts",
        "",
        "- `repo_map.json`",
        "- `architecture.mmd`",
        "- `summary.md`",
    ])
    OUT_DIR.joinpath("summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = git_ls_files()
    repo_map = build_repo_map(files)
    OUT_DIR.joinpath("repo_map.json").write_text(
        json.dumps(repo_map, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_mermaid(repo_map)
    write_summary(repo_map)
    print(f"Generated intelligence artifacts in {OUT_DIR.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
