# Installation Guide

This repository contains two variants. Install exactly one variant for the environment where it will run.

> **Do not install the repository root as a skill.** It contains two `SKILL.md` files with different platform behavior.

## Option 1 — ChatGPT, Claude web/desktop, or another AI platform

Use the full distribution at:

```text
distributions/ai-platform/powerpoint-skill/
```

This version includes `assets/Corporate_Template.pptx` and uses that bundled file as the presentation base.

When installing conversationally from GitHub, use an explicit instruction such as:

> Install the AI-platform PowerPoint skill from `distributions/ai-platform/powerpoint-skill`. Ignore the PowerPoint add-in distribution.

For a platform that accepts custom-skill ZIP files, build the archives as described below and upload:

```text
dist/powerpoint-skill-ai-platform.zip
```

For a local agent, copy or register only the `distributions/ai-platform/powerpoint-skill` folder in that agent's skill directory.

## Option 2 — PowerPoint software add-in

Use the compact distribution at:

```text
distributions/powerpoint-addin/powerpoint-addin-skill/
```

This version does not contain a PPTX template. Before Create mode, open the official PowerPoint template in PowerPoint and save a working copy. Modify and Review modes use the currently open deck.

When installing conversationally from GitHub, use an explicit instruction such as:

> Install the PowerPoint add-in skill from `distributions/powerpoint-addin/powerpoint-addin-skill`. Ignore the AI-platform distribution.

For an add-in that accepts a ZIP file, build the archives as described below and upload:

```text
dist/powerpoint-addin-skill.zip
```

## Build and validate both archives

From the repository root, install the validation dependency once:

```powershell
python -m pip install -r requirements-dev.txt
```

Then run:

```powershell
# Windows PowerShell
& .\scripts\validate-and-package.ps1

# PowerShell 7 on Windows, macOS, or Linux
pwsh ./scripts/validate-and-package.ps1
```

The script:

- checks both skill identities and folder names;
- prevents unintended drift in shared references and schemas;
- validates the JSON schemas and DeckSpec example;
- verifies bundled-template versus open-presentation behavior;
- creates one correctly rooted skill folder in each ZIP; and
- rejects an add-in ZIP larger than 50 KB.

Generated archives are written to `dist/` and are intentionally not committed.

## Updating

Pull the latest repository revision, rebuild the archives, and reinstall the one distribution used by the target platform.
