# Search strategy and output formats

## Contents

- Query construction
- Cross-domain inspiration
- Mode-specific workflow
- Reading priority
- Output templates

## Query construction

Translate the scientific question into a query matrix before searching:

| Axis | Examples |
|---|---|
| Process | carbon fixation, mineralization, erosion, deoxygenation |
| Mechanism | hydrogen oxidation, anaplerosis, redox coupling |
| System | lake water column, sediment, rhizosphere |
| Method | isotope tracing, microsensors, metagenomics, flux model |
| Outcome | rate, threshold, contribution, causal effect |
| Vocabulary variants | abbreviations, gene names, older terminology, Chinese/English terms |

Run at least one narrow mechanism query, one broader concept query, and one method query. Add seed-paper citation tracing when central terminology is unstable.

For local full-text search, generate a compact set of exact terms and synonyms, then use `search_local_index.py` or `rg` over extracted text. Inspect the original PDF for all included evidence.

## Cross-domain inspiration

Search analog systems only when a transfer mechanism can be stated. Candidate domains include deep ocean, groundwater, subseafloor sediment, hydrothermal systems, caves, soils and subsurface, wetlands, wastewater bioreactors, and engineered redox reactors.

For every cross-domain paper record separately:

- `borrowable idea`: method, conceptual model, tracer, analysis, or experimental contrast;
- `transfer mechanism`: why it might apply;
- `boundary mismatch`: what differs from the focal system;
- `inspiration_value`: high/moderate/low;
- `direct_evidence_value`: high/moderate/low.

Never use inspiration value as direct evidence.

## Mode-specific workflow

### Radar

1. Define period and topic portfolio.
2. Search local additions and qualifying online papers.
3. Screen titles/abstracts; retrieve full text only for finalists.
4. Rank and report the smallest useful reading queue.

### Deep-dive

1. Frame the exact claim or decision.
2. Search local full text first.
3. Search high-quality online sources and trace citations.
4. Read primary full text, build claim-level evidence rows, assess conflicts.
5. Answer first; then show evidence, gaps, and implications.

### Question-discovery

1. Map established findings and repeated assumptions.
2. Identify contradictions, scale gaps, method blind spots, unmeasured rates, and causal ambiguity.
3. Reject questions answerable by one routine measurement or questions with no feasible discriminating test.
4. Rank by importance, novelty, tractability, evidence gap, and fit to available capabilities.

### Citation-trace

1. Verify seed metadata.
2. Trace backward to original methods and foundational claims.
3. Trace forward to replications, contradictions, and applications.
4. Collapse duplicate versions and distinguish citation from genuine evidentiary use.

## Reading priority

Score qualitatively or on a declared 1-5 scale:

- scientific importance;
- relevance to current project;
- methodological novelty;
- evidence quality;
- cross-domain transferability;
- likelihood of changing an existing decision.

Journal tier is a gate and context feature, not the final reading score.

## Output templates

### Radar brief

1. `This period's major advances` — 3-5 must-read papers.
2. `Worth knowing` — 5-10 concise entries.
3. `Methods worth borrowing` — 2-4 when available.
4. `Cross-domain inspiration` — 2-4 with transfer limits.
5. `Possible impact on current projects` — changes, no-change, or uncertainty.
6. `Human reading decision` — a ranked queue, never an automatic declaration of what the user must believe.

For every listed paper include: citation, journal tier, contribution, new method, borrowable idea, relevance, evidence strength, and why it matters.

### Deep-dive brief

1. Direct answer with confidence and scope.
2. Search coverage: local roots searched, online databases/sources, dates, query families.
3. Claim-evidence matrix.
4. Conflicting evidence and alternative explanations.
5. What remains unproven.
6. Implications for the project or experiment.
7. Prioritized papers and full-text availability.

### Search log

Record date, mode, question, query strings, sources, date filters, quality gate, local roots, results screened, full texts read, exclusions by reason, and known coverage limitations.

