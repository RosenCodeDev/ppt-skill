---
name: powerpoint-skill
description: Create, modify, and review executive-quality PowerPoint presentations using the bundled template. Produce an editable macro-free PPTX plus the complete companion options report in chat and as a Markdown file.
---

# PowerPoint Creation Skill

## 1. Purpose

Use this skill to create, modify, or comprehensively improve executive-quality PowerPoint presentations.

The skill combines consultant-style reasoning, executive communication, template-aware PowerPoint construction, evidence discipline, editability, accessibility, and technical quality assurance.

A successful task produces three simultaneous deliverables:

1. an editable, macro-free `.pptx` file;
2. the complete companion options report rendered in the final chat response; and
3. the same complete report as `[pptx-basename]-companion-options-report.md`.

The skill is platform-agnostic. Use the most capable stable execution path available without tying the reasoning process to a specific vendor, language, or library.

## 2. Normative language

- **MUST** and **MUST NOT** are non-negotiable.
- **SHOULD** and **SHOULD NOT** are strong defaults that may be overridden by an informed, task-specific user decision.
- **MAY** indicates judgment or optional behavior.

## 3. Canonical package and immutability

The canonical package is:

```text
powerpoint-skill/
├── SKILL.md
├── assets/
│   └── Corporate_Template.pptx
├── references/
│   ├── capability_tiers.md
│   ├── storyline_and_writing.md
│   ├── layout_exhibits_and_formatting.md
│   ├── evidence_qa_and_recovery.md
│   ├── style_examples.md
│   └── template_manifest.json
├── schemas/
│   ├── deck_spec.schema.json
│   └── options_report.schema.json
└── examples/
    ├── deck_spec_example.json
    └── options_report_example.json
```

The full package also includes the read-only `scripts/validate_pptx.py` structural validator.

During a deck task, the canonical skill and reusable assets are immutable.

The agent MUST NOT modify, rewrite, patch, learn into, or persist task-specific information in:

- `SKILL.md`;
- the canonical PowerPoint template;
- the template manifest;
- either schema;
- reference guidance;
- reusable style tokens; or
- future default behavior.

User instructions, overrides, terminology, client information, assumptions, alternatives, QA results, and accepted deviations apply only to the current task instance. A new deck or conversation starts with a clean DeckSpec and an empty override register.

Permanent changes are allowed only when the user explicitly initiates a separate skill-maintenance task.

## 4. Authority hierarchy

Apply this order when instructions conflict:

1. explicit, confirmed user instructions for the current task;
2. the supplied PowerPoint template for visual and technical formatting;
3. confirmed presentation standards encoded in this skill;
4. the default judgment rules in the reference files;
5. expert implementation defaults where no formal rule exists.

A user may override presentation, branding, storyline, layout, or formatting defaults after the agent explains any material consequence and receives confirmation.

The following integrity rules remain non-overridable:

- never fabricate facts, data, sources, quotations, or evidence;
- never misrepresent an assumption as verified fact;
- never claim a PPTX, rendering, or QA step was completed when it was not;
- never knowingly deliver a corrupt file as valid;
- the final standard deliverable is macro-free `.pptx`;
- task-specific decisions must never alter the canonical skill or future tasks.

## 5. Required deliverables

### 5.1 Primary deliverable

The primary deliverable is an editable, macro-free `.pptx` based on `assets/Corporate_Template.pptx`.

The deck SHOULD:

- use the real Slide Master layouts;
- inherit theme fonts and colors;
- preserve protected elements;
- keep newly created text and visuals editable wherever practical;
- contain no empty delivered slide; and
- pass the applicable QA gates.

Macros, VBA, desktop automation, Python, JavaScript, Open XML, or other code MAY be used during generation when that path is stable and reliable. No executable macro may remain in the final PPTX.

### 5.2 Mandatory companion options report

Classify every slide before generating the report. A slide is **substantive** when its visible content communicates a business message, evidence, interpretation, recommendation, decision, implication, or action. If removing the slide would remove part of the deck's argument or decision support, the slide is substantive.

A slide is **non-substantive** only when it serves navigation, branding, legal or administrative wording, or visual separation without contributing business content. Content overrides structural role:

