---
name: powerpoint-addin-skill
description: Create, modify, and review executive-quality the firm presentations through the currently open PowerPoint presentation. Produce an editable macro-free PPTX plus the complete companion options report in chat and as a Markdown file.
---

# PowerPoint Add-In

Create, modify, or review an executive presentation through the currently open
PowerPoint file while preserving its template, evidence, editability,
accessibility, and technical integrity.

## Non-negotiable contract

A standard completed task has three simultaneous deliverables:

1. an editable, macro-free `.pptx`;
2. the complete companion options report in the final response; and
3. the identical report in `[pptx-basename]-companion-options-report.md`.

Never fabricate evidence, misstate completed QA, knowingly deliver corruption,
retain macros, or persist task-specific decisions into the canonical skill.
Use one fresh task-scoped DeckSpec conforming to
`schemas/deck_spec.schema.json` as the source of content, evidence, selected
layouts, alternatives, overrides, accessibility, QA, and report data.

## Platform entrypoint

Work only through the currently open PowerPoint presentation. In Create mode,
confirm that it was created from the provided template. Validate
its master, 22 layouts, slide size, theme, and protected elements against
`references/template_manifest.json` when the add-in exposes those properties.
If it does not match, ask the user to open the official template or explicitly
authorize a provisional fallback.

Do not expect bundled assets, scripts, runtime providers, or a local template.
Read `references/platform_execution.md` before changing the presentation.

## Route the task

- **Create** — read `references/mode_workflows.md#Create` and
  `references/semantic_visual_planning.md`.
- **Targeted Modify** — read
  `references/mode_workflows.md#Targeted-Modify`; preserve everything outside
  the authorized scope.
- **Review and Improve** — read
  `references/mode_workflows.md#Review-and-Improve` before changing anything.

Load detailed references only when their phase begins:

- capability choice: `references/capability_tiers.md`;
- storyline and copy: `references/storyline_and_writing.md`;
- layouts, exhibits, formatting, accessibility:
  `references/layout_exhibits_and_formatting.md`;
- evidence, QA, labels, recovery: `references/evidence_qa_and_recovery.md`;
- report construction after content freeze:
  `references/companion_options_report.md`.

## Shared workflow

1. Inspect the open presentation and supplied sources. Establish objective,
   audience, required decision/action, scope, blueprint, constraints, and gaps.
   Assign stable IDs to every decision-critical objective, numeric target,
   guardrail, decision condition, and required evidence item.
2. Build the evidence ledger and governing thought. Stress-test the argument.
3. Build a coherent answer-first storyline and title strip.
4. Raise blueprint conflicts once and record confirmed task-scoped overrides.
5. Create and validate DeckSpec before implementation. Capture alternatives as
   choices are made. Map each decision-critical item to a required slide
   element; a planning note alone is not coverage.
6. Use native layouts, placeholders, text, charts, tables, diagrams, notes, and
   accessibility features. Use Blank only for a justified custom composition.
7. Label provisional content visibly where a reader could mistake it for fact.
8. Use two QA passes: compare DeckSpec with the actual presentation, then
   inspect rendered slides for visual and communication defects.
9. Freeze the deck, then generate both exhaustive report renderings from the
   final DeckSpec.

## PowerPoint preservation and QA

Through PowerPoint, check slide order and IDs, masters, layouts, notes, macros,
links, embedded data, protected elements, placeholders, and unsupported
objects. Never auto-delete an unknown or possible orphan part. Preserve before
rebuilding; rebuild before flattening; disclose unavoidable degradation.

In Targeted Modify, do not normalize unrelated slides or shared masters. In
Review, inventory what works before changing it. Review mode without an
explicit improvement request remains read-only.

Structural integrity, missing required content, concrete overflow/collision,
broken assets, macros, and corruption are blockers. Subjective style, title,
voice, or density suggestions are advisory unless they expose a concrete
defect. Render and inspect every final slide; do not treat schema validation as
visual QA.
Reconcile the actual PowerPoint text, charts, tables, and labels to the
decision-critical requirement list. A missing or contradicted target or
guardrail is a hard blocker even when it appears in DeckSpec or speaker notes.

## Reporting and completion

Every slide records `substantive`, `substantive_reason`, `modified_in_task`, and
`companion_coverage`. Substantive or modified slides receive full report
coverage. Option 1 always equals the delivered PPTX. Reporting only T1 is
incomplete.

After validation, read `references/companion_options_report.md`. Do not claim
normal completion until the deck opens, is macro-free, applicable QA is
complete, report parity is checked, and all three deliverables are present. If
a valid PPTX cannot be produced, provide DeckSpec and both complete reports,
state that the PPTX is missing, and mark the task incomplete.
