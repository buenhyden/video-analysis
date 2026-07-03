#!/usr/bin/env bash
# Pre-Tool Validate Hook — checks read/write path and content safety
# Called before Read|Write|Edit|MultiEdit tool execution
# Exit 1 to BLOCK the tool call; exit 0 to ALLOW

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"

TARGET="${CLAUDE_TOOL_INPUT_FILE_PATH:-}"

# No path provided — allow (not a file write)
[[ -z "$TARGET" ]] && exit 0

# Normalize to relative path
REL="${TARGET#"$PROJECT_DIR/"}"

is_sensitive_example_path() {
  local path="$1"
  case "$path" in
    *.example|*.sample|*.template|*.template.*|*/examples/*)
      return 0
      ;;
    .env.example|*/.env.example|.env.sample|*/.env.sample|.env.template|*/.env.template)
      return 0
      ;;
  esac
  return 1
}

is_sensitive_path() {
  local path="$1"
  is_sensitive_example_path "$path" && return 1

  case "$path" in
    auth.json|*/auth.json|*.pem|*.key|*.p12|*.pfx|*.kdbx|*/id_rsa|*/id_ed25519)
      return 0
      ;;
    .env|*/.env|.env.*|*/.env.*)
      return 0
      ;;
    .bash_history|*/.bash_history|.zsh_history|*/.zsh_history|.python_history|*/.python_history)
      return 0
      ;;
    */logs/*.db|*/logs/*.sqlite|*/logs/*.sqlite3|*/.claude/*.db|*/.codex/*.db)
      return 0
      ;;
  esac

  return 1
}

if is_sensitive_path "$REL"; then
  echo "❌ PRE-TOOL BLOCK: Sensitive local file path '$REL' requires explicit human handling." >&2
  echo "   Do not read or mutate credentials, private keys, auth files, shell history, or log databases through agent tooling." >&2
  echo "   See AGENTS.md Codex Runtime and Agent Governance rules." >&2
  exit 1
fi

# Block introduction of GitHub-native AI instruction layers.
# This repository keeps AI instruction ownership in .claude/** and docs/00.agent-governance/**.
if [[ "$REL" == ".github/copilot-instructions.md" ]] || [[ "$REL" == .github/instructions/* ]]; then
  echo "❌ PRE-TOOL BLOCK: GitHub-native instruction files are not used in this repository." >&2
  echo "   Keep AI instruction policy in .claude/** and docs/00.agent-governance/**." >&2
  echo "   See docs/00.agent-governance/rules/github-repository-governance.md §11." >&2
  exit 1
fi

# Block provider-specific or legacy runtime policy surfaces that must not become
# reusable template policy. `.codex/agents/*.toml` is the only shared Codex
# compatibility surface; tracked `.agents/**` is limited to the Graphify helper
# allowlist.
case "$REL" in
  .codex/hooks.json|.codex/hooks|.codex/hooks/*)
    echo "❌ PRE-TOOL BLOCK: Codex-specific hook policy is forbidden." >&2
    echo "   Hook policy belongs in .claude/settings.json, .claude/hooks/**, and provider-neutral ws hook replay." >&2
    exit 1
    ;;
  .codex/agents/*.toml)
    ;;
  .codex/*)
    echo "❌ PRE-TOOL BLOCK: .codex may contain only synchronized agent compatibility metadata." >&2
    echo "   Allowed shared surface: .codex/agents/*.toml." >&2
    exit 1
    ;;
  .agents/README.md|.agents/rules/graphify.md|.agents/workflows/graphify.md)
    ;;
  .agents/skills|.agents/skills/*|.agents/*)
    echo "❌ PRE-TOOL BLOCK: .agents/** is legacy/helper-only and cannot define new policy." >&2
    echo "   Allowed shared files: .agents/README.md, .agents/rules/graphify.md, .agents/workflows/graphify.md." >&2
    exit 1
    ;;
esac

# Block writes containing GitHub token literals to repository-local paths
# Covers: classic PAT (ghp_), OAuth token (gho_), fine-grained PAT (github_pat_)
GITHUB_TOKEN_PATTERN='(ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{82})'
# Edit tool sets CLAUDE_TOOL_INPUT_NEW_STRING; Write tool sets CLAUDE_TOOL_INPUT_CONTENT
CONTENT="${CLAUDE_TOOL_INPUT_CONTENT:-${CLAUDE_TOOL_INPUT_NEW_STRING:-}}"
if [[ -n "$CONTENT" && "$REL" == .github/workflows/* ]]; then
  if echo "$CONTENT" | grep -qE '(^|[[:space:]])pull_request_target([[:space:]]*:|[[:space:]]*$)' 2>/dev/null; then
    echo "❌ PRE-TOOL BLOCK: pull_request_target is prohibited in workflow files." >&2
    echo "   It expands fork PR trust boundaries and can expose write permissions or secrets." >&2
    exit 1
  fi

  if echo "$CONTENT" | grep -qE '(^|[[:space:]])permissions:[[:space:]]+write-all([[:space:]]|$)' 2>/dev/null; then
    echo "❌ PRE-TOOL BLOCK: workflow permissions: write-all is prohibited." >&2
    echo "   Use job-level least-privilege permissions instead." >&2
    exit 1
  fi
fi
if [[ -n "$CONTENT" ]] && echo "$CONTENT" | grep -qEe "$GITHUB_TOKEN_PATTERN" 2>/dev/null; then
  echo "❌ PRE-TOOL BLOCK: GitHub token literal detected in write content targeting '$REL'." >&2
  echo "   Tokens must not appear in repository-local files, including settings.local.json." >&2
  echo "   Use host environment pass-through instead." >&2
  echo "   See docs/00.agent-governance/rules/github-repository-governance.md §4." >&2
  exit 1
fi

PRIVATE_KEY_PATTERN='-----BEGIN [A-Z ]*PRIVATE KEY-----'
if [[ -n "$CONTENT" ]] && echo "$CONTENT" | grep -qEe "$PRIVATE_KEY_PATTERN" 2>/dev/null; then
  echo "❌ PRE-TOOL BLOCK: Private key material detected in write content targeting '$REL'." >&2
  echo "   Private keys must never be written into repository-local files." >&2
  exit 1
fi

# Block additional secret patterns per quality-standards.md §3 safety baselines.
# Covers: AI service API keys (sk-), AWS IAM access key IDs (AKIA)
ADDITIONAL_SECRET_PATTERN='sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}'
if [[ -n "$CONTENT" ]] && echo "$CONTENT" | grep -qEe "$ADDITIONAL_SECRET_PATTERN" 2>/dev/null; then
  echo "❌ PRE-TOOL BLOCK: API key or cloud credential literal detected in write content targeting '$REL'." >&2
  echo "   Patterns blocked: AI service API keys (sk-...), AWS access key IDs (AKIA...)." >&2
  echo "   Credentials must never appear in repository-local files." >&2
  echo "   Use host environment variables or a secret manager instead." >&2
  echo "   See docs/00.agent-governance/rules/quality-standards.md §3." >&2
  exit 1
fi

# Block stage-document writes that do not satisfy their docs/99.templates contract
# when the pending write content is available to the hook.
if [[ -f "$PROJECT_DIR/scripts/validation/validate-stage-template-write.py" ]]; then
  python3 "$PROJECT_DIR/scripts/validation/validate-stage-template-write.py"
fi

# Block writes to docs/99.templates/ unless active persona is meta/governance-architect
# (We can't reliably detect active persona here, so we warn only — do not hard-block)
if [[ "$REL" == docs/99.templates/* ]]; then
  echo "⚠️  PRE-TOOL WARNING: Writing to docs/99.templates/ is restricted to meta/Governance Architect persona." >&2
  echo "   If this is intentional (governance or template change), proceed." >&2
fi

# Block writes to docs/00.agent-governance/ if path looks like a code file
if [[ "$REL" == docs/00.agent-governance/* ]] && [[ "$REL" =~ \.(ts|js|py|go|rs|java|sh)$ ]]; then
  echo "❌ PRE-TOOL BLOCK: Code files must not be written to docs/00.agent-governance/." >&2
  exit 1
fi

# Warn if writing outside common declared scopes (advisory only).
# Implementation roots must be declared by the consuming project before use.
ALLOWED_ROOTS="docs/ examples/ .github/ .claude/ scripts/"
MATCH=0
for root in $ALLOWED_ROOTS; do
  [[ "$REL" == ${root}* ]] && MATCH=1 && break
done
# Also allow root config files
[[ "$REL" =~ ^[A-Z_]+\.md$ ]] && MATCH=1
[[ "$REL" =~ ^\. ]] && MATCH=1

if [[ $MATCH -eq 0 ]]; then
  echo "⚠️  PRE-TOOL WARNING: Write target '$REL' is outside known scope roots." >&2
  echo "   Verify this path is within your active persona's Allowed Write paths." >&2
fi

exit 0