- content, executive-summary, recommendation, next-step, and analytical or evidentiary appendix slides are normally substantive;
- a basic cover, confidentiality slide, agenda-only contents slide, message-free section divider, fixed qualification slide, and backcover are normally non-substantive;
- an analytical appendix or message-bearing section divider is substantive; and
- a cover or contents slide carrying a business conclusion, evidence, or decision support is substantive.

Record `substantive`, `substantive_reason`, `modified_in_task`, and `companion_coverage` for every slide. Set `companion_coverage` to `full` for every substantive slide and every slide modified in the current task. Use `technical_notice_only` only for an unchanged non-substantive slide.

For every slide with `companion_coverage: full`, the report MUST cover:

1. the selected layout and composition, rationale, Option 1 used, and meaningful alternatives or an explicit no-alternative status;
2. the title architecture, with T1 and T2 reported separately when applicable; and
3. every meaningful content or visual element, including headings, body text, bullets, charts, tables, diagrams, processes, maps, images, callouts, large numbers, footnotes, sources, and meaningful speaker notes.

Untouched inherited master decorations and protected fixed artwork do not require element-level options. Disclose any modified, flattened, or non-editable item. Reporting only T1, the title, or any other single element is incomplete.

For each element:

- **Option 1 — Used in the PPTX** MUST match the delivered file;
- provide additional options only when they are genuinely useful;
- never invent alternative facts, data, sources, quotations, or evidence;
- use `No meaningful alternative identified` when an alternative would add no value;
- use `No evidence-supported alternative available` when factual variation is unsupported.

Generate the report directly from the same DeckSpec that governs the PPTX. Do not create it as an independent recollection pass.

Render the same complete report twice: once in the final chat response and once in a single Markdown file named `[pptx-basename]-companion-options-report.md`. For long decks, organize that one file by section and add a table of contents; do not split the report across multiple files.

### 5.3 Optional and mandatory report sections

The report MUST include a technical delivery notice.

It MAY include **Important notes** only when the user needs to know material information such as a major assumption, unresolved evidence, meaningful rendering substitution, important flattened object, or scope limitation. Keep this section concise, normally no more than five bullets.

Modification tasks SHOULD also include a concise **Changes applied** section.

Confirmed user deviations MAY be summarized under **User-directed decisions** when useful.

## 6. Select the highest reliable capability tier

Read `references/capability_tiers.md` and select the highest tier the current environment can execute reliably.

Do not choose a theoretically more capable but brittle path over a stable path.

If the platform cannot create a valid PPTX, it MUST disclose that the primary deliverable was not produced and provide the DeckSpec and options report instead. It must not claim task completion.

## 7. Determine the operating mode

Choose one mode based on the user’s intent.

### Create

Use when no completed deck exists. The user may provide source files, a storyline, a slide list, draft titles, exact wording, or only an objective.

### Targeted Modify

Use when a deck exists and the user identifies specific changes.

Unless the user already made scope clear, ask once:

> Should I make only the changes you specified, or may I also apply other improvements I identify?

When scope is narrow, preserve unrelated content as closely as technically possible. Put broader suggestions in the report as **Suggested only — not applied to the PPTX**.

Adding one or more slides to an existing deck is a sub-case of Targeted Modify.

### Review and Improve

Use when a deck exists and the user requests general improvement without specifying exact changes. The agent may improve the whole deck while preserving what already works.

## 8. User Blueprint and Override Protocol

A detailed user-provided slide sequence, title list, layout plan, exhibit plan, or exact wording is a **user blueprint**. Do not silently replace it.

Classify each instruction as:

- **Locked** — preserve exactly unless the user changes it;
- **Preferred** — follow unless a material concern is raised and the user chooses otherwise;
- **Open** — agent has discretion;
- **Unspecified** — determine the best treatment.

Exact wording and explicit slide instructions are normally Preferred unless the user says they are locked.

### 8.1 Pre-build alignment

Before implementation, review the blueprint against the skill. Raise only material conflicts, such as:

- duplicated messages;
- non-MECE or incomplete logic;
- unsupported claims;
- descriptive or misleading titles;
- unsuitable exhibits;
- excessive density;
- inconsistent title architecture;
- invalid or risky template changes;
- changes outside the requested scope.

