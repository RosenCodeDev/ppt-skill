# Companion options report

Read after the presentation and DeckSpec are stable. Capture decisions and
alternatives during planning, but defer exhaustive rendering until finalization.

A slide is substantive when visible content contributes a business message,
evidence, interpretation, recommendation, decision, implication, or action.
Content overrides structural role. Record `substantive`, `substantive_reason`,
`modified_in_task`, and `companion_coverage` for every slide. Every substantive
or modified slide uses `full`; only unchanged non-substantive slides use
`technical_notice_only`.

For every full-coverage slide, report:

1. selected layout/composition, rationale, Option 1, and meaningful alternatives
   or an explicit no-alternative status;
2. T1 and T2 separately when applicable; and
3. every meaningful text, chart, table, diagram, image, callout, number,
   footnote, source, and speaker-note element.

Untouched inherited decorations need no element options. Disclose modified,
flattened, substituted, or non-editable content. Reporting only T1 is
incomplete. Option 1 must match the final presentation and DeckSpec. Never
invent factual alternatives. Use `No meaningful alternative identified` or
`No evidence-supported alternative available` where appropriate.

Validate structured data against `schemas/options_report.schema.json`. Render
the same complete report in the final response and one file named
`[pptx-basename]-companion-options-report.md`. Long decks may use a table of
contents, never multiple report files.

Include a technical delivery notice covering template, fonts/fallbacks,
capability path, rendering, QA, native structural status, unsupported objects,
unresolved evidence, unchanged non-substantive slides and reasons, material
user deviations, and platform limits. Require chat/Markdown and Option 1/PPTX
parity before completion.
