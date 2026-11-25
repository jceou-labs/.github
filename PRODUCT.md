# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

GitHub organization profile README (`profile/README.md`): GitHub-flavoured Markdown with sanitized HTML. No CSS or
JavaScript; visual design ships as images stored in this repository (`profile/assets/`), with `<picture>` and
`prefers-color-scheme` for light and dark themes.

## Users

Developers who use Claude Code and land on github.com/jceou-labs, usually from a link in one of the tool
repositories or from search. They are deciding in a few seconds whether these tools are worth a look, then which
one to open or install.

## Product Purpose

jceou-labs is a workshop of free, open-source tools for Claude Code, built by a practitioner for their own daily
work and shared as is. The profile page shows the four tools, what each one does, and how to install it. Success:
a visitor understands the set at a glance and opens or installs a tool.

## Positioning

Tools made for real use first, then published: each one solves a problem met while working with Claude Code every
day (context filling up, long work drifting, tracking several projects, needing images without a paid API).

## Operating Context

Seen on GitHub's organization page, in light or dark theme, on desktop and phone. The README sits in GitHub's own
layout, next to its sidebar (People, Repositories) and above the pinned repositories.

## Capabilities and Constraints

- Four tools, all MIT: `claude-context` (context gauge mod, plugin `context-claude`), `claude-workflow-skills` (nine skills, plugin
  `workflow-skills`), `claude-project-tracker` (offline tracking pages), `claude-local-images` (local image
  generation, plugin `local-images`).
- Install lines: `/plugin install <plugin> --marketplace jceou-labs/<repo>`; the tracker is downloaded and installed
  by asking Claude to follow its INSTALL.md.
- `claude-local-images` is tested on Windows with NVIDIA only so far.

## Brand Commitments

- Name: jceou-labs. No logo, palette or typeface existed before this page (the previous avatar was GitHub's default).
- Tone: sober and concrete, a workshop rather than a company. No personal name, employer or private detail.

## Evidence on Hand

- Real screenshots and images in the tool repositories: `claude-context/docs/band.png`,
  `claude-project-tracker/docs/{project,overview}.png`, `claude-local-images/docs/*.jpg`.
- No users, stars, testimonials or adoption figures yet: none may be claimed.

## Product Principles

1. Show the real tool, not a promise: screenshots and actual install lines.
2. Each tool stands alone; the set is a bonus, never a requirement.
3. Plain words over marketing; nothing claimed that has not been tested.
