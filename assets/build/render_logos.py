"""Render three avatar proposals for the jceou-labs organization from the wall's own material.

Run from the repository root: python assets/build/render_logos.py
Writes .impeccable/build/logos/logo-{a,b,c}.png (512 px) and a sheet with small sizes.
"""
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path.cwd()
OUT = ROOT / ".impeccable/build/logos"
FONTS = ("https://fonts.googleapis.com/css2?family=Palanquin+Dark:wght@400;600&display=block")
PEG = (ROOT / "assets/plates/pegboard.png").as_uri()
PACK = (ROOT / "assets/plates/pack-context.png").as_uri()

# the pegboard plate has holes every 68.8 px from (45.6, 58); this offset puts holes at 187.2 and 324.8 px
BASE = f"""
  html,body{{margin:0;width:512px;height:512px;overflow:hidden}}
  .peg{{position:absolute;inset:0;background:#9d9e9d url({PEG}) -408.8px -421.2px / 1536px 1024px}}
"""

LOGOS = {
    "a": f"""<style>{BASE}
      .card{{position:absolute;left:56px;top:96px;width:400px;height:320px;background:#121212;border-radius:10px;
             box-shadow:10px 16px 18px rgba(0,0,0,.42);display:flex;align-items:center;justify-content:center}}
      .card span{{font:400 230px/1 'Palanquin Dark',sans-serif;color:#f4f4f2;letter-spacing:-0.02em;margin-top:22px}}
    </style><div class="peg"></div><div class="card"><span>jl</span></div>""",
    "b": f"""<style>{BASE}
      img{{position:absolute;left:50%;top:-14px;height:600px;transform:translateX(-50%);
           filter:drop-shadow(8px 14px 12px rgba(0,0,0,.4))}}
    </style><div class="peg"></div><img src="{PACK}" alt="">""",
    "c": f"""<style>{BASE}
      .pegs{{position:absolute;inset:0}}
      .pegs i{{position:absolute;width:118px;height:118px;border-radius:50%;
               box-shadow:inset -8px -10px 0 rgba(0,0,0,.18), 8px 12px 14px rgba(0,0,0,.4)}}
    </style><div class="peg"></div>
    <div class="pegs">
      <i style="left:128.2px;top:128.2px;background:#f4772b"></i>
      <i style="left:265.8px;top:128.2px;background:#7b4dff"></i>
      <i style="left:128.2px;top:265.8px;background:#00b3a4"></i>
      <i style="left:265.8px;top:265.8px;background:#f5d31c"></i>
    </div>""",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 512, "height": 512}, device_scale_factor=1)
        for key, body in LOGOS.items():
            html = OUT / f"logo-{key}.html"
            html.write_text(f"<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='{FONTS}'></head><body>{body}</body></html>", encoding="utf-8")
            page.goto(html.as_uri())
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            page.screenshot(path=str(OUT / f"logo-{key}.png"))
        browser.close()
    # sheet: each proposal at 256, 64 and 32 px, in a rounded-square mask like GitHub's org avatar
    sheet = Image.new("RGB", (3 * 300, 380), (246, 248, 250))
    for i, key in enumerate(LOGOS):
        im = Image.open(OUT / f"logo-{key}.png").convert("RGB")
        x = i * 300 + 22
        sheet.paste(im.resize((256, 256), Image.LANCZOS), (x, 20))
        sheet.paste(im.resize((64, 64), Image.LANCZOS), (x, 296))
        sheet.paste(im.resize((32, 32), Image.LANCZOS), (x + 80, 312))
    sheet.save(OUT / "sheet.png")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
