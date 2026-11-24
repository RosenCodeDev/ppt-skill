# Layouts, Exhibits, and Formatting

## 1. Template-first design

The supplied PPTX is the visual and technical source of truth.

Use:

- its masters and layouts;
- its placeholders;
- its theme fonts and colors;
- its slide dimensions;
- its fixed legal and closing pages;
- its footer, source, copyright, and page-number positions.

Do not reconstruct template elements manually when the actual layout is available.

When using a standard layout:

- populate its placeholders first;
- do not move or resize inherited placeholders;
- do not move protected non-placeholder artwork;
- use Blank instead when the intended composition is incompatible with the layout.

## 2. Standard layout decision guide

The standard layouts are the default vocabulary, not absolute restrictions.

| Layout | Primary use | Avoid when |
|---|---|---|
| Title Slide | Standard cover without dominant imagery | The cover is intentionally image-led |
| Title and Content | One dominant full-width content block | The message requires strong parallel comparison |
| Title Only | Chart-led or custom content beneath a standard title | A standard body placeholder would improve structure |
| 2 Columns | Two equal concepts, alternatives, or evidence blocks | One side is materially more important |
| 3 Columns | Three parallel categories, stages, or options | The columns require dense text or unequal emphasis |
| 4 Columns | Four concise parallel categories or stages | Each column requires substantial explanation |
| Title and Content with Heading | One content area requiring a local heading | The local heading adds no information |
| 2 Columns with Heading | Two equal blocks requiring local headings | The headings merely repeat T1/T2 |
| 2 Columns 2/3 Split | Dominant left exhibit or narrative plus supporting right commentary | The right side is equally important or needs greater width |
| 2 Columns 1/3 Split | Supporting left context plus dominant right exhibit or narrative | The left side is the dominant message |
| 3 Columns with Heading | Three parallel blocks with local headings | The slide becomes a dense card grid |
| 4 Columns with Heading | Four concise blocks with local headings | The content needs more than short, parallel statements |
| Big Photo Right | Image-led story with explanatory content on the left | The image is decorative or weakly related |
| CV - Bio with Photo | Consultant or expert biography | A general team overview is needed instead |
| One Pager Credential | Situation, approach, and impact credential | The material is not a credential or cannot be expressed in three parts |
| Section | Major section transition | The deck is short or the divider interrupts momentum |
| Title Slide with Picture | Cover with a prominent image | The image adds little value |
| Contents | Mandatory agenda or table of contents | Never omit by default |
| Confidentiality | Fixed confidentiality page | Do not repurpose |
| Qualification | Fixed qualifications page | Do not repurpose |
| Backcover | Fixed closing page | Do not repurpose |
| Blank | Custom analytical exhibit or impact composition | Never use as an empty finished slide |

## 3. Layout selection questions

Before choosing a layout, ask:

- What single message must dominate?
- What must the reader see first, second, and third?
- Are the content blocks equal or unequal in importance?
- Are headings required to distinguish parallel concepts?
- Is the slide primarily narrative, analytical, visual, or comparative?
- Does an image carry evidence or merely decoration?
- Can a standard layout communicate the message without distortion?

There is no universal “chart left, bullets right” rule.

## 4. Blank layout and custom compositions

Blank is a construction canvas, never a finished blank page.

Use it for:

- highly custom analytical exhibits;
- impact statements or large numbers;
- bespoke processes, systems, or operating models;
- layouts not supported by the standard placeholders;
- a clearly superior arrangement.

Custom layouts should be relatively rare. The standard layouts are comprehensive and should be preferred when they communicate the message well.

### Custom-grid discipline

Use the grid and anchors in `template_manifest.json`.

At minimum:

- preserve the title, footer, source, and page-number zones;
- align major objects to recurring template anchors;
- use the standard 0.5-inch gutter where applicable;
- maintain consistent margins and baselines;
- give the slide one obvious reading path;
- use whitespace deliberately;
- avoid distributing objects merely to fill the page.

### New layouts and masters

Use this hierarchy:

1. existing standard layout;
2. Blank with a custom composition;
3. new custom layout only when repeated use across several slides makes it materially beneficial;
4. additional master only when explicitly requested or genuinely required for preserved client branding.

Only create a layout or master through a stable method that can be validated. Record the reason in the DeckSpec.

Prefer native slide add/delete. Use raw OOXML only with immediate validation, and never shallow-copy relationships that could share mutable notes, charts, media, or embedded data.

