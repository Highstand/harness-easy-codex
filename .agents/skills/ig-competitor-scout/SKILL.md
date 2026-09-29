---
name: ig-competitor-scout
description: 경쟁사 인스타그램 공개 게시물을 Aside로 조사하고 근거가 있는 패턴 보고서를 작성한다. 경쟁사 분석이나 레퍼런스 수집 요청에 사용한다.
---
# 경쟁사 조사

프로젝트 루트 기준 경로다. 먼저 `AGENTS.md`와 `brand.md`의 경쟁사·조사 목적을 읽는다.
계정이 없으면 2~3개를 묻고 답을 받아 경쟁사 표에 기록한다. 기본 범위는 최근 30일, 계정당 최대 12건이다.

## 수집

1. 연결된 Aside MCP 도구를 확인한다. 없으면 `.codex/config.toml`과 `aside mcp` 설치/PATH 확인을 안내한다. 연결된 도구 없이 수집 성공을 주장하지 않는다.
2. 로그인 화면이면 사용자에게 Aside에서 로그인하도록 요청한다. 비밀번호를 다루지 않는다.
3. 계정과 게시물을 하나씩 열어 실제 보이는 정보를 읽고 스크린샷을 저장한다. 팔로우·좋아요·저장·댓글·DM을 실행하지 않는다.
4. 기간 밖 고정 게시물과 중복 shortCode는 제외한다. 차단되면 재시도로 밀어붙이지 않고 부분 결과와 중단 사유를 기록한다.
5. `research/{handle}/{YYYY-MM}/posts.json`과 같은 폴더에 게시물 스크린샷을 저장한다. YYYY-MM은 수집 실행 월이다.

```json
[{"shortCode":"example","url":"https://www.instagram.com/p/example/","timestamp":null,"type":"Image","likesCount":null,"commentsCount":null,"caption":"실제 읽은 캡션","image":"research/handle/YYYY-MM/example.png"}]
```

필드: shortCode, url, timestamp(ISO 시각 또는 null), type(Image/Video/Sidecar 또는 null), likesCount, commentsCount, caption, image(프로젝트 상대 경로 또는 null).
좋아요가 명시적으로 숨김이면 -1, 단순히 확인 못 했으면 null이다. 댓글·팔로워 등 미확보 수치는 null, 0은 실제 0일 때만 쓴다.
이미지 파일은 실제 저장 여부를 확인한다. 화면을 보지 못한 게시물의 시각 특징을 추측하지 않는다.
기존 posts.json이 있으면 수집 일자와 범위를 알리고 재사용/갱신 여부를 확인한다. 포함된 예제를 오늘 수집한 결과로 표시하지 않는다.

## 분석과 전달

- 좋아요 중앙값은 null과 -1을 제외한다. 유효 값이 없으면 null이다. 표본의 반응과 성과 원인을 구분한다.
- 상위 최대 5건을 실제 스크린샷으로 확인한다. 좋아요가 모두 미확보이면 최근 게시물로 대체했다고 적는다.
- 반복 패턴마다 서로 다른 근거 URL 2개 이상. 한 건뿐이면 단일 관찰로 분리한다. 구성·주제의 참고점을 정리하고 경쟁사 문구/이미지를 새 콘텐츠에 복제하지 않는다.
- `outputs/research/{날짜}_competitor-report.md`와 JSON에 요약·표본·패턴·근거 URL·적용 아이디어·미확보를 저장한다. 같은 날짜의 기존 보고서는 덮어쓰지 않고 실행 접미사를 붙인다.
- JSON 형식은 `scripts/make-report.js` 상단 스키마를 따른다. PPTX를 요청받으면 아래 명령으로 만든다.

```sh
node scripts/make-report.js outputs/research/{보고서명}.json
```

사용자에게 파일 경로, 핵심 발견, 표본 범위와 미확보를 보여준다. 기획 단계에는 보고서 경로를 전달한다.
Apify는 사용자가 선택하고 실제 도구·비용 조건을 확인한 경우만 대체한다. 위 posts.json 형식으로 정규화하며 이번 배포본에는 Apify 실행 어댑터가 없다.
