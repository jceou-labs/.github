"""Render one social preview per tool (1280 x 640, GitHub's size) from the wall banner.

Each preview keeps the wall's own board, header card and pack: the other packs are taken down, the header card
and the tool's pack are moved by whole hole pitches so every hook still lands in a hole, and the card carries
the tool's name and description.
Run from the repository root, after render.py: python assets/build/render_previews.py
Writes assets/previews/<repo>.jpg (GitHub takes social previews under 1 MB).
"""
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path.cwd()
OUT = ROOT / "assets/previews"
PITCH = 68.8
CLIP = {"x": 112.0, "y": 300.0, "width": 1400.0, "height": 700.0}  # wall pixels, 2:1
PACK_HOLE = 1215.2   # a hole column (45.6 + 17 pitches) for the moved pack
HEAD_SHIFT = (-4 * PITCH, 5 * PITCH)

TOOLS = [
    ("claude-context", "Context gauge above the Claude Code prompt, with Compact and Handoff note buttons."),
    ("claude-project-tracker", "Offline project pages kept up to date by Claude Code: done, remaining, waiting for you."),
    ("claude-local-images", "Generate images locally from Claude Code with ComfyUI and Z-Image Turbo."),
    ("claude-workflow-skills", "Nine Claude Code skills that keep long work on track: plans, handoffs, reviews."),
]

STAGE = """
(([index, name, desc, packHole, headShift]) => {
  document.querySelector('.title').remove();
  document.querySelector('.sub').remove();
  const head = document.querySelector('.head');
  const px = v => parseFloat(v);
  head.style.left = (px(head.style.left) + headShift[0]) + 'px';
  head.style.top = (px(head.style.top) + headShift[1]) + 'px';
  // five elements per pack, in order: plate, window, sheen, label, strip
  const parts = [...document.querySelectorAll('.wall > .pack, .wall > .win, .wall > .sheen, .wall > .label, .wall > .strip')];
  const packs = [];
  for (let i = 0; i < parts.length; i += 5) packs.push(parts.slice(i, i + 5));
  packs.forEach((p, i) => {
    if (i !== index) { p.forEach(e => e.remove()); return; }
    const dx = packHole - (px(p[0].style.left) + 256);
    p.forEach(e => e.style.left = (px(e.style.left) + dx) + 'px');
  });
  return true;
})
"""

CARD = """
(([name, desc, box, fixed]) => {
  const d = document.createElement('div');
  d.className = 'pv';
  Object.assign(d.style, {position: 'absolute', left: box[0] + 'px', top: box[1] + 'px', width: box[2] + 'px',
    height: box[3] + 'px', display: 'flex', flexDirection: 'column', justifyContent: 'center',
    padding: '0 44px', boxSizing: 'border-box'});
  d.innerHTML = `<div style="font:600 22px/1 'Outfit',sans-serif;color:#bdbdb9;letter-spacing:.02em">jceou-labs</div>
    <div class="pvname" style="font:800 60px/1.05 'Outfit',sans-serif;color:#f4f4f2;letter-spacing:-0.025em;
      white-space:nowrap;align-self:flex-start;margin-top:10px">${name}</div>
    <div style="font:500 22px/1.3 'Palanquin',sans-serif;color:#dcdcd9;margin-top:14px">${desc}</div>`;
  document.querySelector('.wall').appendChild(d);
  const n = d.querySelector('.pvname');
  let s = fixed || 60;
  n.style.fontSize = s + 'px';
  while (!fixed && s > 30 && n.offsetWidth > box[2] - 88) { s -= 1; n.style.fontSize = s + 'px'; }
  return s;
})
"""


def head_card_box():
    """The black card's box on the wall, as render.py places it (640 px wide, top at 92)."""
    from render import measure  # same folder
    m = measure()
    hx0, hy0, hx1, hy1 = m["header"]
    k = 640.0 / (hx1 - hx0)
    return [768 - 320 + HEAD_SHIFT[0], 92 + HEAD_SHIFT[1], 640.0, (hy1 - hy0) * k]


def main():
    import sys
    sys.path.insert(0, str(ROOT / "assets/build"))
    OUT.mkdir(parents=True, exist_ok=True)
    box = head_card_box()
    wall = ROOT / "assets/build/wall.html"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1536, "height": 1024}, device_scale_factor=2 * 1280 / CLIP["width"])
        # one name size for the whole set: the largest that fits the longest name
        sizes = []
        for i, (name, desc) in enumerate(TOOLS):
            page.goto(wall.as_uri())
            page.wait_for_selector("body[data-ready='1']")
            sizes.append(page.evaluate(CARD, [name, desc, box, None]))
        size = min(sizes)
        for i, (name, desc) in enumerate(TOOLS):
            page.goto(wall.as_uri())
            page.wait_for_selector("body[data-ready='1']")
            page.evaluate(STAGE, [i, name, desc, PACK_HOLE, list(HEAD_SHIFT)])
            page.evaluate(CARD, [name, desc, box, size])
            raw = OUT / f"{name}-2x.png"
            page.screenshot(path=str(raw), clip=CLIP)
            Image.open(raw).convert("RGB").resize((1280, 640), Image.LANCZOS).save(OUT / f"{name}.jpg", quality=90, optimize=True, progressive=True)
            raw.unlink()
            print(name, "name size", size)
        browser.close()
    print("wrote", OUT, json.dumps(box))


if __name__ == "__main__":
    main()
