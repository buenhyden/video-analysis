# Design System Governance

This rule defines the frontend/mobile/app design-system gate for AI agents.

## Authority

- `DESIGN.md` at the repository root is the single source of truth for all UI and frontend visual design decisions.
- `DESIGN.md` is intentionally kept at the workspace root and is not promoted into `docs/99.templates/`.
- New projects that use this repository as a template must fill root `DESIGN.md` in place before frontend/mobile/app/UI Stage 04 specs are approved.
- `docs/03.specs/<feature-id>/spec.md` must include `## Frontend Design Contract` when frontend, mobile, app, or UI implementation is in scope.
- Design deviations that cannot be expressed through `DESIGN.md` tokens require an ADR in `docs/02.architecture/decisions/`.
- Stage 06 frontend tasks must capture evidence that implementation references DESIGN.md token groups.

## Constraints

Before writing any frontend/mobile/app code, read `DESIGN.md`.

Stop immediately when either condition is true:

- `version` is absent or still `<string>`
- `name` is absent or still `<string>`

The agent must ask the product owner to define the design system before frontend implementation proceeds.

## Token Requirements

Frontend code must reference tokens from `DESIGN.md` for:

- colors
- typography
- spacing
- radius
- component styling and states

Hardcoded visual values are forbidden unless an ADR records the exception and the feature spec links that ADR.

## Spec Contract

Frontend specs must record:

- `DESIGN.md` link using `../../../DESIGN.md` from the feature spec package
- design system readiness status
- token groups used by the feature
- new reusable components introduced
- token deviations or the absence of deviations

## Update Rules

- Do not create a design-system template under `docs/99.templates/`; root `DESIGN.md` is the fill-in-place source for project-specific design systems.
- Add new component token groups to `DESIGN.md` before closing implementation tasks.
- Bump the design system version when a breaking design-system change is introduced.
- Record implementation evidence in `docs/04.execution/tasks/` after frontend work is complete.
- Keep DESIGN.md initialized before creating or approving frontend/mobile/app Stage 04 Specs.

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## File references

- `docs/LLM-WIKI.md`
