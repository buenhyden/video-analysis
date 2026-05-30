---
version: <string> # e.g., "alpha", "1.0", "2.0-beta"
name: <string> # project name, e.g., "MyApp"
description: <string> # optional — one-line brand description
colors:
  primary-base: <Color>
  surface-base: <Color>
  text-primary: <Color>
  border-subtle: <Color>
  state-error: <Color>
typography:
  body-md:
    fontFamily: <string>
    fontSize: <Dimension>
    lineHeight: <Dimension | number>
    fontWeight: <number | string>
  heading-md:
    fontFamily: <string>
    fontSize: <Dimension>
    lineHeight: <Dimension | number>
    fontWeight: <number | string>
rounded:
  sm: <Dimension>
  md: <Dimension>
spacing:
  sm: <Dimension | number>
  md: <Dimension | number>
  lg: <Dimension | number>
components:
  button-primary:
    background: colors.primary-base
    foreground: colors.text-primary
    radius: rounded.md
    paddingInline: spacing.md
---

# Design System

<!-- Target: DESIGN.md (root) -->

## Usage Guidance

- **When to use**: Single source of truth for all UI/frontend visual design.
- **Mandatory sections**: Brand & Style, Colors, Typography, Components.
- **Naming rule**: `DESIGN.md`.
- **Hard Stops**: STOP if `version` is absent or `name` is `<string>`. STOP if UI code uses hardcoded values instead of tokens.

## Purpose

The Design System ensures visual consistency and professional aesthetics across the entire application. It provides a shared language (tokens) for designers and developers to describe UI elements.

<!-- AI AGENT INSTRUCTION:
Read this entire file before writing any frontend/UI code.
If `version` or `name` in the YAML frontmatter is still "<string>",
HARD STOP — ask the product owner to define the design system first.
All color, typography, spacing, and component decisions must reference tokens
defined in the YAML frontmatter above. Never hardcode visual values.
-->

## Authority

DESIGN.md is the workspace source template and project-local source of truth for
frontend, mobile, app, and UI visual decisions. New projects must initialize this
file before their first frontend Stage 04 Spec. Existing projects must keep it
current whenever reusable UI tokens or component treatments change.

This file intentionally lives at the workspace root rather than in
`docs/99.templates/`; downstream projects fill this root file in place as their
project-specific design system.

Agents must not treat screenshots, ad hoc CSS, or a generated component as a
design-system substitute. If a UI decision is not represented here, add or update
the relevant token group before closing implementation, or record an ADR for a
deliberate deviation.

## Phase 0 — New Project Initialization

> **For new projects**: Fill this file BEFORE any other frontend or UI work begins.
> This is the first required step for any project with a frontend, mobile, or app layer.

### Step 1 — Fill the YAML frontmatter (above)

Minimum required fields before Stage 04 Spec:

| Field | Example | Required |
| :--- | :--- | :--- |
| `version` | `"alpha"` | Yes — HARD STOP if `<string>` |
| `name` | `"MyApp"` | Yes — HARD STOP if `<string>` |
| `description` | `"One-line brand description"` | Recommended |
| `colors.primary-base` | `"#1A73E8"` | Yes — at least one color token |
| `typography.body-md` | `fontFamily`, `fontSize`, `lineHeight`, `fontWeight` | Yes |

### Step 2 — Fill the markdown sections below

Minimum sections to complete before the first frontend spec:

- `## Brand & Style` — one paragraph describing the product personality
- `## Colors` — primary palette tokens at minimum
- `## Typography` — `body-md` and one heading level
- `## Components` — button-primary token group at minimum

### Step 3 — Connect to specs

Every frontend spec in `docs/03.specs/<feature-id>/spec.md` must link this file:

```markdown
## Frontend Design Contract

- **Design System**: `../../../DESIGN.md` — version: [fill in]
- **Design System Status**: Initialized / Partial / Complete
- **Token Groups Used**: [list token groups this feature uses]
```

### Step 4 — Record deviations

Any value not expressible via DESIGN.md tokens must be recorded as an ADR in `docs/02.architecture/decisions/`.

### Step 5 — Keep Stage 04 and Stage 06 in sync

