"""Compose the jceou-labs wall banner from its plates and render it to profile/assets/wall.jpg.

Run from the repository root: python assets/build/render.py
Needs Pillow and Playwright for Python (Chromium). Fonts load from Google Fonts.
"""
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path.cwd()
PLATES = ROOT / "assets/plates"
OUT = ROOT / "profile/assets"
W, H = 1536, 1024
SCALE = 1.25  # 1920 px wide: sharp at GitHub's README width on high-density screens

# hole grid from make_plates.py: each hook ring sits on a hole
HOOK_ROW = 402.0
PACKS = [
    {"id": "context", "hole_x": 252.0, "name": "claude-context", "ink": "#141414",
     "contents": "Gauge · Compact · Handoff note", "strip": "/plugin install context-claude"},
    {"id": "tracker", "hole_x": 596.0, "name": "claude-project-tracker", "ink": "#ffffff",
     "contents": "Project pages · Overview · Offline", "strip": "Ask Claude: follow INSTALL.md"},
    {"id": "images", "hole_x": 940.0, "name": "claude-local-images", "ink": "#141414",
     "contents": "ComfyUI · Z-Image Turbo · your GPU", "strip": "/plugin install local-images"},
    {"id": "skills", "hole_x": 1284.0, "name": "claude-workflow-skills", "ink": "#141414",
     "contents": "9 skills · plan · handoff · review", "strip": "/plugin install workflow-skills"},
]
SKILLS = ["session-handoff", "session-retro", "plan-first", "adversarial-review", "repo-sweep",
          "bottleneck-log", "reusable-bricks", "stack-discipline", "secrets-centralization"]

FONTS = ("https://fonts.googleapis.com/css2?family=Palanquin+Dark:wght@400;600"
         "&family=Palanquin:wght@400;500&family=Outfit:wght@500;600;800"
         "&family=JetBrains+Mono:wght@500;700&display=block")


def bbox(path, test):
    im = Image.open(path).convert("RGBA")
    px = im.load()
    xs, ys = [], []
    for y in range(im.height):
        for x in range(im.width):
            if test(*px[x, y]):
                xs.append(x)
                ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def measure():
    pack = PLATES / "pack-context.png"
    # the card: opaque, saturated pixels
    card = bbox(pack, lambda r, g, b, a: a > 250 and max(r, g, b) - min(r, g, b) > 80)
    # the hook: topmost opaque pixels in the central column
    im = Image.open(pack).convert("RGBA")
    tip = next(y for y in range(im.height) for x in range(236, 276) if im.getpixel((x, y))[3] > 200)
    # the black band: the dark opaque rows under the coloured part of the card
    dark_rows = [y for y in range(card[3], im.height)
                 if sum(1 for x in range(card[0], card[2]) if im.getpixel((x, y))[3] > 250
                        and max(im.getpixel((x, y))[:3]) < 40) > (card[2] - card[0]) * 0.6]
    band = (card[0], card[3] + 1, card[2], max(dark_rows))
    # the header card: rows and columns that are mostly dark (the hooks are thin and drop out)
    hd = Image.open(PLATES / "header-card.png").convert("RGBA")
    hp = hd.load()
    is_dark = lambda x, y: hp[x, y][3] > 250 and max(hp[x, y][:3]) < 75
    rows = [y for y in range(hd.height) if sum(is_dark(x, y) for x in range(0, hd.width, 4)) > hd.width / 4 * 0.5]
    cols = [x for x in range(hd.width) if sum(is_dark(x, y) for y in range(0, hd.height, 4)) > hd.height / 4 * 0.5]
    header = (min(cols), min(rows), max(cols), max(rows))
    return {"card": card, "ring_y": tip + 7, "band": band, "header": header,
            "header_size": Image.open(PLATES / "header-card.png").size}


def skills_window(page):
    rows = "".join(f"<li>{s}</li>" for s in SKILLS)
    page.set_viewport_size({"width": 368, "height": 284})
    page.set_content(f"""<!doctype html><html><head><link rel="stylesheet" href="{FONTS}"><style>
      html,body{{margin:0;background:#161616;width:368px;height:284px;overflow:hidden}}
      ul{{list-style:none;margin:0;padding:22px 26px;font:500 20px/27.5px 'JetBrains Mono',monospace;color:#e8e8e6}}
      li:nth-child(odd){{color:#f5d31c}}
    </style></head><body><ul>{rows}</ul></body></html>""")
    page.evaluate("document.fonts.ready")
    page.screenshot(path=str(PLATES / "window-skills.png"))


