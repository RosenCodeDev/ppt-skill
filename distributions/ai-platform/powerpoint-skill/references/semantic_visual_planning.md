# Semantic visual planning

Use for Create and for any materially added or recomposed slide. Decide what a
slide must communicate before selecting a layout.

For every substantive slide, record in RenderPlan or the task working record:

- communication job and supported assertion;
- semantic relationship in the evidence;
- primary visual carrier;
- intended reading order and emphasis hierarchy;
- audience/decision-moment density;
- whether the slide anchors the argument;
- standard-layout fit or custom-composition rationale;
- editability, accessibility, evidence, and fallback treatment.

## Bind decision-critical requirements

Before layout selection, extract every objective, numeric target, guardrail,
decision condition, hard constraint, and explicitly required evidence item.
Give each a stable requirement ID. In DeckSpec, map each required item to at
least one target slide and element. In RenderPlan, bind it to the required
element, its planned representation, and short verification tokens that must be
visible in the emitted slide.

Verify the actual final PPTX—not merely DeckSpec, notes, or authoring source.
A historical baseline does not cover a future target; an implication does not
cover an explicit guardrail. Missing or contradicted required items block the
build. Prefer concise consolidation (for example, a KPI guardrail row or
decision-condition strip) over adding a low-value slide.

Useful relationships include parallel categories, ordered progression,
calendar sequence, quantitative comparison, change from baseline,
part-to-whole, distribution, correlation, hierarchy, ownership, geography,
trade-off/prioritization, and cause/effect.

## Choose the visual carrier

- Use a chart when a quantitative relationship is the message. Use a table
  when exact values or row/column lookup matter more than the pattern.
- Use a waterfall for explained change, a timeline for dated sequence, a
  process for ordered actions, a hierarchy for reporting or ownership, and a
  matrix only when both axes have real meaning.
- Use a map only when location changes the conclusion. Use a large number only
  when that number is the point, not decoration.
- Use images for context, evidence, or human relevance. Do not fill empty space
  with generic stock imagery.
- Keep required charts, tables, and diagrams editable. Decorative visuals must
  follow the active presentation tool's rules.

Prefer one clear canvas composition over a dashboard of repeated cards. Use
parallel structure where items are comparable, but vary layouts when the
narrative relationship changes. Preserve deliberate whitespace. Executive
decision pages usually need lower density than analysis or appendix pages.

## Layout selection

Map the plan to the 22 template layouts only after the relationship and carrier
are clear. Prefer native placeholders without moving or resizing them. Use
Blank only when no standard layout communicates the message without
distortion. A custom composition must follow the manifest grid and retain
title/footer/protected areas.

Heading layouts contain paired heading/body groups; they are not twice as many
independent content slots. A provider may select one only when its manifest
bindings model those groups and its compatibility tests pass. Unknown layouts
or unsupported placeholder roles fail closed.

Before rendering, estimate text, table, and item capacity. First simplify;
then restructure; split with stable slide lineage when evidence cannot fit.
Never hide content loss by shrinking below the template's readable range.

## Writing and design diagnostics

Use direct, specific language. Analytical slides may use a supported finding as
the title; setup, definition, process, and navigation slides may use a plain
topic title. Do not use word count as a proxy for title quality.

Treat voice, density, grid, and aesthetic rules as advisory unless they reveal
overflow, illegibility, unsupported claims, or another concrete defect.