## 5. Protected elements

Do not move or redesign, absent a confirmed task-specific user override:

- organization logo, if present;
- client-logo area;
- copyright;
- page number;
- footer and source area;
- footer separator line;
- fixed Confidentiality content;
- fixed Qualification content;
- Backcover artwork;
- other non-placeholder master or layout artwork.

Do not mutate the canonical template. Generate from a copy.

On a populated template slide, remove a complete unused optional group instead of clearing only its text and leaving icons, headings, or connectors. Do so only when it is slide-level, DeckSpec-unused, unprotected, uninherited, and in scope. Preserve native paragraphs, runs, bullets, and list levels elsewhere.

## 6. Visual hierarchy and reading flow

A slide should be easy to read left to right, top to bottom, or through another deliberate sequence that is immediately apparent.

Use:

- size to reflect importance;
- position to establish sequence;
- proximity to group related items;
- alignment to create order;
- contrast to direct attention;
- whitespace to establish focus;
- repetition to create consistency.

Avoid:

- changing reading direction mid-slide;
- equal visual weight for unequal messages;
- dense edge-to-edge content;
- floating objects without a shared grid;
- decorations that compete with evidence.

## 7. Font behavior

The active template governs fonts.

Current theme:

- Marsh Serif for headings and titles;
- Noto Sans for body content.

Fallback order:

1. Marsh Serif and Noto Sans;
2. Calibri for all text.

When fallbacks are used:

- keep text editable;
- do not convert text to images or outlines;
- notify the user;
- preserve theme references where possible;
- distinguish preview substitution from an actual font change in the PPTX.

Do not force font embedding through brittle methods. Preserve the template’s behavior where reliably supported.

## 8. Color behavior

Use black, white, and blue as the visual foundation.

Use accents to:

- highlight the principal insight;
- distinguish categories;
- reinforce a meaningful association;
- show positive, negative, warning, or priority status where appropriate.

Use the fewest colors needed. Multiple accents are acceptable when genuinely necessary for categorical distinction.

Avoid:

- decorative color;
- rainbow palettes;
- repeated highlights that eliminate hierarchy;
- Microsoft standard colors outside the template theme;
- color changes that have no semantic meaning.

## 9. Exhibit selection by analytical intent

Choose the simplest visual that proves the message.

### Comparison

Use ranked horizontal bars for category comparison, especially with long labels. Use columns when discrete time periods or compact category names make them clearer.

### Trend

Use lines for continuous or multi-period trends. Use columns when discrete period-to-period values are the focus.

### Composition

Use stacked bars or columns when composition must also be compared. Use pie or doughnut only rarely, for a simple static whole with few segments and no need for precise comparison.

### Distribution

Use histograms, box plots, dot plots, or ranges when the spread and outliers matter. Do not replace a distribution with an average-only chart.

### Relationship

Use scatter plots for correlation or relationship. Use bubbles only when the third magnitude is meaningful and legible.

### Bridge or waterfall

Use a waterfall for movement from a start value to an end value. Order drivers logically and reconcile the bridge.

### Scenario or option comparison

Use a table, matrix, bars, or small multiples depending on whether exact values, trade-offs, or patterns matter most.

### Flow and process

Use diagrams, swim lanes, timelines, or process flows. The visual direction must be unambiguous.

### Geography

Use a map only when location itself is analytically important. Otherwise a ranked chart is often clearer.

### Detailed values

Use a table when the audience needs exact values, the analytical process, or a detailed financial view. Use tables sparingly in the main story.

### Impact statement

Use a large number or concise statement when one quantified result or implication should dominate.

## 10. Chart construction

Every chart should:

- support the title;
- have one main takeaway;
- label units and time periods;
- explain abbreviations;
- include a source;
- use consistent number formats;
- use a meaningful order;
- annotate the important implication where useful;
- avoid misleading axes or scales;
- reconcile with underlying data.

Prefer direct labels where they reduce legend lookup.

Keep legend order, stack order, and narrative order consistent.

Remove unnecessary:

- borders;
- backgrounds;
- gridlines;
- data labels;
- decimals;
- series;
- markers;
- secondary axes.

Do not use 3D effects.

Use dual axes only when the relationship cannot be communicated more clearly another way and the scales are explicitly labeled.

## 11. Tables

