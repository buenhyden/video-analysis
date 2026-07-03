---
name: research-brief
description: Produces structured pre-implementation research briefs for libraries, patterns, APIs, and architectural options. Use before major implementation or architecture work. Triggers on 'research this library', 'compare these options', 'literature review', 'prior research analysis', 'evaluate this API', 'architecture option comparison', 'organize research materials', 'search for papers', 'research trend analysis', 'literature search', or any request to gather evidence before a technical decision.
---

# Research Brief

Run focused technical research before implementation starts.

## Research Modes

| Mode                           | Trigger                                          | Scope                                         |
| ------------------------------ | ------------------------------------------------ | --------------------------------------------- |
| Library Evaluation             | "Evaluate this library / compare these packages" | Features, maturity, license, maintenance      |
| Pattern Analysis               | "What patterns exist for X"                      | Implementation patterns, trade-offs, adoption |
| External API Research          | "How does this API work"                         | Auth, rate limits, data models, SDK quality   |
| Architecture Option Comparison | "What are our options for X"                     | Capabilities, fit, risk per option            |
| Academic / Prior Art           | "Literature review", "prior research on X"       | Papers, thematic synthesis, research gaps     |

## Workflow

### Phase 1: Scope Definition

1. Define the decision question and success criteria before searching anything.
2. Extract from the request:
   - **Research question**: What decision will this brief inform?
   - **Success criteria**: What makes one option clearly better?
   - **Constraints**: Time period, language, licensing, budget, compatibility
   - **Existing materials** (optional): ADRs, specs, existing docs to build on
3. Save the scoped question to `_workspace/00_research_scope.md`.

### Phase 2: Local Evidence First

Read relevant local documents before searching externally:

- Existing ADRs in `docs/02.architecture/decisions/`
- Architecture docs in `docs/02.architecture/requirements/`
- Related specs in `docs/03.specs/`
- Agent guidance in `.Codex/agents/`

If the answer is already in local docs, report it — do not re-research what is already decided.

### Phase 3: Primary Source Collection

Gather primary-source evidence for external technologies:

**Source Hierarchy:**

| Priority | Source Type                           | Use When                              |
| -------- | ------------------------------------- | ------------------------------------- |
| 1        | Official documentation / changelog    | Always — authoritative                |
| 2        | Repository README and issues          | Implementation details, known bugs    |
| 3        | Academic papers (for research briefs) | Prior art, algorithm correctness      |
| 4        | Reputable blog posts / case studies   | Real-world usage patterns             |
| 5        | Community forums                      | Edge cases only; verify independently |

**Search Protocol:**

- Prefer Boolean queries for academic research: `("topic A") AND ("topic B") NOT ("topic C")`
- Verify version currency: check the date on every source
- For each option, find at least one primary source and one independent usage report

Save raw evidence to `_workspace/01_evidence.md`.

### Phase 4: Findings Analysis

Separate findings into three categories:

**Facts** — verifiable claims with a source citation:

```
Claim: [statement]
Source: [URL or document]
Verified: Yes / Partial / No
```

**Trade-offs** — genuine tensions where reasonable people disagree:

```
Option A advantage: [what A does better]
Option B advantage: [what B does better]
Context dependency: [when to prefer each]
```

**Open Questions** — things the research could not resolve:

```
Question: [what is unknown]
Why it matters: [impact on the decision]
How to resolve: [experiment, prototype, ask expert]
```

Save to `_workspace/02_findings.md`.

### Phase 5: Option Comparison

For each option evaluated, produce a structured comparison:

```
## Option Comparison

| Criterion | Option A | Option B | Option C |
|-----------|---------|---------|---------|
| Maturity | | | |
| License | | | |
| Maintenance | | | |
| Performance | | | |
| Learning curve | | | |
| Community | | | |
| Fit to constraints | | | |
```

Weight criteria by the decision's success criteria defined in Phase 1.

### Phase 6: Recommendation

End with an explicit recommendation and its assumptions:

```
## Recommendation

**Recommended**: [Option / pattern / library]

**Rationale**: [Why this option wins on the success criteria]

**Key Assumptions**:
- [Assumption 1 — if this is wrong, the recommendation may change]
- [Assumption 2]

**Risks**:
- [Risk 1 with mitigation]

**Unresolved Questions** (must answer before implementation):
- [Question requiring prototype or expert input]
```

Save to `_workspace/03_recommendation.md`.

### Phase 7: Output Brief

Assemble the final brief with all sections:

- Research context (question, constraints, scope)
- Key questions answered
- Findings: facts / trade-offs / open questions
- Option comparison table
- Recommendation with rationale and assumptions
- Unresolved questions with resolution plan

## Output Format

```markdown
# Research Brief: [Topic]

> **Decision**: [What will be decided using this brief]
> **Requested by**: [persona or stage]
> **Date**: YYYY-MM-DD

## Summary

[2–3 sentences: what was found and what is recommended]

## Research Scope

[Decision question, constraints, success criteria]

## Findings

### Facts

...

### Trade-offs

...

## Option Comparison

[Table]

## Recommendation

[Recommendation + rationale + assumptions]

## Open Questions

[List with resolution plan]

## Sources

[Numbered list of all cited sources]
```

## Academic Research Support

For literature review requests, apply thematic synthesis:

| Synthesis Step              | Action                                                  |
| --------------------------- | ------------------------------------------------------- |
| Thematic coding             | Group sources by recurring themes                       |
| Research gap identification | Note what is absent from existing literature            |
| Temporal development        | Track how the field evolved over time                   |
| Consistency verification    | Cross-check claims between sources; flag contradictions |

Citation formats — default to APA 7th unless specified:

- APA 7th: `Author, A. A. (Year). Title. Journal, Vol(Issue), pages. DOI`
- Chicago: `Author. "Title." Journal Vol, no. Issue (Year): pages.`

## Rules

- Research is read-only — do not modify any project files during a research brief.
- Prefer official docs and repository-native evidence over secondary sources.
- If evidence conflicts, call out the conflict explicitly with both sources cited.
- Do not present preference as fact — label opinions as opinions.
- Mark unverified claims as "[unverified]" rather than omitting them.

## Error Handling

| Scenario                           | Strategy                                                            |
| ---------------------------------- | ------------------------------------------------------------------- |
| Web search failure                 | Recommend based on known primary sources; note "search limitations" |
| Full text inaccessible             | Work from abstract; mark "full text unverified"                     |
| Insufficient sources               | Expand to adjacent fields; label as "preliminary synthesis"         |
| Evidence conflicts between sources | Report both; identify which is more authoritative and why           |
| Citation format unknown            | Apply APA 7th as default; note format assumption                    |
