<p align="center">
  <img src="https://raw.githubusercontent.com/jceou-labs/.github/main/profile/assets/wall.jpg" alt="A pegboard wall with a black card reading jceou-labs, Free tools for Claude Code, above four blister packs: claude-context, claude-project-tracker, claude-local-images and claude-workflow-skills, each showing the tool through its window" width="100%">
</p>

Free, open-source tools for [Claude Code](https://claude.com/claude-code), built and used day to day on real
projects. Each one works on its own.

| Tool | What it does |
|---|---|
| **[claude-context](https://github.com/jceou-labs/claude-context)** | A slim gauge above the prompt showing how close the context is to auto-compaction, with Compact and Handoff note buttons. |
| **[claude-project-tracker](https://github.com/jceou-labs/claude-project-tracker)** | Offline pages showing where each project stands (done, remaining, waiting for you), kept up to date by Claude. |
| **[claude-local-images](https://github.com/jceou-labs/claude-local-images)** | Lets Claude generate images on your own graphics card with ComfyUI and Z-Image Turbo: free, unlimited, private. Tested on Windows with an NVIDIA card so far. |
| **[claude-workflow-skills](https://github.com/jceou-labs/claude-workflow-skills)** | Nine skills that keep long work on track: plan on disk, session handoffs, adversarial review, repository sweeps, recurring friction fixed for good. |

### Install

At the prompt of a Claude Code session, one line per tool:

```
/plugin install context-claude --marketplace jceou-labs/claude-context
/plugin install local-images --marketplace jceou-labs/claude-local-images
/plugin install workflow-skills --marketplace jceou-labs/claude-workflow-skills
```

The project tracker is a folder, not a plugin: [download it](https://github.com/jceou-labs/claude-project-tracker), then ask Claude
"Install the project tracker in this folder by following INSTALL.md."

### In use

<p>
  <img src="https://raw.githubusercontent.com/jceou-labs/claude-context/main/docs/band.png" alt="The context gauge above the Claude Code prompt" width="100%">
</p>
<p>
  <img src="https://raw.githubusercontent.com/jceou-labs/claude-project-tracker/main/docs/overview.png" alt="The project tracker overview page" width="49%">
  <img src="https://raw.githubusercontent.com/jceou-labs/claude-local-images/main/docs/text-to-image.jpg" alt="An image generated locally by claude-local-images" width="49%">
</p>

All under the MIT license. Issues and suggestions are welcome on each repository.
