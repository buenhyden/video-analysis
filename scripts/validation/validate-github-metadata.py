#!/usr/bin/env python3
"""Validate non-workflow GitHub metadata for the governance template."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GITHUB_DIR = ROOT / ".github"
WORKFLOW_DIR = GITHUB_DIR / "workflows"

STALE_TEXT = {
    "verify-application.yml": "stale application workflow name",
    "docs/prd": "non-canonical PRD docs path",
    "docs/ard": "non-canonical ARD docs path",
    "docs/11.postmortems": "invalid docs folder path",
    "Node.js/NPM": "default stack wording",
    "ARCHITECTURE.md": "stale root architecture router",
    "Governance Check": "removed duplicate workflow name",
    ".github/copilot-instructions.md": "GitHub-native AI instruction layer path",
    ".github/instructions/": "GitHub-native AI instruction layer path",
}
FORBIDDEN_ACTIVE_GLOBS = {
    "web/**",
    "server/**",
    "app/**",
    "desktop/**",
    "monitoring/**",
    "tests/**",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}
CONDITIONAL_COVERAGE_MARKERS = (
    "Every pull request must pass the 90% test coverage gate after an active implementation stack manifest exists",
    "Conditional Test Coverage Enforcement",
    "MIN_COVERAGE=\"${MIN_COVERAGE:-90}\"",
    "has_active_stack_manifest",
    "QUALITY GATE SKIPPED",
)
DERIVED_REQUIRED_PLACEHOLDERS = {
    "OWNER/REPO": "GitHub discussion/docs URLs must use the derived repository slug",
    "<owner>/<repo>": "security advisory URLs must use the derived repository slug",
    "<org>/<repo>": "issue template placeholders must use the derived repository slug",
    "security@example.com": "SECURITY.md must use a real security contact",
    "@your-org/": "CODEOWNERS must use real users or teams",
    "your-github-username-or-team": "Dependabot reviewer examples must use real owners",
}
REQUIRED_CODEOWNERS_PATHS = {
    ".github/workflows/**": "workflow files require devops/infra owner review",
    ".github/gates/**": "GitHub gate helpers require devops/infra owner review",
    ".github/scripts/**": "GitHub workflow helper scripts require devops/infra owner review",
    ".github/zizmor.yml": "workflow scanner config requires devops/infra owner review",
    ".github/**": "remaining GitHub metadata requires maintainer review",
}
CODEOWNER_OWNER_RE = r"@[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?"
ALLOWED_WORKFLOW_CLASSIFICATIONS = {
    "CI/CD gate",
    "Security gate",
    "Repository intelligence",
    "Release automation",
    "Diagnostics",
    "Repository automation",
}
EXPECTED_WORKFLOW_CLASSIFICATIONS = {
    "ai-remediation.yml": "Diagnostics",
    "autopilot-intelligence.yml": "Repository intelligence",
    "ci-global.yml": "CI/CD gate",
    "ci-security.yml": "Security gate",
    "generate-changelog.yml": "Release automation",
    "greetings.yml": "Repository automation",
    "labeler.yml": "Repository automation",
    "stale.yml": "Repository automation",
}
ALLOWED_DUPLICATE_BASENAMES = {
    "labeler.yml": {
        Path("labeler.yml"),
        Path("workflows/labeler.yml"),
    },
}


def iter_github_text_files() -> list[Path]:
    suffixes = {".md", ".yml", ".yaml", ".sh", ""}
    return [
        path
        for path in sorted(GITHUB_DIR.rglob("*"))
        if path.is_file() and path.suffix in suffixes
    ]


def validate_labeler() -> list[str]:
    path = GITHUB_DIR / "labeler.yml"
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for glob in sorted(FORBIDDEN_ACTIVE_GLOBS):
        if glob in text:
            errors.append(
                f"{path.relative_to(ROOT)}: active labeler glob `{glob}` implies a default stack"
            )
    return errors


def validate_text_drift() -> list[str]:
    errors: list[str] = []
    for path in iter_github_text_files():
        if "examples/fullstack-starter" in path.as_posix():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(ROOT)
        for marker, reason in STALE_TEXT.items():
            if marker in text:
                errors.append(f"{rel}: contains {reason} `{marker}`")
    return errors


def validate_pr_template() -> list[str]:
    path = GITHUB_DIR / "PULL_REQUEST_TEMPLATE.md"
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if "Resolves #" in text and "optional when known/available" not in text:
        errors.append(
            f"{path.relative_to(ROOT)}: issue linking must be optional when known/available"
        )
    if "coverage is > 80%" in text or "no exceptions" in text.lower():
        errors.append(
            f"{path.relative_to(ROOT)}: coverage wording must describe the conditional base-template exception"
        )
    if CONDITIONAL_COVERAGE_MARKERS[0] not in text:
        errors.append(
            f"{path.relative_to(ROOT)}: missing conditional 90% coverage checklist wording"
        )
    return errors


def validate_coverage_gate() -> list[str]:
    path = GITHUB_DIR / "gates/check-coverage.sh"
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for marker in CONDITIONAL_COVERAGE_MARKERS[1:]:
        if marker not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing conditional coverage marker `{marker}`")
    if "no active stack manifest" not in text:
        errors.append(
            f"{path.relative_to(ROOT)}: coverage skip must be limited to the no-active-stack-manifest case"
        )
    return errors


def validate_removed_workflow() -> list[str]:
    errors: list[str] = []
    if (GITHUB_DIR / "workflows/governance-check.yml").exists():
        errors.append(".github/workflows/governance-check.yml: duplicate workflow must remain removed")
    if (GITHUB_DIR / "workflows/security-scan.yml").exists():
        errors.append(".github/workflows/security-scan.yml: duplicate security workflow must remain removed")
    return errors


def validate_codeowners() -> list[str]:
    path = GITHUB_DIR / "CODEOWNERS"
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for required_path, reason in REQUIRED_CODEOWNERS_PATHS.items():
        pattern = re.compile(
            rf"^{re.escape(required_path)}\s+{CODEOWNER_OWNER_RE}\s*$",
            re.MULTILINE,
        )
        if not pattern.search(text):
            errors.append(f"{path.relative_to(ROOT)}: missing owner line for `{required_path}` ({reason})")
    return errors


def validate_about_workflow_coverage() -> list[str]:
    path = GITHUB_DIR / "ABOUT.md"
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    workflow_names = {workflow.name for workflow in WORKFLOW_DIR.glob("*.yml")}
    expected_workflow_names = set(EXPECTED_WORKFLOW_CLASSIFICATIONS)
    inventory_rows: list[tuple[str, str]] = []
    in_inventory = False
    for line in text.splitlines():
        if line.strip() == "## Workflow Inventory":
            in_inventory = True
            continue
        if in_inventory and line.startswith("## "):
            break
        if not in_inventory or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] == "Workflow" or set(cells[0]) <= {"-", ":"}:
            continue
        if cells[0].startswith("`") and cells[0].endswith("`"):
            inventory_rows.append((cells[0].strip("`"), cells[1]))

    seen: dict[str, list[str]] = defaultdict(list)
    for workflow_name, classification in inventory_rows:
        seen[workflow_name].append(classification)
        if workflow_name not in workflow_names:
            errors.append(
                f"{path.relative_to(ROOT)}: workflow inventory includes unknown workflow `{workflow_name}`"
            )
        if workflow_name not in expected_workflow_names:
            errors.append(
                f"{path.relative_to(ROOT)}: workflow `{workflow_name}` is not in the expected role matrix"
            )
        if classification not in ALLOWED_WORKFLOW_CLASSIFICATIONS:
            errors.append(
                f"{path.relative_to(ROOT)}: workflow `{workflow_name}` uses unknown classification `{classification}`"
            )
        elif (
            workflow_name in EXPECTED_WORKFLOW_CLASSIFICATIONS
            and classification != EXPECTED_WORKFLOW_CLASSIFICATIONS[workflow_name]
        ):
            errors.append(
                f"{path.relative_to(ROOT)}: workflow `{workflow_name}` classification must be `{EXPECTED_WORKFLOW_CLASSIFICATIONS[workflow_name]}`, got `{classification}`"
            )

    for workflow_name in sorted(workflow_names):
        if workflow_name not in seen:
            errors.append(
                f"{path.relative_to(ROOT)}: missing workflow coverage entry `{workflow_name}`"
            )
        elif len(seen[workflow_name]) != 1:
            errors.append(
                f"{path.relative_to(ROOT)}: workflow `{workflow_name}` must appear exactly once in Workflow Inventory"
            )
    for workflow_name in sorted(expected_workflow_names - workflow_names):
        errors.append(
            f"{path.relative_to(ROOT)}: expected role-matrix workflow `{workflow_name}` is missing from .github/workflows"
        )
    for workflow_name in sorted(workflow_names - expected_workflow_names):
        errors.append(
            f"{path.relative_to(ROOT)}: unexpected active workflow `{workflow_name}` must be added to the role matrix first"
        )
    return errors


def validate_security_branch_policy() -> list[str]:
    path = GITHUB_DIR / "SECURITY.md"
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    required_rows = {
        "main": "production security support",
        "dev": "integration security validation",
    }
    for branch, reason in required_rows.items():
        pattern = re.compile(rf"^\|\s*{branch}\s*\|.*\bYes\b", re.MULTILINE)
        if not pattern.search(text):
            errors.append(
                f"{path.relative_to(ROOT)}: missing supported `{branch}` row for {reason}"
            )
    return errors


def validate_duplicate_github_surfaces() -> list[str]:
    errors: list[str] = []
    basename_locations: dict[str, set[Path]] = defaultdict(set)
    content_locations: dict[str, list[Path]] = defaultdict(list)

    for path in sorted(GITHUB_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(GITHUB_DIR)
        basename_locations[path.name].add(rel)
        content_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        content_locations[content_hash].append(rel)

    for basename, locations in sorted(basename_locations.items()):
        if len(locations) <= 1:
            continue
        if ALLOWED_DUPLICATE_BASENAMES.get(basename) == locations:
            continue
        rendered = ", ".join(str(location) for location in sorted(locations))
        errors.append(
            f"{GITHUB_DIR.relative_to(ROOT)}: duplicate basename `{basename}` found in {rendered}"
        )

    for locations in content_locations.values():
        if len(locations) <= 1:
            continue
        rendered = ", ".join(str(location) for location in sorted(locations))
        errors.append(
            f"{GITHUB_DIR.relative_to(ROOT)}: duplicate file content found in {rendered}"
        )

    return errors


def validate_no_github_native_instruction_layer() -> list[str]:
    errors: list[str] = []
    forbidden_paths = [
        GITHUB_DIR / "copilot-instructions.md",
        GITHUB_DIR / "instructions",
    ]
    for path in forbidden_paths:
        if path.exists():
            errors.append(
                f"{path.relative_to(ROOT)}: GitHub-native AI instruction layer is prohibited"
            )
    return errors


def validate_derived_placeholders() -> list[str]:
    errors: list[str] = []
    for path in iter_github_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(ROOT)
        for marker, reason in DERIVED_REQUIRED_PLACEHOLDERS.items():
            if marker in text:
                errors.append(f"{rel}: unresolved derived-project placeholder `{marker}` ({reason})")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-derived",
        action="store_true",
        help="fail unresolved owner/repo/security/CODEOWNERS placeholders after bootstrap",
    )
    args = parser.parse_args()

    if not GITHUB_DIR.exists():
        print(".github directory is missing.", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors.extend(validate_text_drift())
    errors.extend(validate_labeler())
    errors.extend(validate_pr_template())
    errors.extend(validate_coverage_gate())
    errors.extend(validate_removed_workflow())
    errors.extend(validate_codeowners())
    errors.extend(validate_about_workflow_coverage())
    errors.extend(validate_security_branch_policy())
    errors.extend(validate_duplicate_github_surfaces())
    errors.extend(validate_no_github_native_instruction_layer())
    if args.strict_derived:
        errors.extend(validate_derived_placeholders())

    if errors:
        print("GitHub metadata validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GitHub metadata validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