- Stage 04 frontend specs must list the token groups they use.
- Stage 06 implementation tasks must capture evidence that UI code references
  DESIGN.md tokens rather than untracked visual values.
- Any new reusable component must add or reuse a `components.*` token group here
  before task closure.

---

## Brand & Style

<!-- This section is a holistic description of a product's look and feel. It defines the brand personality, target audience, and the emotional response the UI should evoke, such as whether it should feel playful or professional, dense or spacious. It serves as foundational context for guiding the agent's high-level stylistic decisions when a specific rule or token isn't explicitly defined. -->

## Colors

<!--
This section defines the color palettes for the design system.

At least the `primary` color palette must be defined, and additional color palettes may be defined as needed.

When there are multiple color palettes, the design system may assign a semantic role for each palette. A common convention is to name the palettes in this order: `primary`, `secondary`, `tertiary`, and `neutral`.

The `colors` section defines all color design tokens. The color tokens should be derived from the key color palettes defined in the markdown prose. The exact mapping from color palettes to color tokens may follow any consistent naming convention.

It is a
map\<string, Color>, that maps the name of the color token to its value.
 -->

Required token groups:

- `primary-*`: brand and primary action colors.
- `surface-*`: page, panel, overlay, and component surface colors.
- `text-*`: foreground colors for all readable text.
- `border-*`: dividers, outlines, focus rings, and subtle boundaries.
- `state-*`: error, warning, success, info, disabled, and selected states.
- `focus-*`: focus indicators for keyboard and accessibility states.
- `overlay-*`: scrims, modal backdrops, popovers, and elevated overlays when used.

Agents must reference these tokens by name in frontend code. Literal hex, RGB,
HSL, shadow color, or ad hoc palette values are not allowed in implementation
unless an ADR records the exception.

## Typography

<!--
This section defines typography levels.

Most design systems have 9 - 15 typography levels. The design system may prescribe a role for each typography level.

A common naming convention for typography levels is to use semantic categories such as `headline`, `display`, `body`, `label`, `caption`. Each category may further be divided into different sizes, such as `small`, `medium`, and `large`.

The `typography` section defines the precise font properties for the typography design tokens.

It is a
map\<string, Typography>
-->

Required minimum:

- `body-md` for default readable text.
- at least one heading token, such as `heading-md`.
- label/caption tokens when compact controls, tables, sidebars, forms, or dense
  dashboards are implemented.

Typography tokens must define font family, size, line height, and weight. Do not
scale font sizes directly with viewport width in implementation code.

## Layout & Spacing

<!--
Also known as "Layout & Spacing".

This section describes the layout and spacing strategy.

Many design systems follow a grid-based layout. Others, like Liquid Glass, use margins, safe areas, and dynamic padding.

The spacing section defines the spacing design tokens. These may include spacing units that are useful for implementing the layout model. For example, a fixed grid layout may have spacing units for column spans, gutters, and margins.

It is a
map\<string, Dimension | number> that maps the spacing scale identifier to a dimension value or a unitless number (e.g., column counts or ratios).
-->

## Elevation & Depth

<!--
Also known as "Elevation".

This section describes how visual hierarchy is conveyed based on the design style. If elevation is used, it defines the required styling (spread, blur, color). For flat designs, this section explains the alternative methods used to convey visual hierarchy (e.g., borders, color contrast).
-->

## Shapes

<!--
This section describes how visual elements are shaped.

The `rounded` section defines the design tokens for rounded corners used in
buttons, cards, and other rectangular shapes.

-->

## Components

<!--
This section provides style guidance for component atoms within the design system. The following are common component types. Design systems are encouraged to define additional components relevant to their domain.

* **Buttons**: Covers primary, secondary, and tertiary variants, including sizing, padding, and states.
* **Chips**: Covers selection chips, filter chips, and action chips.
* **Lists**: Covers styling for list items, dividers, and leading/trailing elements.
* **Tooltips**: Covers positioning, colors, and timing.
* **Checkboxes**: Covers checked, unchecked, and indeterminate states.
* **Radio buttons**: Covers selected and unselected states.
* **Input fields**: Covers text inputs, text areas, labels, helper text, and error states.

