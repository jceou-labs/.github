"""Build the raster plates for the jceou-labs wall banner.

- pegboard.png: generated galvanized steel (steel.png) with holes punched on an exact grid,
  so every peg hook lands in a hole.
- window-*.png: the screen shown inside each blister pack, cut from each tool's real screenshots.

Run from the repository root: python assets/build/make_plates.py <steel.png> <sources-dir>
<sources-dir> holds band.png (claude-context), overview.png (claude-project-tracker) and
text-to-image.jpg (claude-local-images). window-skills.png is rendered by render.py.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

W, H = 1536, 1024
PITCH = 68.8          # hole pitch: four packs sit 5 pitches apart (344 px, as in the comp)
X0, Y0 = 45.6, 58.0   # first hole column and row
HOLE_R = 10.5
PLATES = Path("assets/plates")
INSERT = (368, 284)   # 2x the dark insert inside a pack plate (184 x 142)


def hole_centres():
    cols = [X0 + PITCH * i for i in range(-1, int(W / PITCH) + 2)]
    rows = [Y0 + PITCH * j for j in range(-1, int(H / PITCH) + 2)]
    return [(x, y) for x in cols for y in rows]


def pegboard(steel_path):
    s = 2  # draw at 2x, then downsample for clean edges
    steel = Image.open(steel_path).convert("RGB").resize((W, H), Image.LANCZOS)
    # pull the generated steel to a neutral grey: keep its mottling, drop the blue cast
    grey = steel.convert("L").convert("RGB")
    steel = Image.blend(steel, grey, 0.7)
    # bring the zinc spangle forward and lift the board to the comp's lighter grey
    steel = ImageEnhance.Contrast(steel).enhance(1.45)
    steel = ImageEnhance.Brightness(steel).enhance(1.12)
    big = steel.resize((W * s, H * s), Image.LANCZOS)
    shade = Image.new("L", big.size, 0)
    rim = Image.new("L", big.size, 0)
    hole = Image.new("L", big.size, 0)
    ds, dr, dh = ImageDraw.Draw(shade), ImageDraw.Draw(rim), ImageDraw.Draw(hole)
    for x, y in hole_centres():
        cx, cy, r = x * s, y * s, HOLE_R * s
        # pressed edge: a soft dark ring above-left, a light lip below-right
        ds.ellipse((cx - r - 5, cy - r - 5, cx + r + 2, cy + r + 2), fill=120)
        dr.ellipse((cx - r + 1, cy - r + 2, cx + r + 3, cy + r + 4), fill=150)
        dh.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    shade = shade.filter(ImageFilter.GaussianBlur(4 * s))
    rim = rim.filter(ImageFilter.GaussianBlur(1.2 * s))
    dark = Image.new("RGB", big.size, (22, 22, 22))
    light = Image.new("RGB", big.size, (205, 207, 207))
    out = Image.composite(Image.new("RGB", big.size, (70, 70, 70)), big, shade.point(lambda v: v * 0.45))
    out = Image.composite(light, out, rim.point(lambda v: v * 0.55))
    # the hole itself: near black, a touch lighter at its lower edge (the board behind)
    inner = Image.new("L", big.size, 0)
    di = ImageDraw.Draw(inner)
    for x, y in hole_centres():
        cx, cy, r = x * s, y * s, HOLE_R * s
        di.ellipse((cx - r + 3, cy - r + 7, cx + r - 3, cy + r - 1), fill=60)
    out = Image.composite(dark, out, hole)
    out = Image.composite(Image.new("RGB", big.size, (58, 56, 52)), out, inner.filter(ImageFilter.GaussianBlur(3 * s)))
    out = out.resize((W, H), Image.LANCZOS)
    out.save(PLATES / "pegboard.png")


def fit(img, size, focus=(0.5, 0.5)):
    """Crop img to the aspect of size around focus, then resize."""
    tw, th = size
    w, h = img.size
    if w / h > tw / th:
        nw = round(h * tw / th)
        x = round((w - nw) * focus[0])
        img = img.crop((x, 0, x + nw, h))
    else:
        nh = round(w * th / tw)
        y = round((h - nh) * focus[1])
        img = img.crop((0, y, w, y + nh))
    return img.resize(size, Image.LANCZOS)


def windows(src):
    src = Path(src)
    tw, th = INSERT
    # claude-context: the real band, cut in three and enlarged so it fills the window:
    # the percentage and bar, the token count, then the two buttons
    band = Image.open(src / "band.png").convert("RGB")
    win = Image.new("RGB", INSERT, (24, 24, 24))
    gauge = band.crop((0, 0, 312, 52))
    gauge = gauge.resize((tw - 24, round(52 * (tw - 24) / 312)), Image.LANCZOS)
    count = band.crop((312, 0, 400, 52))
    count = count.resize((round(88 * 1.7), round(52 * 1.7)), Image.LANCZOS)
    buttons = band.crop((522, 0, 770, 52))
    buttons = buttons.resize((round(248 * 1.35), round(52 * 1.35)), Image.LANCZOS)
    gap = 6
    y = (th - gauge.height - count.height - buttons.height - 2 * gap) // 2
    win.paste(gauge, (12, y))
    win.paste(count, (tw - count.width - 6, y + gauge.height + gap))
    win.paste(buttons, (tw - buttons.width - 6, y + gauge.height + count.height + 2 * gap))
    win.save(PLATES / "window-context.png")
    # claude-project-tracker: the overview page, its headline and figures
    ov = Image.open(src / "overview.png").convert("RGB").crop((20, 96, 760, 666))
    fit(ov, INSERT).save(PLATES / "window-tracker.png")
    # claude-local-images: an image it generated
    ti = Image.open(src / "text-to-image.jpg").convert("RGB")
    fit(ti, INSERT, (0.5, 0.5)).save(PLATES / "window-images.png")


if __name__ == "__main__":
    PLATES.mkdir(parents=True, exist_ok=True)
    pegboard(sys.argv[1])
    windows(sys.argv[2])
    print("plates written to", PLATES)