Use a table when exact values or detailed comparison are essential.

A good table:

- has a clear title or heading;
- uses concise row and column labels;
- highlights only the cells that matter;
- aligns numbers consistently;
- uses consistent units and decimals;
- avoids unnecessary borders;
- groups information logically;
- remains readable at normal viewing size.

Avoid deeply nested or highly merged structures. Consider splitting or moving to the appendix when density is excessive.

## 12. Diagrams and processes

Use diagrams for relationships, operating models, processes, systems, and responsibilities.

Rules:

- one clear direction;
- consistent shape language;
- consistent line weight and connector style;
- short labels;
- no crossing connectors where avoidable;
- visual emphasis aligned to the message;
- no decorative icons that do not encode meaning.

Prefer native shapes and connectors for new diagrams when they provide better control and reliability than SmartArt.

## 13. Images and photography

Use imagery only when it adds evidence, context, emotion, or recognition.

Do not add stock photography merely to fill space.

For photographs:

- use adequate resolution;
- crop deliberately;
- preserve aspect ratio;
- avoid distortion;
- confirm copyright and permitted use;
- consider inclusion and representation.

Use Big Photo Right or Title Slide with Picture when the image is genuinely central.

## 14. Screenshots and flattened visuals

Screenshots are permitted when:

- exact interface or document fidelity matters;
- editable recreation is impractical;
- the source application is unavailable;
- reconstruction would add little value.

When used:

- crop irrelevant application chrome where appropriate;
- maintain adequate resolution;
- add a subtle drop shadow only when it helps distinguish a document screenshot from the white slide background;
- do not apply screenshot-style shadows to ordinary imagery;
- repeat or describe important text that appears only inside the image;
- add meaningful alt text where supported;
- disclose material loss of editability.

## 15. PDF-derived content

Recreate important charts, tables, and text as editable content when practical and valuable.

Retain PDF-derived imagery when:

- fidelity matters more than editability;
- the original branding or design must remain intact;
- reconstruction could introduce error;
- the effort is disproportionate to the benefit.

Maintain readability, copyright discipline, attribution, and disclosure of limited editability.

## 16. SmartArt, SVG, icons, and other objects

### SmartArt

- preserve existing SmartArt when stable;
- use it for new content only when it is reliable and suitable;
- prefer native shapes and connectors when they offer better control;
- add alt text to meaningful SmartArt where supported.

### SVG and vector assets

- prefer approved vector assets when the platform preserves them reliably;
- validate rendering and editability;
- avoid unexpected font or clipping behavior inside SVGs;
- use high-resolution raster fallback when necessary.

### Icons

- use approved internal sources where available;
- use icons only when they encode meaning;
- keep style, stroke, fill, and scale consistent;
- do not build repetitive decorative icon grids.

### OLE, embedded media, and complex objects

Preserve when safe and necessary. Rebuild only through a stable method. Flatten only after preservation and safe rebuilding fail. Disclose the treatment.

## 17. Editable charts and data

Prefer live, editable charts.

- embed relevant underlying data;
- avoid links to external workbooks;
- remove unrelated worksheets and hidden data;
- do not embed confidential calculations that are not required;
- preserve only the data needed to understand and edit the chart;
- validate that the chart opens and updates correctly.

A static chart image is a fallback, not a default.

## 18. Accessibility

Apply accessibility practices when technically possible:

- sufficient text/background contrast;
- no color-only meaning;
- caution with red/green distinctions;
- direct labels, shapes, symbols, or patterns where useful;
- meaningful alt text for charts, images, maps, and diagrams;
- mark decorative imagery as decorative where supported;
- give substantive slides unique titles;
- use clear headings;
- keep tables structurally simple;
- identify table headers;
- maintain readable text sizes and whitespace;
- repeat important information that otherwise exists only inside an image.

Alt text for a chart should communicate the main insight, not merely say “bar chart.”

## 19. Generic AI-slide patterns to avoid

Avoid:

- decorative gradients;
- glossy effects;
- unnecessary rounded cards;
- icon-in-circle repetition;
- excessive centered text;
- the same three-column layout on most slides;
- ornamental accent bars;
- stock imagery used as filler;
- excessive pills and badges;
- forced symmetry that hides priority;
- generic dashboard aesthetics unrelated to the template;
- oversized decorative numbers without analytical context;
- fake interfaces or controls that imply interactivity the PPTX does not have.