> **Note:** The components specification is actively evolving. The current structure provides intentional flexibility for domain-specific component definitions while the spec matures.

The components section defines a collection of design tokens used to ensure consistent styling of common components. It's a map\<string, map\<string, string>> that maps a component identifier to a group of sub token names and values. The design token values may be literal values, or references to previously defined design tokens.

**Variants**. A component may have a variant for different UI states such as active, hover, pressed, etc. Those variant components may be defined under a different but related key, for example, "button-primary", "button-primary-hover", "button-primary-active". The agent will consider all variants and make the appropriate styling decisions.
-->

Required component token coverage before implementation:

- interactive controls: buttons, icon buttons, links, checkboxes/radio controls,
  text inputs, selects, sliders, menus, tabs, and tooltips when used.
- data display: tables, list rows, status badges, empty states, and error states
  when used.
- layout primitives: page shell, navigation, modal/dialog, toolbar, and panel
  treatments when used.

Every new reusable component introduced by a frontend feature must either use an
existing component token group or add a new group here before implementation is
closed.

Each component token group should define the minimum visual contract needed for
consistent implementation: surface/foreground color, border or outline, radius,
spacing, typography reference, focus state, disabled state, and interaction
states when applicable. Compact operational tools should prefer dense,
predictable controls over marketing-style layout unless the PRD explicitly calls
for a promotional page.

## Do's and Don'ts

<!--
This section provides practical guidelines and common pitfalls. These act as guardrails when creating designs.
-->

# Recommended Token Names (Non-Normative)

<!--
The following names are commonly used across design systems. They are not required but are provided as guidance for consistency.

**Colors:** `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`

**Typography:** `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`

**Rounded:** `none`, `sm`, `md`, `lg`, `xl`, `full`
-->

# Consumer Behavior for Unknown Content

<!--
When a DESIGN.md consumer encounters content not defined by this spec:

| Scenario | Behavior | Example |
| --- | --- | --- |
| Unknown section heading | Preserve; do not error | `## Iconography` |
| Unknown color token name | Accept if value is valid | `surface-container-high: '#ede7dd'` |
| Unknown typography token name | Accept as valid typography | `telemetry-data` |
| Unknown spacing value | Accept; store as string if not a valid dimension | `grid-columns: '5'` |
| Unknown component property | Accept with warning | `borderColor` |
| Duplicate section heading | Error; reject the file | Two `## Colors` headings |
-->

## AI Execution Checklist

### Entry Gate (Before Any Frontend Work)

- [ ] `version` field is set (not `<string>`) — design system is initialized
- [ ] `name` field is set to the actual project name
- [ ] `colors.primary` palette is defined with at least a base token
- [ ] `typography` section has at least `body-md` and one heading level
- [ ] `## Brand & Style` section describes the product personality (not empty/comment-only)
- [ ] This file is committed to the repo before Stage 04 Spec for any frontend feature

### During Implementation

- [ ] Every color value in UI code references a token from this file (no hardcoded hex)
- [ ] Every font-size references a typography token
- [ ] Every spacing value uses a token from the `spacing` map
- [ ] New component patterns introduced during implementation are added to `## Components`
- [ ] Deviations from this design system are recorded in `docs/02.architecture/decisions/`
- [ ] Frontend specs link this file from `docs/03.specs/<feature-id>/spec.md`
      using `../../../DESIGN.md`

### Exit Gate (After Feature Delivery)

- [ ] New component tokens documented if new components were introduced
- [ ] `version` bumped if breaking design changes were made
- [ ] `docs/03.specs/<feature-id>/spec.md` links back to this file under `## Frontend Design Contract`

## Related Documents

- **Frontend Scope Rules**: `docs/00.agent-governance/scopes/frontend.md`
- **Feature Spec**: `docs/03.specs/<feature-id>/spec.md` — must reference this file under `## Frontend Design Contract`
- **Design Decisions (ADR)**: `docs/02.architecture/decisions/` — record significant design system choices here
- **Template Reference**: `docs/99.templates/` — spec and task templates for frontend features