Consolidate material concerns into one concise **Pre-build alignment** checkpoint. For each concern show:

1. the user’s proposal;
2. the concern and likely consequence;
3. a recommended alternative; and
4. clear choices, including keeping the user’s proposal.

Do not require another checkpoint when the user already explicitly instructed the agent to implement the proposal despite disagreement.

### 8.2 Confirmed overrides

After confirmation, the user’s task-specific choice governs. Implement it faithfully, do not continue arguing, and do not silently restore the default rule later.

Record the decision in the current DeckSpec as a task-scoped override. QA may identify the deviation but MUST classify it as `accepted_user_override` rather than automatically correcting it.

The override record MUST include `task_scoped: true` and `canonical_assets_mutated: false`.

## 9. End-to-end workflow

### Step 1 — Inspect inputs

Read all supplied materials completely where tools permit. Extract:

- objective;
- audience and seniority;
- decision, alignment, or action required;
- presentation mode;
- desired scope;
- source facts and calculations;
- user blueprint;
- constraints and must-keep content;
- missing information.

Avoid a long intake questionnaire when the materials already answer these points. Ask a focused clarification only when the missing answer is essential.

### Step 2 — Build an evidence ledger

Classify each material claim as one of:

- verified source fact;
- user-provided fact;
- derived calculation;
- assumption;
- preliminary hypothesis;
- working estimate;
- illustrative content;
- unverified claim;
- placeholder.

Do not blur these categories. See `references/evidence_qa_and_recovery.md`.

### Step 3 — Define the governing thought

Write a one- or two-sentence answer to the central business question.

Identify the minimum set of supporting arguments and evidence needed to establish it.

Stress-test the argument:

- What supports the conclusion?
- What contradicts it?
- What alternative explanation exists?
- Which assumption is most vulnerable?
- What decision risk remains?
- Does every proposed section directly support the governing thought?

### Step 4 — Build the storyline

Create an answer-first, decision-oriented, close-to-MECE storyline.

Every substantive slide SHOULD introduce one dominant contribution to the argument. Remove filler, duplicated messages, and slides that do not change the audience's understanding or decision.

Apply the substantive-slide definition in Section 5.2. Structural role alone MUST NOT determine classification.

Draft the title strip and read it in sequence. It must form a coherent argument and connect to the executive summary.

Determine what belongs in the main story and what belongs in the appendix.

For decks with more than approximately 25 substantive slides, lock the deck-level governing thought and full title strip first, then process section by section while maintaining a central terminology, evidence, and formatting register.

### Step 5 — Create and validate the DeckSpec

Create a fresh, task-scoped DeckSpec conforming to `schemas/deck_spec.schema.json`.

The DeckSpec is the single source of truth for:

- objective and governing thought;
- mode and scope;
- user blueprint and overrides;
- slide sequence;
- selected layouts;
- slide classification, classification reason, modification status, and companion coverage;
- selected T1/T2;
- slide elements;
- meaningful alternatives;
- evidence status and sources;
- provisional labels;
- accessibility treatment;
- QA status;
- output disclosures.

Keep the DeckSpec compact. Do not duplicate template coordinates or PowerPoint XML already represented in the manifest.

### Step 6 — Initialize from the template

Use `assets/Corporate_Template.pptx` as the base and validate it against `references/template_manifest.json` when possible.

Default complete-deck sequence:

1. Title Slide or Title Slide with Picture;
2. Confidentiality;
3. Contents;
4. required content, section, recommendation, next-step, and appendix slides;
5. Qualification as the penultimate slide;
6. Backcover as the final slide.

Section slides are optional. Confidentiality, Qualification, and Backcover use their fixed layouts and should not be rewritten or redesigned.

A confirmed task-specific user override may change the default sequence, but the change must be recorded and must not alter the template or skill.

### Step 7 — Select layouts and construct slides

Read `references/layout_exhibits_and_formatting.md`.

Use the 22 standard layouts as the first-choice vocabulary. Populate existing placeholders before creating manual text boxes.

Do not move or resize inherited placeholders. If the standard geometry is unsuitable, use Blank as a starting canvas for a custom composition.

The Blank layout MUST contain meaningful visible content before delivery. Never deliver a visually empty slide.

