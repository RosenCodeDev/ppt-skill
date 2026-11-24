# Companion options report

Read after PPTX content and DeckSpec are stable. Capture selected values and
alternatives throughout planning, but do not load or render the exhaustive
report while designing slides.

## Coverage classification

A slide is substantive when visible content communicates a business message,
evidence, interpretation, recommendation, decision, implication, or action. If
removing it removes part of the argument or decision support, it is
substantive. Content overrides structural role.

Basic covers, confidentiality, agenda-only contents, message-free dividers,
fixed qualification pages, and backcovers are normally non-substantive.
Analytical appendices, message-bearing dividers, or covers/contents containing
a conclusion remain substantive.

Record `substantive`, `substantive_reason`, `modified_in_task`, and
`companion_coverage` for every slide. Use `full` for every substantive or
modified slide. Use `technical_notice_only` only for unchanged,
non-substantive slides.

## Full-coverage slide requirements

For each full-coverage slide, report:

1. selected layout/composition, rationale, Option 1 used, and meaningful
   alternatives or an explicit no-alternative status;
2. T1 and T2 separately when applicable; and
3. every meaningful element, including headings, body text, bullets, charts,
   tables, diagrams, processes, maps, images, callouts, large numbers,
   footnotes, sources, and meaningful speaker notes.

Untouched inherited master decorations and protected fixed artwork do not need
element-level options. Disclose every modified, flattened, substituted, or
non-editable item. Reporting only T1, the title, or another single element is
incomplete.

For each element:

- Option 1 must match the delivered PPTX and the selected DeckSpec value.
- Include alternatives only when they are genuinely useful and already
  recorded in DeckSpec.
- Never invent alternative facts, figures, sources, quotations, or evidence.
- Use `No meaningful alternative identified` when variation adds no value.
- Use `No evidence-supported alternative available` when factual variation is
  unsupported.

## Rendering and parity

Generate structured options data conforming to
`schemas/options_report.schema.json`, then render the same complete report:

- in the final chat response; and
- in one Markdown file named
  `[pptx-basename]-companion-options-report.md`.

For long decks, add a table of contents and organize the single file by
section. Never split the report into multiple files. Generate from final
DeckSpec and, when used, reconcile against RenderPlan and BuildManifest first.

The report must include a technical delivery notice covering template, fonts
and fallbacks, capability/provider path, rendering performed, QA categories,
native structural status, unsupported objects, unresolved evidence, unchanged
non-substantive slides and reasons, material user-directed deviations, and
platform limitations.

Include `Important notes` only for material assumptions or limitations.
Modification work should include `Changes applied`; confirmed deviations may
appear under `User-directed decisions`.

Completion requires exact chat/Markdown parity and Option 1/PPTX parity.
