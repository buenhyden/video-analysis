#!/usr/bin/env bash
# validate-skill-quality.sh
# Checks .claude/skills/ and .claude/agents/ for required structure and current runtime policy.
# Usage: ./scripts/validation/validate-skill-quality.sh
# Exit: 0=pass, 1=warnings, 2=failures

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"
FAILURES=0
WARNINGS=0

echo "=== Skill & Agent Quality Validation ==="

# --- 1. Skill files: frontmatter name + description required ---
echo "[ Check 1 ] Skill frontmatter..."
while IFS= read -r -d '' skill_file; do
  has_name=$(grep -c "^name:" "$skill_file" || true)
  has_desc=$(grep -c "^description:" "$skill_file" || true)
  skill_rel="${skill_file#"$REPO_ROOT"/}"

  if [[ $has_name -eq 0 ]]; then
    echo "  ❌ FAIL: $skill_rel — missing 'name:' in frontmatter"
    FAILURES=$((FAILURES + 1))
  fi
  if [[ $has_desc -eq 0 ]]; then
    echo "  ❌ FAIL: $skill_rel — missing 'description:' in frontmatter"
    FAILURES=$((FAILURES + 1))
  fi

  # Check description length (pushy = more detail)
  desc_len=$(grep "^description:" "$skill_file" | wc -c || true)
  if [[ $desc_len -lt 80 ]]; then
    echo "  ⚠️  WARN: $skill_rel — description too short ($desc_len chars, aim >80)"
    WARNINGS=$((WARNINGS + 1))
  fi

  # Check skill.md size (target <500 lines)
  line_count=$(wc -l < "$skill_file")
  if [[ $line_count -gt 500 ]]; then
    echo "  ⚠️  WARN: $skill_rel — $line_count lines (target <500, move heavy content to references/)"
    WARNINGS=$((WARNINGS + 1))
  fi
done < <(find "$REPO_ROOT/.claude/skills" -name "skill.md" -print0 2>/dev/null)
echo "  ✅ Skill frontmatter check: done"

# --- 2. Agent files: validate current Opus/Sonnet hierarchy ---
echo "[ Check 2 ] Agent model setting..."
OPUS_AGENTS=(
  "governance-architect.md"
  "product-manager.md"
  "system-architect.md"
  "infra-devops.md"
  "ops-manager.md"
  "sre-ops.md"
  "code-reviewer.md"
  "risk-manager.md"
)
SONNET_AGENTS=(
  "backend-engineer.md"
  "docs-governance.md"
  "frontend-engineer.md"
  "git-commit.md"
  "qa-inspector.md"
  "security-engineer.md"
  "researcher.md"
  "technical-writer.md"
  "wiki-curator.md"
)
ALL_EXPECTED_AGENTS=("${OPUS_AGENTS[@]}" "${SONNET_AGENTS[@]}")

check_agent_model() {
  local file_name="$1"
  local expected="$2"
  local agent_file="$REPO_ROOT/.claude/agents/$file_name"
  local agent_rel=".claude/agents/$file_name"

  if [[ ! -f "$agent_file" ]]; then
    echo "  ❌ FAIL: $agent_rel — expected active agent file missing"
    FAILURES=$((FAILURES + 1))
    return
  fi

  local has_model
  has_model=$(grep -c "^model:" "$agent_file" || true)
  if [[ $has_model -eq 0 ]]; then
    echo "  ❌ FAIL: $agent_rel — missing 'model:' in frontmatter"
    FAILURES=$((FAILURES + 1))
    return
  fi

  local model_val
  model_val=$(grep "^model:" "$agent_file" | awk '{print $2}')
  if [[ "$model_val" != "$expected" ]]; then
    echo "  ❌ FAIL: $agent_rel — model is '$model_val' (expected: $expected)"
    FAILURES=$((FAILURES + 1))
  fi
}

for agent in "${OPUS_AGENTS[@]}"; do
  check_agent_model "$agent" "opus"
done
for agent in "${SONNET_AGENTS[@]}"; do
  check_agent_model "$agent" "sonnet"
done

while IFS= read -r -d '' agent_file; do
  agent_base="$(basename "$agent_file")"
  covered=0
  for expected in "${ALL_EXPECTED_AGENTS[@]}"; do
    if [[ "$agent_base" == "$expected" ]]; then
      covered=1
      break
    fi
  done
  if [[ $covered -eq 0 ]]; then
    echo "  ❌ FAIL: .claude/agents/$agent_base — active agent is not covered by the model policy"
    FAILURES=$((FAILURES + 1))
  fi
done < <(find "$REPO_ROOT/.claude/agents" -maxdepth 1 -name "*.md" -print0 2>/dev/null)
echo "  ✅ Agent model check: done"

