# Provider and build contract

Use for deterministic Create builds in the full distribution.

## Provider boundary

A provider receives a validated DeckSpec, RenderPlan, template, manifest, and a
new private job directory. It writes only a staged candidate and a bound result;
it never decides release eligibility or overwrites a delivery file.

The provider result must identify interface/provider/engine versions and bind
the input hashes, candidate hash, slide count, actual layouts, physical slide
lineage, element dispositions, warnings, and errors. Unsupported capability is
an explicit result, never a silent fallback.

The publishable Codex provider must use the installed Presentations skill's
supported `@oai/artifact-tool` authoring/finalization path. The current toolchain
does not reliably preserve the template's two embedded think-cell/OLE payloads
on a no-op import/export. Until the owner classifies those parts as optional for
new decks or the tool preserves them, the native provider must report
`unsupported` rather than claim full template fidelity.

The recovered evaluation provider is external, hash-pinned, Create-only, and
must reject `publication_intent: publish`. Its output is always ineligible for
release while rights and provider parity remain unresolved.

## Fail-closed run contract

- Create a unique empty job directory; reject pre-existing outputs or receipts.
- Validate schemas and recompute every declared input hash before generation.
- Reject unknown layout, intent, strategy, role, or content key.
- Require expected-to-emitted slide and required-element completeness.
- Require one RenderPlan binding for every decision-critical DeckSpec item and
  verify its declared tokens in the actual emitted slide content. A plan-only
  objective or guardrail is missing content.
- Reject compilation skips, strategy exceptions, permissive fallback, stale
  gate results, artifacts older than run start, and hash/path mismatches.
- Run the provider diagnostic, the repository structural validator, platform
  finalizer/import checks, and rendered visual review as separate evidence.
- Bind every artifact into BuildManifest. An evaluation-only provider always
  sets delivery ineligible.

BuildManifest records a disposition for each requirement. Required items may
be `verified_emitted`, `missing`, or `contradicted`; the latter two are hard
blockers. Do not infer target coverage from a related baseline or from the
requirement's presence in DeckSpec.

Hard findings block. Advisory findings require recorded disposition. Never use
the recovered runtime's numeric score as an aesthetic or delivery decision.
