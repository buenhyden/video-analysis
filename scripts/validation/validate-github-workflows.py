#!/usr/bin/env python3
"""Validate repository GitHub Actions governance rules."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

WORKFLOW_DIR = Path(".github/workflows")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TAG_OR_BRANCH_RE = re.compile(r"^[A-Za-z0-9_./-]+$")
DIRECT_PROTECTED_PUSH_RE = re.compile(
    r"git\s+push(?:\s+--[A-Za-z0-9_=:/.-]+)*\s+origin\s+"
    r"(?:(?:refs/heads/)?(?:main|dev)|HEAD:(?:refs/heads/)?(?:main|dev))\b"
)
AUTO_MERGE_RE = re.compile(
    r"(gh\s+pr\s+merge|auto-merge|enablePullRequestAutoMerge)", re.IGNORECASE
)
STACK_PATH_RE = re.compile(r"\b(web|server|app|desktop|monitoring|tests)/")
SCRIPT_REF_RE = re.compile(r"\b(?:bash|python3?)\s+(scripts/[A-Za-z0-9_./-]+)")
CANONICAL_VALIDATE_CMD = "bash scripts/ws.sh validate"
REQUIRED_BRANCHES = {"main", "dev"}
PROHIBITED_EVENTS = {"pull_request_target"}
CHANGELOG_PR_HELPER = ".github/scripts/render-changelog-pr-body.mjs"
COVERAGE_GATE = ".github/gates/check-coverage.sh"
CHECKOUT_CREDENTIALS_ALLOWLIST = {
    ("generate-changelog.yml", "changelog", "Checkout main"),
}
ALLOWED_DUPLICATE_ACTIONS = {
    "actions/checkout",
    "actions/setup-python",
    "actions/upload-artifact",
}
IGNORED_DUPLICATE_RUN_PREFIXES = (
    "echo ",
    "cat <<",
)
EXPECTED_WORKFLOW_MATRIX = {
    "ai-remediation.yml": {
        "name": "CI Failure Diagnostics",
        "jobs": {"on-failure": "on-failure"},
        "allowed_actions": {"actions/checkout"},
        "required_actions": {"actions/checkout"},
        "script_refs": {"scripts/ws.sh", "scripts/ci/collect-context.sh"},
        "required_text": {
            "bash scripts/ws.sh info",
            "bash scripts/ci/collect-context.sh",
            "Policy: diagnostics only; no automatic protected-branch changes.",
        },
    },
    "autopilot-intelligence.yml": {
        "name": "Repository Intelligence",
        "jobs": {"intelligence": "Generate Intelligence"},
        "allowed_actions": {"actions/checkout", "actions/upload-artifact"},
        "required_actions": {"actions/checkout", "actions/upload-artifact"},
        "script_refs": {"scripts/ws.sh"},
        "required_text": {"bash scripts/ws.sh intelligence"},
    },
    "ci-global.yml": {
        "name": "Template CI / 템플릿 정합성 검증",
        "jobs": {
            "pre-commit": "Pre-commit Checks / 정적 분석 및 포맷팅",
            "verify-template": "Verify Template / 템플릿 검증",
            "test-coverage": "Test Coverage / conditional 90%",
        },
        "allowed_actions": {
            "actions/checkout",
            "actions/setup-python",
            "pre-commit/action",
        },
        "required_actions": {
            "actions/checkout",
            "actions/setup-python",
            "pre-commit/action",
        },
        "script_refs": {"scripts/ws.sh"},
        "required_text": {
            CANONICAL_VALIDATE_CMD,
            "bash .github/gates/check-coverage.sh",
            "COVERAGE_FILE",
            "Enforce conditional 90% coverage",
        },
    },
    "ci-security.yml": {
        "name": "Security CI",
        "jobs": {
            "security-audit": "Local security and secret checks",
            "codeql-analyze": "Optional CodeQL analysis",
        },
        "allowed_actions": {
            "actions/checkout",
            "actions/upload-artifact",
            "github/codeql-action/analyze",
            "github/codeql-action/init",
            "gitleaks/gitleaks-action",
        },
        "required_actions": {
            "actions/checkout",
            "actions/upload-artifact",
            "github/codeql-action/analyze",
            "github/codeql-action/init",
            "gitleaks/gitleaks-action",
        },
        "script_refs": {"scripts/ci/validate-security.sh"},
        "required_text": {
            "bash scripts/ci/validate-security.sh",
            "gitleaks-report",
            "languages: actions",
            "CODE_SCANNING_REQUIRED",
        },
    },
    "generate-changelog.yml": {
        "name": "Generate Changelog",
        "jobs": {"changelog": "Generate changelog PR"},
        "allowed_actions": {
            "actions/checkout",
            "actions/github-script",
            "orhun/git-cliff-action",
        },
        "required_actions": {
            "actions/checkout",
            "actions/github-script",
            "orhun/git-cliff-action",
        },
        "script_refs": set(),
        "required_text": {
            'BRANCH="chore/changelog-${RELEASE_TAG}"',
            CHANGELOG_PR_HELPER,
            "github.rest.pulls.create",
            "github.rest.pulls.update",
            "base: 'main'",
        },
    },
    "greetings.yml": {
        "name": "Greeting",
        "jobs": {"greeting": "greeting"},
        "allowed_actions": {"actions/first-interaction"},
        "required_actions": {"actions/first-interaction"},
        "script_refs": set(),
        "required_text": set(),
    },
    "labeler.yml": {
        "name": "Pull Request Labeler",
        "jobs": {"triage": "triage"},
        "allowed_actions": {"actions/labeler"},
        "required_actions": {"actions/labeler"},
        "script_refs": set(),
        "required_text": set(),
    },
    "stale.yml": {
        "name": "Close Stale Issues and PRs",
        "jobs": {"stale": "stale"},
        "allowed_actions": {"actions/stale"},
        "required_actions": {"actions/stale"},
        "script_refs": set(),
        "required_text": set(),
    },
}


def is_first_party_action(ref: str) -> bool:
    return ref.startswith("actions/")


def iter_runs(job: dict[str, Any]) -> str:
    chunks: list[str] = []
    for step in job.get("steps", []) or []:
        if isinstance(step, dict) and isinstance(step.get("run"), str):
            chunks.append(step["run"])
    return "\n".join(chunks)


def workflow_on(data: dict[str, Any]) -> Any:
    return data.get("on", data.get(True, {}))


def workflow_event_names(on_block: Any) -> set[str]:
    if isinstance(on_block, str):
        return {on_block}
    if isinstance(on_block, list) and all(isinstance(item, str) for item in on_block):
        return set(on_block)
    if isinstance(on_block, dict):
        return {str(key) for key in on_block.keys()}
    return set()


def workflow_run_text(data: dict[str, Any]) -> str:
    jobs = data.get("jobs")
    if not isinstance(jobs, dict):
        return ""
    return "\n".join(
        iter_runs(job) for job in jobs.values() if isinstance(job, dict)
    )


def workflow_has_write_permissions(data: dict[str, Any]) -> bool:
    jobs = data.get("jobs")
    if not isinstance(jobs, dict):
        return False
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        permissions = job.get("permissions")
        if isinstance(permissions, str) and "write" in permissions:
            return True
        if isinstance(permissions, dict) and any(
            value in {"write", "write-all"} for value in permissions.values()
        ):
            return True
    return False


def codeql_languages_include_actions(step: dict[str, Any]) -> bool:
    uses = step.get("uses")
    if not isinstance(uses, str):
        return False
    action = uses.rsplit("@", 1)[0].lower()
    if action != "github/codeql-action/init":
        return False
    with_block = step.get("with")
    if not isinstance(with_block, dict):
        return False
    languages = with_block.get("languages")
    if isinstance(languages, str):
        return "actions" in {
            language.strip() for language in languages.split(",") if language.strip()
        }
    if isinstance(languages, list):
        return "actions" in {str(language).strip() for language in languages}
    return False


def step_uses_action(step: dict[str, Any], expected_action: str) -> bool:
    uses = step.get("uses")
    if not isinstance(uses, str):
        return False
    return uses.rsplit("@", 1)[0].lower() == expected_action


def workflow_action_names(data: dict[str, Any]) -> set[str]:
    actions: set[str] = set()
    jobs = data.get("jobs")
    if not isinstance(jobs, dict):
        return actions
    for job in jobs.values():
        if not isinstance(job, dict):
            continue
        steps = job.get("steps")
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            if isinstance(uses, str) and "@" in uses:
                actions.add(uses.rsplit("@", 1)[0].lower())
    return actions


def job_display_name(job_id: str, job: dict[str, Any]) -> str:
    name = job.get("name")
    return name if isinstance(name, str) and name else job_id


def normalize_branches(value: Any) -> set[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        return {value}
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return set(value)
    return set()


def validate_branch_filters(path: Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    on_block = workflow_on(data)
    if not isinstance(on_block, dict):
        for event_name in sorted(workflow_event_names(on_block) & {"push", "pull_request"}):
            errors.append(
                f"{path}: `{event_name}` must use explicit branches {sorted(REQUIRED_BRANCHES)}"
            )
        return errors
    for event_name in ("push", "pull_request"):
        event = on_block.get(event_name)
        if not isinstance(event, dict):
            continue
        if event_name == "push" and "tags" in event and "branches" not in event:
            continue
        branches = normalize_branches(event.get("branches"))
        if branches != REQUIRED_BRANCHES:
            errors.append(
                f"{path}: `{event_name}` branches must be {sorted(REQUIRED_BRANCHES)}, got {sorted(branches or [])}"
            )
    workflow_run = on_block.get("workflow_run")
    if isinstance(workflow_run, dict):
        branches = normalize_branches(workflow_run.get("branches"))
        if branches != REQUIRED_BRANCHES:
            errors.append(
                f"{path}: `workflow_run` branches must be {sorted(REQUIRED_BRANCHES)}, got {sorted(branches or [])}"
            )
    return errors


def requires_concurrency(data: dict[str, Any]) -> bool:
    on_block = workflow_on(data)
    event_names = workflow_event_names(on_block)
    if {"pull_request", "workflow_run", "schedule"} & event_names:
        return True
    if workflow_has_write_permissions(data):
        return True
    if not isinstance(on_block, dict):
        return False
    push = on_block.get("push")
    return isinstance(push, dict) and ("branches" in push or "tags" in push)


def validate_events(path: Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    on_block = workflow_on(data)
    event_names = workflow_event_names(on_block)
    for event_name in sorted(PROHIBITED_EVENTS & event_names):
        errors.append(f"{path}: `{event_name}` is prohibited for this template")
    if requires_concurrency(data) and "concurrency" not in data:
        errors.append(
            f"{path}: branch/workflow-run/schedule/tag/write workflows must declare top-level `concurrency`"
        )
    return errors


def validate_permissions(prefix: str, permissions: Any) -> list[str]:
    errors: list[str] = []
    if isinstance(permissions, str):
        errors.append(f"{prefix}: `permissions` must be a least-privilege mapping")
        if permissions == "write-all":
            errors.append(f"{prefix}: `permissions: write-all` is prohibited")
        return errors
    if not isinstance(permissions, dict):
        errors.append(f"{prefix}: `permissions` must be a mapping")
        return errors
    for scope, value in permissions.items():
        if value == "write-all":
            errors.append(f"{prefix}: `{scope}: write-all` is prohibited")
    return errors


def token_env_is_used(run_text: str, token_name: str) -> bool:
    return token_name in run_text


def checkout_persists_credentials(step: dict[str, Any]) -> bool:
    with_block = step.get("with")
    if not isinstance(with_block, dict):
        return True
    value = with_block.get("persist-credentials")
    return value is True or (isinstance(value, str) and value.lower() == "true")


def checkout_credentials_allowed(path: Path, job_id: str, step: dict[str, Any]) -> bool:
    step_name = step.get("name", "")
    return (path.name, job_id, step_name) in CHECKOUT_CREDENTIALS_ALLOWLIST


def validate_workflow(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report parser detail
        return [f"{path}: YAML parse failed: {exc}"]

    if not isinstance(data, dict):
        return [f"{path}: workflow must be a mapping"]

    for key in ("name", "jobs"):
        if key not in data:
            errors.append(f"{path}: missing required top-level key `{key}`")
    if "permissions" in data:
        errors.append(
            f"{path}: workflow-level `permissions` is prohibited; set job-level permissions"
        )
    if "on" not in data and True not in data:
        errors.append(f"{path}: missing required top-level key `on`")
    errors.extend(validate_branch_filters(path, data))
    errors.extend(validate_events(path, data))

    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        errors.append(f"{path}: `jobs` must be a non-empty mapping")
        return errors

    for job_id, job in jobs.items():
        if not isinstance(job, dict):
            errors.append(f"{path}: job `{job_id}` must be a mapping")
            continue
        prefix = f"{path}: job `{job_id}`"
        if not job.get("runs-on"):
            errors.append(f"{prefix}: missing `runs-on`")
        if "permissions" not in job:
            errors.append(f"{prefix}: missing job-level `permissions`")
        else:
            errors.extend(validate_permissions(prefix, job.get("permissions")))
        if "timeout-minutes" not in job:
            errors.append(f"{prefix}: missing `timeout-minutes`")
        steps = job.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"{prefix}: `steps` must be non-empty")
            continue

        codeql_actions_analysis = any(
            isinstance(step, dict) and codeql_languages_include_actions(step)
            for step in steps
        )
        run_text = iter_runs(job)
        if DIRECT_PROTECTED_PUSH_RE.search(run_text):
            errors.append(f"{prefix}: direct push to protected branch is prohibited")
        if AUTO_MERGE_RE.search(run_text):
            errors.append(f"{prefix}: auto-merge behavior is prohibited")
        for script_ref in SCRIPT_REF_RE.findall(run_text):
            if not Path(script_ref).exists():
                errors.append(f"{prefix}: references missing script `{script_ref}`")
        if STACK_PATH_RE.search(run_text):
            errors.append(
                f"{prefix}: active workflow references stack/example path; keep stack workflows under examples/"
            )
        permissions = job.get("permissions")
        if (
            isinstance(permissions, dict)
            and permissions.get("pull-requests") == "write"
            and AUTO_MERGE_RE.search(run_text)
        ):
            errors.append(
                f"{prefix}: pull-requests: write cannot combine with auto-merge"
            )

        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                errors.append(f"{prefix}: step {index} must be a mapping")
                continue
            if codeql_actions_analysis and step_uses_action(
                step, "github/codeql-action/autobuild"
            ):
                errors.append(
                    f"{prefix}: step {index} must not run CodeQL autobuild for `languages: actions`"
                )
            step_run = step.get("run")
            step_env = step.get("env")
            if isinstance(step_run, str) and isinstance(step_env, dict):
                for token_name in ("GITHUB_TOKEN", "GH_TOKEN"):
                    if token_name in step_env and not token_env_is_used(
                        step_run, token_name
                    ):
                        errors.append(
                            f"{prefix}: step {index} declares unused `{token_name}` env"
                        )
            uses = step.get("uses")
            if not isinstance(uses, str):
                continue
            if "@" not in uses:
                errors.append(f"{prefix}: step {index} action `{uses}` missing ref")
                continue
            action, ref = uses.rsplit("@", 1)
            if action == "actions/checkout" and checkout_persists_credentials(step):
                if not checkout_credentials_allowed(path, job_id, step):
                    errors.append(
                        f"{prefix}: step {index} checkout must set `persist-credentials: false`"
                    )
            if is_first_party_action(action):
                continue
            if not FULL_SHA_RE.fullmatch(ref):
                errors.append(
                    f"{prefix}: step {index} third-party action `{uses}` must pin a full SHA"
                )
            elif not TAG_OR_BRANCH_RE.fullmatch(ref):
                errors.append(f"{prefix}: step {index} action ref `{ref}` is invalid")

    return errors


def validate_workflow_roles(workflow_data: dict[Path, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    removed = WORKFLOW_DIR / "governance-check.yml"
    if removed.exists():
        errors.append(f"{removed}: duplicate governance workflow must remain removed")

    canonical_runners = [
        path
        for path, data in workflow_data.items()
        if CANONICAL_VALIDATE_CMD in workflow_run_text(data)
    ]
    if canonical_runners != [WORKFLOW_DIR / "ci-global.yml"]:
        errors.append(
            "canonical validation command must run only in .github/workflows/ci-global.yml; "
            f"found {[str(path) for path in canonical_runners]}"
        )
    changelog_path = WORKFLOW_DIR / "generate-changelog.yml"
    changelog_data = workflow_data.get(changelog_path)
    if changelog_data is not None:
        if CHANGELOG_PR_HELPER not in workflow_run_text(changelog_data):
            errors.append(
                f"{changelog_path}: changelog PR body must be rendered by `{CHANGELOG_PR_HELPER}`"
            )
        if not Path(CHANGELOG_PR_HELPER).exists():
            errors.append(f"{changelog_path}: missing helper `{CHANGELOG_PR_HELPER}`")
        changelog_text = yaml.safe_dump(changelog_data, sort_keys=True)
        if "github.rest.pulls.update" not in changelog_text:
            errors.append(
                f"{changelog_path}: existing changelog PRs must be updated, not only detected"
            )
    return errors


def validate_workflow_role_matrix(workflow_data: dict[Path, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    expected_names = set(EXPECTED_WORKFLOW_MATRIX)
    actual_names = {path.name for path in workflow_data}
    missing = expected_names - actual_names
    unexpected = actual_names - expected_names

    for workflow_name in sorted(missing):
        errors.append(f"{WORKFLOW_DIR / workflow_name}: expected active workflow is missing")
    for workflow_name in sorted(unexpected):
        errors.append(
            f"{WORKFLOW_DIR / workflow_name}: unexpected active workflow; update the role matrix before adding workflows"
        )

    workflow_name_locations: dict[str, list[str]] = defaultdict(list)
    job_id_locations: dict[str, list[str]] = defaultdict(list)
    job_display_locations: dict[str, list[str]] = defaultdict(list)

    for path, data in workflow_data.items():
        workflow_name = data.get("name")
        if isinstance(workflow_name, str):
            workflow_name_locations[workflow_name].append(str(path))
        jobs = data.get("jobs")
        if not isinstance(jobs, dict):
            continue
        for job_id, job in jobs.items():
            if not isinstance(job, dict):
                continue
            job_id_locations[str(job_id)].append(str(path))
            job_display_locations[job_display_name(str(job_id), job)].append(
                f"{path}: job `{job_id}`"
            )

    for workflow_name, locations in sorted(workflow_name_locations.items()):
        if len(locations) > 1:
            errors.append(
                f"duplicate workflow display name `{workflow_name}` appears in {locations}"
            )
    for job_id, locations in sorted(job_id_locations.items()):
        if len(locations) > 1:
            errors.append(f"duplicate workflow job id `{job_id}` appears in {locations}")
    for display_name, locations in sorted(job_display_locations.items()):
        if len(locations) > 1:
            errors.append(
                f"duplicate workflow job display name `{display_name}` appears in {locations}"
            )

    for path, data in sorted(workflow_data.items()):
        policy = EXPECTED_WORKFLOW_MATRIX.get(path.name)
        if policy is None:
            continue
        expected_name = policy["name"]
        actual_name = data.get("name")
        if actual_name != expected_name:
            errors.append(
                f"{path}: workflow name must stay `{expected_name}`, got `{actual_name}`"
            )

        jobs = data.get("jobs")
        if not isinstance(jobs, dict):
            continue
        expected_jobs = policy["jobs"]
        actual_jobs = set(jobs)
        if actual_jobs != set(expected_jobs):
            errors.append(
                f"{path}: jobs must be {sorted(expected_jobs)}, got {sorted(actual_jobs)}"
            )
        for job_id, expected_display in expected_jobs.items():
            job = jobs.get(job_id)
            if not isinstance(job, dict):
                continue
            actual_display = job_display_name(job_id, job)
            if actual_display != expected_display:
                errors.append(
                    f"{path}: job `{job_id}` display name must stay `{expected_display}`, got `{actual_display}`"
                )

        actions = workflow_action_names(data)
        allowed_actions = set(policy["allowed_actions"])
        required_actions = set(policy["required_actions"])
        extra_actions = actions - allowed_actions
        missing_actions = required_actions - actions
        if extra_actions:
            errors.append(
                f"{path}: workflow role uses unexpected actions {sorted(extra_actions)}"
            )
        if missing_actions:
            errors.append(
                f"{path}: workflow role is missing required actions {sorted(missing_actions)}"
            )

        run_text = workflow_run_text(data)
        script_refs = set(SCRIPT_REF_RE.findall(run_text))
        expected_script_refs = set(policy["script_refs"])
        if script_refs != expected_script_refs:
            errors.append(
                f"{path}: workflow role script refs must be {sorted(expected_script_refs)}, got {sorted(script_refs)}"
            )
        for required_text in sorted(policy["required_text"]):
            if required_text not in yaml.safe_dump(data, sort_keys=True) and required_text not in run_text:
                errors.append(
                    f"{path}: workflow role is missing required marker `{required_text}`"
                )
    return errors


def normalize_run_signature(run_text: str) -> str | None:
    lines = []
    for raw_line in run_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(re.sub(r"\s+", " ", line))
    if not lines:
        return None
    normalized = " && ".join(lines)
    if normalized.startswith(IGNORED_DUPLICATE_RUN_PREFIXES):
        return None
    return f"run:{normalized}"


def normalize_step_signature(step: dict[str, Any]) -> str | None:
    uses = step.get("uses")
    if isinstance(uses, str) and "@" in uses:
        action = uses.rsplit("@", 1)[0].lower()
        if action in ALLOWED_DUPLICATE_ACTIONS:
            return None
        return f"uses:{action}"
    run_text = step.get("run")
    if isinstance(run_text, str):
        return normalize_run_signature(run_text)
    return None


def validate_duplicate_jobs_and_steps(workflow_data: dict[Path, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    step_locations: dict[str, list[str]] = defaultdict(list)
    job_signatures: dict[tuple[str, ...], list[str]] = defaultdict(list)

    for path, data in workflow_data.items():
        jobs = data.get("jobs")
        if not isinstance(jobs, dict):
            continue
        for job_id, job in jobs.items():
            if not isinstance(job, dict):
                continue
            steps = job.get("steps")
            if not isinstance(steps, list):
                continue
            meaningful_steps: list[str] = []
            for index, step in enumerate(steps, start=1):
                if not isinstance(step, dict):
                    continue
                signature = normalize_step_signature(step)
                if signature is None:
                    continue
                location = f"{path}: job `{job_id}` step {index}"
                step_locations[signature].append(location)
                meaningful_steps.append(signature)
            if len(meaningful_steps) >= 2:
                job_signatures[tuple(meaningful_steps)].append(f"{path}: job `{job_id}`")

    for signature, locations in sorted(step_locations.items()):
        if len(locations) > 1:
            errors.append(
                "duplicate meaningful workflow step detected: "
                f"{signature} appears in {locations}"
            )
    for signature, locations in sorted(job_signatures.items()):
        if len(locations) > 1:
            errors.append(
                "duplicate meaningful workflow job detected: "
                f"{list(signature)} appears in {locations}"
            )
    return errors


def validate_coverage_gate_contract() -> list[str]:
    errors: list[str] = []
    path = Path(COVERAGE_GATE)
    if not path.exists():
        return [f"{COVERAGE_GATE}: coverage gate script is missing"]

    text = path.read_text(encoding="utf-8", errors="ignore")
    required_markers = {
        "has_active_stack_manifest",
        "QUALITY GATE SKIPPED",
        "package.json",
        "pyproject.toml",
        "go.mod",
        "Cargo.toml",
    }
    for marker in sorted(required_markers):
        if marker not in text:
            errors.append(
                f"{COVERAGE_GATE}: missing conditional coverage marker `{marker}`"
            )
    return errors


def main() -> int:
    workflows = sorted(WORKFLOW_DIR.glob("*.yml"))
    if not workflows:
        print("No GitHub Actions workflows found.", file=sys.stderr)
        return 1

    errors: list[str] = []
    workflow_data: dict[Path, dict[str, Any]] = {}
    for path in workflows:
        errors.extend(validate_workflow(path))
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict):
            workflow_data[path] = data
    errors.extend(validate_workflow_roles(workflow_data))
    errors.extend(validate_workflow_role_matrix(workflow_data))
    errors.extend(validate_duplicate_jobs_and_steps(workflow_data))
    errors.extend(validate_coverage_gate_contract())

    if errors:
        print("GitHub workflow governance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"GitHub workflow governance validation passed ({len(workflows)} workflows).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
