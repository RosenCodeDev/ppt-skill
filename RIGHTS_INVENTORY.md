# Rights inventory

This inventory records what the repository can currently prove about origin and
redistribution. It is not a license or legal opinion. An `unverified` entry must
not be treated as permission to publish, sublicense, or redistribute the file.

| Material | Location | Current evidence | Status before redistribution |
| --- | --- | --- | --- |
| Skill instructions, schemas, validators, and packaging scripts | Repository text and source files | No repository-wide license or author grant is present | Unverified |
| PowerPoint template | `distributions/ai-platform/powerpoint-skill/assets/Corporate_Template.pptx` | Branded binary; no asset license is present | Unverified; obtain owner authorization or replace |
| Embedded Marsh Serif and Noto Sans font parts | Inside `Corporate_Template.pptx` | Font binaries are embedded; no redistribution terms are present | Unverified; confirm embedding and redistribution rights |
| Template visual assets | `Corporate_Template.pptx` and `assets/icon.svg` | No standalone asset grant is present | Unverified; confirm redistribution rights |
| Brand, writing, and formatting guidance | Skill references | No provenance or publication grant is present | Unverified |
| Recovered Deck Builder runtime 2.6.18 | External `Custom GPT` repository | SHA-256 is known; no verified reuse license is present | Evaluation-only dependency; never package here without authorization |
| Recovered 500 SVG icons | Inside the external runtime archive | Provider comments are not adequate license evidence | Do not copy or package without verified attribution and terms |
| Recovered template, fonts, and knowledge files | External `Custom GPT` repository | Migration notes identify unresolved provenance | Do not copy or package without authorization |
| Vendored `svgelements` and other runtime dependencies | External runtime archive | No complete notices bundle has been verified | Inventory and satisfy upstream terms before any vendoring |

## Release gate

No release or push that represents the repository as redistributable may occur
until each included material is either:

1. covered by documented authorization and any required notices; or
2. replaced with an independently created, publishable alternative.

The recovered runtime and its assets must remain outside this repository and
outside release archives while their status is unresolved.
