#!/usr/bin/env python3
"""build-preview.py — plans/{기획명}/content.json → preview/{기획명}/index.html

사용법:
  python3 scripts/build-preview.py {기획명}

content.json 한 장의 키 (ig-content-maker가 쓴다):
  id          카드 식별자
  pattern     content-design.md 2. 카드 패턴의 이름
  label       작은 라벨 (없으면 생략)
  title       큰 제목. 줄바꿈은 \n
  caption     보충 한 줄
  image       assets/content/{기획명}/images/ 안의 파일명 (없으면 자리만 비운다)
  rows        [["항목","내용"], ...] 정보형에서만
  cta         버튼 문구
  decorations [{asset, x, y, width, height}]  좌표는 content-design.md 값 그대로

STYLE은 content-design.md의 값으로 맞춘다. 여기 숫자를 눈대중으로 바꾸지 않는다.
"""
import sys, json, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── content-design.md에서 옮겨 적는 값 ────────────────────────────
STYLE = {
    "card_w": 1080, "card_h": 1350,
    "bg": "#141713", "title": "#FFFFFF", "caption": "#C2C8BE", "accent": "#E6FF65",
    "font": "Pretendard, -apple-system, sans-serif",
}
# ─────────────────────────────────────────────────────────────

def esc(s):
    return html.escape(str(s)).replace("\n", "<br>")

BRAND_DIR = "current-source"  # assets/brand/current-source/ (content-design.md 5)

def asset_path(name):
    for d in (ROOT/"assets/brand"/BRAND_DIR, ROOT/"assets/brand"):
        if (d/name).exists():
            return "../../" + str((d/name).relative_to(ROOT))
    return None

def card_kind(c):
    pat = c.get("pattern", "")
    for word, kind in [("표지", "cover"), ("마무리", "cta"), ("정보", "info"), ("전폭", "wide"), ("가로 사진", "inset")]:
        if word in pat:
            return kind
    raise ValueError(f"지원하지 않는 패턴: {pat}. 기획에 맞게 렌더러를 확장하세요.")