# --- 3. Agent scope import coverage ---
echo "[ Check 3 ] Agent scope import coverage..."
AGENT_DIR="$REPO_ROOT/.claude/agents"
if [[ ! -d "$AGENT_DIR" ]]; then
  echo "  ❌ FAIL: .claude/agents/ missing"
  FAILURES=$((FAILURES + 1))
else
  while IFS= read -r -d '' agent_file; do
    agent_rel="${agent_file#"$REPO_ROOT"/}"
    if grep -q "@docs/00.agent-governance/scopes/" "$agent_file" \
      || grep -q "Cross-layer role" "$agent_file"; then
      echo "  ✅ $agent_rel"
    else
      echo "  ❌ FAIL: $agent_rel — missing governance scope @import or cross-layer role marker"
      FAILURES=$((FAILURES + 1))
    fi
  done < <(find "$AGENT_DIR" -maxdepth 1 -name "*.md" -print0 2>/dev/null)
fi
echo "  ✅ Agent scope coverage check: done"

# --- 4. Codex compatibility parity ---
echo "[ Check 4 ] Codex compatibility parity..."
CODEX_AGENT_DIR="$REPO_ROOT/.codex/agents"
if [[ ! -d "$CODEX_AGENT_DIR" ]]; then
  echo "  ❌ FAIL: .codex/agents/ missing"
  FAILURES=$((FAILURES + 1))
else
  claude_names="$(find "$AGENT_DIR" -maxdepth 1 -name "*.md" -printf "%f\n" 2>/dev/null | sed 's/\.md$/.toml/' | sort)"
  codex_names="$(find "$CODEX_AGENT_DIR" -maxdepth 1 -name "*.toml" -printf "%f\n" 2>/dev/null | sort)"
  if [[ "$claude_names" != "$codex_names" ]]; then
    echo "  ❌ FAIL: .codex/agents/ names must match .claude/agents/"
    FAILURES=$((FAILURES + 1))
  fi

  while IFS= read -r -d '' codex_file; do
    codex_rel="${codex_file#"$REPO_ROOT"/}"
    if ! grep -q '^name = "' "$codex_file"; then
      echo "  ❌ FAIL: $codex_rel — missing name"
      FAILURES=$((FAILURES + 1))
    fi
    if ! grep -q '^description = "' "$codex_file"; then
      echo "  ❌ FAIL: $codex_rel — missing description"
      FAILURES=$((FAILURES + 1))
    fi
    if ! grep -q '^developer_instructions = """' "$codex_file"; then
      echo "  ❌ FAIL: $codex_rel — missing developer_instructions"
      FAILURES=$((FAILURES + 1))
    fi
    if ! grep -q "@docs/00.agent-governance/scopes/" "$codex_file" \
      && ! grep -q "Cross-layer role" "$codex_file"; then
      echo "  ❌ FAIL: $codex_rel — missing synchronized governance scope marker"
      FAILURES=$((FAILURES + 1))
    fi
  done < <(find "$CODEX_AGENT_DIR" -maxdepth 1 -name "*.toml" -print0 2>/dev/null)

  if ! description_parity_output="$(python3 - "$REPO_ROOT" <<'PY'
from pathlib import Path
import sys
import tomllib

root = Path(sys.argv[1])
claude_dir = root / ".claude/agents"
codex_dir = root / ".codex/agents"
errors: list[str] = []


