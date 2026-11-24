# AI-platform execution

Use the bundled `assets/Corporate_Template.pptx` as a read-only source and build in a
separate task workspace.

For Codex creation/editing, follow the installed Presentations skill: resolve
the bundled workspace dependencies, use JavaScript ES modules with
`@oai/artifact-tool`, mark the artifact operation exactly once, export a draft,
run `finalizePresentation`, render every final slide, and inspect it. Do not
install substitute runtimes or use `python-pptx` as the publishable path.

Preserve the 16:9 canvas, master/layout family, theme, protected shapes, notes,
and required embedded data. Artifact Tool currently drops the template's two
embedded OLE/think-cell parts during a no-op round trip and cannot decode the
embedded OpenType font payloads. Treat that as a publishable-provider blocker
until the asset owner authorizes omission for new decks or the platform
preserves them. Record installed font/fallback behavior and inspect renders.

The root-level evaluation provider may call the recovered Python runtime only
for local comparison. It must remain outside this skill folder and release ZIP.
