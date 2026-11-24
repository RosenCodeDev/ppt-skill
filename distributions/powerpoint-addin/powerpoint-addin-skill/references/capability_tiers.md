# Capability Tiers

Select the highest tier that is both available and reliable. Do not choose a brittle path merely because it offers more theoretical control.

## Tier 1 — Text-only reasoning

### Typical capabilities

- read text and some uploaded content;
- develop a storyline;
- create a DeckSpec;
- create the options report;
- provide implementation instructions.

### Limitations

- cannot create or validate a binary PPTX;
- cannot inspect the supplied Slide Master;
- cannot guarantee template fidelity;
- cannot render slides;
- cannot verify overflow, overlap, or file integrity.

### Required behavior

- complete the reasoning, DeckSpec, and options report;
- state clearly that the required PPTX was not produced;
- never imply that file generation or visual QA occurred;
- do not provide an untested compiler script merely to appear more capable.

The task remains incomplete because the primary deliverable is missing.

## Tier 2 — Native presentation-generation platform

### Typical capabilities

- generate or edit a PPTX through built-in platform tools;
- use an uploaded template as a visual base;
- create text, shapes, charts, and images;
- export a presentation.

### Possible limitations

- incomplete access to raw master/layout metadata;
- inability to instantiate layouts by exact name;
- automatic theme substitution or auto-design behavior;
- limited read-back of the generated PPTX;
- limited rendering or object-level QA;
- uncertain editability of generated charts and diagrams.

### Required behavior

- use the uploaded template rather than a generic theme;
- disable or avoid auto-design behavior where possible;
- map each intended layout to the closest available native layout;
- use generic fallbacks recorded in the template manifest when exact layout instantiation is unavailable;
- preserve editable text and objects where the platform supports them;
- disclose any layout, font, rendering, or editability uncertainty;
- perform all QA that the platform can substantiate.

Do not claim exact template fidelity when the platform cannot verify it.

## Tier 3 — Programmatic PPTX generation

### Typical capabilities

- inspect the PPTX package;
- enumerate masters, layouts, placeholders, and theme resources;
- add slides using specific layouts;
- create native editable objects;
- inspect relationships and embedded data;
- run deterministic validation;
- render through an available compatible renderer.

### Required behavior

- validate the template against the manifest hash or regenerate the manifest;
- use exact layout names where supported;
- populate placeholders before adding manual objects;
- preserve non-placeholder master and layout artwork;
- keep charts editable with relevant embedded data;
- avoid external workbook links;
- validate the final OOXML/ZIP package;
- confirm that no VBA project remains;
- render every slide when a reliable renderer exists;
- distinguish PowerPoint-native rendering from third-party preview rendering.

### Risks to manage

- text autofit differences across renderers;
- loss of run-level formatting during text replacement;
- incomplete SmartArt or OLE support;
- SVG/EMF conversion differences;
- chart-feature loss;
- theme-color drift from literal RGB assignments;
- master duplication when importing slides;
- fonts available in the file but not in the rendering environment.

## Tier 4 — Desktop PowerPoint automation

### Typical capabilities

- use the PowerPoint object model;
- instantiate actual layouts;
- access PowerPoint’s rendering, text fitting, and chart engine;
- update or inspect complex native objects;
- run VBA or other automation during generation;
- open, save, and re-open the final deck in PowerPoint.

### Required behavior

- prefer PowerPoint-native operations when they are more stable than low-level package editing;
- use macros only during generation when justified;
- remove all macros and save the final output as `.pptx`;
- test that the final file opens without repair prompts;
- avoid leaving external links, automation hooks, or hidden macro content;
- validate that task automation did not mutate the canonical template asset.

### Risks to manage

- platform dependence;
- Office security policies;
- automation timeouts or modal dialogs;
- different behavior between Windows, Mac, and web versions;
- accidental saving over the canonical template;
- brittle reliance on add-ins that are not available to the user.

## Capability declaration

Record the chosen tier in the DeckSpec and final technical delivery notice.

For each major QA category, record one of:

- completed;
- partially completed;
- skipped — capability unavailable;
- failed — unresolved issue disclosed.

At Tier 2, run available native structural checks and mark unavailable package/render checks skipped. At Tier 3 or 4, run the read-only validator when available; block on failures and inspect warnings natively or visually. Deterministic validation never replaces rendered or judgment-based QA.

## Reliability rule

Use this priority:

1. a stable method that preserves template fidelity and editability;
2. a stable method with disclosed limitations;
3. a more capable but brittle method only when necessary and testable;
4. stop rather than create a corrupt or falsely represented deliverable.
