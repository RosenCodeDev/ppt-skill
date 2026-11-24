---
name: powerpoint-skill
description: Create, modify, and review executive-quality PowerPoint presentations using the bundled template. Produce an editable macro-free PPTX plus the complete companion options report in chat and as a Markdown file.
---

# PowerPoint

Create, modify, or review an executive presentation while preserving the
template, evidence, editability, accessibility, and delivery integrity.

## Non-negotiable contract

A standard completed task has three simultaneous deliverables:

1. an editable, macro-free `.pptx`;
2. the complete companion options report in the final response; and
3. the identical report in `[pptx-basename]-companion-options-report.md`.

Never fabricate evidence, present an assumption as fact, claim an unperformed
check, knowingly deliver corruption, retain macros, or write task-specific
decisions into this skill. Confirmed user direction governs within those
integrity limits. The canonical skill, template, manifest, schemas, references,
and reusable defaults are immutable during an ordinary deck task.

Use one fresh task-scoped DeckSpec conforming to
`schemas/deck_spec.schema.json`. It remains the public source of authored
content, evidence, layouts, alternatives, overrides, accessibility, QA, and
report data. Do not add renderer-specific fields to DeckSpec.

## Start from the bundled template

Work from a copy of `assets/Corporate_Template.pptx`. Never overwrite the canonical
file. Verify its SHA-256 and structure against
`references/template_manifest.json`. The 22 layouts are available vocabulary,
not a quota. Use a layout only when it communicates the content well.

For local Codex PPTX work, follow the installed Presentations skill and its
supported JavaScript `@oai/artifact-tool` finalization workflow. Do not use
`python-pptx` or raw OOXML as the publishable authoring path. The recovered
Python renderer is an external, evaluation-only provider and may not enter a
release package or make a build eligible for publication.

Read `references/platform_execution.md` before authoring or changing a PPTX.

## Route the task

Choose exactly one mode:

- **Create** — no completed deck exists. Read
  `references/mode_workflows.md#Create`, then
  `references/semantic_visual_planning.md`.
- **Targeted Modify** — the user identifies specific edits. Read
  `references/mode_workflows.md#Targeted-Modify` and preserve everything
  outside the authorized scope.
- **Review and Improve** — the user requests general improvement. Read
  `references/mode_workflows.md#Review-and-Improve` before changing anything.

Always read `references/capability_tiers.md` and select the highest reliable
execution tier. Load other guidance only when its phase begins:

- storyline, titles, and copy: `references/storyline_and_writing.md`;
- layouts, exhibits, formatting, and accessibility:
  `references/layout_exhibits_and_formatting.md`;
- evidence, provisional labels, QA, and recovery:
  `references/evidence_qa_and_recovery.md`;
- small quality examples, only when useful: `references/style_examples.md`;
- provider and build contracts for deterministic Create:
  `references/provider_interface.md`;
- exhaustive report rendering, only after the PPTX content is stable:
  `references/companion_options_report.md`.

## Shared workflow

1. Inspect supplied material completely. Infer the objective, audience,
   decision or action, presentation mode, scope, user blueprint, constraints,
   required evidence, and real information gaps. Assign stable IDs to every
   decision-critical objective, target, guardrail, decision, and constraint.
2. Classify material claims in the evidence ledger. Keep verified facts,
   user-provided facts, calculations, assumptions, hypotheses, estimates,
   illustrative content, unverified claims, and placeholders distinct.
3. Define the governing thought and minimum supporting argument. Test
   counter-evidence, alternative explanations, vulnerable assumptions, and
   decision risk.
4. Build an answer-first storyline and coherent title strip. Remove filler and
   duplication. Separate the main argument from appendix detail.
5. Respect a user blueprint. Treat instructions as Locked, Preferred, Open, or
   Unspecified. Raise material conflicts once in a concise pre-build alignment
   checkpoint and record confirmed choices as task-scoped overrides.
6. Create and validate DeckSpec before implementation. Record selected values
   and meaningful alternatives while decisions are made, not from memory. Map
   every decision-critical requirement to a required slide element; merely
   recording it in DeckSpec does not count as coverage.
7. Construct the deck through the selected platform path. Populate native
   layouts and placeholders before using a justified custom composition.
8. Label provisional content visibly when a reader could mistake it for fact.
9. Run deterministic structural QA and rendered visual/communication QA. Fix
   affected items and repeat until the checks pass or recovery is exhausted.
10. Freeze PPTX and DeckSpec, then load the report reference and produce both
    complete report renderings from the same final records.

## Deterministic Create contract

For a provider-backed Create build, derive RenderPlan 1.0 conforming to
`schemas/render_plan.schema.json`. It binds each DeckSpec slide and required
element to an exact layout, semantic role, exhibit strategy, content key,
placeholder/group binding, and overflow policy. Unknown layouts, strategies,
or content keys fail rather than silently falling back.

Every run uses a new clean job directory and emits BuildManifest 1.0 conforming
to `schemas/build_manifest.schema.json`. The manifest binds DeckSpec,
RenderPlan, template, provider, PPTX, gate, validator, and render artifacts by
hash; maps logical slides to physical slides; and records every required
element as emitted, substituted, dropped, or failed.

RenderPlan must bind every `required_in_deck` decision-critical requirement to
an exact slide, required element, planned representation, and verification
tokens. BuildManifest must reconcile those bindings against actual emitted
slide content. A missing or contradicted requirement is a hard blocker even
when the storyline otherwise looks complete.

The recovered evaluation provider:

- is permitted only for `publication_intent: evaluate`;
- remains external and is selected with an explicit path and pinned hash;
- starts with only verified shared layouts eligible;
- must deny unknown and unsafe heading layouts;
- may enable a heading layout only after grouped heading/body bindings pass
  compatibility tests; and
- always produces `delivery.status: ineligible`.

## QA and delivery gate

Run `python scripts/validate_pptx.py <pptx> --format json` as an additional
read-only structural check when the environment has a working Python
interpreter. The validator resolves the packaged template manifest itself.

A build is blocked by a compiler or renderer exception, skipped required
check, stale or malformed artifact, hash mismatch, missing slide or element,
unexpected layout substitution, dropped required content, macro, corruption,
broken relationship or asset, concrete overflow/collision, failed openability,
or DeckSpec/report/PPTX disagreement.
Treat an objective, numeric target, guardrail, decision condition, or required
evidence item that appears only in planning records—but not in the actual
slides—as missing required content. Verify the delivered PPTX, not intent.

Subjective design, title, voice, density, and minor grid warnings are advisory
unless they reveal a concrete defect. Review and record their disposition; do
not let a numeric aesthetic score determine delivery.

Render every final slide. Inspect individual slides at full size and use a
contact sheet only for flow and consistency. Check clipping, overlap, hierarchy,
font substitution, charts, images, spacing, protected content, and unresolved
placeholders. Never claim PowerPoint inspection unless it actually occurred.

## Reporting and completion

Classify every slide with `substantive`, `substantive_reason`,
`modified_in_task`, and `companion_coverage`. Every substantive or modified
slide receives full coverage. Option 1 must equal the delivered PPTX.

After validation, read `references/companion_options_report.md` and generate the
complete report. Reporting only T1 or another single element is incomplete.

Do not claim normal completion until the PPTX exists and opens, is macro-free,
applicable QA is complete, report parity is checked, and all three deliverables
are present. If a valid PPTX cannot be produced, provide DeckSpec and both
complete reports, state that the PPTX is missing, and mark the task incomplete.
