# /run-preflight

Run the preflight checklist before starting any task. Equivalent to manually working through `docs/00.agent-governance/rules/preflight-checklist.md`.

## What This Command Does

Performs the Entry Gate checks automatically:

1. Verifies a non-README PRD anchor exists in `docs/01.requirements/` when the task writes project-owned downstream stage documents.
2. Verifies Spec anchor exists in `docs/03.specs/` for implementation tasks.
3. Checks that the active persona's required scope file exists.
4. Confirms no broken references in recently modified docs.
5. Reports environment readiness when setup, validation prerequisites, local tooling, or runtime readiness are in scope.
6. Outputs a pass/fail checklist.

Release-template skeleton maintenance and initial intake/bootstrap work are exceptions:
they may start from README skeletons and the intake rule before a project PRD exists.
For ordinary derived-project work, complete intake and create the bootstrap PRD seed
before authoring ARD, ADR, spec, plan, task, operations, or reference documents.
Template-maintenance work on `dev` may use an active-template-contract PRD when
the lifecycle rule explicitly classifies it as template history.

## Steps

```bash
# 1. Check PRD anchor.
# README.md is release-skeleton guidance, not a PRD. Accept either the
# bootstrap-generated intake seed or a non-README document whose frontmatter,
# title, or H1 identifies it as PRD/Product Requirements.
python3 - <<'PY'
from pathlib import Path
import re
import sys

anchors = []
for path in sorted(Path("docs/01.requirements").glob("*.md")):
    if path.name == "README.md":
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    head = "\n".join(text.splitlines()[:60])
    if path.match("*project-intake-prd.md") or re.search(r"\b(PRD|Product Requirements)\b", head, re.IGNORECASE):
        anchors.append(path.as_posix())

if anchors:
    print(f"✅ Non-README PRD anchor found: {anchors[0]}")
else:
    print("❌ No non-README PRD anchor in docs/01.requirements/")
    sys.exit(1)
PY

# 2. Check Spec anchor (for implementation)
ls docs/03.specs/ 2>/dev/null && echo "✅ Spec directory exists" || echo "❌ No specs in docs/03.specs/"

# 3. Check templates
for t in prd ard adr spec; do
  [[ -f "docs/99.templates/${t}.template.md" ]] && echo "✅ Template: ${t}" || echo "❌ MISSING template: ${t}"
done

# 4. Validate cross-links
bash scripts/validation/validate-cross-links.sh

# 5. Governance check
bash scripts/validation/validate-doc-governance.sh

# 6. Environment readiness report when local tooling or setup is in scope
bash scripts/ws.sh setup
```

If environment readiness is not in scope, step 6 may be skipped. Do not install tools or mutate local configuration from preflight.

## GitHub Governance Check (when `.github/**` is in scope)

Run this additional check if the task touches `.github/**`, CI/CD files, or agent runtime configuration:

```bash
# Check for GitHub token literals in tracked files
git ls-files | xargs grep -lE '(ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{82})' 2>/dev/null \
  && echo "❌ GitHub token literal found in tracked files" \
  || echo "✅ No GitHub token literals in tracked files"

# Verify settings.local.json is not tracked
git ls-files .claude/settings.local.json | grep -q . \
  && echo "❌ settings.local.json is tracked — must be gitignored" \
  || echo "✅ settings.local.json is not tracked"

# Verify GitHub-native instruction files are absent
test -f .github/copilot-instructions.md -o -d .github/instructions \
  && echo "❌ GitHub-native instruction layer detected under .github/" \
  || echo "✅ No GitHub-native instruction layer under .github/"

# Verify repository-local files do not contain GitHub token literals
find .claude .github docs -type f 2>/dev/null | xargs grep -lE '(ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{82})' 2>/dev/null \
  && echo "❌ GitHub token literal found in repository-local files" \
  || echo "✅ No GitHub token literals in repository-local files"
```

See `docs/00.agent-governance/rules/github-repository-governance.md` for full policy.

## On Failure

Stop and resolve before proceeding. Hard stop conditions:

- Missing non-README PRD/Spec anchors for implementation work
- Missing intake PRD seed for derived-project downstream stage authoring
- Broken internal references
- Template missing for required stage
- Missing core governance runtime prerequisites for a task that depends on local validation
- GitHub token literal found in any tracked file