def frontmatter_description(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    try:
        block = text.split("---", 2)[1]
    except IndexError:
        return None
    for line in block.splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"')
    return None


for claude_file in sorted(claude_dir.glob("*.md")):
    codex_file = codex_dir / f"{claude_file.stem}.toml"
    if not codex_file.exists():
        continue

    claude_description = frontmatter_description(claude_file)
    if not claude_description:
        errors.append(f"{claude_file.relative_to(root)} — missing description frontmatter")
        continue

    try:
        codex_data = tomllib.loads(codex_file.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        errors.append(f"{codex_file.relative_to(root)} — invalid TOML: {exc}")
        continue

    codex_description = codex_data.get("description")
    if codex_description != claude_description:
        errors.append(
            f"{codex_file.relative_to(root)} — description must match "
            f"{claude_file.relative_to(root)}"
        )

for error in errors:
    print(error)
raise SystemExit(1 if errors else 0)
PY
  )"; then
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      echo "  ❌ FAIL: $line"
      FAILURES=$((FAILURES + 1))
    done <<< "$description_parity_output"
  else
    echo "  ✅ Codex metadata description parity OK"
  fi
fi

if [[ -d "$REPO_ROOT/.codex" ]]; then
  while IFS= read -r -d '' codex_file; do
    codex_rel="${codex_file#"$REPO_ROOT"/}"
    if [[ "$codex_rel" == .codex/agents/*.toml ]]; then
      continue
    fi
    echo "  ❌ FAIL: $codex_rel — .codex may contain only synchronized agent compatibility metadata"
    FAILURES=$((FAILURES + 1))
  done < <(find "$REPO_ROOT/.codex" -type f -print0 2>/dev/null)
fi
echo "  ✅ Codex compatibility parity check: done"

# --- 5. Settings separation policy ---
echo "[ Check 5 ] Settings separation..."
if git -C "$REPO_ROOT" ls-files --error-unmatch ".claude/settings.local.json" >/dev/null 2>&1; then
  echo "  ❌ FAIL: .claude/settings.local.json must not be tracked"
  FAILURES=$((FAILURES + 1))
else
  echo "  ✅ Settings separation OK"
fi

# --- 6. Commands directory policy ---
echo "[ Check 6 ] Commands directory policy..."
if [[ -d "$REPO_ROOT/.claude/commands" ]]; then
  echo "  ℹ️  INFO: .claude/commands/ present — allowed when aligned to active runtime workflows"
else
  echo "  ✅ No commands directory: OK"
fi

# --- 7. spec-driven-sdlc hard-stop policy ---
echo "[ Check 7 ] spec-driven-sdlc hard-stop policy..."
SDLC_SKILL="$REPO_ROOT/.claude/skills/spec-driven-sdlc/skill.md"
if [[ ! -f "$SDLC_SKILL" ]]; then
  echo "  ❌ FAIL: .claude/skills/spec-driven-sdlc/skill.md missing"
  FAILURES=$((FAILURES + 1))
else
  for required_section in \
    "DDD Decision Tree" \
    "SDD Mandatory Conditions" \
    "TDD Gate" \
    "Stage Transition Hard Stops"; do
    if ! grep -q "^## $required_section$" "$SDLC_SKILL"; then
      echo "  ❌ FAIL: spec-driven-sdlc — missing '$required_section'"
      FAILURES=$((FAILURES + 1))
    fi
  done
fi
echo "  ✅ spec-driven-sdlc policy check: done"

# --- 8. Harness skill inventory parity ---
echo "[ Check 8 ] Harness skill inventory parity..."
HARNESS_LIBRARY="$REPO_ROOT/docs/00.agent-governance/rules/harness-library.md"
if [[ ! -f "$HARNESS_LIBRARY" ]]; then
  echo "  ❌ FAIL: docs/00.agent-governance/rules/harness-library.md missing"
  FAILURES=$((FAILURES + 1))
else
  BACKTICK="\`"
  expected_skills="$(grep -o "${BACKTICK}[A-Za-z0-9_-]\\+/skill\\.md${BACKTICK}" "$HARNESS_LIBRARY" \
    | sed "s#${BACKTICK}##g; s#/skill\\.md##" \
    | sort -u)"
  actual_skills="$(find "$REPO_ROOT/.claude/skills" -mindepth 2 -maxdepth 2 -type f -name "skill.md" -printf "%h\n" 2>/dev/null \
    | sed "s#^$REPO_ROOT/.claude/skills/##" \
    | sort -u)"

  if [[ -z "$expected_skills" ]]; then
    echo "  ❌ FAIL: harness-library.md — no active skill inventory entries found"
    FAILURES=$((FAILURES + 1))
  fi

  missing_skills="$(comm -23 <(printf '%s\n' "$expected_skills") <(printf '%s\n' "$actual_skills") || true)"
  unregistered_skills="$(comm -13 <(printf '%s\n' "$expected_skills") <(printf '%s\n' "$actual_skills") || true)"

  if [[ -n "$missing_skills" ]]; then
    while IFS= read -r skill_name; do
      [[ -z "$skill_name" ]] && continue
      echo "  ❌ FAIL: .claude/skills/$skill_name/skill.md — registered in harness-library.md but missing"
      FAILURES=$((FAILURES + 1))
    done <<< "$missing_skills"
  fi

  if [[ -n "$unregistered_skills" ]]; then
    while IFS= read -r skill_name; do
      [[ -z "$skill_name" ]] && continue
      echo "  ❌ FAIL: .claude/skills/$skill_name/skill.md — active skill is not registered in harness-library.md"
      FAILURES=$((FAILURES + 1))
    done <<< "$unregistered_skills"
  fi

  if [[ -z "$missing_skills" && -z "$unregistered_skills" && -n "$expected_skills" ]]; then
    echo "  ✅ Harness skill inventory parity OK"
  fi
fi

# --- Summary ---
echo ""
echo "=== Summary ==="
echo "Failures: $FAILURES | Warnings: $WARNINGS"

if [[ $FAILURES -gt 0 ]]; then
  exit 2
elif [[ $WARNINGS -gt 0 ]]; then
  exit 1
else
  echo "✅ All skill/agent quality checks passed."
  exit 0
fi
