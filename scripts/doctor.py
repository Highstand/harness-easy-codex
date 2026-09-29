#!/usr/bin/env python3
"""로컬 파일 준비만 검사한다. MCP 인증·시각 품질을 판정하지 않는다."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tomllib

ROOT = Path(__file__).resolve().parents[1]
errors = []

def check(ok, message):
    print(('OK   ' if ok else 'FAIL ') + message)
    if not ok:
        errors.append(message)

for name in ['AGENTS.md', 'brand.md', 'content-design.md',
             '.agents/skills/ig-competitor-scout/SKILL.md',
             '.agents/skills/ig-content-maker/SKILL.md',
             'preview/assets/PretendardVariable.woff2', 'preview/assets/OFL.txt']:
    f = ROOT / name
    check(f.is_file() and f.stat().st_size > 0, name)
try:
    cfg = tomllib.loads((ROOT / '.codex/config.toml').read_text())
    check(cfg['mcp_servers']['aside']['args'] == ['mcp'], 'Aside MCP 설정 형식')
except (OSError, ValueError, KeyError) as e:
    check(False, f'MCP 설정: {e}')
for name in ['node', 'npm']:
    check(bool(shutil.which(name)), f'{name} 실행 파일')
for name in ['codex', 'aside']:
    print(('OK   ' if shutil.which(name) else 'TODO ') + f'{name} CLI (앱 연결 상태는 별도 확인)')
if shutil.which('node'):
    result = subprocess.run(['node', '-e', "require('pptxgenjs')"], cwd=ROOT, capture_output=True)
    check(result.returncode == 0, 'PPTX 라이브러리 — 없으면 npm ci')
try:
    mf = ROOT / 'assets/brand/current-source/manifest.json'
    for item in json.loads(mf.read_text())['files']:
        f = mf.parent / item['file']
        check(f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() == item['sha256'], '원본 SVG 해시: ' + item['file'])
except (OSError, ValueError, KeyError) as e:
    check(False, f'에셋 manifest: {e}')
if '현재 링크 확인 필요' in (ROOT/'content-design.md').read_text():
    print('TODO 최신 Figma 원본 링크와 노드 관계 확인 (이관 문서에 표시됨)')
print('TODO 외부 실제 연결: Aside 로그인·읽기, Figma 읽기/쓰기, 이미지 생성, 브라우저 검수')
print(f'로컬 필수 오류 {len(errors)}개. 이 결과는 외부 도구 연결·자동화 전체 성공을 뜻하지 않습니다.')
sys.exit(1 if errors else 0)
