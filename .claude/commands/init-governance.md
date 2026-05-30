# /init-governance

Initialize the governance layer for a new project derived from this template.

## What This Command Does

Runs the bootstrap sequence for a fresh repository clone or a new feature branch:

1. Verifies all governance files exist and link correctly.
2. Confirms project initialization intake is available before new-project stage authoring.
3. Checks that `.pre-commit-config.yaml` is present and hooks are installed.
4. Confirms `docs/99.templates/` is complete (all required templates present).
5. Outputs a readiness report.

## Steps

```bash
# 1. Verify governance structure
bash scripts/validation/validate-doc-governance.sh

# 2. Verify cross-links
bash scripts/validation/validate-cross-links.sh

# 3. Reproduce CI pre-commit checks when the tool is available locally
pre-commit --version && pre-commit run --all-files --show-diff-on-failure || echo "pre-commit unavailable; rely on ws validate and CI"

# 4. Confirm required templates exist
for t in prd ard adr spec tests guide operation slo runbook incident postmortem plan task readme reference; do
  f="docs/99.templates/${t}.template.md"
  [[ -f "$f" ]] && echo "✅ $f" || echo "❌ MISSING: $f"
done

# 5. Confirm intake rule exists
test -f docs/00.agent-governance/rules/project-initialization-intake.md && echo "✅ intake rule"
```

## Expected Output

All checks green before starting any feature work. If any check fails, resolve before proceeding.
