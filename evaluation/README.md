# Evaluation-only provider

`recovered_runtime_provider.py` bridges to the separately stored recovered Deck
Builder runtime for controlled local comparisons. It does not grant rights to
the external materials, copy them into this repository, or produce a
release-eligible artifact.

The caller supplies the external skill directory explicitly and uses a new
empty job directory outside the repository. The provider verifies hashes,
denies unverified layouts, forces the planned layout, rejects silent drops and
skipped hard gates, runs the repository validator, and emits an ineligible
BuildManifest.

Never include this folder in either installable distribution or release ZIP.