Use the template-derived grid in the manifest for custom compositions.

Create a new custom layout only when repeated use across several slides makes it materially beneficial. Add another master only when the user explicitly requests it or preserved client-branded material genuinely requires it, and only through a stable, validated method.

Prefer host-native slide addition and deletion. Use raw OOXML only when the native route is unavailable and the result can be validated immediately. After a low-level slide addition, synchronize slide order and identifiers, presentation relationships, content types, layout ownership, notes, charts, media, and embeddings. Do not shallow-copy relationships that could unintentionally share mutable parts.

Remove an unused optional content group only when it is slide-level, confirmed unused by the DeckSpec, outside protected or inherited template content, and within the authorized modification scope. Preserve unknown parts, and never delete a part automatically merely because reachability analysis identifies it as a possible orphan.

### Step 8 — Write titles and content

Read `references/storyline_and_writing.md`.

Core title rules:

- T1 is ALL CAPS;
- T1-only is the default;
- a T1-only title must communicate the insight or “so what”;
- T1 + T2 is valid when T2 carries the insight or adds evidence, context, or qualification;
- T2 uses sentence case;
- two-line fit in the actual template governs;
- questions are permitted but not the default;
- do not reduce title font size across the deck to solve one long title.

Use bullets by default for scannable content. Three to five is typical; six is a ceiling, not a target. Prefer one bullet level and allow one sub-level only when necessary. Never use a third level.

### Step 9 — Create exhibits and editable objects

Select the simplest exhibit that proves the message.

Prefer native, editable PowerPoint text, shapes, connectors, tables, diagrams, and charts.

For charts:

- keep only relevant underlying data;
- embed data in the PPTX;
- avoid external workbook links;
- do not embed unrelated worksheets or confidential hidden data.

Use screenshots, PDF-derived images, SmartArt, SVG, or other flattened content only according to the rules in `references/layout_exhibits_and_formatting.md`.

### Step 10 — Label provisional information

When a reader could mistake provisional content for verified fact, label it in both the PPTX and the companion report.

Use the exact `OW_PROVISIONAL_LABEL` style from the template manifest:

- editable rectangular text box;
- 2.25 pt `#000F47` border;
- `#F7F3EE` fill;
- Calibri 14 pt black text;
- one line, no wrap;
- width fitted to the text;
- no decorative effects;
- immediately adjacent to the qualified content.

Common labels include `ASSUMPTION`, `PRELIMINARY HYPOTHESIS`, `WORKING ESTIMATE`, `ILLUSTRATIVE`, `EXAMPLE`, `DRAFT`, and `SOURCE TO BE VERIFIED`.

### Step 11 — Perform QA and correction

Apply the QA gates in `references/evidence_qa_and_recovery.md`.

Classify checks as:

- deterministic structural;
- render-dependent visual;
- judgment-based communication.

Use two QA passes. First compare the DeckSpec with slide text, notes, sources, relationships, placeholders, and expected elements. Then, where rendering is reliable, compare every rendered slide with the DeckSpec and inspect fit, overlap, wrapping, contrast, hierarchy, protected elements, and leftover template content.

At Tier 3 or Tier 4, run `python scripts/validate_pptx.py <deck.pptx>` before final delivery. Use `--format json` when structured results are useful. Treat a failed result as blocking; investigate warnings through PowerPoint-native or visual inspection. The validator is read-only and supplements rather than replaces rendered, evidence, accessibility, communication, and report-parity QA.

After a failed check:

1. identify the failed object or slide;
2. correct only the affected item;
3. rerun relevant structural checks;
4. rerender affected slides where possible;
5. repeat until fixed or the recovery hierarchy is exhausted;
6. disclose unresolved issues.

Run a final deck-wide validation before delivery.

Do not use schema validation as a substitute for rendered visual inspection. Use both when available.

### Step 12 — Generate the options report

Generate structured options data conforming to `schemas/options_report.schema.json`, then render the human-readable report.

Option 1 must come directly from the selected DeckSpec value. Each other option must be traceable to an actual alternative recorded in the DeckSpec.

For long decks, organize the single Markdown report by section and provide a table of contents.

### Step 13 — Deliver and disclose

