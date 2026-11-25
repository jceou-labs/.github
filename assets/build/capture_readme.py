"""Capture profile/README.md as GitHub renders it, before anything is pushed.

The README is converted with marked and styled with github-markdown-css (light theme), at GitHub's
README column widths; the banner URL is pointed at the local profile/assets/wall.jpg.
Run from the repository root: python assets/build/capture_readme.py
Writes .impeccable/review/desktop.png and .impeccable/review/mobile.png.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path.cwd()
REVIEW = ROOT / ".impeccable/review"
BANNER = "https://raw.githubusercontent.com/jceou-labs/.github/main/profile/assets/wall.jpg"

PAGE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.8.1/github-markdown-light.css">
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<style>
  body { margin:0; background:#ffffff; }
  .frame { max-width:%(col)dpx; margin:24px auto; border:1px solid #d0d7de; border-radius:6px; padding:%(pad)dpx; }
</style></head><body>
<div class="frame"><article class="markdown-body" id="md"></article></div>
<script>
  document.getElementById('md').innerHTML = marked.parse(%(md)s);
  Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))
    .then(() => document.body.dataset.ready = '1');
</script></body></html>"""


def capture(page, name, width, col, pad):
    md = (ROOT / "profile/README.md").read_text(encoding="utf-8")
    md = md.replace(BANNER, (ROOT / "profile/assets/wall.jpg").as_uri())
    html = REVIEW / f"readme-{name}.html"
    html.write_text(PAGE % {"col": col, "pad": pad, "md": json.dumps(md)}, encoding="utf-8")
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(html.as_uri())
    page.wait_for_selector("body[data-ready='1']", timeout=60000)
    broken = page.evaluate("[...document.images].filter(i => !i.naturalWidth).map(i => i.src)")
    page.screenshot(path=str(REVIEW / f"{name}.png"), full_page=True)
    print(name, "broken images:", broken or "none")


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(device_scale_factor=1)
        capture(page, "desktop", 1280, 830, 32)   # GitHub org profile README column
        page.close()
        page = browser.new_page(device_scale_factor=2, is_mobile=True)
        capture(page, "mobile", 390, 360, 16)
        browser.close()


if __name__ == "__main__":
    main()
