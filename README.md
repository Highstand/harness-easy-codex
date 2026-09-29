# SNS 콘텐츠 자동화 — Codex 하네스

경쟁사 조사 → 우리 브랜드에 맞는 기획 → 새 이미지와 HTML 프리뷰 → Figma 제작.
기존 Claude Code 실습 폴더를 복사해 Codex에서 읽는 규칙과 프로젝트 스킬로 바꾼 버전입니다.

## 처음 시작하기

1. Codex 앱에서 **이 폴더를 프로젝트로 열고 새 작업을 시작**합니다. CLI라면 이 폴더에서 `codex`를 실행합니다.
2. 아래 명령으로 보고서 라이브러리 설치와 로컬 준비 상태를 확인합니다.
3. Aside 설치 및 인스타그램 로그인, Codex의 Figma 연결을 확인합니다. 설정은 [SETUP.md](docs/SETUP.md)를 참고하세요.

```sh
npm ci
npm run doctor
```

첫 요청은 이 정도면 됩니다.

```text
이 프로젝트로 카드뉴스를 만들어보려고 해. 준비 상태부터 확인해줘.
```

## 실습 흐름

| 순서 | 자연어 요청 | 결과와 확인 |
|---|---|---|
| 준비 | 아래 준비 프롬프트 | 두 가이드·원본 에셋·도구 연결 확인 |
| 조사 | 경쟁사 분석해줘 | 근거와 패턴, 미확보 확인. PPTX는 선택 |
| 기획 | 새 주제 3개 추천해줘 | 주제 선택 |
| 기획 확정 | 1번으로 5장 기획해서 plan.md에 정리해줘 | 카피·사진 방향·CTA 확인 |
| 프리뷰 | 이 기획에 맞는 새 이미지로 HTML 프리뷰를 만들어줘 | 브라우저에서 확인·수정, 필수 |
| Figma | 이 프리뷰로 확정할게. 아래 피그마에 만들어줘. [결과 링크] | 새 섹션·편집 가능한 텍스트 |
| 검수 | 확정 프리뷰와 비교해서 검수해줘 | 차이 수정·미검증 사항 기록 |

준비할 때:

```text
brand.md와 content-design.md, 아래 원본을 읽어줘.
재사용할 로고와 장식을 확인하고, 부족한 자료만 알려줘.
[원본 피그마 링크]
```

경쟁사 지정:

```text
brand.md에 경쟁사로 nikerunning, adidasrunning을 넣어줘.
러닝 콘텐츠의 주제와 구성을 참고하고 싶어.
```

기존 예제로 보고서까지 확인하려면:

```text
기존 수집 자료로 분석 흐름과 보고서만 확인해줘. 새로 수집하지 않아도 돼.
```

## 폴더가 맡는 역할

| 파일 | 역할 |
|---|---|
| `AGENTS.md` | Codex가 읽는 진행 순서와 확인 지점 |
| `.agents/skills/ig-competitor-scout/SKILL.md` | 경쟁사 수집·분석 절차 |
| `.agents/skills/ig-content-maker/SKILL.md` | 주제·기획·이미지·프리뷰·Figma 절차 |
| `.codex/config.toml` | 프로젝트 Aside MCP 연결 |
| `brand.md` / `content-design.md` | Figma Agent와 정리한 브랜드·시각 기준 |
| `scripts/` | 로컬 보고서·런메이트 예제 프리뷰 생성 |
| `assets/brand/` | 다시 그리지 않고 사용할 원본 SVG |
| `plans/` / `preview/` | 기획과 시안, Figma 전달 기록 |

스킬 두 개는 독립 에이전트를 자동으로 띄우는 설정이 아닙니다. Codex가 요청에 맞는 절차를 읽고 수행합니다.
긴 명령을 외우거나 별도 에이전트 이름을 지정할 필요는 없습니다.

## 포함된 예제 열기

### 이번 Codex 작업: 첫 러닝 모임

`first-run-hello`는 이 프로젝트에서 새로 기획·이미지 생성·프리뷰 검수·Figma 제작을 진행한 5장 카드뉴스입니다. 가상 서비스 시안이며 CTA는 실제 페이지로 연결되지 않습니다.

- [기획과 승인 기록](plans/first-run-hello/plan.md) · [확정 카피](plans/first-run-hello/content.json)
- [HTML 시안](preview/first-run-hello/index.html) · [시안 이미지](preview/first-run-hello/preview.png)
- [Figma 결과](https://www.figma.com/design/1D7Jqr9ku3boaa7GVbeAUm/?node-id=209-296) · [결과 이미지](preview/first-run-hello/figma-final.png)
- [검수 기록](plans/first-run-hello/source-review.md) · [이미지 생성 프롬프트](assets/content/first-run-hello/image-prompts.json)

저장소 루트에서 아래 서버를 실행한 뒤 `http://localhost:8767/preview/first-run-hello/index.html`을 여세요. Figma 원본 열람은 해당 파일의 공유 권한에 따릅니다.

```sh
python3 -m http.server 8767 --bind 127.0.0.1
```

이 시안에는 전용 `style.css`가 적용되어 있습니다. 일반 예제 렌더러로 덮어쓰지 말고 기획의 구현 기록을 참고하세요.

### 이관된 과거 예제

`lonely-evening-run`과 2026-09-29 조사 자료는 **Claude Code 원본에서 가져온 기존 예제**입니다. 새 Codex 실행 결과가 아닙니다.
새 실습은 다른 기획명으로 시작합니다. 예제의 Figma 링크는 과거 전달 기록입니다.

```sh
python3 scripts/build-preview.py lonely-evening-run
python3 -m http.server 8766 --bind 127.0.0.1
```

[예제 프리뷰 열기](http://localhost:8766/preview/lonely-evening-run/index.html)

다른 브랜드로 사용할 때는 두 가이드와 원본 에셋을 교체하고 렌더러도 새 기준으로 조정합니다.
현재 렌더러가 임의의 디자인 문서를 자동 해석하는 범용 엔진은 아닙니다.
이 폴더는 이미지 파일도 Git에 포함할 수 있도록 설정했습니다. 공개 저장소에 올리기 전 경쟁사 캡처와 생성 이미지의 공유 범위를 확인하세요.

변경 내역·검증 범위: [MIGRATION.md](docs/MIGRATION.md). 촬영용 흐름: [촬영안](docs/촬영안-Codex.md).
