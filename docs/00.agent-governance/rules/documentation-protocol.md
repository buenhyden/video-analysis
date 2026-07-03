# Documentation Protocol (March 2026)

This protocol defines how documentation must be authored and maintained for human readability and AI execution.

## 1. Canonical Separation

- `docs/00.agent-governance/`: AI execution governance layer.
- `docs/01.requirements` through `docs/05.operations`, plus `90` and `99`: canonical project content layer.
- Authoritative stage documents must be written only inside the compact canonical tree.

Governance files interpret and route; canonical files store product/engineering truth.

The `main` branch is the clean release-template surface. In `main`,
`docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`,
`docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/`
must contain only README skeleton guides until a derived project bootstrap
creates project-specific documents from intake. Source-template history belongs
on `dev` or a maintenance branch.

Use `template-document-lifecycle.md` to classify whether a non-README document
is a `project-seed`, `template-maintenance`, `active-template-contract`,
`archive/reference`, `example`, or `remove-candidate` before moving, deleting,
or reusing it in a derived workspace.

## 2. Language Policy

- Governance layer (`docs/00.agent-governance/*`): English only.
- Runtime instruction layer (`.claude/**`, root shims): English only.
- Human-facing repository guides (for example root `README.md`, `docs/README.md`): Korean.
- Technical execution artifacts used directly by agents (for example technical specs): English by default for consistency.

## 3. Template Policy

When creating a document in canonical stages, use templates from `docs/99.templates/`.
Template selection authority is `rules/stage-gate-matrix.md`.
Every governed Markdown template must expose target, entry gate, exit gate,
hard-stop conditions, downstream trigger, evidence rule, and related-document
coverage unless it is a runtime state template with an explicit exemption.

Agents must treat template selection as a hard gate, not as authoring advice.
Before creating or modifying non-README documents under `docs/01.requirements/`,
`docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`,
`docs/05.operations/`, or `docs/90.references/`, load the matching template from
`docs/99.templates/`, preserve the required stage-specific sections, and fill the
document from that contract. `scripts/validation/validate-doc-readiness.py`
enforces representative template markers for every compact stage path.
`pre-tool-validate.sh` blocks pending writes when the tool input contains the
new document body; `post-tool-validate.sh`, the Stop hook, and `ws validate`
re-check the repository after writes.

Generated seed documents must keep `status: draft`, retain TODO language for
unknown facts, and avoid claiming that downstream architecture, implementation,
rollout, SLO, or operations decisions are approved.
Bootstrap creates only the Stage 01 draft PRD seed. Other stage documents are
created from templates only when their stage gate is reached.

## 4. README Synchronization

Update relevant README files when:

1. scope or behavior changed
2. executable commands changed
3. entrypoints or folder responsibilities changed

Root and supporting README files must follow the base contract in
`docs/99.templates/readme.template.md`: overview, audience, scope, in-scope and
out-of-scope boundaries, structure, work instructions, and related references.
Supporting README files under `docs/` must also keep a `Documents` table
reconciled with actual child files and folders. YAML metadata blocks, when
present, must start at the first line of the README.

README naming rules for reusable folders must include path portability guidance
from `standards.md`: generated relative paths should stay within 140
characters, the current absolute workspace path within 220 characters, and each
path segment within 80 characters. New generated names should use lowercase
kebab-case slugs with no spaces or Windows-reserved characters.

## 5. Metadata Expectations

All canonical documentation must include the following frontmatter fields:

- `title`: Descriptive document title.
- `version`: Version identifier (e.g., alpha, 1.0.0).
- `owner`: Responsible persona or team.
- `layer`: Workspace layer (for example product, architecture, common, meta, cross, operations, governance, references).
- `stage`: Compact stage identifier (00-05, 90, 99).
- `status`: Lifecycle status (draft, review, active, completed, deprecated).
- `last-updated`: Date of last modification (YYYY-MM-DD).

**HALT** if any of these fields are missing or contain uninitialized `<string>` values (excluding `last-updated` in templates).

### Template Conformance Baseline

New or modified non-README Markdown documents under `docs/01.requirements/` through
`docs/05.operations/incidents/` and `docs/90.references/` must conform to the current
stage template contract. At minimum, they must include the required frontmatter
fields above, `## AI Execution Checklist`, `## Related Documents`, and the
stage-specific headings required by the matching template. Machine-readable
contracts under `docs/03.specs/<feature-id>/contracts/` must use the approved
template target names and markers for `openapi.template.yaml`,
`extended/schema.template.graphql`, or `extended/service.template.proto`.

