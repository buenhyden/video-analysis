#!/usr/bin/env python3
"""Validate stack version drift only when active stack roots exist."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACTIVE_ROOT_NAMES = ("web", "server", "app", "desktop", "monitoring", "tests")


def git_tracked_files(root_name: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--", root_name],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def has_local_files(path: Path) -> bool:
    return any(child.is_file() for child in path.rglob("*"))


def active_roots() -> list[Path]:
    roots: list[Path] = []
    for root_name in ACTIVE_ROOT_NAMES:
        path = ROOT / root_name
        if not path.is_dir():
            continue
        if git_tracked_files(root_name) or has_local_files(path):
            roots.append(path)
    return roots


def read_json(path: Path) -> tuple[dict, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report parser detail
        return {}, f"{path.relative_to(ROOT)}: JSON parse failed: {exc}"
    if not isinstance(data, dict):
        return {}, f"{path.relative_to(ROOT)}: JSON root must be an object"
    return data, None


def workflow_setup_versions(tool_name: str) -> set[str]:
    versions: set[str] = set()
    workflow_root = ROOT / ".github/workflows"
    if not workflow_root.exists():
        return versions
    version_key = f"{tool_name}-version"
    pattern = re.compile(rf"{re.escape(version_key)}:\s*['\"]?([0-9]+(?:\.[0-9]+)?)")
    for path in workflow_root.glob("*.yml"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        versions.update(pattern.findall(text))
    return versions


def major(version: str) -> str | None:
    match = re.search(r"([0-9]+)", version)
    return match.group(1) if match else None


def major_minor(version: str) -> str | None:
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", version)
    return match.group(1) if match else None


def validate_node(root: Path) -> list[str]:
    errors: list[str] = []
    package_json = root / "package.json"
    if not package_json.exists():
        return errors

    package, parse_error = read_json(package_json)
    if parse_error:
        return [parse_error]

    lock_path = root / "package-lock.json"
    if not lock_path.exists():
        errors.append(
            f"{package_json.relative_to(ROOT)}: active Node manifest requires package-lock.json"
        )
    else:
        lock, lock_error = read_json(lock_path)
        if lock_error:
            errors.append(lock_error)
        else:
            manifest_version = package.get("version")
            lock_version = None
            packages = lock.get("packages")
            if isinstance(packages, dict) and isinstance(packages.get(""), dict):
                lock_version = packages[""].get("version")
            lock_version = lock_version or lock.get("version")
            if manifest_version and lock_version and manifest_version != lock_version:
                errors.append(
                    f"{lock_path.relative_to(ROOT)}: package version `{lock_version}` "
                    f"does not match package.json `{manifest_version}`"
                )

    engines = package.get("engines")
    node_engine = engines.get("node") if isinstance(engines, dict) else None
    setup_node_versions = workflow_setup_versions("node")
    if isinstance(node_engine, str) and setup_node_versions:
        engine_major = major(node_engine)
        workflow_majors = {major(version) for version in setup_node_versions}
        if engine_major and engine_major not in workflow_majors:
            errors.append(
                f"{package_json.relative_to(ROOT)}: engines.node `{node_engine}` "
                f"does not match workflow node versions {sorted(setup_node_versions)}"
            )
    return errors


def validate_python(root: Path) -> list[str]:
    errors: list[str] = []
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return errors

    text = pyproject.read_text(encoding="utf-8", errors="ignore")
    requires_match = re.search(r"requires-python\s*=\s*['\"]([^'\"]+)['\"]", text)
    setup_python_versions = workflow_setup_versions("python")
    if requires_match and setup_python_versions:
        required = requires_match.group(1)
        required_version = major_minor(required)
        workflow_versions = {major_minor(version) for version in setup_python_versions}
        if required_version and required_version not in workflow_versions:
            errors.append(
                f"{pyproject.relative_to(ROOT)}: requires-python `{required}` "
                f"does not match workflow python versions {sorted(setup_python_versions)}"
            )
    return errors


def validate_docker(root: Path) -> list[str]:
    errors: list[str] = []
    dockerfiles = [
        path
        for path in root.rglob("*")
        if path.name == "Dockerfile" or path.suffix == ".Dockerfile"
    ]
    for path in dockerfiles:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped.upper().startswith("FROM "):
                continue
            image = stripped.split()[1]
            if image in {"scratch"} or image.startswith("$"):
                continue
            if ":" not in image or image.endswith(":latest"):
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: Docker base image must use an explicit non-latest tag"
                )
    return errors


def main() -> int:
    errors: list[str] = []
    roots = active_roots()
    if not roots:
        print("Version drift validation passed: no active stack roots.")
        return 0

    for root in roots:
        errors.extend(validate_node(root))
        errors.extend(validate_python(root))
        errors.extend(validate_docker(root))

    if errors:
        print("Version drift validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    names = ", ".join(path.name for path in roots)
    print(f"Version drift validation passed for active roots: {names}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
