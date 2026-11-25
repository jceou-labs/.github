---
name: jceou-labs
description: A hardware-store peg-hook display; each Claude Code tool hangs on the wall as a packaged product.
colors:
  pegboard-steel: "#9a9da0"
  sign-black: "#181818"
  sign-paper: "#f4f4f2"
  sign-subtitle: "#dcdcd9"
  strip-black: "#101010"
  ink-black: "#141414"
  ink-white: "#ffffff"
  pack-orange: "#ee7725"
  pack-violet: "#7547f9"
  pack-teal: "#00afa0"
  pack-yellow: "#efcd16"
typography:
  display:
    fontFamily: "Outfit, sans-serif"
    fontSize: "118px"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Outfit, sans-serif"
    fontSize: "36px"
    fontWeight: 500
    lineHeight: 1
  title:
    fontFamily: "Outfit, sans-serif"
    fontSize: "34px"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  label:
    fontFamily: "Outfit, sans-serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.02em"
  body:
    fontFamily: "Palanquin, sans-serif"
    fontSize: "15px"
    fontWeight: 500
    lineHeight: 1.2
  mono:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "17px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.01em"
rounded:
  window: "7px"
spacing:
  hole-pitch: "68.8px"
  pack-pitch: "344px"
  contents-inset: "22px"
components:
  pack-context:
    backgroundColor: "{colors.pack-orange}"
    textColor: "{colors.ink-black}"
    width: "282px"
  pack-tracker:
    backgroundColor: "{colors.pack-violet}"
    textColor: "{colors.ink-white}"
    width: "282px"
  pack-images:
    backgroundColor: "{colors.pack-teal}"
    textColor: "{colors.ink-black}"
    width: "282px"
  pack-skills:
    backgroundColor: "{colors.pack-yellow}"
    textColor: "{colors.ink-black}"
    width: "282px"
  price-strip:
    backgroundColor: "{colors.strip-black}"
    textColor: "{colors.sign-paper}"
    typography: "{typography.mono}"
    height: "60px"
  header-sign:
    backgroundColor: "{colors.sign-black}"
    textColor: "{colors.sign-paper}"
    typography: "{typography.display}"
    width: "640px"
  blister-window:
    rounded: "{rounded.window}"
    width: "184px"
    height: "142px"
---

# Design System: jceou-labs

## Overview

**Creative North Star: "Le présentoir de quincaillerie" (the hardware-store peg-hook display)**

The organization is a wall in a hardware store. A perforated galvanized steel pegboard fills the frame, a black sign hangs from two hooks and names the workshop, and each tool hangs below it on its own peg hook as a blister pack you can take home in one line. Each pack shows the real tool through its clear window, names itself on the card and puts its install command on the black price strip.

The world is photographed retail stock, not illustration: real steel mottling, punched holes, chrome hooks, vacuum-formed plastic with a sheen, soft cast shadows. Colour belongs to the packs alone; everything else is steel, black and clear plastic. The page stays sober and concrete: a workshop rather than a company.

Every surface is a single composed raster (`profile/assets/wall.jpg`, 1920 x 1280), assembled from plates by `assets/build/render.py` through the HTML compositor `assets/build/wall.html` at a 1536 x 1024 layout rendered at 1.25x. All values below are layout px at 1536; multiply by 1.25 for the shipped JPEG.

**Key Characteristics:**
- One steel pegboard, one hole pitch, every hook on a hole.
- One saturated colour per tool, nowhere else.
- Real tool imagery in every window; no invented text on any pack.
- The install line is the loudest line on each pack, set like a price strip.
- Real, selectable text lives below the banner in GitHub's own Markdown.

## Colors

Neutral steel and black carry the wall; four saturated pack colours, one per tool, carry the identity.

### Primary
- **Pack Orange** (`pack-orange`): the card of claude-context. Black ink.
- **Pack Violet** (`pack-violet`): the card of claude-project-tracker. The only pack with white ink.
- **Pack Teal** (`pack-teal`): the card of claude-local-images. Black ink.
- **Pack Yellow** (`pack-yellow`): the card of claude-workflow-skills. Black ink.

Pack values are medians measured on the shipped plates (`assets/plates/pack-*.png`); the plates are rasters, so these are the reference hues, not CSS fills.

### Neutral
- **Pegboard Steel** (`pegboard-steel`): the galvanized board behind everything, neutral grey with its blue cast pulled out (70% desaturated in `make_plates.py`). The compositor's flat fallback is a near match.
- **Sign Black** (`sign-black`): the header sign, a matte near-black card (the plate is darkened to 78% brightness in the compositor).
- **Sign Paper** (`sign-paper`): the wordmark on the sign and the command text on every price strip.
- **Sign Subtitle** (`sign-subtitle`): the sign's second line, one step quieter than the wordmark.
- **Strip Black** (`strip-black`): the price-strip band at the foot of every pack, part of the pack plate.
- **Ink Black** (`ink-black`) / **Ink White** (`ink-white`): pack card text, chosen per pack by contrast.

### Named Rules
**The One Colour Per Pack Rule.** Each tool owns exactly one saturated colour, used on its card and nowhere else on the wall. The sign, the board, the hooks and the strips stay steel, black and clear.

**The Ink By Contrast Rule.** Card ink is black (`#141414`) unless black falls below 4.5:1 on the pack colour, then white. Violet is the only current case (black 3.8:1, white 4.8:1).

## Typography

**Display Font:** Outfit (sans-serif fallback)
**Body Font:** Palanquin (sans-serif fallback)
**Label/Mono Font:** JetBrains Mono (monospace fallback)

