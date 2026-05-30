# GitHub Repository Governance (April 2026)

> SSOT for all GitHub repository security and operational policies in this repository.
> Agents, scopes, and hooks MUST reference this file rather than re-declaring policy inline.

## 1. Branch Protection

- `main` and `dev` MUST be protected branches at all times.
- Direct push to `main` or `dev` is prohibited; all changes arrive via PR.
- Required: at least 1 approving review before merge.
- Required: all required branch-protection checks listed in §8 must pass before merge.
- Required: PRs must be up-to-date with the base branch before merge.
- Stale approvals are dismissed on new commits.
- Branch deletion after merge is allowed; force-push is prohibited.

Reference: [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

## 2. Code Owners (CODEOWNERS)

- `.github/CODEOWNERS` defines mandatory review assignments per path.
- Governance layer (`docs/00.agent-governance/`) requires review from at least one governance owner.
- Security layer (`docs/05.operations/incidents/`, including postmortems) requires security owner review.
- Workflow files (`.github/workflows/`), GitHub gate helpers (`.github/gates/`), GitHub workflow helper scripts (`.github/scripts/`), and workflow scanner config (`.github/zizmor.yml`) require infra owner review.
- **Placeholder state**: When `CODEOWNERS` contains placeholder owners, enforcement MUST NOT be activated until real owners are assigned. Add a warning comment at the top of the file.

Reference: [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

## 3. GitHub Actions — Secure Use

### 3a. GITHUB_TOKEN Minimum Privilege

- Workflows declare `permissions:` at the job level, not repository-wide.
- Default permission is `read-all`; write access granted only to the specific scope needed.
- Never use `permissions: write-all`.
- Branch-filtered, `workflow_run`, scheduled, tag-triggered, and write-permission workflows must declare `concurrency` to prevent duplicate or conflicting runs.
- Checkout credentials must use `persist-credentials: false` unless a workflow is explicitly creating a generated non-protected branch.

### 3b. Third-Party Action Pinning

- All third-party actions (not `actions/*`) MUST be pinned to a full-length commit SHA, not a tag or branch reference.
- Example: `uses: aquasecurity/trivy-action@a20de5420d57c4102486cdd9349b532bf6eb53b1` not `@v0.20.0`.
- First-party `actions/*` may use tag references.

### 3c. OIDC over PAT for Cloud Authentication

- Workflows that authenticate to cloud providers (AWS, GCP, Azure) MUST use OIDC token exchange.
- PAT-based cloud authentication is prohibited in workflows; use `GITHUB_TOKEN` or OIDC.

Reference: [OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect)

### 3d. Workflow Automation Limits

- Workflows MUST NOT auto-approve PRs they themselves triggered.
- Workflows MUST NOT create PRs and then merge them without human review.
- The `pull-requests: write` permission must not be combined with auto-merge enablement in the same workflow unless explicitly approved via ADR.
- `pull_request_target` is prohibited in the base template unless a future ADR approves the trust boundary and threat model.

Reference: [Secure use reference](https://docs.github.com/en/enterprise-server@3.16/actions/reference/security/secure-use)

## 4. Personal Access Tokens (PAT)

- PAT use in this repository is an exception, not the default.
- Use `GITHUB_TOKEN` wherever possible; use OIDC for cloud; use fine-grained PAT with minimum scopes when PAT is unavoidable.
- PATs MUST NOT appear as literal values in any repository-local file:
  - `.claude/**`, `.github/**`, `docs/**`, root config files, workflow files, and `.claude/settings.local.json`.
  - `.claude/settings.local.json` may reference environment variable names or pass-through wiring only; it must never embed the secret value itself.
  - Valid storage locations are host environment secrets (OS keychain, shell env, CI secret store) outside tracked repository content.
- Classic PATs are prohibited for new integrations; fine-grained PATs only.
- PAT expiry MUST be set (maximum 90 days recommended).

Reference: [Managing personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

## 5. Secret Exposure Response

When a secret (PAT, API key, token) is detected in any tracked file:

1. **Revoke immediately**: Invalidate the exposed credential before any other action.
2. **Rotate**: Issue a replacement credential with minimum required scope.
3. **Remove from history**: Use `git filter-repo` or GitHub's sensitive data removal process to purge the secret from all commits; force-push to all branches after purge.
4. **Audit**: Check audit log for any unauthorized use of the exposed secret during the exposure window.
5. **Document**: Record the incident in `docs/05.operations/incidents/` following the incident template.

Reference: [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## 6. Secret Scanning and Push Protection

> **Private Repository Note**: Secret scanning and push protection require GitHub Advanced Security (GHAS) for private repositories. Enable if GHAS is available; otherwise rely on pre-tool hook guards (`.claude/hooks/pre-tool-validate.sh`) and `quality-standards.md` safety baselines as compensating controls.

- **If GHAS is available**: Enable secret scanning for all branches; alerts reviewed within 48 hours. Enable push protection; bypasses require documented justification in the PR.
- **If GHAS is not available**: Pre-tool and post-tool hooks block GitHub token literals (`ghp_`, `gho_`, `github_pat_`). Additional secret patterns must be added to hook scripts as needed.
- When push protection blocks a push, do NOT use the bypass without security owner approval.
- Custom patterns for project-specific secrets (e.g., internal API key prefixes) should be added to the secret scanning configuration if GHAS is active.

Reference: [About push protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection)

## 7. Code Scanning

> **Private Repository Note**: CodeQL and code scanning require GitHub Advanced Security (GHAS) for private repositories. The workflow is configured as non-blocking to accommodate template repositories without GHAS.

- **If GHAS is available**: Enable CodeQL analysis to run on `push` to `main`/`dev` and on all PRs targeting those branches; triage alerts before release. Treat CodeQL as blocking only when repository code scanning is enabled and `CODE_SCANNING_REQUIRED=true`.
- **If GHAS is not available**: CodeQL analysis/upload remains non-blocking (see `.github/workflows/ci-security.yml`). Active local controls remain Gitleaks plus `bash scripts/ci/validate-security.sh`.
- Third-party SAST tools such as Semgrep OSS or Trivy may supplement the active security gates when explicitly configured by a future governance update.
- CodeQL GitHub Actions analysis must not include compiled-language autobuild steps unless a future stack-specific workflow introduces a compiled language analysis matrix.

## 8. Required Status Checks

- The following checks must pass before any merge into protected branches `main` or `dev`:
  - Canonical workspace validation (`bash scripts/ws.sh validate`)
  - Pre-commit and static checks (`.pre-commit-config.yaml` basis)
  - Conditional 90% line test coverage gate (`.github/gates/check-coverage.sh`; base template may skip only when no active stack manifest exists)
  - Local security and secret checks (`bash scripts/ci/validate-security.sh`, Gitleaks, and configured secret-detection hooks)
  - Stack-specific unit/integration tests when the derived project declares an implementation stack
  - CodeQL/code scanning only when GHAS or equivalent code scanning support is enabled and `CODE_SCANNING_REQUIRED=true`
- Repository automation and diagnostic workflows are not required merge gates unless a future governance update promotes them. This includes `greetings.yml`, `labeler.yml`, `stale.yml`, `ai-remediation.yml`, changelog PR generation, and repository intelligence.
- Check names must be unique and stable; renaming a check requires updating branch protection rules.

## 9. Repository Settings Follow-Up

The following items require manual action in GitHub repository settings (not automated by this governance file):

- [ ] Enable branch protection rules for `main` and `dev` (Settings → Branches)
- [ ] Set required reviewers count (≥ 1) and dismiss stale reviews
- [ ] Enable "Require branches to be up to date" for merge
- [ ] Add required status checks by exact check name
- [ ] Add the conditional coverage job/check to branch protection for every PR path
- [ ] Enable "Require review from Code Owners"
- [ ] Enable Secret scanning + Push protection (Settings → Security) — **requires GHAS for private repos**
- [ ] Enable CodeQL (Settings → Code security → Code scanning) — **requires GHAS for private repos**
- [ ] Replace placeholder owners in `.github/CODEOWNERS` before enforcing

## 10. Template Repository Notice

This is a **template repository**. Placeholder values in CODEOWNERS, SECURITY.md, and PR templates MUST be replaced before enforcement is activated. Governance policy declared here applies to all repositories derived from this template but enforcement must be configured per-repository.

## 11. AI Instruction Layer Ownership

- This repository does **not** adopt GitHub-native AI instruction layers such as:
  - `.github/copilot-instructions.md`
  - `.github/instructions/**`
- Canonical AI instruction ownership remains in:
  - `.claude/**` for Claude runtime behavior and local guardrails
  - `docs/00.agent-governance/**` for repository policy SSOT
- `.github/**` is reserved for repository operations only:
  - workflows
  - templates
  - CODEOWNERS
  - SECURITY policy
  - other GitHub operational metadata
- If a future repository wants GitHub-native instruction files, that is an archetype change and requires an ADR plus a governance update before introduction.

### Private Repository Defaults

This repository is **private**. Features gated behind GitHub Advanced Security (GHAS) are conditional:

| Feature | Public Repo | Private Repo (no GHAS) | Private Repo (GHAS) |
| --- | --- | --- | --- |
| Secret scanning | ✅ free | ❌ unavailable | ✅ available |
| Push protection | ✅ free | ❌ unavailable | ✅ available |
| CodeQL / code scanning | ✅ free | ❌ unavailable | ✅ available |
| Branch protection | ✅ free | ✅ free | ✅ free |
| CODEOWNERS enforcement | ✅ free | ✅ free | ✅ free |
| Required status checks | ✅ free | ✅ free | ✅ free |

**Compensating controls for private repos without GHAS**:

- Pre/post-tool hooks block token literals at agent write time
- `quality-standards.md` safety baselines enforce pattern bans in governance reviews
- CodeQL workflow is non-blocking; upgrade to blocking when GHAS is activated

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