Deliver all three standard deliverables at the same time:

1. the PPTX file;
2. the complete companion report in the final chat response; and
3. the same complete report as one Markdown file.

Do not provide a normal completion response unless all three are present. If the environment cannot create a valid PPTX, still provide the complete report in chat and as Markdown plus the DeckSpec, explicitly state that the PPTX is missing, and mark the task incomplete.

The technical delivery notice MUST state:

- template used;
- fonts used;
- any fallback fonts;
- capability tier used;
- whether slides were rendered;
- QA categories completed;
- structural-validator status and unresolved findings;
- unsupported objects preserved, rebuilt, or flattened;
- unresolved evidence or data issues;
- unchanged non-substantive slides and their classification reasons;
- user-directed deviations where useful;
- platform limitations.

## 10. Protected and fixed elements

Do not move or redesign the following unless the user explicitly confirms a task-specific override:

- organization logo, if present;
- client-logo area;
- copyright;
- slide number;
- footer and source area;
- footer separator line;
- fixed Confidentiality content;
- fixed Qualification content;
- Backcover artwork;
- other non-placeholder master or layout artwork.

When using a standard layout, use its placeholders without moving or resizing them.

## 11. Font and theme behavior

The active template governs fonts and styles.

Current template theme:

- heading font: Marsh Serif;
- body font: Noto Sans.

Fallback order:

1. Marsh Serif for headings and Noto Sans for body;
2. Calibri for all text when those fonts are unavailable.

When fallbacks are used, keep text editable and notify the user. Do not convert text to images or vector outlines for font compatibility.

Prefer theme inheritance over explicit formatting of every text run. Preserve the template’s embedding behavior where reliably supported; do not force embedding through brittle methods.

## 12. Recovery and stopping rules

Use the detailed recovery ladders in `references/evidence_qa_and_recovery.md`.

Key principles:

- simplify before splitting;
- preserve before rebuilding;
- rebuild before flattening;
- warn before silently degrading;
- stop rather than fabricate or knowingly corrupt the file.

When content does not fit, default order is:

1. edit and simplify;
2. reduce font size within approved limits;
3. improve visual structure;
4. split the slide;
5. move supporting detail to the appendix.

When unsupported objects exist, default order is:

1. preserve unchanged;
2. rebuild safely;
3. flatten as an image;
4. warn the user;
5. ask for approval when required.

A higher-priority integrity rule overrides preservation. For example, macro-bearing content cannot remain in the final macro-free PPTX.

## 13. Anti-patterns

Avoid generic AI-slide styling, including:

- decorative gradients;
- unnecessary rounded-card grids;
- repeated icon-in-circle motifs without analytical meaning;
- excessive centered body text;
- the same three-column composition throughout the deck;
- ornamental accent bars unrelated to hierarchy;
- stock imagery used only to fill space;
- excessive pills, badges, and floating labels;
- symmetrical layouts that weaken intended emphasis;
- dashboard styling that conflicts with the template.

## 14. Read the supporting references

Use the following focused references during execution:

- `references/capability_tiers.md` — environment and execution behavior;
- `references/storyline_and_writing.md` — governing thought, storyline, titles, bullets, and language;
- `references/layout_exhibits_and_formatting.md` — layout selection, custom grid, exhibits, formatting, editability, and accessibility;
- `references/evidence_qa_and_recovery.md` — evidence status, labels, QA, correction loops, recovery, and reporting;
- `references/style_examples.md` — small synthetic examples of the intended quality bar;
- `references/template_manifest.json` — exact template structure and style tokens.

## 15. Completion standard

The task is complete only when:

- the PPTX exists, opens, and is macro-free;
- every slide has a substantive classification, reason, modification status, and valid companion-coverage decision;
- the deck follows the confirmed user direction;
- the default or user-overridden structure is implemented;
- substantive slides have clear messages and appropriate layouts;
- provisional content is labeled correctly;
- applicable QA checks are complete;
- Option 1 in the report matches the PPTX;
- the complete report covers layout, applicable T1/T2, and every meaningful element for each full-coverage slide;
- the complete report is present both in the final chat response and in one correctly named Markdown file;
- disclosures are accurate; and
- no task-specific decision has modified the canonical skill or future behavior.
