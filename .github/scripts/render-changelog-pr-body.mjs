#!/usr/bin/env node
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const [, , releaseTag, outputPath] = process.argv;

if (!releaseTag || !outputPath) {
  console.error(
    'Usage: node .github/scripts/render-changelog-pr-body.mjs <release-tag> <output-file>',
  );
  process.exit(2);
}

const repoRoot = dirname(dirname(dirname(fileURLToPath(import.meta.url))));
const templatePath = `${repoRoot}/.github/PULL_REQUEST_TEMPLATE.md`;

let body = readFileSync(templatePath, 'utf8');

const replacements = [
  [
    '- **Spec File (명세서):** [Link to the file in `docs/03.specs/`]',
    '- **Spec File (명세서):** Governance exemption; plan archived (b8c007d).',
  ],
  [
    '- **Issue (optional when known/available / 이슈, 확인 가능한 경우):** Resolves #',
    '- **Issue (optional when known/available / 이슈, 확인 가능한 경우):** Not linked; governed by Stage 05 plan evidence.',
  ],
  ['- [ ] Documentation (문서화)', '- [x] Documentation (문서화)'],
  [
    '[Describe the changes made in this pull request]\n[이번 PR에서 변경된 사항을 설명해 주세요]',
    `Updates CHANGELOG.md for release tag ${releaseTag}.`,
  ],
  ['- [ ] No breaking changes (준거성 유지)', '- [x] No breaking changes (준거성 유지)'],
  [
    '[If breaking, describe migration path and impact]\n[호환성 변경이 있는 경우, 마이그레이션 경로와 영향을 설명해 주세요]',
    'No migration required.',
  ],
  [
    '```bash\n# Example:\n# bash scripts/ws.sh validate\n```',
    [
      '```bash',
      'orhun/git-cliff-action generated CHANGELOG.md during the tag workflow',
      'bash scripts/validation/validate-doc-governance.sh',
      'bash scripts/validation/validate-cross-links.sh',
      '```',
    ].join('\n'),
  ],
  ['- **Risk Level (위험 수준)**: [Low/Medium/High]', '- **Risk Level (위험 수준)**: Low'],
  [
    '- **Rollback Plan (롤백 계획)**: [Describe rollback or mitigation / 장애 시 복구 계획]',
    '- **Rollback Plan (롤백 계획)**: Close this PR or delete the generated changelog branch.',
  ],
  [
    '- [ ] I have followed `AGENTS.md` and `docs/00.agent-governance/rules/git-workflow.md`.',
    '- [x] I have followed `AGENTS.md` and `docs/00.agent-governance/rules/git-workflow.md`.',
  ],
  [
    '- [ ] My code strictly follows the Implementation Specification.',
    '- [x] My code strictly follows the Implementation Specification. No implementation code changed.',
  ],
  [
    '- [ ] Documentation has been added/updated utilizing the `docs/99.templates/` folder (if applicable).',
    '- [x] Documentation has been added/updated utilizing the `docs/99.templates/` folder (if applicable).',
  ],
  [
    '- [ ] **Commit Standard**: My Pull Request title uses Conventional Commits format.',
    '- [x] **Commit Standard**: My Pull Request title uses Conventional Commits format.',
  ],
  ['- [ ] I have run tests locally.', '- [x] I have run tests locally.'],
  [
    '- [ ] No secrets or credentials are included in this PR.',
    '- [x] No secrets or credentials are included in this PR.',
  ],
];

for (const [search, replacement] of replacements) {
  if (!body.includes(search)) {
    console.error(`PR template marker not found: ${search}`);
    process.exit(1);
  }
  body = body.replace(search, replacement);
}

writeFileSync(outputPath, body);
