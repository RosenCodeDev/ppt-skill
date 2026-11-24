# Evidence, Quality Assurance, and Recovery

## 1. Evidence status taxonomy

Classify material claims before slide construction.

### Verified source fact

A fact explicitly supported by an accessible source.

Record:

- source identifier;
- source location where available;
- relevant date or period;
- whether the fact was independently reconciled.

### User-provided fact

A fact stated by the user or contained in user-provided material but not independently verified.

Do not silently upgrade it to independently verified status.

### Derived calculation

A result calculated from identified inputs.

Record:

- inputs;
- formula or method;
- units;
- rounding;
- assumptions.

### Assumption

A proposition adopted to proceed in the absence of complete evidence.

### Preliminary hypothesis

A testable explanation or expected conclusion that still requires validation.

### Working estimate

A provisional numerical estimate based on incomplete or directional information.

### Illustrative content

Data, examples, or structures used only to demonstrate a concept. It must not be confused with actual performance or evidence.

### Unverified claim

A claim that appears in the input but cannot be confirmed from accessible sources.

### Placeholder

A deliberately incomplete field awaiting user input or analysis.

## 2. Non-fabrication

Never fabricate:

- facts;
- numbers;
- chart data;
- sources;
- citations;
- quotations;
- dates;
- page numbers;
- client information;
- evidence-supported alternatives.

When evidence is unavailable, use a clearly labeled assumption, estimate, illustration, unverified claim, or placeholder.

## 3. PPTX-visible qualification

Place a visible label in the PPTX whenever a reader could otherwise mistake provisional material for verified fact.

Use the `OW_PROVISIONAL_LABEL` style token from the template manifest.

Common labels:

- `ASSUMPTION`;
- `PRELIMINARY HYPOTHESIS`;
- `WORKING ESTIMATE`;
- `ILLUSTRATIVE`;
- `EXAMPLE`;
- `DRAFT`;
- `SOURCE TO BE VERIFIED`.

The label must sit immediately adjacent to the qualified content. Its scope must be visually unambiguous.

Do not use a slide-level label when only one number or exhibit is provisional. Label the specific item.

## 4. Footnote, subtitle, label, or report-only notice

Use the least intrusive treatment that prevents misunderstanding.

### Use a visible label when

- the status is essential to interpreting the slide;
- the content could be mistaken for verified fact;
- the slide may circulate without the companion report.

### Use a footnote when

- the methodology or condition requires a concise explanation;
- the content is verified but needs scope, timing, or definition;
- a label alone would not explain the qualification.

### Use T2 when

- the qualification applies to the slide’s principal message;
- the scope or evidence condition belongs in the title hierarchy;
- the additional context remains concise.

### Use report-only disclosure when

- the issue is technical rather than interpretive;
- it concerns generation, rendering, fonts, or editability;
- it does not affect how a reader should understand the slide.

## 5. Companion-report evidence explanation

For each material provisional item, record:

- affected slide and element;
- evidence status;
- basis;
- reason the provisional treatment was necessary;
- potential effect on the conclusion;
- validation needed;
- visible treatment used in the PPTX.

## 6. Source and footnote discipline

Use the template source and footnote area.

Preferred order:

1. unnumbered notes;
2. numbered footnotes;
3. source.

Sources should be specific enough for the user to identify the underlying material.

Maintain consistency in:

- source naming;
- dates;
- access dates where required;
- number formats;
- units;
- terminology;
- footnote symbols.

Do not cite a source that does not support the claim.

## 7. User override register

A confirmed user override is task-scoped and belongs only to the current DeckSpec.

Each record should include:

- scope;
- user direction;
- default rule in conflict;
- likely consequence;
- alternatives offered;
- confirmation status;
- implementation decision;
- `task_scoped: true`;
- `canonical_assets_mutated: false`.

QA may detect the deviation but must classify it as `accepted_user_override` rather than automatically reversing it.

A new task begins with an empty override register.

## 8. QA architecture

Use three distinct QA categories.

### 8.1 Deterministic structural checks

These checks can be established from the file or DeckSpec without visual judgment.

Examples:

- PPTX exists and is a valid ZIP/OOXML package;
- file extension is `.pptx`;
- no VBA project or macro-enabled content remains;
- required default or user-overridden slide sequence is present;
- no delivered slide is empty;
- expected slide dimensions are used;
- template hash or manifest relationship is understood;
- expected layouts are available;
- no broken media relationships;
- no external chart-workbook links;
- chart data is embedded where intended;
- no leftover template prompts or placeholder text;
- protected fixed objects still exist;
- no unintended additional masters;
- all substantive slides have titles;
- report Option 1 values map to selected DeckSpec values;
- canonical package files were not modified.

