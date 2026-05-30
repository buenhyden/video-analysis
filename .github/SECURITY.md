# Security Policy / 보안 정책

> **주의**: 이 저장소를 공개하기 전에 자리표시자(placeholder) 연락처를 실제 채널로 교체하십시오.

## Supported Versions / 지원 버전

보안 수정을 지원하는 현재 브랜치 정책을 정의합니다.

| Branch / 브랜치 | Purpose / 목적 | Supported / 지원 여부 |
| :--- | :--- | :--- |
| main | Production release line / 프로덕션 릴리스 라인 | Yes (예) |
| dev | Integration validation line / 통합 검증 라인 | Yes (예) |

Security fixes must arrive through reviewed pull requests. Direct pushes to
`main` or `dev` are prohibited by repository governance.

## Reporting a Vulnerability / 취약점 보고 방법

보안 관련 취약점은 공개 이슈로 생성하지 마십시오. (Please do not open public issues for security vulnerabilities).

1. 보안 담당 채널로 비공개 보고서를 제출하십시오:
   - 이메일: `security@example.com`
   - 또는 GitHub 보안 권고: `https://github.com/<owner>/<repo>/security/advisories/new`
2. 재현 절차, 영향도 및 영향받는 파일을 포함하십시오.
3. 가능한 경우 PoC(proof-of-concept)와 제안하는 완화책을 포함하십시오.

### 예상 응답 목표 (Response Targets)

- 초기 분류 확인: 영업일 기준 2일 이내
- 심각도 평가: 영업일 기준 5일 이내
- 수정 계획 공유: 검증 완료 후 공유

## Disclosure Process / 공개 프로세스

1. 보고서 검증 및 심각도 할당.
2. 비공개 브랜치/저장소에서 수정 사항 준비.
3. 패치 릴리스 및 관련 문서 업데이트.
4. 수정 사항 적용 후 공식 보안 권고(Advisory) 게시.

## Secret Exposure Response / 시크릿 노출 대응

저장소 내 토큰·API 키·비밀번호가 커밋 이력에 발견된 경우:

1. **즉시 revoke**: 노출된 자격증명을 다른 조치보다 먼저 무효화합니다.
2. **Rotate**: 최소 권한으로 새 자격증명을 발급합니다.
3. **이력 제거**: `git filter-repo` 또는 GitHub 민감 데이터 제거 절차로 모든 브랜치에서 시크릿을 삭제합니다.
4. **감사**: 노출 기간 동안 해당 자격증명이 무단 사용되었는지 감사 로그를 확인합니다.
5. **문서화**: `docs/05.operations/incidents/` 에 인시던트 기록을 남깁니다.

자세한 내용: `docs/00.agent-governance/rules/github-repository-governance.md` §5
