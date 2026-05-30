# Pull Request / 제출된 변경 사항

> **Warning**: Your PR Title MUST follow the **Conventional Commits** format (`feat:`, `fix:`, `docs:`, etc.) as mandated by `docs/00.agent-governance/rules/git-workflow.md`!
> **주의**: PR 제목은 반드시 **Conventional Commits** 형식을 따라야 합니다.

## Related Specification / 관련 명세

- **Spec File (명세서):** [Link to the file in `docs/03.specs/`]
- **Issue (optional when known/available / 이슈, 확인 가능한 경우):** Resolves #

## Change Type / 변경 유형

- [ ] Feature (기능 추가)
- [ ] Bug fix (버그 수정)
- [ ] Refactor (리팩토링)
- [ ] Documentation (문서화)
- [ ] Test (테스트)
- [ ] CI/CD (CI/CD 및 workflow)
- [ ] Chore (정리 및 유지보수)
- [ ] Operations / Runbook (운영 및 런북)

## Description / 변경 상세

[Describe the changes made in this pull request]
[이번 PR에서 변경된 사항을 설명해 주세요]

## Breaking Changes / 주요 변경 및 영향

- [ ] No breaking changes (준거성 유지)
- [ ] Breaking changes included (호환성 변경 포함)

[If breaking, describe migration path and impact]
[호환성 변경이 있는 경우, 마이그레이션 경로와 영향을 설명해 주세요]

## Validation Evidence / 검증 증거

List exact commands used and outcome. (실행한 명령어와 결과물을 기재해 주세요).

```bash
# Example:
# bash scripts/ws.sh validate
# COVERAGE_FILE=coverage/coverage.xml bash .github/gates/check-coverage.sh
```

## Risk Assessment / 리스크 평가

- **Risk Level (위험 수준)**: [Low/Medium/High]
- **Rollback Plan (롤백 계획)**: [Describe rollback or mitigation / 장애 시 복구 계획]

## Validations / 필수 체크리스트

- [ ] I have followed `AGENTS.md` and `docs/00.agent-governance/rules/git-workflow.md`. (에이전트/PR 거버넌스를 읽고 준수함)
- [ ] My code strictly follows the Implementation Specification. (코드가 구현 명세를 엄격히 따름)
- [ ] Documentation has been added/updated utilizing the `docs/99.templates/` folder (if applicable). (템플릿을 사용하여 문서를 최신화함)
- [ ] If this is an incomplete but valuable checkpoint, WIP state is recorded in the PR description or governed task/progress documents. (미완료 체크포인트인 경우 WIP 상태를 PR 설명 또는 governed task/progress 문서에 기록함)
- [ ] **Commit Standard**: My Pull Request title uses Conventional Commits format. (PR 제목 형식을 준수함)
- [ ] I have run tests locally. (로컬 테스트를 통과함)
- [ ] **Conditional Test Coverage:** Every pull request must pass the 90% test coverage gate after an active implementation stack manifest exists. The base template may skip only when no active stack manifest is present. (구현 스택 manifest가 존재하면 모든 PR은 90% 테스트 커버리지 게이트를 통과해야 하며, 기본 템플릿은 활성 스택 manifest가 없을 때만 skip 가능)
- [ ] No secrets or credentials are included in this PR. (명시적인 토큰이나 비밀번호가 포함되지 않음)
- [ ] If operational behavior changed, runbook updates were added under `docs/05.operations/runbooks/`. (운영 변경 시 런북을 업데이트함)
