# Codex 연결과 실행

| 준비 | 확인 방법 |
|---|---|
| Codex 앱 또는 CLI | 이 폴더를 프로젝트로 열기. 모델은 사용자 설정을 따름 |
| Node.js / npm | `node --version`, `npm --version` |
| Python 3.11+ | `python3 --version` (준비 검사에 tomllib 사용) |
| 보고서 라이브러리 | `npm ci` |
| Aside | `command -v aside`, 설치된 앱에서 로그인 |
| Figma | Codex에 Figma 플러그인 연결, 원본 읽기와 디자인 쓰기 가능 여부 확인 |
| 이미지 생성 | Codex에 제공된 이미지 생성 기능. 없으면 외부 도구 결과 파일 전달 |
| 프리뷰 확인 | 연결된 브라우저 도구 또는 사용자의 로컬 브라우저 |

## Aside

프로젝트 `.codex/config.toml`에 `command = "aside"`, `args = ["mcp"]`를 설정했습니다.
Codex가 프로젝트를 신뢰한 경우에만 프로젝트 설정을 읽습니다. 폴더를 새로 열고 `/mcp`에서 연결 상태를 확인합니다.
Aside는 별도 설치·로그인이 필요하며 이 폴더가 설치나 로그인 정보를 포함하지 않습니다.
기존 원본과 같은 Aside MCP 실행 방식을 사용합니다. 설치가 필요하면 Aside 공식 설치 안내를 따릅니다.

```sh
aside mcp
```

STDIO 서버라 터미널에서 출력 없이 기다릴 수 있습니다. 확인 후 Ctrl+C로 종료합니다.
앱에서 실행 파일을 못 찾으면 터미널의 `command -v aside` 결과를 `.codex/config.toml`의 command에 넣습니다.
사용자별 절대 경로는 공유 배포본에 넣지 않습니다. 전역에 같은 Aside 설정이 있으면 중복 서버 등록을 피합니다.

## Figma

이미 설치·인증된 Figma 플러그인을 우선 사용합니다. 이 프로젝트는 Figma 연결을 중복 등록하거나 기존 인증을 변경하지 않습니다.
원본 노드를 읽는 기능과 새 편집 가능한 노드를 만드는 기능이 모두 있는지 새 작업에서 확인합니다.
일반 MCP 연결만 있고 디자인 쓰기 기능이 없으면 읽기에는 쓸 수 있어도 이 실습의 최종 제작은 진행할 수 없습니다.
원본 링크와 결과를 만들 페이지 링크를 각각 전달합니다.

## 자료와 폰트

런메이트 에셋은 복사한 실제 SVG입니다. `manifest.json`의 해시를 doctor에서 검사합니다.
원본 디자인 가이드에 기재된 노드와 에셋 manifest의 섹션이 달라서 현재 원본 링크 확인이 필요합니다. 이전 실측 파일은 원본 폴더에도 없었습니다.
PretendardVariable.woff2는 기존 로컬 프로젝트의 파일을 가져왔습니다. `preview/assets/OFL.txt`와 함께 배포합니다.

## 확인 명령

```sh
npm run doctor
python3 scripts/build-preview.py lonely-evening-run
python3 -m http.server 8766 --bind 127.0.0.1
```

doctor는 파일·라이브러리 준비를 검사합니다. MCP 로그인, 실제 수집, 이미지 생성, Figma 쓰기는 해당 도구로 별도 확인해야 합니다.

## 참고한 공식 문서

- [AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Codex 프로젝트 스킬](https://developers.openai.com/codex/skills)
- [MCP 설정](https://developers.openai.com/codex/mcp)
