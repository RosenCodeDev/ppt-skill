# PowerPoint Skills

This repository contains two separately installable distributions of the PowerPoint skill. They share the same consulting, writing, layout, evidence, and QA guidance, but acquire the PowerPoint template differently.

> **Do not install the repository root as a skill.** Choose exactly one distribution below and install only that folder or its corresponding ZIP archive.

## Choose the correct distribution

| Where the skill will run | Install this distribution | Template behavior |
|---|---|---|
| ChatGPT or Claude web/desktop, Codex, Claude Code, or another file-capable AI platform | [`distributions/ai-platform/powerpoint-skill`](./distributions/ai-platform/powerpoint-skill/) | Uses the bundled `assets/Corporate_Template.pptx` |
| PowerPoint software add-in | [`distributions/powerpoint-addin/powerpoint-addin-skill`](./distributions/powerpoint-addin/powerpoint-addin-skill/) | Uses the template and Slide Master of the currently open presentation |

The packages have distinct skill names so an installer or AI can identify the intended target unambiguously:

- `powerpoint-skill` — AI-platform distribution
- `powerpoint-addin-skill` — PowerPoint add-in distribution

See [INSTALL.md](./INSTALL.md) for installation and packaging instructions.

## Repository layout

```text
distributions/
├── ai-platform/
│   └── powerpoint-skill/
└── powerpoint-addin/
    └── powerpoint-addin-skill/
scripts/
├── validate-and-package.ps1
└── validate-json.py
```

## Validate and build release archives

Install the validation dependency once:

```powershell
python -m pip install -r requirements-dev.txt
```

Then validate and package:

```powershell
# Windows PowerShell
& .\scripts\validate-and-package.ps1

# PowerShell 7 on Windows, macOS, or Linux
pwsh ./scripts/validate-and-package.ps1
```

The command validates both distributions and creates these ignored release artifacts in `dist/`:

- `powerpoint-skill-ai-platform.zip`
- `powerpoint-addin-skill.zip`

The add-in archive is kept below 50 KB to prevent accidental size regressions.

## License

MIT — free to use, fork, and adapt.
