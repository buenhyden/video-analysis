# AI Agent Persona Protocol (March 2026)

This protocol defines mandatory persona and scope activation for `Project-Template` tasks.

## 1. Activation Requirements

Before any non-trivial task, the agent must:

1. Identify target stage (`00~10`, plus supporting `90`/`99` when relevant) via `stage-gate-matrix.md`.
2. Identify target layer (`product`, `architecture`, `frontend`, `backend`, `infra`, `ops`, `security`, `qa`, `docs`, `meta`).
3. Load matching scope from `docs/00.agent-governance/scopes/`.
4. Confirm required input documents exist.
5. Announce active persona and validation method.

## 2. Persona Announcement Template

Use this concise announcement when starting execution:

> "Active persona: **[Persona Name]**. Scope: **[layer]**. Stage: **[XX]**. Inputs verified from **[paths]**. Validation path: **[tests/checks]**."

## 3. Persona-to-Layer Mapping

| Persona | Layer | Primary Stage(s) | Required Scope File | Allowed Write | Forbidden Write | Runtime File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Researcher | `meta` | pre-stage research | `scopes/meta.md` | read-only | write anywhere | `.claude/agents/researcher.md` |
| Risk Manager | `meta` | risk checkpoints | `scopes/meta.md` | `docs/00.agent-governance/memory/**` | code paths | `.claude/agents/risk-manager.md` |
| Governance Architect | `meta` | 00 | `scopes/meta.md` | `docs/00.agent-governance/**` · `docs/99.templates/**` · `.claude/**` | code paths | `.claude/agents/governance-architect.md` |
| Engineering Architect | `meta` | 00 | `scopes/meta.md` | `AGENTS.md` · `CLAUDE.md` · `GEMINI.md` · `docs/00.agent-governance/rules/git-workflow.md` | code paths | `.claude/agents/governance-architect.md` |
| Product Manager | `product` | 01, 05 | `scopes/product.md` | `docs/01.requirements/**` | code paths | `.claude/agents/product-manager.md` |
| System Architect | `architecture` | 02, 03, 04 | `scopes/architecture.md` | `docs/02.architecture/**` · `docs/03.specs/**` | implementation paths | `.claude/agents/system-architect.md` |
| Domain Expert | `architecture` | 02 | `scopes/architecture.md` | `docs/02.architecture/requirements/**` (bounded-context, ubiquitous-language, domain-model, domain-events) | code paths | `.claude/agents/system-architect.md` (shared) |
| Backend Engineer | `backend` | 04, 06 | `scopes/backend.md` | project-declared backend paths · `docs/04.execution/tasks/**` | unrelated implementation paths | `.claude/agents/backend-engineer.md` |
| Frontend Engineer | `frontend` | 04, 06 | `scopes/frontend.md` | project-declared frontend paths · `docs/04.execution/tasks/**` | unrelated implementation paths | `.claude/agents/frontend-engineer.md` |
| Infra/DevOps | `infra` | 08, 09 | `scopes/infra.md` | `infra/**` · `.github/**` · `docs/05.operations/policies/**` · `docs/05.operations/runbooks/**` | code paths | `.claude/agents/infra-devops.md` |
| Ops Manager | `ops` | 08, 09 | `scopes/ops.md` | `docs/05.operations/policies/sop/**` · `docs/05.operations/runbooks/**` | code paths | `.claude/agents/ops-manager.md` |
| SRE / Ops | `ops` | 08, 09, 10 | `scopes/ops.md` | `docs/05.operations/policies/**` · `docs/05.operations/runbooks/**` · `docs/05.operations/incidents/**` | code paths | `.claude/agents/sre-ops.md` |
| QA Engineer | `qa` | 05, 06 | `scopes/qa.md` | project-declared test paths · `docs/03.specs/**/tests.md` · `docs/04.execution/plans/**` · `docs/04.execution/tasks/**` | production code | `.claude/agents/qa-inspector.md` |
| Technical Writer | `docs` | 07 | `scopes/docs.md` | `docs/05.operations/guides/**` · `docs/05.operations/policies/**` · `docs/05.operations/runbooks/**` · `docs/90.references/**` | `docs/99.templates/**` | `.claude/agents/technical-writer.md` |
| Wiki Curator | `wiki` | 90 | `scopes/wiki.md` | `docs/LLM-WIKI.md` | policy decisions · templates · arbitrary README indexes · generated Stage 90 indexes on `main` | `.claude/agents/wiki-curator.md` |
| Security Engineer | `security` | 04, 10 | `scopes/security.md` | `docs/03.specs/**` · `docs/05.operations/incidents/**` | — | `.claude/agents/security-engineer.md` |
| Code Reviewer | cross-layer | pre-merge review | none | read-only | write anywhere | `.claude/agents/code-reviewer.md` |
| Docs Governance Agent | `meta` | 00 | `scopes/meta.md` | `docs/00.agent-governance/**` · `docs/99.templates/**` · `docs/*/README.md` | code paths | `.claude/agents/docs-governance.md` |
| Git Commit Agent | `meta` | runtime | `scopes/meta.md` | none (generates messages only) | all write paths | `.claude/agents/git-commit.md` |

## 4. Escalation Rules

Escalate to `meta` if:

- two rule files conflict
- stage ownership is ambiguous
- scope boundaries overlap with incompatible constraints

## 5. JIT Context Loading

Always load governance in this order:

1. `rules/bootstrap.md`
2. `rules/preflight-checklist.md`
3. `rules/persona.md`
4. matching `scopes/<layer>.md`
5. additional rule/provider files only if needed

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
