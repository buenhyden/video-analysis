# .agents

Legacy/helper compatibility surface for optional Graphify guidance.

`.claude/**`, `.codex/agents/*.toml`, and Stage 00 governance are authoritative.
Graphify policy lives in [Documentation Protocol §11](../docs/00.agent-governance/rules/documentation-protocol.md).
Files under this directory may point to helper workflows, but must not define
independent agent policy, active skills, hooks, or reusable template ownership.
The tracked allowlist is `README.md`, `rules/graphify.md`, and `workflows/graphify.md`;
new `.agents/**` files require Stage 00 governance and validator updates.