Legacy content-hash baselines are not part of the compact contract.

## 6. Prohibited Patterns

- No policy duplication between root shims and detailed governance files.
- No references to non-existing paths.
- No machine-specific absolute paths in shared governance docs.
- No spaces or Windows-reserved characters in new reusable generated document paths.
- No ad hoc final-output buckets for stage documents.
- No local skill instruction may describe `_workspace/` as the final destination for authoritative PRD, Spec, Plan, or agent-memory artifacts.
- No `.codex/hooks.json`, `.codex/hooks/**`, or `.agents/skills/**` runtime policy surfaces.

## 7. DOCS 3 GLOBAL RULES (HALT Conditions)

These three rules are active on every task. A **HALT** means stop and resolve before proceeding.

### R1 — Content Creation

Read the matching template from `docs/99.templates/` BEFORE creating any stage document.
Fill all sections. Remove all `[placeholder]` text. Add `status: draft` to frontmatter.
New or modified non-README compact stage and Stage 90 Markdown documents must
include `## AI Execution Checklist` and `## Related Documents`.
For new derived projects, complete `project-initialization-intake.md` before
creating any PRD, ARD, ADR, spec, plan, task, operation, or reference document.
Classify inherited video-analysis documents with
`template-document-lifecycle.md` before treating them as project content.

| Stage | Path                                 | Primary Template                                  | Supplementary Templates (Expanded Mode)                                                                                                                                |
| :---- | :----------------------------------- | :------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 01    | `docs/01.requirements/`              | `prd.template.md`                                 | —                                                                                                                                                                      |
| 02    | `docs/02.architecture/requirements/` | `ard.template.md`                                 | `expanded/bounded-context.template.md` · `expanded/ubiquitous-language.template.md`                                                                                    |
| 02    | `docs/02.architecture/decisions/`    | `adr.template.md`                                 | —                                                                                                                                                                      |
| 03    | `docs/03.specs/<feature-id>/`        | `spec.template.md`                                | `api-spec.template.md` · `expanded/tactical-model.template.md` · `expanded/domain-model.template.md` · `expanded/domain-events.template.md` · `tests.template.md` · `openapi.template.yaml` · `extended/schema.template.graphql` · `extended/service.template.proto` |
| 04    | `docs/04.execution/plans/`           | `plan.template.md`                                | —                                                                                                                                                                      |
| 04    | `docs/04.execution/tasks/`           | `task.template.md`                                | —                                                                                                                                                                      |
| 05    | `docs/05.operations/guides/`         | `guide.template.md`                               | —                                                                                                                                                                      |
| 05    | `docs/05.operations/policies/`       | `operation.template.md` · `slo.template.md`       | —                                                                                                                                                                      |
| 05    | `docs/05.operations/runbooks/`       | `runbook.template.md`                             | —                                                                                                                                                                      |
| 05    | `docs/05.operations/incidents/`      | `incident.template.md` · `postmortem.template.md` | —                                                                                                                                                                      |
| 90    | `docs/90.references/`                | `reference.template.md`                           | —                                                                                                                                                                      |

\* `extended/` templates are optional and technology-specific. Use only when the target project adopts that technology (e.g., GraphQL, gRPC). Do not treat as required supplementary templates.

**HALT** if template is missing.
**HALT** if a document cannot satisfy the template contract for its stage path.
**NEVER edit** `docs/99.templates/` — read-only except for `meta` / Governance Architect persona.

**Template Hard Stop Rule**: Every governed Markdown template in `docs/99.templates/` contains a `Hard Stop Conditions` field in its AI Execution Checklist. Read and enforce it before writing the first line of any stage document. If the hard stop condition is true, stop immediately and resolve the blocker before continuing.

**Design System Hard Stop (Phase 0)**: Before starting any frontend, mobile, or UI implementation, the root `DESIGN.md` must be initialized. **HALT** if `version` or `name` is still `<string>`. AI agents must request design system definition before starting UI code.

**DDD Mandatory Rule (Stage 02)**: Every ARD must populate `## DDD Strategic Design` with at minimum the condensed Bounded Context Overlay (context name, responsibilities, aggregates, invariants, integration contracts) and Ubiquitous Language Overlay (minimum 3 terms). The DDD Trigger Condition must be evaluated and its result recorded. An ARD is **INCOMPLETE** if these sections are empty or contain only placeholder text.