def wall_html(m):
    cx0, cy0, cx1, cy1 = m["card"]
    card_w = cx1 - cx0
    band_top = m["band"][1]
    hx0, hy0, hx1, hy1 = m["header"]
    hw, hh = m["header_size"]
    head_card_w = 640.0
    k = head_card_w / (hx1 - hx0)
    head_left = 768 - (hx0 + (hx1 - hx0) / 2) * k
    head_top = 92 - hy0 * k
    card_box = (head_left + hx0 * k, 92, head_card_w, (hy1 - hy0) * k)

    packs = []
    for p in PACKS:
        left = p["hole_x"] - 256
        top = HOOK_ROW - m["ring_y"]
        packs.append(f"""
      <img class="plate pack" src="../../assets/plates/pack-{p['id']}.png" style="left:{left}px;top:{top}px" alt="">
      <img class="win" src="../../assets/plates/window-{p['id']}.png" style="left:{left + 164}px;top:{top + 292}px" alt="">
      <div class="sheen" style="left:{left + 164}px;top:{top + 292}px;width:184px;height:142px"></div>
      <div class="label" style="left:{left + cx0}px;top:{top + 486}px;width:{card_w}px;color:{p['ink']}">
        <div class="brand">claude-</div>
        <div class="name">{p['name'].removeprefix('claude-')}</div>
        <div class="contents">{p['contents']}</div>
      </div>
      <div class="strip" style="left:{left + cx0}px;top:{top + band_top}px;width:{card_w}px;height:{m['band'][3] - band_top}px"><span>{p['strip']}</span></div>""")

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>jceou-labs wall</title>
<link rel="stylesheet" href="{FONTS}">
<style>
  :root {{ --ink:#141414; --paper:#f4f4f2; }}
  html,body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; background:#9d9e9d; }}
  .wall {{ position:relative; width:{W}px; height:{H}px; background:url(../../assets/plates/pegboard.png) 0 0/{W}px {H}px; }}
  .plate {{ position:absolute; filter:drop-shadow(7px 12px 9px rgba(0,0,0,.38)); }}
  .head {{ width:{hw * k}px; height:{hh * k}px; filter:brightness(.78) contrast(1.15) drop-shadow(7px 12px 9px rgba(0,0,0,.38)); }}
  .win {{ position:absolute; width:184px; height:142px; border-radius:7px; }}
  .sheen {{ position:absolute; border-radius:7px; pointer-events:none;
           background:linear-gradient(135deg, rgba(255,255,255,.28) 0%, rgba(255,255,255,.06) 32%, rgba(255,255,255,0) 55%); }}
  .title {{ position:absolute; left:{card_box[0]}px; width:{card_box[2]}px; top:{card_box[1] + 50}px; text-align:center;
           font:800 118px/1 'Outfit',sans-serif; color:var(--paper); letter-spacing:-0.03em; }}
  .sub {{ position:absolute; left:{card_box[0]}px; width:{card_box[2]}px; top:{card_box[1] + 190}px; text-align:center;
         font:500 36px/1 'Outfit',sans-serif; color:#dcdcd9; }}
  .label {{ position:absolute; text-align:center; }}
  .brand {{ font:600 17px/1 'Outfit',sans-serif; letter-spacing:0.02em; opacity:.85; }}
  .name {{ font:800 var(--name-size, 30px)/1.05 'Outfit',sans-serif; letter-spacing:-0.02em; white-space:nowrap; margin-top:3px; display:inline-block; }}
  .contents {{ margin:9px 22px 0; padding-top:8px; border-top:1.5px solid currentColor;
              font:500 15px/1.2 'Palanquin',sans-serif; opacity:.92; white-space:nowrap; }}
  .strip {{ position:absolute; display:flex; align-items:center; justify-content:center;
           font:700 var(--strip-size, 15px)/1 'JetBrains Mono',monospace; color:#f4f4f2; letter-spacing:-0.01em; white-space:nowrap; }}
</style></head>
<body><div class="wall">
  <img class="plate head" src="../../assets/plates/header-card.png" style="position:absolute;left:{head_left}px;top:{head_top}px" alt="">
  <div class="title">jceou-labs</div>
  <div class="sub">Free tools for Claude Code</div>
  {''.join(packs)}
</div>
<script>
  // one name size for all four packs: the largest that fits the longest name
  const names = [...document.querySelectorAll('.name')];
  let size = 34;
  const fits = () => names.every(n => n.offsetWidth <= n.parentElement.clientWidth * 0.86);
  document.fonts.ready.then(() => {{
    while (size > 14) {{ document.documentElement.style.setProperty('--name-size', size + 'px'); if (fits()) break; size -= 0.5; }}
    const strips = [...document.querySelectorAll('.strip span')];
    let s = 17;
    while (s > 10) {{ document.documentElement.style.setProperty('--strip-size', s + 'px');
      if (strips.every(x => x.offsetWidth <= x.parentElement.clientWidth - 22)) break; s -= 0.5; }}
    document.body.dataset.ready = '1';
  }});
</script>
</body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m = measure()
    print("measure", json.dumps(m))
    src = ROOT / "assets/build/wall.html"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(device_scale_factor=1)
        skills_window(page)
        page.close()
        src.write_text(wall_html(m), encoding="utf-8")
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        page.goto(src.as_uri())
        page.wait_for_selector("body[data-ready='1']")
        png = ROOT / ".impeccable/build/wall-render.png"
        page.screenshot(path=str(png))
        page.set_viewport_size({"width": W, "height": H})
        browser.close()
    Image.open(png).convert("RGB").save(OUT / "wall.jpg", quality=88, optimize=True, progressive=True)
    print("wrote", OUT / "wall.jpg")


if __name__ == "__main__":
    main()