**Character:** Outfit is the printed packaging voice, heavy and geometric like a retail card; Palanquin is the small contents line; JetBrains Mono is the command, the one place the terminal shows through. All load from Google Fonts with `display=block` so the render never captures a fallback.

### Hierarchy
- **Display** (Outfit 800, 118px, line-height 1, -0.03em): the wordmark `jceou-labs` on the sign, centred in a 640px card.
- **Headline** (Outfit 500, 36px, line-height 1): the sign's second line, "Free tools for Claude Code".
- **Title** (Outfit 800, fitted from 34px down, line-height 1.05, -0.02em): the tool name minus its `claude-` prefix. One size for all packs: the largest at which the longest name fits 86% of the card width.
- **Label** (Outfit 600, 17px, +0.02em, 85% opacity): the `claude-` prefix above each name; the name is split, never extended with invented words.
- **Body** (Palanquin 500, 15px, line-height 1.2, 92% opacity): the contents line, three or four real parts joined by middle dots, under a 1.5px rule in the ink colour, inset 22px.
- **Mono** (JetBrains Mono 700, fitted from 17px down, -0.01em): the install command on the price strip. One size for all strips: the largest at which every command fits with 22px to spare.

### Named Rules
**The Shared Size Rule.** Names fit together and strips fit together: one computed size per role across all packs, so no pack looks louder than another.

## Layout

The pegboard is the only grid. Holes sit every **68.8px** (`hole-pitch`) from a first hole at (45.6, 58), punched in `make_plates.py`. Packs hang one per hole column, **five pitches apart** (`pack-pitch`, 344px): hook rings on row y = 402 at x = 252, 596, 940, 1284. The sign hangs centred on x = 768 from two hooks, its card top at y = 92, 640px wide.

Inside a pack plate (512 x 768) everything is offset from the hook: blister window at (+164, +292), label block at +486, price strip on the plate's measured black band. `render.py` measures the card, hook tip and band from the pixels, so moving a pack means changing its hole column only.

The README below the banner uses GitHub's own layout: a two-column table (tool, what it does), an Install code block, the tracker sentence, and an In use row of screenshots at 100% and 2 x 49%.

## Elevation & Depth

Depth is physical: every hanging object casts one soft shadow onto the board, down and to the right as from a ceiling light. The blister windows add a diagonal plastic sheen. No other depth device is used.

### Shadow Vocabulary
- **Hanging shadow** (`filter: drop-shadow(7px 12px 9px rgba(0,0,0,.38))`): sign and packs, the same light for every object.
- **Blister sheen** (`linear-gradient(135deg, rgba(255,255,255,.28) 0%, rgba(255,255,255,.06) 32%, transparent 55%)`): over each window, clipped to its 7px radius.

### Named Rules
**The One Light Rule.** One light source for the whole wall; a new object takes the same shadow offset, blur and opacity.

## Shapes

Shapes come from the objects: the rectangular sign, the pack card with rounded top corners and a euro-slot hang hole, the moulded blister bubble, the screen inset with gently rounded corners (7px), round punched holes (10.5px radius). Nothing is drawn as an abstract UI shape.

## Components

### Pack (signature)
A blister card hanging on one hook. Plate: `assets/plates/pack-<id>.png`, coloured card, blister bubble, black price-strip band, no printed text. The compositor adds, top to bottom: the window, the `claude-` label, the name, the ruled contents line, the command on the strip. Card width 282px.

### Blister window
184 x 142px, 7px radius, sheen overlay. The plate is cut from the tool's own material at 2x (368 x 284): claude-context recomposes its real gauge band (gauge, token count, buttons); claude-project-tracker crops its real overview page; claude-local-images shows an image it generated; claude-workflow-skills lists its nine real skill names in JetBrains Mono on `#161616`, alternate lines in yellow.

### Header sign
Matte black card on two hooks, wordmark plus subtitle in sign paper. Plate `header-card.png`, text set by the compositor.

### Price strip
The black band at the foot of each pack, 60px tall, one line of JetBrains Mono 700 in sign paper: the real install command, or the real install instruction when the tool is not a plugin.

### Adding a fifth tool
1. Pick a fifth saturated pack colour, distinct in hue from orange, violet, teal and yellow; set the ink by The Ink By Contrast Rule.
2. Make its pack plate from the existing ones: same hook, blister and band, recoloured, no text. Cut its window plate from the tool's real screenshot in `make_plates.py`.
3. Give it a hole column in `PACKS` in `render.py`. Five 282px cards do not fit at five pitches in 1536px; drop to four pitches (275.2px) with packs scaled uniformly to fit, and shift the hole origin by half a pitch in `make_plates.py` so the middle pack still centres on x = 768.
4. Re-run `make_plates.py`, then `render.py`; add the tool to the README table and Install block.

## Do's and Don'ts

### Do:
- **Do** put every hook ring on a pegboard hole; positions are hole columns, multiples of 68.8px.
- **Do** show the real tool in each window: its own screenshot, output or real content.
- **Do** keep text on the wall to real names, real contents and real install lines, set by the compositor.
- **Do** ship the banner as one opaque composed JPEG with its own background, so it reads the same in GitHub light and dark themes.
- **Do** keep everything a reader needs (description, install lines, links) as real Markdown text below the banner.

### Don't:
- **Don't** print invented text, logos or fake labels on the pack plates; packs carry no text of their own.
- **Don't** use a pack colour outside its own pack, or give two tools the same colour.
- **Don't** rely on CSS, JavaScript or transparency in the README; GitHub strips the first two and the theme shows through the third.
