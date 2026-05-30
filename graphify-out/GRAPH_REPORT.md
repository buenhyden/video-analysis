# Graph Report - Project-Template  (2026-05-22)

## Corpus Check
- 9 files · ~152,194 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 500 nodes · 838 edges · 22 communities detected
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 41 edges (avg confidence: 0.75)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 27 edges
2. `Workspace Agent Contract` - 14 edges
3. `validate_path_label_href_alignment()` - 13 edges
4. `validate_workflow()` - 12 edges
5. `main()` - 12 edges
6. `Agent Scope Definitions Index` - 12 edges
7. `LLM-WIKI Navigation Index` - 11 edges
8. `Technical Specification` - 11 edges
9. `Stage-Gate SDLC` - 11 edges
10. `validate_template_inventory_cells()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Bandit Security Scan Scope` --conceptually_related_to--> `Stage 00 Governance Policy Surface`  [INFERRED]
  bandit.yaml → AGENTS.md
- `README Contracts` --conceptually_related_to--> `Script Inventory Source`  [INFERRED]
  scripts/validation/validate-doc-readiness.py → scripts/README.md
- `No GitHub-Native AI Instruction Layer` --implements--> `Workspace Agent Contract`  [EXTRACTED]
  docs/00.agent-governance/providers/gemini.md → AGENTS.md
- `UI Design Hard Stop` --conceptually_related_to--> `Canonical Templates Directory`  [INFERRED]
  DESIGN.md → AGENTS.md
- `MkDocs Stage-Gate Navigation` --implements--> `Stage-Gate SDLC Flow`  [EXTRACTED]
  mkdocs.yml → AGENTS.md

