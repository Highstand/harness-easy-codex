# Claude Code → Codex 이관 기록

작성: 2026-09-29. 원본 `/Users/bibi/harness-easy/` → 별도 복사본 `/Users/bibi/harness-easy-codex/`.
[사용자 기획안](https://docs.google.com/document/d/1jKHyGuDZ43jrEVH_tJKV-M_FOnF1Rnnd1M83TB-tCxw/edit)을 읽고 조사→브랜드 결합→기획→필수 프리뷰→Figma 흐름을 반영했다.
원본 폴더, Google 문서, Figma 장표, 개인 전역 Codex 설정은 수정하지 않았다.

## 바뀐 부분

| 기존 | Codex 버전 |
|---|---|
| CLAUDE.md | AGENTS.md — 진행 순서·사용자 확인·파일 연결 |
| .claude/agents/*.md | .agents/skills/*/SKILL.md — 조사 / 제작 절차 |
| sonnet 지정·부모/서브에이전트 위임 | 사용자 Codex 모델 설정, 현재 작업에서 스킬 수행 |
| .mcp.json Aside | .codex/config.toml Aside STDIO |
| Claude 로컬 허용 설정 | 복사하지 않음. 개인 인증·승인 설정을 배포하지 않음 |
| Figma 뒤 사진 생성 안내 | 사진→프리뷰 확인→Figma로 순서 통일 |
| 보고서 PPTX 필수 | 분석 MD/JSON이 연결 자료, PPTX는 선택 |
| txt-* 템플릿 전용 JS | scripts/legacy/에 보존, 기본 흐름에서 제외 |
| 원본 프리뷰 렌더러 | 예제용임을 명시, 누락 사진·미지원 패턴·잘못된 기획명 검사 |
| 누락된 폰트 | 기존 contents-automation-v2의 PretendardVariable.woff2 + 공식 OFL |

스킬은 Claude의 별도 에이전트 런타임을 그대로 복제한 기능이 아니다. 담당 절차를 Codex가 필요할 때 읽는 구성이다.
하네스의 핵심인 진행 규칙·파일 전달·검수 순서는 유지했다.

## 보존과 제외

- 브랜드·디자인 문서, 원본 SVG, 조사 데이터/스크린샷, 기획, 생성 사진, 프리뷰, 기존 Figma 전달 기록을 보존했다.
- 원본의 .git, node_modules, .claude, .mcp.json, CLAUDE.md, _to_delete, .DS_Store, .env 계열은 복사 대상에서 제외했다.
- 사용하지 않는 npm curl 의존성을 제거했다. PPTX 의존 패키지 image-size는 보안 수정 버전 2.0.4로 고정하고 예제 보고서 생성으로 확인했다.
- 포함 예제는 과거 작업이며 새로운 수집·새 생성으로 표시하지 않는다. 새 콘텐츠는 다른 slug로 만든다.
- 사진까지 전달되도록 이미지 파일을 무조건 Git에서 제외하던 규칙을 바꿨다. 공개 공유 범위는 배포자가 결정한다.

## 검증 결과

| 검증 | 결과 |
|---|---|
| 원본 파일 체크섬 비교 | 변경 없음 (`source-checksums.json`) |
| Codex 스킬 검사 | 두 SKILL.md 모두 quick_validate 통과 |
| 프로젝트 TOML·자료·SVG 해시 | doctor 필수 오류 0 |
| 의존성 설치 | npm install/ci 실행, 최종 audit 알려진 취약점 0 |
| 예제 HTML | 5장 렌더링 성공 |
| 실제 Chromium 렌더 | 폰트 로딩 성공, 이미지 누락 0, 자리 표시 0, 가로 텍스트 넘침 0 |
| 렌더 이미지 확인 | `validation/preview.png`에서 5장 배치 확인 |
| 누락 이미지·잘못된 slug·미지원 패턴 | 임시 입력으로 오류/초안 표시 확인 |
| 기존 데이터 PPTX 재생성 | 6슬라이드, 11 미디어, 약 762KB (`validation/existing-data-report.pptx`) |

검증용 보고서는 과거 JSON으로 재생성했으며 새 경쟁사 분석이 아니다. 기존 예제 Figma 전달 기록도 그대로 과거 기록이다.

## 남은 연결 확인

- Aside 실제 인스타그램 로그인과 새 수집, Codex 작업에서의 MCP 발견.
- 이미지 생성 도구로 새 사진 생성.
- Figma 읽기와 쓰기 도구 연결, 새 섹션 제작과 원본 대비 검수.
- content-design.md의 원본 링크가 손상되어 있었다. 에셋 manifest의 섹션 186:3741과 가이드의 122:* 카드 노드 관계를 실제 Figma에서 확인해야 한다. 출처 후보만 적었고 검증 완료로 표시하지 않았다.
- 원본에서 언급한 실측 JSON과 이전 가이드 파일은 원본 폴더에 없으므로 없는 파일을 근거로 확정하지 않도록 표시했다.

연결 작업을 대신했다고 주장하지 않으며, 계정·크레딧을 사용하는 외부 제작은 이번 이관 검증에서 실행하지 않았다.

## 공식 설정 근거

- [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [프로젝트 스킬](https://developers.openai.com/codex/skills)
- [프로젝트 MCP 설정](https://developers.openai.com/codex/mcp)
- [Pretendard 라이선스](https://github.com/orioncactus/pretendard/blob/main/LICENSE)