### 8.2 Render-dependent visual checks

These require slide rendering or reliable visual inspection.

Examples:

- clipped or overflowing text;
- awkward line breaks;
- overlapping objects;
- hidden labels;
- distorted or pixelated images;
- unreadable chart labels;
- weak contrast;
- poor spacing or alignment;
- objects outside the visible slide;
- visually ambiguous label scope;
- broken custom-layout hierarchy;
- inconsistent visual density;
- font substitution that changes fit;
- legal or closing pages rendered incorrectly.

### 8.3 Judgment-based communication checks

These require consultant and design judgment.

Examples:

- governing thought is clear;
- storyline is decision-relevant;
- title strip forms a coherent argument;
- each slide has one dominant message;
- the title accurately reflects the evidence;
- the exhibit proves the message;
- the structure is close to MECE;
- counter-evidence and risks are handled credibly;
- executive summary reconciles with the detailed slides;
- no filler or repeated slide exists;
- layout and density are appropriate for the audience and use case;
- recommendations follow from the analysis.

### 8.4 Two-pass inspection

First compare the DeckSpec with slide text, notes, sources, placeholders, relationships, expected elements, and inherited content. Then compare reliable renders with the DeckSpec for fit, overlap, wrapping, contrast, hierarchy, protected elements, and template remnants. Rerender corrections and finish with a deck-wide pass.

### 8.5 OOXML relationship invariants

Prefer host-native slide add/delete. Use raw OOXML only with immediate validation. After low-level addition or duplication, synchronize presentation order/IDs/relationships and content types; require one layout per slide and unique reciprocal notes ownership; duplicate mutable charts, media, notes, and embedded data instead of shallow-sharing them.

Require internal relationships to resolve. Block external workbooks, linked chart data/media, external OLE, and executable controls; review hyperlinks separately. Reachability may report possible orphaned slides, notes, media, charts, and embeddings but must never delete them. Preserve unknown parts unless an integrity rule prohibits them.

When available, the structural validator is read-only. It may establish package, relationship, macro, external-data, notes, layout, content-type, and manifest facts. It cannot establish rendered quality, storyline, evidence accuracy, accessibility completeness, or report parity; retain the render-dependent and judgment-based gates.

## 9. QA gates

### Gate 1 — Governing thought and storyline

Check:

- central question answered;
- supporting logic complete;
- counter-evidence considered;
- section structure coherent;
- title strip compelling;
- no filler or duplication.

### Gate 2 — Evidence and integrity

Check:

- claims supported or appropriately classified;
- assumptions and estimates labeled;
- calculations reconciled;
- sources present;
- no fabricated alternatives;
- user overrides recorded.

### Gate 3 — Slide communication

Check:

- one dominant message;
- title/body alignment;
- appropriate layout;
- readable hierarchy;
- density appropriate;
- exhibit proves the conclusion.

### Gate 4 — Template and brand

Check:

- correct template;
- correct master and layouts;
- protected elements intact;
- placeholders used correctly;
- fonts and colors consistent;
- standard pages preserved;
- custom layouts aligned to the template grid.

### Gate 5 — Technical file quality

Run available deterministic checks for:

- package validity;
- macros;
- media relationships;
- external links;
- slide identifier, order, content-type, layout, and notes-ownership invariants;
- possible orphaned parts without automatic deletion;
- layout/master integrity;
- empty slides;
- placeholder remnants;
- overflow indicators;
- unsupported objects;
- report parity.

### Gate 6 — Rendered inspection

When technically possible:

- render every slide;
- compare every rendered slide with its expected DeckSpec content and layout;
- inspect every slide at normal viewing size;
- inspect dense charts and custom layouts more closely;
- rerender corrected slides and check that fixes introduced no regressions;
- distinguish preview-renderer substitution from actual PPTX changes.

A dedicated thumbnail or slide-sorter review is not required.

## 10. Correction loop

For every failed QA item:

1. identify the specific slide, object, and failed rule;
2. determine whether the issue is accidental, an accepted user override, or an unavoidable limitation;
3. correct only the affected item when possible;
4. rerun the relevant structural checks;
5. rerender affected slides when possible;
6. repeat until fixed or the recovery hierarchy is exhausted;
7. disclose unresolved issues.