**SDD Mandatory Rule (Stage 03)**: A Mermaid `sequenceDiagram` is required for every flow involving 3 or more distinct components. A `stateDiagram-v2` is required when state transitions affect correctness or rollback. These are not optional suggestions — a spec is **INCOMPLETE** without them.

**TDD Mandatory Rule (Stage 04 spec → Stage 05 plan gate)**: `tests.md` must be created in `docs/03.specs/<feature-id>/` using `tests.template.md` and linked in the spec before execution planning begins. The TDD Readiness table in `spec.md` must map every `impl` behavior to a test case or a documented exemption. A spec is **INCOMPLETE** without this table.

### R2 — Auto-Indexing

After every change to a `docs/` folder → update the folder's `README.md` using `readme.template.md`.
Use `bash scripts/docs/update-doc-readme-index.sh <docs-relative-dir>` to refresh a
folder `Documents` table from current files. The target is relative to `docs/`;
examples include `04.execution/plans` and `99.templates/extended`.
For release-skeleton stage READMEs, the updater preserves existing document
ownership labels (`project-seed`, `active-template-contract`,
`template-maintenance`, `archive/reference`, `example`, `remove-candidate`)
when the row already exists; do not overwrite those classifications with
generic frontmatter status without re-running the lifecycle classification.

Required README table format:

```markdown
| File | Type | Summary | Status | Last Modified |
```

**BLOCKED** (cannot close task) until the relevant README is updated.

### R3 — Cross-Referencing

Every stage document must include a `## Related Documents` section with relative links
(`../../01.requirements/...` etc.) to required upstream documents.

**INCOMPLETE** if required upstream links are absent. Relative paths only — no absolute paths.

## 8. Diagram Standards

Mermaid diagrams are the standard format for all architectural and design diagrams.

| Diagram Type     | When Required                       | Mermaid Syntax                     |
| :--------------- | :---------------------------------- | :--------------------------------- |
| Sequence diagram | ≥3 component interactions in a spec | `sequenceDiagram`                  |
| State machine    | State transitions in a spec         | `stateDiagram-v2`                  |
| C4 Context       | System-level context in ARD         | `C4Context`                        |
| C4 Container     | Deployment units in ARD             | `C4Container`                      |
| Context map      | Multi-bounded-context systems       | `graph LR` with domain annotations |

**INCOMPLETE** if a spec with 3+ component interactions lacks a sequence diagram.

## 9. Canonical Output Routing

- Final PRDs must live in `docs/01.requirements/YYYY-MM-DD-<feature>.md`.
- Final Specs must live in `docs/03.specs/<feature-id>/spec.md`.
- Final Plans must live in `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`.
- Agent-design deliverables must live in the parent spec's Agent Role & IO sections (`docs/03.specs/<feature-id>/spec.md`) or in the `Memory & Context Strategy` section.
- Active methodology, active progress, and durable agent memory must live under `docs/00.agent-governance/memory/`.
- `docs/00.agent-governance/memory/progress.md` must be initialized or repaired from `docs/99.templates/progress.template.md` and updated at phase boundaries, handoffs, blockers, and task closure.
- `docs/00.agent-governance/policy-change-log.md` records versioned policy, SDLC protocol, runtime contract, and validator changes; it must not be used as active task memory.
- `docs/00.agent-governance/sdlc-workflow.md` records the stable human-agent collaboration flow and baton-passing model; it must not be used as active progress or policy history.
- `00.agent-governance/sdlc-workflow.md` without the `docs/` prefix is docs-relative shorthand only. Do not create root `00.agent-governance/` or treat it as a separate workflow authority.
- `00_System/sdlc-workflow.md` is not a video-analysis governance path. Do not create it in this template; if a derived workspace has that file, it is downstream control-plane documentation and must defer to the Stage 00 docs contract here.
- `_workspace/` is reserved for transient coordination artifacts, generated diagnostics, generated intelligence, and local scratch output only.
- Incident records and postmortems live together under `docs/05.operations/incidents/YYYY/INC-###-<title>/`.

## 10. Runtime Workspace State

`_workspace/` is a local runtime output area. It must not define repository policy, methodology, progress state, durable memory, or final governed deliverables.

Allowed `_workspace/` uses:

- `_workspace/audit/` for generated audit artifacts such as local SBOM output.
- `_workspace/diagnostics/` for local diagnostic snapshots.
- `_workspace/dispatch/` for transient dispatch packets.
- `_workspace/intelligence/` for generated repository intelligence.
- `_workspace/scratches/` for local scratch output that is not cited as final evidence.
- `_workspace/swarm/` for transient swarm handoff state.

