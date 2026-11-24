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

Use Python 3.10 or newer and install the validation dependency once:

```powershell
python -m pip install -r requirements-dev.txt
```

Then validate and package:

```powershell
# Windows PowerShell
& .\scripts\validate-and-package.ps1 -PythonExecutable C:\path\to\python.exe

# PowerShell 7 on Windows, macOS, or Linux
pwsh ./scripts/validate-and-package.ps1 -PythonExecutable /path/to/python
```

The command validates both distributions and creates these ignored release artifacts in `dist/`:

- `powerpoint-skill-ai-platform.zip`
- `powerpoint-addin-skill.zip`

The command runs schema, parity, package-structure, and unit-test checks before
creating either archive. Pass `-ValidateOnly` to run the checks without writing
archives, or `-OutputDirectory` to keep generated ZIPs outside the repository.

The add-in archive targets 45 KiB, must not exceed the 47 KiB acceptance ceiling,
and has an absolute 50 KiB packaging limit.

## Rendering-provider boundary

The full skill uses DeckSpec 2.0 as its authored source of truth, derives a strict
RenderPlan 1.0, and records every build in BuildManifest 1.0. The recovered
Custom-GPT runtime is intentionally kept outside this repository and may be used
only through the local evaluation adapter in `evaluation/`. It is not part of
either installable distribution. The publishable native provider remains
fail-closed until it can preserve the protected embedded objects in the bundled
template through a supported presentation API.

## Rights and redistribution

No repository-wide license is currently provided. Do not assume that the
branded template, embedded fonts, logos, code, or other third-party materials
may be redistributed. Review the status of each material before any release;
see [`RIGHTS_INVENTORY.md`](./RIGHTS_INVENTORY.md).