After corrections, run a final deck-wide validation.

## 11. Content-fit recovery

When content does not fit, use this order:

1. edit and simplify content;
2. reduce font size within approved limits;
3. improve the visual structure;
4. split the slide;
5. move supporting detail to the appendix.

For a title that does not fit, choose among:

- shorten T1;
- revise wording;
- use T1 + T2.

Do not reduce title font size across the deck to solve one slide.

If the user confirms a dense one-slide solution after being advised to split, implement the strongest possible one-slide version and record the override.

## 12. Layout recovery

If the ideal standard layout is unavailable:

- adapt the closest standard layout without moving its placeholders; or
- use Blank and build a custom composition aligned to the template grid.

Do not deliver a blank slide.

## 13. Unsupported-object recovery

Default order:

1. preserve unchanged;
2. rebuild safely;
3. flatten as an image;
4. warn the user;
5. ask for approval when required.

A higher-priority integrity rule overrides this order. For example:

- remove or rebuild macro-bearing content because the final deck must be macro-free;
- do not preserve an object that corrupts the file;
- do not preserve an external link that exposes inaccessible or confidential data.

Reachability analysis may identify possible orphaned parts, but it must not trigger automatic deletion. Preserve and report unknown parts unless a higher-priority integrity rule requires removal.

## 14. Images and rendering recovery

### Low-resolution image

Use it when necessary and warn the user. Do not fabricate a higher-resolution source.

### Rendering differences

Preserve the editable PPTX and notify the user about font or rendering differences.

### Missing template fonts

Use the fallback hierarchy and disclose substitutions.

### Template unavailable

Use fallback layout and font rules, create a provisional deck, and clearly warn the user.

### Unverified source

Preserve the content only with an appropriate visible qualification and report disclosure. Do not present it as verified.

## 15. Blocking errors

Stop or deliver only partial artifacts when:

- a valid PPTX cannot be created;
- the file is corrupt or triggers repair warnings that cannot be resolved;
- required facts would need to be fabricated;
- a user instruction is technically impossible and no acceptable fallback exists;
- fixed legal content cannot be preserved and the user has not accepted an alternative;
- the platform cannot access the template and the user rejects provisional fallback behavior.
- the read-only structural validator reports an unresolved blocking defect.

Disclose the exact limitation. Never claim full completion.

## 16. Options-report parity

Generate the report from the selected values and alternatives in the DeckSpec.

Required parity controls:

- Option 1 is the selected DeckSpec value;
- every full-coverage slide reports its selected layout and applicable T1/T2 separately;
- each PPTX element has a stable element identifier;
- the report references that identifier;
- the report contains every DeckSpec element identifier exactly once for each full-coverage slide;
- read back the PPTX where possible and compare current text/layout to the DeckSpec;
- record parity status as verified, partially verified, or not technically verifiable.

Do not generate report alternatives solely after construction if they were not considered or recorded in the DeckSpec.

## 17. Long-deck reporting

For more than approximately 25 substantive slides:

- create one Markdown report with a deck-level table of contents;
- organize the report with section headings;
- preserve slide identifiers throughout the file;
- include the technical delivery notice once;
- avoid repeating unchanged global rules in every section;
- include every full-coverage slide even when an element has no meaningful alternative; and
- render the same complete report in the final chat response.

## 18. Important notes

Include the optional **Important notes** section only for material information the user needs to act on or understand.

Suitable items include:

- a conclusion depends on a major assumption;
- evidence is incomplete or conflicting;
- a source could not be verified;
- an important object was flattened;
- a font substitution materially affected layout;
- scope limitations materially affect interpretation.

Keep it concise, normally three to five bullets. Omit it when unnecessary.

## 19. Changes applied

For Targeted Modify and Review and Improve, include a concise summary of material changes, such as:

- slide rewritten;
- exhibit replaced;
- slide split or combined;
- source corrected;
- layout changed;
- content preserved intentionally.

Do not turn this into a third full report.

## 20. Technical delivery notice

Always disclose:

- template used;
- fonts used;
- fallback fonts;
- capability tier;
- rendering status;
- QA categories completed;
- structural-validator or native structural-check status and unresolved findings;
- unsupported objects preserved, rebuilt, or flattened;
- unresolved evidence or data issues;
- unchanged non-substantive slides and their classification reasons;
- user-directed deviations where useful;
- platform limitations;
- report/PPTX parity status.