Authority order:

1. `AGENTS.md`, provider routers, and `docs/00.agent-governance/**`.
2. Governed stage documents under `docs/01.requirements/` through `docs/05.operations/`.
3. Generated `_workspace/**` artifacts as optional supporting input only.

If `_workspace/**` conflicts with `docs/00.agent-governance/**`, the Stage 00 governance document wins. Promote durable findings into `docs/00.agent-governance/memory/` or the appropriate governed stage document before using them as evidence.

### Memory and Policy Boundaries

| Surface                                                | Canonical Role                                                                | Promotion Rule                                                                                       |
| :----------------------------------------------------- | :---------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| `docs/00.agent-governance/memory/methodology.md`       | Active methodology and run-state memory.                                      | Promote taxonomy or hard-stop changes to Stage 00 rules/templates.                                   |
| `docs/00.agent-governance/memory/progress.md`          | Active task progress, durable run notes, handoff state, and blockers.         | Promote final evidence to the owning stage document.                                                 |
| `docs/00.agent-governance/memory/YYYY-MM-DD-<slug>.md` | Focused durable lessons and non-obvious context.                              | Promote stable rules to Stage 00 governance and record the policy change.                            |
| `docs/00.agent-governance/policy-change-log.md`        | Versioned policy, SDLC protocol, runtime contract, and validator changes.     | Link to ADR, plan, task, or user request; do not store active progress here.                         |
| `docs/00.agent-governance/sdlc-workflow.md`            | Stable collaboration flow, baton handoff points, and review checkpoints.      | Update only when the workflow model changes; do not store progress, memory, or version history here. |
| `00.agent-governance/sdlc-workflow.md`                 | Docs-relative shorthand for `docs/00.agent-governance/sdlc-workflow.md` only. | Must not become a root-level duplicate authority surface.                                            |
| `00_System/sdlc-workflow.md`                           | No canonical role in video-analysis.                                        | Must not duplicate or override Stage 00 workflow, policy, memory, or progress records.               |
| `_workspace/**`                                        | Transient coordination or generated output.                                   | Inspect and promote durable findings before citing as authority.                                     |

## 11. Optional Generated Intelligence

- `_workspace/intelligence/` is the built-in generated output created by `bash scripts/ws.sh intelligence`.
- `graphify-out/` is optional local generated intelligence. Use `graphify-out/GRAPH_REPORT.md` only when it exists, is current, and materially helps the task.
- Treat Graphify output as supporting context only. It never overrides source files, root routers, Stage 00 governance, templates, validators, current workspace evidence, or `main` release-template skeleton policy.
- If `graphify-out/wiki/index.md` exists, use it as navigation aid only. Still inspect canonical source files before making decisions.
- If Graphify tools are active, graph queries may supplement `rg` and source inspection for relationship questions. Do not block work or validation because Graphify is unavailable.
- Run `graphify update .` only when Graphify is installed, the graph was used for the current task, and refreshing it is relevant to the approved scope.
- Derived projects may regenerate Graphify output only after project intake. Do not promote generated Graphify output into `docs/90.references/` unless a governed reference document cites reviewed source evidence.

## 12. Centralized Evidence Rules

To ensure autonomous agent traceability, every stage transition requires explicit evidence:

| Stage / Document                 | Required Evidence Link                                                                                                                                                                                           |
| :------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **01.requirements**              | Link to original user request, business constraint, or discovery issue.                                                                                                                                          |
| **02.architecture/requirements** | ARD must map to upstream PRD. DDD overlays must cite domain experts or ARD.                                                                                                                                      |
| **02.architecture/decisions**    | Link to the specific spec, plan, or issue that necessitated the decision.                                                                                                                                        |
| **03.specs**                     | Link upstream to 01.requirements or 02.architecture/requirements. Link to SDD sequence diagrams if 3+ components.                                                                                                |
| **04.execution/plans**           | Link to upstream Spec. Link to the `tests.md` file created before execution.                                                                                                                                     |
| **04.execution/tasks**           | `impl` tasks must contain non-empty TDD RED-GREEN-REFACTOR execution logs.                                                                                                                                       |
| **05.operations/guides**         | Link to the execution task that finalized the behavior being documented.                                                                                                                                         |
| **05.operations/policies**       | Link to the target environment's SLI/SLO dashboard or monitoring configuration.                                                                                                                                  |
| **05.operations/runbooks**       | Link to the operations policy or incident that necessitated the runbook.                                                                                                                                         |
| **05.operations/incidents**      | Link to the original alert, log trace, or customer report.                                                                                                                                                       |
| **90.references**                | Cite the source material, standard, owning internal document, review basis, or provenance explicitly. Generated `_workspace/**` output is supporting input only unless promoted through reviewed reference text. |

