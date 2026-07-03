#!/usr/bin/env python3
"""Validate template-readiness details that are easy to miss in Markdown lint."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_DOC_DIRS = [
    "00.agent-governance",
    "01.requirements",
    "02.architecture",
    "03.specs",
    "04.execution",
    "05.operations",
    "90.references",
    "99.templates",
]
CANONICAL_STAGE_DIRS = [
    "01.requirements",
    "02.architecture/requirements",
    "02.architecture/decisions",
    "03.specs",
    "04.execution/plans",
    "04.execution/tasks",
    "05.operations/guides",
    "05.operations/policies",
    "05.operations/runbooks",
    "05.operations/incidents",
    "90.references",
]
CANONICAL_STAGE_TEMPLATE_CONTRACTS: list[tuple[str, list[tuple[str, list[str]]]]] = [
    (
        "docs/01.requirements/",
        [
            (
                "prd.template.md",
                ["## Vision", "## Functional Requirements", "## Acceptance Criteria"],
            )
        ],
    ),
    (
        "docs/02.architecture/requirements/",
        [
            (
                "ard.template.md",
                [
                    "## Quality Attributes",
                    "## System Overview & Context",
                    "## DDD Strategic Design",
                ],
            ),
            (
                "expanded/bounded-context.template.md",
                [
                    "## Context Summary",
                    "## Purpose & Responsibility",
                    "## Context Boundaries",
                ],
            ),
            (
                "expanded/ubiquitous-language.template.md",
                [
                    "## Bounded Context",
                    "## Glossary",
                    "## Homonyms & Context Collisions",
                ],
            ),
        ],
    ),
    (
        "docs/02.architecture/decisions/",
        [
            (
                "adr.template.md",
                [
                    "## Status",
                    "## Context",
                    "## Decision",
                    "## Consequences",
                    "## Alternatives",
                ],
            )
        ],
    ),
    (
        "docs/03.specs/",
        [
            (
                "spec.template.md",
                [
                    "## Core Design",
                    "## Component Interaction & Sequence (SDD)",
                    "## TDD Readiness (Mandatory Before `docs/04.execution/plans/`)",
                ],
            ),
            (
                "api-spec.template.md",
                [
                    "## Parent Spec",
                    "## API Style",
                    "## Endpoint / Operation Catalog",
                ],
            ),
            (
                "tests.template.md",
                ["## Parent Documents", "## TDD Scope", "## Test Matrix"],
            ),
            (
                "expanded/tactical-model.template.md",
                [
                    "## 1. Domain Model (Logical)",
                    "## 2. Data Model (Physical)",
                    "## 3. Migration & Compatibility",
                ],
            ),
            (
                "expanded/domain-model.template.md",
                ["## Aggregates", "## Entities", "## Repository Contracts"],
            ),
            (
                "expanded/domain-events.template.md",
                ["## Event Catalog", "## Event Schemas", "## Event Flow Diagram"],
            ),
        ],
    ),
    (
        "docs/04.execution/plans/",
        [
            (
                "plan.template.md",
                ["## Work Breakdown", "## Verification Plan", "## Risks & Mitigations"],
            )
        ],
    ),
    (
        "docs/04.execution/tasks/",
        [
            (
                "task.template.md",
                [
                    "## Inputs",
                    "## Task Table",
                    "## Verification Summary",
                    "## TDD Evidence Protocol",
                ],
            )
        ],
    ),
    (
        "docs/05.operations/guides/",
        [
            (
                "guide.template.md",
                [
                    "## Target Audience",
                    "## Step-by-step Instructions",
                    "## Troubleshooting",
                ],
            )
        ],
    ),
    (
        "docs/05.operations/policies/",
        [
            (
                "operation.template.md",
                ["## Policy Scope", "## Controls", "## Verification"],
            ),
            (
                "slo.template.md",
                [
                    "## 1. Service Context",
                    "## 2. Service Level Objectives (SLOs)",
                    "## 3. Error Budget Policy",
                ],
            ),
        ],
    ),
    (
        "docs/05.operations/runbooks/",
        [
            (
                "runbook.template.md",
                [
                    "## When to Use",
                    "## Procedure or Checklist",
                    "## Safe Rollback or Recovery Procedure",
                    "## Escalation Path",
                ],
            )
        ],
    ),
    (
        "docs/05.operations/incidents/",
        [
            (
                "incident.template.md",
                [
                    "## Incident Metadata",
                    "## Incident Summary",
                    "## Impact",
                    "## Timeline",
                    "## Evidence",
                ],
            ),
            (
                "postmortem.template.md",
                [
                    "## Incident Summary",
                    "## Root Cause Analysis",
                    "## Action Items",
                    "## Prevention and Verification",
                ],
            ),
        ],
    ),
    (
        "docs/90.references/",
        [
            (
                "reference.template.md",
                [
                    "## Objectives",
                    "## Reference Classification",
                    "## Definitions / Facts",
                    "## Sources",
                ],
            )
        ],
    ),
]
REQUIRED_CANONICAL_FRONTMATTER_FIELDS = {
    "title",
    "version",
    "owner",
    "layer",
    "stage",
    "status",
    "last-updated",
}
REQUIRED_CANONICAL_TEMPLATE_SECTIONS = [
    "## AI Execution Checklist",
    "## Related Documents",
]
LEGACY_TEMPLATE_CONFORMANCE_BASELINE: dict[str, str] = {}
STALE_SCAN_PATHS = [
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / "GEMINI.md",
    ROOT / ".claude",
    ROOT / "scripts",
    ROOT / "docs/LLM-WIKI.md",
    ROOT / "docs/05.operations/guides",
    ROOT / "docs/05.operations/policies",
    ROOT / "docs/90.references",
    ROOT / "docs/00.agent-governance",
    ROOT / ".codex",
    ROOT / ".agents",
    ROOT / ".agent",
]
AT_IMPORT_SCAN_PATHS = [
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / "GEMINI.md",
    ROOT / ".claude/CLAUDE.md",
    ROOT / "docs/00.agent-governance",
]
STALE_PATTERNS = {
    r"\bdevelop\b": "use `dev` for the active integration branch",
    r"implementation_plan\.md": "use execution plan paths under `docs/04.execution/plans/`",
    r"\btask\.md\b": "use execution task paths under `docs/04.execution/tasks/`",
    r"Transcendent": "use audit-ready template wording",
    r"Immortal": "use audit-ready template wording",
    r"Soul of the Repository": "use explicit governance wording",
    r"AGENTS\.md\s*/\s*AGENTS\.md": "reference `AGENTS.md / CLAUDE.md / GEMINI.md` correctly",
    r"AGENTS\.md\s*§\d+": "reference stable AGENTS.md section names or canonical governance files",
    r"Escallation": "fix typo to `Escalation`",
    "security"
    + r"_reminder_hook\.py": "use the active Claude hook files and CI/CD governance rule",
    r"`\.github/\*\*`or": "add a space after the inline `.github/**` marker",
    "with" + r"`rules/": "add a space before inline governance rule links",
    r"14\s+mandatory\s+folders": "use the current 8-folder compact docs policy",
    r"14\s+allowed\s+top-level\s+folders": "use the current 8-folder compact docs policy",
    r"14" + r"-folder": "use the current 8-folder compact docs policy",
    r"13\s+authorized\s+ones": "use the current 8-folder compact docs policy",
    r"docs/02~04": "use explicit compact paths under `docs/02.architecture/` and `docs/03.specs/`",
    r"docs/05~06": "use explicit compact paths under `docs/04.execution/plans/` and `docs/04.execution/tasks/`",
    r"docs/07~09": "use explicit compact paths under `docs/05.operations/` and `docs/90.references/`",
    r"docs/08~09": "use explicit compact operations paths under `docs/05.operations/`",
    r"docs/05\.plans/": "use `docs/04.execution/plans/` in the compact docs model",
    r"docs/06\.tasks/": "use `docs/04.execution/tasks/` in the compact docs model",
    r"docs/07\.guides/": "use `docs/05.operations/guides/` in the compact docs model",
    r"docs/08\.operations/": "use `docs/05.operations/policies/` in the compact docs model",
    r"docs/09\.runbooks/": "use `docs/05.operations/runbooks/` in the compact docs model",
    r"docs/10\.incidents/": "use `docs/05.operations/incidents/` in the compact docs model",
    r"root\s+`LLM-WIKI\.md`": "use `docs/LLM-WIKI.md` for the canonical LLM-WIKI path",
    r"\|\s*\*\*05\*\*\s*\|\s*`05\.operations/`": "use Stage 07-10 rows for operations subfolders",
    r"\." + r"Codex/": "use the active `.claude/` runtime path",
    r"ws\s+propose": "removed ws command",
    r"ws\s+fix": "removed ws command",
    r"ws\s+quality": "removed ws command",
    r"ws\s+architect": "removed ws command",
    r"ws\s+pipeline": "removed ws command",
    "H"
    + "100": "do not keep external harness labels in active governance/runtime surfaces",
    "Harness"
    + "-100": "do not keep external harness labels in active governance/runtime surfaces",
    "harness"
    + "-100": "do not keep external harness labels in active governance/runtime surfaces",
    "file"
    + r"://": "shared repository outputs must use relative repository paths, not machine-specific file URLs",
}
STAGE00_REQUIRED_RULES = [
    "agentic.md",
    "bootstrap.md",
    "harness-library.md",
    "persona.md",
    "preflight-checklist.md",
    "project-initialization-intake.md",
    "release-process.md",
    "stage-gate-matrix.md",
    "standards.md",
    "subagent-protocol.md",
    "template-document-lifecycle.md",
]
# Paths authorized in documentation-protocol.md §13 as "retained on dev" or
# "may omit on main". Referenced in governance docs but absent on main by design.
AUTHORIZED_OPTIONAL_DOC_PATHS: set[str] = {
    "docs/02.architecture/requirements/research/",
    "docs/05.operations/policies/post-launch/",
    "docs/05.operations/policies/resilience/",
    "docs/90.references/knowledge/",
}
REQUIRED_TOP_LEVEL_README_SECTIONS = [
    "## Purpose & Scope",
    "### In Scope",
    "### Out of Scope",
    "## Mandatory Templates",
    "## Naming Rules",
    "## Lifecycle Rules",
    "## Cross-Reference Rules",
    "## Usage Examples",
    "## AI Authoring Guidance",
    "## AI Execution Checklist",
    "## Documents",
    "## Related Documents",
]
TEMPLATE_CLASSIFICATION_MARKERS = [
    "## Template Classification",
    "Core templates",
    "Optional expanded templates",
    "Optional technology-specific templates",
    "Machine-readable templates",
]
UNINITIALIZED_TEMPLATE_INVENTORY_CELLS = {"<string>", "YYYY-MM-DD"}
PATH_LABEL_SUFFIXES = (
    ".md",
    ".yaml",
    ".yml",
    ".graphql",
    ".proto",
    ".sh",
    ".py",
    ".toml",
    ".json",
)
ROOT_README_REQUIRED_SECTIONS = [
    "## Overview",
    "## Audience",
    "## Scope",
    "### In Scope",
    "### Out of Scope",
    "## Structure",
    "## How to Work in This Area",
]
SUPPORTING_README_REQUIRED_SECTIONS = [
    "## Overview",
    "## Audience",
    "## Scope",
    "### In Scope",
    "### Out of Scope",
    "## Structure",
    "## How to Work in This Area",
]
RELEASE_SKELETON_READMES = {
    "docs/01.requirements/README.md",
    "docs/02.architecture/README.md",
    "docs/02.architecture/requirements/README.md",
    "docs/02.architecture/decisions/README.md",
    "docs/03.specs/README.md",
    "docs/04.execution/README.md",
    "docs/04.execution/plans/README.md",
    "docs/04.execution/tasks/README.md",
    "docs/05.operations/README.md",
    "docs/05.operations/guides/README.md",
    "docs/05.operations/policies/README.md",
    "docs/05.operations/runbooks/README.md",
    "docs/05.operations/incidents/README.md",
    "docs/90.references/README.md",
}
README_INDEX_SUFFIXES = {".md", ".yaml", ".yml", ".graphql", ".proto"}
QA_SCOPE = ROOT / "docs/00.agent-governance/scopes/qa.md"
TESTS_TEMPLATE = ROOT / "docs/99.templates/tests.template.md"
PROGRESS_TEMPLATE = ROOT / "docs/99.templates/progress.template.md"
PROGRESS_MEMORY = ROOT / "docs/00.agent-governance/memory/progress.md"
SDLC_WORKFLOW = ROOT / "docs/00.agent-governance/sdlc-workflow.md"
EXTERNAL_DOT_AGENT_GOVERNANCE_SDLC_WORKFLOW = (
    ROOT / "00.agent-governance/sdlc-workflow.md"
)
EXTERNAL_SYSTEM_SDLC_WORKFLOW = ROOT / "00_System/sdlc-workflow.md"
TEMPLATE_TARGET_RELATIVE_RULES = {
    "docs/99.templates/ard.template.md": {
        "required": [
            "`[../../03.specs/<feature-id>/domain-model.md]`",
            "`[../decisions/####-<short-title>.md]`",
            "`[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../../03.specs/<feature-id>/spec.md]`",
            "`[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`",
        ],
        "forbidden": [
            "`[../03.specs/<feature-id>/domain-model.md]`",
            "`[../02.architecture/decisions/####-<short-title>.md]`",
            "`[../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
        ],
    },
    "docs/99.templates/adr.template.md": {
        "required": [
            "`[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../requirements/####-<system-or-domain>.md]`",
            "`[../../03.specs/<feature-id>/spec.md]`",
            "`[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`",
        ],
        "forbidden": [
            "`[../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../02.architecture/requirements/####-<system-or-domain>.md]`",
            "`[../03.specs/<feature-id>/spec.md]`",
            "`[../04.execution/plans/YYYY-MM-DD-<feature>.md]`",
        ],
    },
    "docs/99.templates/plan.template.md": {
        "required": [
            "`[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../../02.architecture/requirements/####-<system-or-domain>.md]`",
            "`[../../03.specs/<feature-id>/spec.md]`",
            "`[../../02.architecture/decisions/####-<short-title>.md]`",
        ],
        "forbidden": [
            "`[../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../02.architecture/requirements/####-<system-or-domain>.md]`",
            "`[../03.specs/<feature-id>/spec.md]`",
            "`[../02.architecture/decisions/####-<short-title>.md]`",
        ],
    },
    "docs/99.templates/task.template.md": {
        "required": [
            "`[../../03.specs/<feature-id>/spec.md]`",
            "`[../plans/YYYY-MM-DD-<feature>.md]`",
            "`[../../03.specs/<feature-id>/tests.md]`",
        ],
        "forbidden": [
            "`[../03.specs/<feature-id>/spec.md]`",
            "`[../04.execution/plans/YYYY-MM-DD-<feature>.md]`",
            "`[../03.specs/<feature-id>/tests.md]`",
        ],
    },
    "docs/99.templates/guide.template.md": {
        "required": [
            "`[../../03.specs/<feature-id>/spec.md]`",
            "`[../policies/<policy-or-standard>.md]`",
            "`[../runbooks/<topic>.md]`",
        ],
        "forbidden": [
            "`[../03.specs/<feature-id>/spec.md]`",
            "`[../05.operations/policies/<policy-or-standard>.md]`",
            "`[../05.operations/runbooks/<topic>.md]`",
        ],
    },
    "docs/99.templates/runbook.template.md": {
        "required": [
            "`[../../02.architecture/requirements/####-<system-or-domain>.md]`",
            "`[../../02.architecture/decisions/####-<short-title>.md]`",
            "`[../../03.specs/<feature-id>/spec.md]`",
            "`[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`",
            "`[../incidents/YYYY/INC-###-<incident-title>/record.md]`",
            "`[../policies/<policy-or-standard>.md]`",
        ],
        "forbidden": [
            "`[../02.architecture/requirements/####-<system-or-domain>.md]`",
            "`[../03.specs/<feature-id>/spec.md]`",
            "`[../05.operations/incidents/YYYY/INC-###-<incident-title>/record.md]`",
            "`[../05.operations/policies/<policy-or-standard>.md]`",
        ],
    },
    "docs/99.templates/operation.template.md": {
        "required": [
            "`[../../02.architecture/requirements/####-<system-or-domain>.md]`",
            "`[../runbooks/####-<topic>.md]`",
            "`[../incidents/YYYY/INC-###-<incident-title>/postmortem.md]`",
        ],
        "forbidden": [
            "`[../02.architecture/requirements/####-<system-or-domain>.md]`",
            "`[../05.operations/runbooks/####-<topic>.md]`",
            "`[../05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md]`",
        ],
    },
    "docs/99.templates/incident.template.md": {
        "required": [
            "`[../../../runbooks/####-<topic>.md]`",
            "`[../../../policies/<policy-or-standard>.md]`",
            "`[./postmortem.md]`",
        ],
        "forbidden": [
            "`[../../../05.operations/runbooks/####-<topic>.md]`",
            "`[../../../05.operations/policies/<policy-or-standard>.md]`",
        ],
    },
    "docs/99.templates/postmortem.template.md": {
        "required": [
            "`[../../../runbooks/####-<topic>.md]`",
            "`[../../../policies/<policy-or-standard>.md]`",
            "`[./record.md]`",
        ],
        "forbidden": [
            "`[../../../05.operations/runbooks/####-<topic>.md]`",
            "`[../../../05.operations/policies/<policy-or-standard>.md]`",
        ],
    },
    "docs/99.templates/slo.template.md": {
        "required": ["[AGENTS.md](../../../AGENTS.md)"],
        "forbidden": ["[AGENTS.md](../../AGENTS.md)"],
    },
    "docs/99.templates/progress.template.md": {
        "required": [
            "[Memory README](./README.md)",
            "[Documentation Protocol](../rules/documentation-protocol.md)",
            "[Policy Change Log](../policy-change-log.md)",
        ],
        "forbidden": [
            "[Memory README](../00.agent-governance/memory/README.md)",
            "[Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md)",
            "[Policy Change Log](../00.agent-governance/policy-change-log.md)",
        ],
    },
    "docs/99.templates/session-memory.template.md": {
        "required": [
            "`[../../04.execution/tasks/YYYY-MM-DD-<task-name>.md]`",
            "`[../../05.operations/incidents/YYYY/INC-###/postmortem.md]`",
        ],
        "forbidden": [
            "`[../../../04.execution/tasks/YYYY-MM-DD-<task-name>.md]`",
            "`[../../../05.operations/incidents/YYYY/INC-###/postmortem.md]`",
        ],
    },
    "docs/99.templates/expanded/bounded-context.template.md": {
        "required": [
            "`[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../../03.specs/<feature-id>/spec.md]`",
            "`[../../03.specs/<feature-id>/data-model.md]`",
            "`[../decisions/####-<short-title>.md]`",
        ],
        "forbidden": [
            "`[../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../03.specs/<feature-id>/spec.md]`",
            "`[../03.specs/<feature-id>/data-model.md]`",
            "`[../02.architecture/decisions/####-<short-title>.md]`",
        ],
    },
    "docs/99.templates/expanded/ubiquitous-language.template.md": {
        "required": [
            "`[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../../03.specs/<feature-id>/data-model.md]`",
        ],
        "forbidden": [
            "`[../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`",
            "`[../03.specs/<feature-id>/data-model.md]`",
        ],
    },
}
MACHINE_READABLE_TEMPLATE_TARGET_RULES = {
    "docs/99.templates/openapi.template.yaml": [
        "# - Parent Spec: ../spec.md",
        "# - Test Strategy: ../tests.md",
        "# - API Spec: ../api-spec.md",
    ],
    "docs/99.templates/extended/schema.template.graphql": [
        "# - Parent Spec: ../spec.md",
        "# - Test Strategy: ../tests.md",
        "# - API Spec: ../api-spec.md",
    ],
    "docs/99.templates/extended/service.template.proto": [
        "// - Parent Spec: ../spec.md",
        "// - Test Strategy: ../tests.md",
        "// - API Spec: ../api-spec.md",
    ],
}
REQUIRED_PROGRESS_SECTIONS = [
    "## Purpose",
    "## Active Task",
    "## Phase Progress",
    "## Durable Memory Notes",
    "## Key Decisions",
    "## Blockers",
    "## Next Sync",
    "## AI Execution Checklist",
    "## Related Documents",
]
REQUIRED_SDLC_WORKFLOW_SECTIONS = [
    "## Purpose",
    "## Overview",
    "## Scope",
    "## Authority Boundaries",
    "## Workflow Diagram",
    "## Baton Passing Points",
    "## AI Execution Checklist",
    "## Related Documents",
]


def iter_text_files(path: Path):
    if path.is_file():
        yield path
        return
    if not path.exists():
        return
    for child in path.rglob("*"):
        if child.is_file() and child.suffix in {
            ".md",
            ".toml",
            ".json",
            ".yaml",
            ".yml",
            ".sh",
            ".py",
        }:
            yield child


def validate_frontmatter() -> list[str]:
    errors: list[str] = []
    for stage in CANONICAL_STAGE_DIRS:
        stage_dir = ROOT / "docs" / stage
        if not stage_dir.exists():
            continue
        for path in sorted(stage_dir.rglob("*.md")):
            if path.name == "README.md":
                continue
            first_line = path.read_text(encoding="utf-8", errors="ignore").splitlines()[
                :1
            ]
            if first_line != ["---"]:
                errors.append(
                    f"{path.relative_to(ROOT)}: canonical docs must start with YAML frontmatter"
                )
    return errors


def readme_document_links(readme: Path) -> set[str]:
    text = readme.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"^## Documents\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        return set()
    body = match.group("body")
    return set(re.findall(r"\]\((\./[^)]+)\)", body))


def readme_all_links(readme: Path) -> set[str]:
    text = readme.read_text(encoding="utf-8", errors="ignore")
    links = set()
    for link in re.findall(r"\]\((\./[^)#]+)", text):
        links.add(link.rstrip("/"))
    return links


def expected_stage_links(stage_dir: Path) -> set[str]:
    links: set[str] = set()
    for child in sorted(stage_dir.iterdir(), key=lambda p: p.name):
        if child.name == "README.md" or child.name.startswith("."):
            continue
        if child.is_file() and child.suffix in README_INDEX_SUFFIXES:
            links.add(f"./{child.name}")
        elif child.is_dir() and any(child.iterdir()):
            links.add(f"./{child.name}/")
    return links


def expected_readme_links(index_dir: Path) -> set[str]:
    links: set[str] = set()
    for child in sorted(index_dir.iterdir(), key=lambda p: p.name):
        if child.name == "README.md" or child.name.startswith("."):
            continue
        if child.is_file() and child.suffix in README_INDEX_SUFFIXES:
            links.add(f"./{child.name}")
        elif child.is_dir() and any(child.iterdir()):
            links.add(f"./{child.name}/")
    return links


def is_top_level_docs_readme(readme: Path) -> bool:
    docs_root = ROOT / "docs"
    return readme.parent.parent == docs_root and readme.parent.name in ALLOWED_DOC_DIRS


def supporting_readme_paths() -> list[Path]:
    docs_root = ROOT / "docs"
    paths = [ROOT / "docs/README.md", ROOT / "scripts/README.md"]
    for readme in sorted(docs_root.rglob("README.md")):
        if is_top_level_docs_readme(readme):
            continue
        if readme == ROOT / "docs/README.md":
            continue
        paths.append(readme)
    return paths


def indexed_readme_paths() -> list[Path]:
    docs_root = ROOT / "docs"
    paths = [ROOT / "docs/README.md", ROOT / "docs/99.templates/README.md"]
    for readme in sorted(docs_root.rglob("README.md")):
        if is_top_level_docs_readme(readme):
            continue
        if readme == ROOT / "docs/README.md":
            continue
        paths.append(readme)
    return paths


def has_heading(text: str, heading: str) -> bool:
    return re.search(rf"^{re.escape(heading)}\s*$", text, re.M) is not None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def frontmatter_keys(text: str) -> tuple[set[str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return set(), "missing YAML frontmatter"
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return set(), "unterminated YAML frontmatter"
    keys = {
        match.group(1)
        for line in lines[1:end]
        if (match := re.match(r"^([A-Za-z0-9_-]+):", line))
    }
    return keys, None


def canonical_template_conformance_issues(text: str) -> list[str]:
    keys, frontmatter_error = frontmatter_keys(text)
    errors: list[str] = []
    if frontmatter_error:
        errors.append(frontmatter_error)
    else:
        missing = sorted(REQUIRED_CANONICAL_FRONTMATTER_FIELDS - keys)
        if missing:
            errors.append(f"missing frontmatter fields: {missing}")

    for heading in REQUIRED_CANONICAL_TEMPLATE_SECTIONS:
        if not has_heading(text, heading):
            errors.append(f"missing required section `{heading}`")
    return errors


def template_contracts_for_path(rel_path: str) -> list[tuple[str, list[str]]]:
    for prefix, contracts in CANONICAL_STAGE_TEMPLATE_CONTRACTS:
        if rel_path.startswith(prefix):
            return contracts
    return []


def stage_template_contract_issues(rel_path: str, text: str) -> list[str]:
    contracts = template_contracts_for_path(rel_path)
    if not contracts:
        return []

    for _template, required_headings in contracts:
        if all(has_heading(text, heading) for heading in required_headings):
            return []

    expected = ", ".join(template for template, _headings in contracts)
    return [
        f"does not match required docs/99.templates contract for its path; "
        f"expected one of: {expected}"
    ]


def validate_canonical_template_conformance() -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for stage in CANONICAL_STAGE_DIRS:
        stage_dir = ROOT / "docs" / stage
        if not stage_dir.exists():
            continue
        for path in sorted(stage_dir.rglob("*.md")):
            if path.name == "README.md":
                continue
            rel = path.relative_to(ROOT).as_posix()
            seen.add(rel)
            text = path.read_text(encoding="utf-8", errors="ignore")
            issues = canonical_template_conformance_issues(text)
            issues.extend(stage_template_contract_issues(rel, text))
            baseline_hash = LEGACY_TEMPLATE_CONFORMANCE_BASELINE.get(rel)

            if not issues:
                if baseline_hash:
                    errors.append(f"{rel}: remove stale legacy template baseline entry")
                continue

            current_hash = sha256_text(text)
            if baseline_hash == current_hash:
                continue
            if baseline_hash:
                errors.append(
                    f"{rel}: legacy template baseline changed while still non-conforming "
                    f"({'; '.join(issues)}); bring the file into current template conformance "
                    "or intentionally update the baseline"
                )
            else:
                errors.append(
                    f"{rel}: template conformance failed ({'; '.join(issues)})"
                )

    stale_baseline_entries = sorted(set(LEGACY_TEMPLATE_CONFORMANCE_BASELINE) - seen)
    for rel in stale_baseline_entries:
        errors.append(f"{rel}: remove stale legacy template baseline entry")
    return errors


def validate_machine_readable_template_contracts() -> list[str]:
    errors: list[str] = []
    specs_root = ROOT / "docs/03.specs"
    if not specs_root.exists():
        return errors

    for path in sorted(specs_root.rglob("*")):
        if not path.is_file() or path.suffix not in {
            ".yaml",
            ".yml",
            ".graphql",
            ".proto",
        }:
            continue

        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        name = path.name

        if name in {"openapi.yaml", "openapi.yml"}:
            required = ["openapi:", "info:", "paths:"]
            template = "openapi.template.yaml"
        elif name == "schema.graphql":
            required = ["schema", "type "]
            template = "extended/schema.template.graphql"
        elif name == "service.proto":
            required = ['syntax = "proto3";', "service "]
            template = "extended/service.template.proto"
        else:
            errors.append(
                f"{rel}: machine-readable spec contract must use an approved "
                "docs/99.templates target name: openapi.yaml, schema.graphql, or service.proto"
            )
            continue

        missing = [marker for marker in required if marker not in text]
        if missing:
            errors.append(
                f"{rel}: does not match {template}; missing markers {missing}"
            )

    return errors


def validate_top_level_docs_structure() -> list[str]:
    errors: list[str] = []
    docs_root = ROOT / "docs"
    actual = {
        child.name
        for child in docs_root.iterdir()
        if child.is_dir() and not child.name.startswith(".")
    }
    allowed = set(ALLOWED_DOC_DIRS)
    extra = actual - allowed
    missing = allowed - actual
    if extra:
        errors.append(f"docs/: unexpected top-level folders {sorted(extra)}")
    if missing:
        errors.append(f"docs/: missing required top-level folders {sorted(missing)}")
    for folder in ALLOWED_DOC_DIRS:
        readme = docs_root / folder / "README.md"
        if not readme.exists():
            errors.append(
                f"docs/{folder}/README.md: required top-level README is missing"
            )
    return errors


def validate_top_level_readme_contract() -> list[str]:
    errors: list[str] = []
    for folder in ALLOWED_DOC_DIRS:
        readme = ROOT / "docs" / folder / "README.md"
        if not readme.exists():
            continue
        if readme.relative_to(ROOT).as_posix() in RELEASE_SKELETON_READMES:
            continue
        text = readme.read_text(encoding="utf-8", errors="ignore")
        for heading in REQUIRED_TOP_LEVEL_README_SECTIONS:
            if not has_heading(text, heading):
                errors.append(
                    f"{readme.relative_to(ROOT)}: missing required section `{heading}`"
                )
    return errors


def validate_root_readme_contract() -> list[str]:
    errors: list[str] = []
    readme = ROOT / "README.md"
    if not readme.exists():
        return ["README.md: required root README is missing"]

    text = readme.read_text(encoding="utf-8", errors="ignore")
    for heading in ROOT_README_REQUIRED_SECTIONS:
        if not has_heading(text, heading):
            errors.append(f"README.md: missing root README section `{heading}`")
    if not (
        has_heading(text, "## Related Documents")
        or has_heading(text, "## Related References")
    ):
        errors.append(
            "README.md: missing root README section `## Related Documents` or `## Related References`"
        )
    if (
        "video-analysis" in text
        and "docs/99.templates/readme.template.md" not in text
    ):
        errors.append(
            "README.md: root README must reference docs/99.templates/readme.template.md"
        )
    return errors


def validate_readme_frontmatter_position() -> list[str]:
    errors: list[str] = []
    frontmatter_like = re.compile(
        r"(?m)^---\n(?=[\s\S]{0,300}(?:title|version|owner|layer|stage|status|last-updated):)"
    )
    for readme in sorted(ROOT.rglob("README.md")):
        if any(part in {".git", "node_modules"} for part in readme.parts):
            continue
        text = readme.read_text(encoding="utf-8", errors="ignore")
        match = frontmatter_like.search(text)
        if match and match.start() != 0:
            errors.append(
                f"{readme.relative_to(ROOT)}: YAML metadata block must be at the start of the file"
            )
    return errors


def validate_supporting_readme_contract() -> list[str]:
    errors: list[str] = []
    for readme in supporting_readme_paths():
        if not readme.exists():
            errors.append(f"{readme.relative_to(ROOT)}: supporting README is missing")
            continue
        if readme.relative_to(ROOT).as_posix() in RELEASE_SKELETON_READMES:
            continue
        text = readme.read_text(encoding="utf-8", errors="ignore")
        for heading in SUPPORTING_README_REQUIRED_SECTIONS:
            if not has_heading(text, heading):
                errors.append(
                    f"{readme.relative_to(ROOT)}: missing supporting README section `{heading}`"
                )
        if not (
            has_heading(text, "## Related Documents")
            or has_heading(text, "## Related References")
        ):
            errors.append(
                f"{readme.relative_to(ROOT)}: missing supporting README section "
                "`## Related Documents` or `## Related References`"
            )
        if readme.is_relative_to(ROOT / "docs") and not has_heading(
            text, "## Documents"
        ):
            errors.append(
                f"{readme.relative_to(ROOT)}: missing supporting README section `## Documents`"
            )
    return errors


def validate_readme_indexes() -> list[str]:
    errors: list[str] = []
    for stage in CANONICAL_STAGE_DIRS:
        stage_dir = ROOT / "docs" / stage
        readme = stage_dir / "README.md"
        if not readme.exists():
            continue
        expected = expected_stage_links(stage_dir)
        actual = readme_document_links(readme)
        missing = expected - actual
        stale = actual - expected
        if missing:
            errors.append(
                f"{readme.relative_to(ROOT)}: missing Documents rows for {sorted(missing)}"
            )
        if stale:
            errors.append(
                f"{readme.relative_to(ROOT)}: stale Documents rows for {sorted(stale)}"
            )
    return errors


def validate_nested_readme_indexes() -> list[str]:
    errors: list[str] = []
    for readme in indexed_readme_paths():
        if not readme.exists():
            continue
        expected = expected_readme_links(readme.parent)
        actual = readme_document_links(readme)
        missing = expected - actual
        stale = actual - expected
        if missing:
            errors.append(
                f"{readme.relative_to(ROOT)}: missing Documents rows for {sorted(missing)}"
            )
        if stale:
            errors.append(
                f"{readme.relative_to(ROOT)}: stale Documents rows for {sorted(stale)}"
            )
    return errors


def validate_template_inventory() -> list[str]:
    errors: list[str] = []
    template_root = ROOT / "docs/99.templates"
    readme = template_root / "README.md"
    if not readme.exists():
        return ["docs/99.templates/README.md: template inventory README is missing"]

    text = readme.read_text(encoding="utf-8", errors="ignore")
    for marker in TEMPLATE_CLASSIFICATION_MARKERS:
        if marker not in text:
            errors.append(
                f"{readme.relative_to(ROOT)}: missing template classification marker `{marker}`"
            )

    actual_templates = {
        f"./{path.relative_to(template_root).as_posix()}"
        for path in template_root.rglob("*")
        if path.is_file() and path.name != "README.md"
    }
    linked_templates = readme_all_links(readme)
    missing = actual_templates - linked_templates
    stale = {
        link
        for link in linked_templates
        if (template_root / link.removeprefix("./")).suffix
        and not (template_root / link.removeprefix("./")).exists()
    }
    if missing:
        errors.append(
            f"{readme.relative_to(ROOT)}: missing template inventory links for {sorted(missing)}"
        )
    if stale:
        errors.append(
            f"{readme.relative_to(ROOT)}: stale template inventory links for {sorted(stale)}"
        )
    return errors


def template_inventory_readmes() -> list[Path]:
    template_root = ROOT / "docs/99.templates"
    if not template_root.exists():
        return []
    return sorted(path for path in template_root.rglob("README.md") if path.is_file())


def documents_table_rows_with_line_numbers(readme: Path) -> list[tuple[int, str]]:
    text = readme.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"^## Documents\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        return []
    start_line = text[: match.start("body")].count("\n") + 1
    return [
        (start_line + offset, line)
        for offset, line in enumerate(match.group("body").splitlines())
        if line.startswith("|")
    ]


def validate_template_inventory_cells() -> list[str]:
    """Reject placeholder leakage only in template README Documents tables."""
    errors: list[str] = []
    for readme in template_inventory_readmes():
        for line_number, line in documents_table_rows_with_line_numbers(readme):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            for cell in cells:
                if cell in UNINITIALIZED_TEMPLATE_INVENTORY_CELLS:
                    errors.append(
                        f"{readme.relative_to(ROOT)}:{line_number}: Documents table "
                        f"contains uninitialized inventory cell `{cell}`"
                    )
    return errors


def markdown_paths_for_path_label_validation() -> list[Path]:
    paths = [ROOT / "README.md", ROOT / "scripts/README.md"]
    paths.extend(sorted((ROOT / "docs").rglob("*.md")))
    return [path for path in paths if path.exists()]


def strip_code_fences(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            lines.append("")
            continue
        lines.append("" if in_fence else line)
    return "\n".join(lines)


def is_relative_href(href: str) -> bool:
    if not href or href.startswith("#"):
        return False
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href):
        return False
    return True


def link_label_looks_like_relative_path(label: str) -> bool:
    label = label.strip().strip("`")
    if any(marker in label for marker in ("<", ">", "*", "{", "}")):
        return False
    if label.startswith(("./", "../", "docs/")):
        return True
    return "/" in label and label.endswith(PATH_LABEL_SUFFIXES)


def normalized_markdown_link_target(value: str) -> str:
    value = value.strip().strip("`").split("#", 1)[0].rstrip("/")
    return value.removeprefix("./")


def validate_path_label_href_alignment() -> list[str]:
    """Validate only links whose visible label is itself a relative path."""
    errors: list[str] = []
    link_pattern = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
    for path in markdown_paths_for_path_label_validation():
        text = strip_code_fences(path.read_text(encoding="utf-8", errors="ignore"))
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in link_pattern.finditer(line):
                label = match.group(1).strip()
                href = match.group(2).strip()
                if not is_relative_href(href):
                    continue
                if not link_label_looks_like_relative_path(label):
                    continue
                if any(marker in href for marker in ("<", ">", "*", "{", "}")):
                    continue
                if normalized_markdown_link_target(
                    label
                ) != normalized_markdown_link_target(href):
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number}: visible path label "
                        f"`{label}` disagrees with href `{href}`"
                    )
    return errors


def validate_template_target_relative_paths() -> list[str]:
    """Validate template placeholder paths relative to generated target locations."""
    errors: list[str] = []
    for rel, rules in TEMPLATE_TARGET_RELATIVE_RULES.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(
                f"{rel}: target-relative template rule points to missing file"
            )
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for snippet in rules["required"]:
            if snippet not in text:
                errors.append(
                    f"{rel}: missing target-relative template snippet `{snippet}`"
                )
        for snippet in rules["forbidden"]:
            if snippet in text:
                errors.append(
                    f"{rel}: stale template-relative snippet remains `{snippet}`"
                )
    return errors


def validate_machine_readable_template_target_guidance() -> list[str]:
    """Validate target-relative parent references in machine-readable templates."""
    errors: list[str] = []
    for rel, snippets in MACHINE_READABLE_TEMPLATE_TARGET_RULES.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(
                f"{rel}: machine-readable template rule points to missing file"
            )
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for snippet in snippets:
            if snippet not in text:
                errors.append(
                    f"{rel}: missing generated-target parent reference `{snippet}`"
                )
    return errors


def validate_generated_doc_pseudo_links() -> list[str]:
    """Reject code-span pseudo-links in generated Inputs/Related Documents sections."""
    errors: list[str] = []
    section_pattern = re.compile(
        r"^## (?P<section>Inputs|Related Documents)\n(?P<body>.*?)(?=^## |\Z)",
        re.M | re.S,
    )
    pseudo_link_pattern = re.compile(
        r"`(?P<path>(?:(?:\.\.?/)|docs/|[^`/\s]+/)[^`]*\.md(?:#[^`]*)?)`"
    )
    explicit_absence_markers = (
        "not yet created",
        "not present",
        "planned downstream artifact",
        "spec not yet created",
        "archive purged",
        "purged",
        "historical context",
    )
    for stage in CANONICAL_STAGE_DIRS:
        stage_dir = ROOT / "docs" / stage
        if not stage_dir.exists():
            continue
        for path in sorted(stage_dir.rglob("*.md")):
            if path.name == "README.md":
                continue
            rel = path.relative_to(ROOT).as_posix()
            text = strip_code_fences(path.read_text(encoding="utf-8", errors="ignore"))
            for section_match in section_pattern.finditer(text):
                section_start_line = text[: section_match.start("body")].count("\n") + 1
                for offset, line in enumerate(
                    section_match.group("body").splitlines(), start=0
                ):
                    if not pseudo_link_pattern.search(line):
                        continue
                    if any(
                        marker in line.lower() for marker in explicit_absence_markers
                    ):
                        continue
                    errors.append(
                        f"{rel}:{section_start_line + offset}: "
                        f"`{section_match.group('section')}` contains a code-span "
                        "pseudo-link; use a live Markdown link or an explicit absence note"
                    )
    return errors


def authorized_docs_subfolder_patterns() -> list[str]:
    protocol = ROOT / "docs/00.agent-governance/rules/documentation-protocol.md"
    if not protocol.exists():
        return []
    text = protocol.read_text(encoding="utf-8", errors="ignore")
    match = re.search(
        r"### Authorized Subfolders Registry(?P<body>.*?)(?=### Procedure for Adding a New Subfolder|\Z)",
        text,
        re.S,
    )
    if not match:
        return []
    body = match.group("body")
    return sorted({path.rstrip("/") for path in re.findall(r"`(docs/[^`]+/)`", body)})


def path_matches_authorized_subfolder(pattern: str, rel_path: str) -> bool:
    pattern = pattern.rstrip("/")
    rel_path = rel_path.rstrip("/")
    regex = re.escape(pattern)
    regex = regex.replace(re.escape("<feature-id>"), r"[^/]+")
    return re.fullmatch(regex, rel_path) is not None


def git_tracks_path(rel_path: str) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--", rel_path],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return False
    return bool(result.stdout.strip())


def directory_state(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    tracked = git_tracks_path(rel)
    non_empty = any(path.iterdir())
    if tracked and non_empty:
        return "tracked and non-empty"
    if tracked:
        return "tracked"
    if non_empty:
        return "non-empty local-only"
    return "empty local-only"


def validate_docs_subfolder_registry() -> list[str]:
    errors: list[str] = []
    patterns = authorized_docs_subfolder_patterns()
    if not patterns:
        return [
            "docs/00.agent-governance/rules/documentation-protocol.md: missing authorized subfolder registry"
        ]

    docs_root = ROOT / "docs"
    for path in sorted(
        (child for child in docs_root.rglob("*") if child.is_dir()),
        key=lambda p: p.as_posix(),
    ):
        if path.parent == docs_root:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if any(path_matches_authorized_subfolder(pattern, rel) for pattern in patterns):
            continue
        errors.append(
            f"{rel}/: unauthorized docs subfolder ({directory_state(path)}); "
            "remove it or register it in documentation-protocol.md Section 13"
        )
    return errors


def validate_stale_references() -> list[str]:
    errors: list[str] = []
    for root in STALE_SCAN_PATHS:
        for path in iter_text_files(root):
            if path.name in {
                "validate-doc-readiness.py",
                "validate-script-inventory.py",
            }:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern, reason in STALE_PATTERNS.items():
                if re.search(pattern, text):
                    errors.append(
                        f"{path.relative_to(ROOT)}: stale reference `{pattern}` ({reason})"
                    )
    return errors


def validate_stage00_rule_coverage() -> list[str]:
    errors: list[str] = []
    readme = ROOT / "docs/00.agent-governance/README.md"
    text = (
        readme.read_text(encoding="utf-8", errors="ignore") if readme.exists() else ""
    )
    for rule in STAGE00_REQUIRED_RULES:
        rule_path = ROOT / "docs/00.agent-governance/rules" / rule
        if not rule_path.exists():
            errors.append(
                f"docs/00.agent-governance/rules/{rule}: required Stage 00 rule is missing"
            )
        if f"rules/{rule}" not in text:
            errors.append(
                f"{readme.relative_to(ROOT)}: missing Stage 00 rule reference for rules/{rule}"
            )
    return errors


def should_validate_hardcoded_doc_path(path_text: str) -> bool:
    if not path_text.startswith("docs/"):
        return False
    if path_text in AUTHORIZED_OPTIONAL_DOC_PATHS:
        return False
    if path_text.startswith("docs/04.execution/archive/"):
        return False
    if any(
        marker in path_text
        for marker in ("<", ">", "[", "]", "*", "~", "$", "{", "}", "YYYY", "0N", "...")
    ):
        return False
    if path_text.endswith("/**"):
        return False
    return True


def validate_hardcoded_doc_paths() -> list[str]:
    errors: list[str] = []
    target_roots = [
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "GEMINI.md",
        ROOT / ".claude",
        ROOT / "docs/00.agent-governance",
    ]
    pattern = re.compile(r"`(docs/[^`\s)]+)`")
    for root in target_roots:
        for path in iter_text_files(root):
            if (
                path.relative_to(ROOT).as_posix()
                == "docs/00.agent-governance/policy-change-log.md"
            ):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in pattern.finditer(text):
                candidate = match.group(1).rstrip(".,;:")
                if not should_validate_hardcoded_doc_path(candidate):
                    continue
                if not (ROOT / candidate).exists():
                    errors.append(
                        f"{path.relative_to(ROOT)}: hardcoded doc path does not exist `{candidate}`"
                    )
    return errors


def validate_at_imports() -> list[str]:
    """Validate root/provider @ imports that local agent runtimes expand."""
    errors: list[str] = []
    for root in AT_IMPORT_SCAN_PATHS:
        for path in iter_text_files(root):
            if path.suffix != ".md":
                continue
            rel = path.relative_to(ROOT).as_posix()
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8", errors="ignore").splitlines(),
                start=1,
            ):
                stripped = line.strip()
                if not stripped.startswith("@"):
                    continue
                target = stripped[1:].strip().split()[0].rstrip(".,;:")
                if not target or "*" in target:
                    continue
                if target.startswith("/"):
                    errors.append(
                        f"{rel}:{line_number}: @ import must be repository-relative, not absolute `{target}`"
                    )
                    continue
                if target.startswith(("./", "../")):
                    resolved = (path.parent / target).resolve()
                else:
                    resolved = (ROOT / target).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    errors.append(
                        f"{rel}:{line_number}: @ import escapes repository root `{target}`"
                    )
                    continue
                if not resolved.exists():
                    errors.append(
                        f"{rel}:{line_number}: @ import target does not exist `{target}`"
                    )
    return errors


def validate_codex_surface() -> list[str]:
    errors: list[str] = []
    codex_root = ROOT / ".codex"
    if not codex_root.exists():
        return errors
    for path in codex_root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".codex/agents/") and rel.endswith(".toml"):
            continue
        errors.append(
            f"{rel}: .codex may contain only synchronized agent compatibility metadata"
        )
    return errors


def validate_qa_test_strategy_contract() -> list[str]:
    errors: list[str] = []
    if not QA_SCOPE.exists():
        return ["docs/00.agent-governance/scopes/qa.md: QA scope contract is missing"]
    if not TESTS_TEMPLATE.exists():
        return ["docs/99.templates/tests.template.md: tests template is missing"]

    qa_text = QA_SCOPE.read_text(encoding="utf-8", errors="ignore")
    template_text = TESTS_TEMPLATE.read_text(encoding="utf-8", errors="ignore")
    required_markers = [
        "docs/03.specs/<feature-id>/tests.md",
        "docs/04.execution/plans/",
        "docs/04.execution/tasks/",
    ]
    for marker in required_markers:
        if marker not in qa_text:
            errors.append(
                f"{QA_SCOPE.relative_to(ROOT)}: missing QA test strategy marker `{marker}`"
            )
    if "docs/04.execution/plans/`. Use `tests.template.md`" in qa_text:
        errors.append(
            f"{QA_SCOPE.relative_to(ROOT)}: tests.template.md must target "
            "feature-local tests.md, not execution plans"
        )
    if "Target: docs/03.specs/<feature-id>/tests.md" not in template_text:
        errors.append(
            f"{TESTS_TEMPLATE.relative_to(ROOT)}: missing feature-local tests.md target marker"
        )
    return errors


def validate_progress_memory_contract() -> list[str]:
    errors: list[str] = []
    required = [
        (PROGRESS_TEMPLATE, "docs/99.templates/progress.template.md"),
        (PROGRESS_MEMORY, "docs/00.agent-governance/memory/progress.md"),
    ]
    for path, rel in required:
        if not path.exists():
            errors.append(f"{rel}: required progress memory contract file is missing")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        keys, frontmatter_error = frontmatter_keys(text)
        if frontmatter_error:
            errors.append(f"{rel}: {frontmatter_error}")
        else:
            missing = sorted(REQUIRED_CANONICAL_FRONTMATTER_FIELDS - keys)
            if missing:
                errors.append(f"{rel}: missing frontmatter fields: {missing}")
        for heading in REQUIRED_PROGRESS_SECTIONS:
            if not has_heading(text, heading):
                errors.append(f"{rel}: missing required section `{heading}`")
        if "docs/00.agent-governance/memory/progress.md" not in text:
            errors.append(
                f"{rel}: must identify docs/00.agent-governance/memory/progress.md"
            )
        if "_workspace/**" not in text:
            errors.append(f"{rel}: must define _workspace/** as non-authoritative")
    return errors


def validate_sdlc_workflow_contract() -> list[str]:
    errors: list[str] = []
    rel = "docs/00.agent-governance/sdlc-workflow.md"
    if not SDLC_WORKFLOW.exists():
        return [f"{rel}: required SDLC workflow boundary document is missing"]

    text = SDLC_WORKFLOW.read_text(encoding="utf-8", errors="ignore")
    keys, frontmatter_error = frontmatter_keys(text)
    if frontmatter_error:
        errors.append(f"{rel}: {frontmatter_error}")
    else:
        missing = sorted(REQUIRED_CANONICAL_FRONTMATTER_FIELDS - keys)
        if missing:
            errors.append(f"{rel}: missing frontmatter fields: {missing}")
    for heading in REQUIRED_SDLC_WORKFLOW_SECTIONS:
        if not has_heading(text, heading):
            errors.append(f"{rel}: missing required section `{heading}`")
    required_markers = [
        "docs/00.agent-governance/memory/progress.md",
        "docs/00.agent-governance/memory/methodology.md",
        "docs/00.agent-governance/policy-change-log.md",
        "00.agent-governance/sdlc-workflow.md",
        "00_System/sdlc-workflow.md",
        "_workspace/**",
    ]
    for marker in required_markers:
        if marker not in text:
            errors.append(f"{rel}: missing boundary marker `{marker}`")
    if EXTERNAL_SYSTEM_SDLC_WORKFLOW.exists():
        errors.append(
            "00_System/sdlc-workflow.md: duplicate workflow authority is not allowed in video-analysis; "
            "use docs/00.agent-governance/sdlc-workflow.md"
        )
    if EXTERNAL_DOT_AGENT_GOVERNANCE_SDLC_WORKFLOW.exists():
        errors.append(
            "00.agent-governance/sdlc-workflow.md: duplicate workflow authority is not allowed in "
            "video-analysis; use docs/00.agent-governance/sdlc-workflow.md"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_top_level_docs_structure())
    errors.extend(validate_top_level_readme_contract())
    errors.extend(validate_root_readme_contract())
    errors.extend(validate_readme_frontmatter_position())
    errors.extend(validate_supporting_readme_contract())
    errors.extend(validate_frontmatter())
    errors.extend(validate_canonical_template_conformance())
    errors.extend(validate_machine_readable_template_contracts())
    errors.extend(validate_readme_indexes())
    errors.extend(validate_nested_readme_indexes())
    errors.extend(validate_template_inventory())
    errors.extend(validate_template_inventory_cells())
    errors.extend(validate_path_label_href_alignment())
    errors.extend(validate_template_target_relative_paths())
    errors.extend(validate_machine_readable_template_target_guidance())
    errors.extend(validate_generated_doc_pseudo_links())
    errors.extend(validate_docs_subfolder_registry())
    errors.extend(validate_stale_references())
    errors.extend(validate_stage00_rule_coverage())
    errors.extend(validate_hardcoded_doc_paths())
    errors.extend(validate_at_imports())
    errors.extend(validate_codex_surface())
    errors.extend(validate_qa_test_strategy_contract())
    errors.extend(validate_progress_memory_contract())
    errors.extend(validate_sdlc_workflow_contract())

    if errors:
        print("Template readiness validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Template readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
