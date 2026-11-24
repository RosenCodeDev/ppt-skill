# Mode workflows

Read only the mode selected for the current task.

## Create

Use when no completed deck exists.

1. Establish the objective, audience, decision or action, presentation mode,
   source boundaries, image policy, and material constraints. Extract a
   decision-critical requirement register with stable IDs for objectives,
   numeric targets, guardrails, decision conditions, constraints, and required
   evidence. Ask only for missing information that changes the result.
2. Build the evidence ledger, governing thought, supporting argument, title
   strip, and appendix boundary.
3. Create a semantic visual plan for every substantive slide before selecting
   detailed layouts. Bind each required register item to a slide and element
   that visibly carries it. Reserve the strongest visual treatment for
   argument anchors and decision pages.
4. Apply the default structural sequence unless the user confirms another:
   Title, Confidentiality, Contents, content/sections/recommendation/next steps,
   Qualification, Backcover. Section slides are optional.
5. Build through the reliable provider selected for the environment. For a
   deterministic full-skill build, validate DeckSpec, RenderPlan, provider
   result, BuildManifest, final PPTX, and report parity.
6. Classify every delivered slide and complete both QA passes before report
   rendering. Reconcile the requirement register to actual emitted content;
   planning-only coverage fails.

## Targeted Modify

Use when a deck exists and the user identifies specific changes. If scope is
unclear, ask once whether only the named changes or broader improvements are
authorized.

- Work on a copy and snapshot slide order, IDs, layouts, masters, theme, notes,
  hyperlinks, relationships, media, embeddings, unsupported objects, and
  protected shapes before editing.
- Initialize every slide with `modified_in_task: false`; mark only slides that
  actually change.
- Preserve unrelated wording, formatting, geometry, notes, order, inheritance,
  and package parts as closely as the platform supports.
- Do not normalize the whole deck, master, theme, or typography for a local
  edit. Suggestions outside scope belong only in the report as
  `Suggested only — not applied to the PPTX`.
- Treat an added or materially recomposed slide as a small Create task while
  matching the existing deck.
- If an edit cannot be isolated safely, explain the consequence and obtain
  confirmation before broadening scope.
- QA the touched slides and likely side effects, then run final deck-wide
  structural validation. All substantive slides still receive full report
  coverage even when unchanged.

## Review and Improve

Use when the user requests general improvement of an existing deck.

- Inventory what already works and what should remain before changing content.
- Improvement authority applies across the deck but does not authorize new
  facts, silent blueprint changes, brand replacement, fixed-artwork changes, or
  stylistic churn without material benefit.
- Reorder, rewrite, or recompose only when it improves the governing argument,
  usability, evidence integrity, or audience decision.
- Raise material message, sequence, evidence, or blueprint changes at the
  consolidated pre-build alignment checkpoint.
- Preserve unsupported objects whenever safe. Follow the recovery order:
  preserve, rebuild, flatten with disclosure, warn, then stop when integrity
  cannot be maintained.
- Run whole-deck communication, evidence, visual, accessibility, and structural
  QA. Include a concise `Changes applied` section in the report.

If the request is review-only rather than review-and-improve, do not write to
the presentation.
