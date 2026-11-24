# Synthetic Style Examples

These examples illustrate the intended quality bar. They are synthetic and contain no client or project content.

## 1. T1-only titles

### Weak

`CUSTOMER SEGMENTATION`

Why weak: names the topic but does not state the conclusion.

### Strong

`TWO SEGMENTS ACCOUNT FOR MOST ATTRITION AND SHOULD BE PRIORITIZED`

Why strong: makes a specific assertion and states the implication.

---

### Weak

`MARKET UPDATE`

Why weak: does not explain what changed or why it matters.

### Strong

`GROWTH HAS SHIFTED TO SMALLER MARKETS WHERE OUR COVERAGE IS WEAKEST`

Why strong: identifies the change, the gap, and the strategic relevance.

---

### Weak

`THREE REASONS TO TRANSFORM OPERATIONS`

Why weak: announces a list rather than communicating the finding.

### Strong

`FRAGMENTED OWNERSHIP AND MANUAL HANDOFFS ARE DRIVING DELAY AND REWORK`

Why strong: names the root causes and the consequence.

## 2. T1-only versus T1 + T2

### T1-only

**T1**

`LABOR AND INPUT COSTS ACCOUNT FOR MOST OF THE MARGIN DECLINE`

Use when the message fits comfortably and the exhibit supplies detail.

### T1 + T2, topic then insight

**T1**

`MARGIN PRESSURE`

**T2**

Labor and input costs account for most of the decline, while pricing offsets remain limited

Use when the concise topic provides useful hierarchy and T2 carries the full insight.

### T1 + T2, message then evidence

**T1**

`TWO COST CATEGORIES DRIVE MOST OF THE MARGIN DECLINE`

**T2**

Labor and direct materials represent 78% of the year-on-year reduction

Use when T1 states the conclusion and T2 adds quantified support.

## 3. Questions as titles

### Acceptable but not default

`WHICH INTERVENTIONS CAN DELIVER VALUE WITHIN THE NEXT 12 MONTHS?`

Use when the slide deliberately frames a decision and the following content evaluates alternatives.

### Usually stronger declarative alternative

`THREE INTERVENTIONS CAN DELIVER VALUE WITHIN 12 MONTHS`

## 4. Bullet blocks

### Weak

- Customer churn is a problem
- There are many causes of churn
- Service is also an issue
- Pricing may be high
- We should improve retention

Why weak: vague, overlapping, and not evidence-led.

### Strong

- Churn is concentrated in two high-value customer segments
- Service failures explain most exits in Segment A, while price sensitivity dominates Segment B
- Targeted service recovery and differentiated offers address the distinct causes

Why strong: parallel, specific, and logically sequenced from finding to implication.

## 5. Redundancy test

### Redundant

**T1**

`TWO SEGMENTS ACCOUNT FOR MOST ATTRITION`

**T2**

Most attrition comes from two customer segments

**Chart annotation**

Two segments drive most attrition

### Better role separation

**T1**

`TWO SEGMENTS ACCOUNT FOR MOST ATTRITION`

**T2**

Both segments are economically attractive, making retention action urgent

**Chart annotation**

Segments A and B represent 72% of annual losses

## 6. Comparison slide specification

```yaml
purpose: Compare three strategic options and recommend one
layout: 3 Columns with Heading
message: Option B offers the strongest value-risk balance
columns:
  - heading: OPTION A — SCALE
    content:
      - Highest upside
      - Highest investment
      - Longest time to value
  - heading: OPTION B — FOCUS
    content:
      - Strong near-term value
      - Moderate investment
      - Manageable execution risk
    emphasis: recommended
  - heading: OPTION C — DEFEND
    content:
      - Lowest investment
      - Limited upside
      - Does not address structural gap
```

Quality checks:

- criteria are consistent across options;
- Option B is emphasized once, not through multiple competing devices;
- recommendation follows from the comparison;
- detailed assumptions sit in footnotes or appendix.

## 7. Impact slide specification

```yaml
purpose: Make one quantified implication memorable
layout: Blank
message: The current process consumes significant avoidable effort
content:
  large_number: "35%"
  descriptor: "of analyst time is spent on manual reconciliation"
  implication: "Standardized data feeds could redirect capacity to higher-value analysis"
```

Quality checks:

- Blank is populated and aligned to the template grid;
- one number dominates;
- supporting text remains concise;
- source and evidence status are visible;
- decorative elements do not compete with the number.

## 8. Assumption label and explanation

### PPTX treatment

Place an `ASSUMPTION` label immediately beside the affected estimate using the exact manifest style.

Example slide text:

> Implementation could generate $20–25 million in annual savings

Footnote:

> Preliminary estimate based on current staffing and an assumed 15% productivity improvement

### Companion-report treatment

```markdown
### Assumption notice

- **Affected element:** Annual savings estimate
- **Status:** Assumption
- **Basis:** Current staffing and assumed productivity improvement
- **Validation needed:** Confirm role-level workload and implementation cost
- **Treatment in PPTX:** `ASSUMPTION` label and explanatory footnote
```

## 9. User override example

The user requests the descriptive title `CUSTOMER SEGMENTATION`.

The agent raises the concern and offers an insight-led alternative. The user confirms the original title.

DeckSpec record:

```yaml
scope: slide_7.title.t1
user_direction: Keep "CUSTOMER SEGMENTATION"
conflict_rule: T1-only titles should normally communicate the insight
status: confirmed
implementation: preserve_user_title
task_scoped: true
canonical_assets_mutated: false
```

QA result:

```yaml
title_is_insight_led: false
disposition: accepted_user_override
```

The decision applies only to the current deck.

## 10. Complete companion-report slide entry

Use this structure for every slide with `companion_coverage: full`. Reporting only the title is incomplete.

```markdown
## Slide 4 — TWO REGIONS OFFER THE STRONGEST NEAR-TERM GROWTH POTENTIAL

- **Classification:** Substantive
- **Reason:** Removing the slide would remove the regional prioritization recommendation and its supporting evidence.

### Layout

- **Option 1 — Used in the PPTX:** 2 Columns 2/3 Split
- **Rationale:** Gives the ranked chart priority while preserving space for implications.
- **Option 2:** Title and Content — simpler, but weakens the chart/commentary hierarchy.

### T1

- **Option 1 — Used in the PPTX:** TWO REGIONS OFFER THE STRONGEST NEAR-TERM GROWTH POTENTIAL
- **Option 2:** NEAR-TERM GROWTH SHOULD FOCUS ON TWO UNDERPENETRATED REGIONS

### Chart — regional opportunity ranking

- **Option 1 — Used in the PPTX:** Ranked horizontal bar chart highlighting Regions A and B
- **Option 2:** Bubble matrix comparing opportunity and execution feasibility

### Implication bullets

- **Option 1 — Used in the PPTX:** Three bullets covering demand, capability reuse, and staged-launch risk reduction
- **Alternative status:** No evidence-supported alternative available
```

Untouched master artwork does not need its own entry. Include footnotes, sources, meaningful speaker notes, and any modified, flattened, or non-editable object when present.