## 13. Subfolder Authorization Policy

Subfolders within `docs/` stage folders are permitted **only** when:

1. Listed in the registry below, and
2. Their purpose and relation to the parent folder are documented here.

Adding a new subfolder requires updating this registry and committing the change before the subfolder is used.

### Authorized Subfolders Registry

| Subfolder Path                                | Parent Stage | Purpose                                                                                                            | Policy Owner            |
| :-------------------------------------------- | :----------- | :----------------------------------------------------------------------------------------------------------------- | :---------------------- |
| `docs/00.agent-governance/rules/`             | 00           | Governance rule files (bootstrap, git-workflow, persona, etc.)                                                     | Governance Architect    |
| `docs/00.agent-governance/scopes/`            | 00           | Persona scope definitions per discipline                                                                           | Governance Architect    |
| `docs/00.agent-governance/providers/`         | 00           | Provider-specific runtime notes (claude, gemini, agents-md)                                                        | Governance Architect    |
| `docs/00.agent-governance/memory/`            | 00           | Agent session memory and progress tracking                                                                         | Governance Architect    |
| `docs/00.agent-governance/compliance/`        | 00           | Compliance & audit hub (SOC2, privacy) — migrated from former Stage 12                                             | Compliance Officer      |
| `docs/00.agent-governance/data-governance/`   | 00           | Data governance policies (PII, migrations, encryption) — migrated from former Stage 11                             | Data Protection Officer |
| `docs/02.architecture/requirements/`          | 02           | Architecture requirements and reference models                                                                     | System Architect        |
| `docs/02.architecture/requirements/research/` | 02           | Research packages that support an ARD and remain linked from architecture requirements                              | System Architect        |
| `docs/02.architecture/decisions/`             | 02           | Architecture decision records                                                                                      | System Architect        |
| `docs/03.specs/<feature-id>/`                 | 03           | Feature-level spec package containing `spec.md`, `tests.md`, and optional contracts                                | System Architect        |
| `docs/04.execution/plans/`                    | 04           | Active execution plans                                                                                             | Product Manager         |
| `docs/04.execution/tasks/`                    | 04           | Active task and validation evidence                                                                                | QA Inspector            |
| `docs/05.operations/guides/`                  | 05           | Stable user, developer, and operator guides                                                                        | Technical Writer        |
| `docs/05.operations/policies/`                | 05           | Operational policies and standards                                                                                 | Ops Manager             |
| `docs/05.operations/policies/post-launch/`    | 05           | Post-launch policy packages retained on `dev` for template-maintenance evidence and derived-project adaptation       | Ops Manager             |
| `docs/05.operations/policies/resilience/`     | 05           | Resilience policy packages retained on `dev` for template-maintenance evidence and derived-project adaptation        | Ops Manager             |
| `docs/05.operations/runbooks/`                | 05           | Executable operational procedures                                                                                  | SRE / Platform Engineer |
| `docs/05.operations/incidents/`               | 05           | Incident records and postmortems                                                                                   | SRE / Security          |
| `docs/90.references/knowledge/`               | 90           | Reviewed knowledge indexes and reference companions retained on `dev`; `main` release skeleton may omit this folder | Knowledge Curator       |
| `docs/99.templates/expanded/`                 | 99           | Optional expanded Markdown templates for DDD and Stage 04 companion documents                                      | Governance Architect    |
| `docs/99.templates/extended/`                 | 99           | Optional machine-readable contract templates for adopted GraphQL/gRPC technologies                                 | Governance Architect    |

### Procedure for Adding a New Subfolder

1. Update this registry with the new subfolder path, parent stage, purpose, and owner.
2. Create a `README.md` inside the subfolder using `docs/99.templates/readme.template.md`.
   Dynamic Stage 04 feature folders satisfy this requirement with a package README that indexes the feature spec files.
3. Commit the registry update and README in the same atomic commit before adding content.

### HALT Condition

**HALT** if a subfolder exists under `docs/` that is not listed in this registry.
Report the unlisted subfolder and request governance approval before proceeding.
This applies to tracked directories, non-empty local directories, and empty local-only
directories because empty unregistered folders still mislead agents about the canonical
stage structure.

---

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