def card_html(c, plan):
    kind = card_kind(c)
    P = [f'<div class="canvas k-{kind}" data-id="{esc(c["id"])}">']
    # 사진 (없으면 플레이스홀더 — 사진 방향 설명은 plan.md 것을 PHOTO_NOTE로)
    if kind in ("cover", "wide", "inset"):
        img = c.get("image")
        f = ROOT/"assets/content"/plan/"images"/(img or "")
        if img and f.exists():
            P.append(f'<img class="photo" src="../../assets/content/{plan}/images/{esc(img)}" alt="">')
        else:
            note = PHOTO_NOTE.get(c["id"], "사진 자리")
            P.append(f'<div class="photo placeholder"><span>사진 미생성 · {esc(c.get("image"))}<br>{esc(note)}</span></div>')
        if kind == "cover":
            P.append('<div class="grad-cover"></div>')
        else:
            P.append('<div class="grad-top"></div>')
    elif kind == "cta":
        pass
    if kind in ("info",):
        P.append('<div class="grad-top"></div>')
    # 로고
    logo = asset_path("runmate-logo-lime.svg")
    lc = "logo-" + kind
    if logo:
        P.append(f'<img class="logo {lc}" src="{logo}" alt="">')
    else:
        P.append(f'<div class="logo {lc} missing">로고 자리 (에셋 없음)</div>')
    # 카피
    if kind == "cta":
        P.append(f'<h2 class="cta-title">{esc(c["title"])}</h2>')
        P.append(f'<span class="cta">{esc(c["cta"])}</span>')
    elif kind == "cover":
        P.append(f'<h2 class="cover-title">{esc(c["title"])}</h2><p class="cover-cap">{esc(c["caption"])}</p>')
    else:
        P.append('<div class="copy">')
        if c.get("label"): P.append(f'<p class="label">{esc(c["label"])}</p>')
        P.append(f'<h2>{esc(c["title"])}</h2>')
        if c.get("caption"): P.append(f'<p class="caption">{esc(c["caption"])}</p>')
        P.append('</div>')
    if c.get("rows"):
        P.append('<div class="rows">' + "".join(
            f'<div class="row"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in c["rows"]) + "</div>")
    for d in c.get("decorations") or []:
        pos = f'left:{d["x"]}px;top:{d["y"]}px;width:{d["width"]}px;height:{d["height"]}px'
        src = asset_path(d["asset"])
        if src:
            P.append(f'<img class="deco" src="{src}" alt="" style="{pos}">')
        else:
            P.append(f'<div class="deco missing" style="{pos}">{esc(d["asset"])}<br>에셋 없음</div>')
    P.append("</div>")
    return "".join(P)

PHOTO_NOTE = {}

CSS = """
*{{box-sizing:border-box}}
@font-face{{font-family:PretendardLocal;src:url("../assets/PretendardVariable.woff2") format("woff2");font-weight:100 900;font-style:normal;font-display:swap}}
body{{margin:0;padding:32px;background:#eeefe8;font-family:PretendardLocal,{font}}}
h1{{font-size:22px;margin:0 0 24px}}
.gallery{{display:flex;flex-wrap:wrap;gap:24px}}
.shell{{width:360px;height:{sh}px;overflow:hidden}}
.canvas{{position:relative;width:{w}px;height:{h}px;background:{bg};overflow:hidden;
  transform:scale(var(--s,0.3333));transform-origin:top left;font-family:PretendardLocal,{font}}}
.photo{{position:absolute;object-fit:cover}}
.k-cover .photo{{left:0;top:0;width:1080px;height:1350px}}
.k-wide .photo{{left:0;top:454px;width:1080px;height:896px}}
.k-inset .photo{{left:121px;top:656px;width:839px;height:509px;border-radius:16px}}
.placeholder{{display:flex;align-items:center;justify-content:center;text-align:center;color:#8a9085;
  font-size:30px;line-height:1.4;background:#252a23;border:2px dashed #4a5046}}
.grad-cover{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.18) 0%,rgba(0,0,0,0) 48%,rgba(0,0,0,.3) 72%,rgba(0,0,0,.8) 100%)}}
.grad-top{{position:absolute;left:0;top:0;width:1080px;height:728px;background:linear-gradient(180deg,rgba(0,0,0,.8),rgba(0,0,0,0))}}
.k-wide .photo{{z-index:0}}
.k-wide .grad-top{{z-index:1;background:linear-gradient(180deg,rgb(0,0,0) 0%,rgb(0,0,0) 63.19%,rgba(0,0,0,0) 100%)}}  /* 원본 122:8094 gradientTransform: 불투명 0~460px → 투명 728px */
.logo{{position:absolute;width:184px;height:32px;z-index:3}}
.logo-cover{{left:72px;top:72px}} .logo-info,.logo-wide,.logo-inset{{left:775px;top:80px}} .logo-cta{{left:448px;top:240px}}
.missing{{border:2px dashed #E6FF65;color:#E6FF65;font-size:14px;line-height:1.2;display:flex;align-items:center;justify-content:center;text-align:center;background:rgba(230,255,101,.08)}}
.cover-title{{position:absolute;left:72px;top:966px;width:936px;margin:0;z-index:2;color:{title};font-size:88px;font-weight:700;line-height:1.2;letter-spacing:-.02em}}
.cover-cap{{position:absolute;left:72px;top:1206px;width:936px;margin:0;z-index:2;color:{caption};font-size:40px;line-height:1.16;letter-spacing:-.02em;white-space:nowrap}}
.copy{{position:absolute;left:120px;top:192px;width:840px;z-index:2}}
.label{{color:{accent};font-size:36px;font-weight:500;line-height:1.16;letter-spacing:-.02em;margin:0 0 28px;white-space:nowrap}}
h2{{color:{title};font-size:80px;font-weight:700;line-height:1.2;letter-spacing:-.02em;margin:0}}
.caption{{color:{caption};font-size:40px;line-height:1.16;letter-spacing:-.02em;margin:28px 0 0;white-space:nowrap}}
.cta-title{{position:absolute;left:64px;top:320px;width:952px;text-align:center;color:#F5F5EF;font-size:88px;line-height:1.16;z-index:2}}
.cta{{position:absolute;left:351px;top:572px;width:378px;height:85px;border-radius:32px;background:{accent};color:#141713;
  font-size:32px;font-weight:700;line-height:1.4;letter-spacing:-.02em;display:flex;align-items:center;justify-content:center;white-space:nowrap;z-index:2}}
.rows{{position:absolute;left:121px;top:637px;width:839px;z-index:2}}
.row{{display:flex;justify-content:space-between;align-items:center;height:159px;padding:0 80px;margin-bottom:32px;
  border-radius:30px;background:#34362D;color:{title};font-size:34px;line-height:1.16;letter-spacing:-.04em;white-space:nowrap}}
.row b{{font-weight:500}} .row span{{font-weight:400}}
.deco{{position:absolute;z-index:4;pointer-events:none}}
.meta{{margin:8px 0 0;font-size:13px;color:#555}}
"""

def main():
    if len(sys.argv) < 2:
        sys.exit("사용법: python3 scripts/build-preview.py {기획명}")
    plan = sys.argv[1]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", plan):
        sys.exit("기획명은 영문 소문자·숫자·하이픈만 사용하세요")
    src = ROOT / "plans" / plan / "content.json"
    if not src.exists():
        sys.exit(f"없음: {src} — 먼저 기획(A)을 끝내세요")
    cards = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(cards, list) or not cards:
        sys.exit("content.json은 비어 있지 않은 카드 배열이어야 합니다")
    for c in cards:
        card_kind(c)
        if not c.get("id") or not isinstance(c.get("title"), str):
            sys.exit("각 카드에 id와 title이 필요합니다")
        if c.get("image") and Path(c["image"]).name != c["image"]:
            sys.exit("image에는 images 폴더 안의 파일명만 적으세요")
    pm = ROOT / "plans" / plan / "plan.md"
    if pm.exists():
        sec = pm.read_text(encoding="utf-8").split("## 사진 방향")[-1].split("\n## ")[0]
        for line in sec.splitlines():
            m = re.match(r"\|\s*(\d+)\s*\|(.+?)\|(.+?)\|", line)
            if m and int(m.group(1)) <= len(cards):
                PHOTO_NOTE[cards[int(m.group(1))-1]["id"]] = m.group(2).strip() + " / " + m.group(3).strip()
    out_dir = ROOT / "preview" / plan
    out_dir.mkdir(parents=True, exist_ok=True)

    css = CSS.format(w=STYLE["card_w"], h=STYLE["card_h"], sh=int(STYLE["card_h"] / 3),
                     bg=STYLE["bg"], title=STYLE["title"], caption=STYLE["caption"],
                     accent=STYLE["accent"], font=STYLE["font"])
    items = "".join(
        f'<div><article class="shell">{card_html(c, plan)}</article>'
        f'<div class="meta">{i+1}. {esc(c.get("pattern",""))}</div></div>'
        for i, c in enumerate(cards)
    )
    page = (
        '<!doctype html><html lang="ko"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(plan)} 시안</title><style>{css}</style>'
        f'<h1>{esc(plan)} — 카드 {len(cards)}장</h1>'
        f'<section class="gallery">{items}</section></html>'
    )
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    missing = [c["id"] for c in cards if card_kind(c) in ("cover", "wide", "inset")
               and (not c.get("image") or not (ROOT/"assets/content"/plan/"images"/c["image"]).is_file())]
    missing_assets = sorted({d["asset"] for c in cards for d in (c.get("decorations") or []) if not asset_path(d["asset"])})
    if not asset_path("runmate-logo-lime.svg"):
        missing_assets.append("runmate-logo-lime.svg")
    if missing_assets:
        print("에셋 없음: " + ", ".join(missing_assets))
    if not (ROOT/"preview/assets/PretendardVariable.woff2").is_file():
        print("폰트 파일 없음: preview/assets/PretendardVariable.woff2")
    print(f"완료: preview/{plan}/index.html — 카드 {len(cards)}장")
    if missing:
        print(f"사진 없는 카드: {', '.join(missing)} (자리만 비워 뒀습니다)")

if __name__ == "__main__":
    main()