## Hyperedges (group relationships)
- **Runtime Authority Boundary Set** — generate_llm_wiki_index_authority_boundary, agent_hook_dispatch_claude_settings_hooks, validate_runtime_contracts_forbidden_policy_surfaces, validate_doc_readiness_runtime_count_freshness [INFERRED 0.85]
- **Workspace Validation Gate Set** — scripts_readme_ws_validate_gate, validate_doc_readiness_template_readiness_validator, validate_script_inventory_script_inventory_validator, validate_github_workflows_workflow_governance_validator, validate_runtime_contracts_runtime_contract_validator [EXTRACTED 1.00]
- **Stage-Gate Documentation Contract** — agents_stage_gate_flow, agents_docs_8_folder_model, agents_templates_directory, docs_readme_index_contract [EXTRACTED 1.00]
- **Runtime Authority Model** — agents_workspace_contract, agents_canonical_claude_runtime, agents_codex_compatibility_metadata, providers_gemini_runtime_boundary [EXTRACTED 1.00]
- **Runtime Authority Boundary** — concept_canonical_claude_runtime, concept_codex_compatibility_metadata, concept_transient_dispatch_packets, decisions_runtime_compatibility_transient_dispatch [EXTRACTED 1.00]
- **Stage 01-06 Traceability Chain** — requirements_agentic_sdlc_template_governance, requirements_agentic_sdlc_documentation_architecture, decisions_template_hard_stop_enforcement, concept_cross_stage_traceability [EXTRACTED 1.00]
- **Runtime Governance Boundary** — runtime_authority, codex_compatibility_boundary, harness_library_ssot, validation_scripts, stage90_navigation_boundary [EXTRACTED 1.00]
- **Operations Traceability Loop** — operations_policy_guardrails, runbooks_operational_procedures, incident_record, blameless_postmortem, postmortem_feedback_loop [EXTRACTED 1.00]
- **LLM-WIKI Curation Surfaces** — llm_wiki_curation_workflow, llm_wiki_operating_summary, llm_wiki_navigation_index, wiki_curator_role [EXTRACTED 1.00]
- **Operations Feedback Loop** — slo_slo_specification, runbook_operational_runbook, incident_incident_record, guide_user_operator_guide, task_task_list [INFERRED 0.75]
- **SDLC Stage Traceability Chain** — prd_product_requirements_document, ard_architecture_reference_document, adr_architecture_decision_record, spec_technical_specification, plan_implementation_plan, task_task_list [EXTRACTED 1.00]
- **DDD Expansion Companion Set** — ard_ddd_strategic_design, expanded_domain_model, expanded_tactical_model, expanded_ubiquitous_language_glossary, ddd_aggregate_invariants [EXTRACTED 1.00]
- **Domain Driven Design Contract Set** — bounded_context_template_bounded_context, bounded_context_template_ubiquitous_language, domain_events_template_domain_event_catalog, domain_events_template_consumer_contracts [EXTRACTED 1.00]
- **Scope Persona Authority Model** — scopes_agent_scope_definitions, scopes_policy_ssot, concept_stage_gate_taxonomy, concept_runtime_inventory_parity [INFERRED 0.85]
- **Implementation Traceability Chain** — sdlc_procedure_prd_stage, sdlc_procedure_spec_stage, sdlc_procedure_plan_stage, sdlc_procedure_task_stage, sdlc_procedure_universal_evidence_rule [EXTRACTED 1.00]
- **Bootstrap Governance Entry Flow** — bootstrap_sequence, preflight_entry_gate, persona_activation_protocol, stage_gate_matrix, agentic_rpevu_cycle [EXTRACTED 1.00]
- **Runtime Policy Surface Triad** — agents_md_agents_md_ssot, claude_claude_memory_hierarchy, harness_runtime_surfaces, standards_balanced_router [INFERRED 0.85]
- **Governed Memory Boundary** — memory_hub, memory_methodology_state, memory_progress_surface, governance_policy_change_log, governance_baton_workflow [EXTRACTED 1.00]
- **Stage Progression Traceability** — requirements_architecture_reference_documents, specs_specifications_hub, execution_execution_hub, operations_operations_hub [INFERRED 0.85]
- **Compact Docs Migration Validation Closure** — compact_docs_compact_8_folder_model, compact_docs_validation_bundle, tasks_task_evidence_layer [EXTRACTED 1.00]
- **Local Hook Runtime Control Surface** — hooks_claude_settings_contract, hooks_provider_neutral_dispatcher, hooks_ws_hook_command, hooks_hook_policy_hardening [EXTRACTED 1.00]
- **Canonical Governance Boundary** — readme_generated_intelligence_artifacts, readme_governance_rules_index, postflight_checklist_policy_consistency [INFERRED 0.85]
- **Guide Authoring Workflow** — readme_operations_guides, readme_guides_layer, readme_guide_template, onboarding_human_human_onboarding_guide [EXTRACTED 1.00]
- **Hook Policy Hardening Flow** — 2026_05_10_hook_policy_hardening_sensitive_file_guardrails, 2026_05_10_hook_policy_hardening_git_policy_bash_hook, 2026_05_10_hook_policy_hardening_docs_readme_sync_hook, 2026_05_10_hook_policy_hardening_hook_smoke_tests [EXTRACTED 1.00]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (84): authorized_docs_subfolder_patterns(), canonical_template_conformance_issues(), directory_state(), documents_table_rows_with_line_numbers(), expected_readme_links(), expected_stage_links(), frontmatter_keys(), git_tracks_path() (+76 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (41): Claude Runtime Authority, Compact 8-Folder Docs Model, Template Authority in docs/99.templates, Compact Docs Validation Bundle, Execution Hub, GitHub QA Git-flow Revalidation, Strict-Derived Activation Boundary, GitHub Workflow Logic Preservation (+33 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (38): Agent-first Engineering, Blameless Postmortem, Codex Compatibility Boundary, Root DESIGN.md Authority, Governed Templates, docs-governance Role, Docs Governance Refactor Walkthrough, Durable Reference (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (37): Canonical Claude Runtime Surface, Codex Compatibility Metadata, 8-Folder Compact Docs Model, Git-Flow PR-Only Policy, Stage 00 Governance Policy Surface, Graphify Generated Context, Language-Agnostic AI-Native Project Template, Analyze Plan Execute Validate Sync Loop (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (36): Architecture Hub, ADR Layer, Canonical .claude Runtime Surface, Codex Compatibility Metadata, Compact 8-Folder Docs Model, Cross-Stage Traceability, DESIGN.md Hard Stop Gate, LLM-WIKI Operating Summary (+28 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (36): Architecture Decision Record, API Specification, Architecture Reference Document, Bounded Context Overlay, C4 Context Diagram, DDD Strategic Design, Aggregate Invariants, Domain Model (+28 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (33): AI Agent-First Engineering Contract, Hard Stop Enforcement, RPEVU Cycle, AGENTS.md Source Of Truth, Platform Overlay Pattern, Bootstrap Sequence, Canonical Workspace Validation, Mandatory 90 Percent Coverage Gate (+25 more)

### Community 7 - "Community 7"
Cohesion: 0.17
Nodes (25): checkout_credentials_allowed(), checkout_persists_credentials(), codeql_languages_include_actions(), is_first_party_action(), iter_runs(), job_display_name(), main(), normalize_branches() (+17 more)

### Community 8 - "Community 8"
Cohesion: 0.1
Nodes (26): Docs README Sync Hook, Git Policy Bash Hook, Hook Policy Hardening Tasks, Hook Smoke Tests, Sensitive File Guardrails, Cross-Layer Refactoring Gate, Evolution Protocol, Policy Change Log (+18 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (21): Canonical Hook Dispatcher, .claude Settings Hooks, Generated Navigation Authority Boundary, LLM-WIKI Navigation Index, Offline Repository Intelligence, Active Automation Surface, Direct Governance Commands, Script Inventory Source (+13 more)

### Community 10 - "Community 10"
Cohesion: 0.35
Nodes (15): agent_rows(), clean_cell(), codex_rows(), direct_command_rows(), docs_entry_rows(), existing_last_updated(), frontmatter(), main() (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (13): iter_github_text_files(), main(), validate_about_workflow_coverage(), validate_codeowners(), validate_coverage_gate(), validate_derived_placeholders(), validate_duplicate_github_surfaces(), validate_labeler() (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.17
Nodes (13): Anti-Corruption Layer, Bounded Context, Context Boundaries, Context Map Integration Patterns, Parent ARD DDD Trigger, Ubiquitous Language, Consumer Contracts, Domain Event Catalog (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (11): active_roots(), git_tracked_files(), has_local_files(), main(), major(), major_minor(), read_json(), validate_docker() (+3 more)

### Community 14 - "Community 14"
Cohesion: 0.32
Nodes (11): event_commands(), load_settings(), main(), referenced_local_paths(), validate_forbidden_surfaces(), validate_hooks(), validate_local_settings_separation(), validate_permissions() (+3 more)

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (10): dispatch(), first_text(), hydrate_portable_tool_env(), load_hooks(), main(), matcher_applies(), parse_hook_input(), Translate provider-neutral or Codex hook inputs into Claude hook env names. (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.42
Nodes (8): direct_command_scripts(), inventory_rows(), iter_text_files(), main(), retention_markers(), script_files(), ws_case_commands(), ws_help_commands()

### Community 17 - "Community 17"
Cohesion: 0.42
Nodes (8): first_text(), is_target_markdown_stage_doc(), load_readiness(), machine_readable_issues(), main(), read_hook_json(), rel_path_for(), tool_input_from_hook()

### Community 18 - "Community 18"
Cohesion: 0.25
Nodes (9): Workflow Security Policy, Claude GitHub Boundary, Conventional Commits, Git-Flow Strategy, PR-Only Merge Policy, Branch Protection, GitHub Repository Security Policy, Secret Exposure Response (+1 more)

### Community 19 - "Community 19"
Cohesion: 0.46
Nodes (7): build_repo_map(), classify(), count_lines(), git_ls_files(), main(), write_mermaid(), write_summary()

### Community 20 - "Community 20"
Cohesion: 0.5
Nodes (5): Active Methodology, spec-driven-sdlc, Session Progress, Durable Session Memory, Stage 00 Memory

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (3): Compliance and Audit Hub, Data Governance and Integrity Index, Encryption and KMS Standards

## Ambiguous Edges - Review These
- `Stage 05 Plan` → `TDD Auto-Link`  [AMBIGUOUS]
  docs/99.templates/tests.template.md · relation: conceptually_related_to

## Knowledge Gaps
- **80 isolated node(s):** `Translate provider-neutral or Codex hook inputs into Claude hook env names.`, `Reject placeholder leakage only in template README Documents tables.`, `Validate only links whose visible label is itself a relative path.`, `Validate target-relative parent references in machine-readable templates.`, `Reject code-span pseudo-links in generated Inputs/Related Documents sections.` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Stage 05 Plan` and `TDD Auto-Link`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `LLM-WIKI Navigation Index` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `Workspace Validate Gate` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **What connects `Translate provider-neutral or Codex hook inputs into Claude hook env names.`, `Reject placeholder leakage only in template README Documents tables.`, `Validate only links whose visible label is itself a relative path.` to the rest of the system?**
  _80 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._