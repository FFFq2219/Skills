# Evidence schema

## Contents

- Paper registry
- Evidence matrix
- Claim-evidence levels
- Numeric extraction
- Claim synthesis

## Paper registry

Keep one record per intellectual work and link multiple versions when needed.

Required fields:

| Field | Meaning |
|---|---|
| paper_id | DOI, PMID, arXiv ID, or stable internal ID |
| title, authors, year, journal | Verified bibliographic metadata |
| source_origin | `local` or `online` |
| source_type | Article, thesis, review, report, preprint, etc. |
| local_pdf | Existing or managed PDF path, if available |
| source_url | Stable landing page |
| access_route | Local, publisher OA, repository, author manuscript, etc. |
| journal_tier | S/A/B/Excluded/Not applicable/Provisional |
| quality_gate_exception | Exception code or blank |
| status | Discovery-to-inclusion state |
| exclusion_reason | Required when excluded |
| project, topic | Reusable tags |

## Evidence matrix

Create one row per claim-evidence relation, not one row per paper.

| Field | Requirement |
|---|---|
| research_question | Exact question being evaluated |
| claim | Narrow, testable proposition |
| evidence_summary | What was directly observed or measured |
| study_design | Experiment, observation, model, synthesis, method, etc. |
| system_context | Ecosystem, depth, organism, treatment, scale |
| location | Page plus section/figure/table/supplement |
| extraction_method | `text_direct`, `table_direct`, `figure_digitized`, `supplementary`, `calculated`, `inferred` |
| original_value_unit | Exact reported value and unit, if numeric |
| standardized_value_unit | Converted value and unit, if used |
| conversion | Formula, constants, assumptions, and uncertainty |
| study_quality | High/moderate/low/unclear plus rationale |
| evidence_level | A/B/C/D for this claim |
| transferability | High/moderate/low plus rationale |
| alternative_explanation | Strongest plausible rival explanation |
| limitations | Claim-relevant limitations |
| conclusion_status | Supported/provisional/conflicted/unproven/refuted |
| verifier_note | What was checked against the original full text |

## Claim-evidence levels

Assign the level to the paper's support for the specific claim, not to the journal or paper as a whole.

- `A — direct process or experimental evidence`: directly measures the focal process or causal response with a design adequate for the claim.
- `B — strong mechanism or host-level evidence`: identifies a credible mechanism, active host, pathway operation, or tightly linked causal component, but does not directly quantify the complete focal process.
- `C — association or functional potential`: correlation, co-occurrence, gene/pathway potential, indirect proxy, or transfer from a materially different system.
- `D — speculation or unverified inference`: hypothesis, extrapolation, unsupported interpretation, or evidence unavailable for verification.

Downgrade when the inference exceeds the design, transferability is weak, full text cannot be checked, or a necessary assumption is untested. A high-tier journal may provide C-level support for a particular lake claim; a thesis may provide A/B-level support for a directly documented calibration.

## Numeric extraction

For every extracted number preserve:

1. Original image/table/text location.
2. Axis labels, legend, treatment, sample size, error representation, and statistical annotation.
3. Original unit and exact value or digitization precision.
4. Any conversion formula and constants.
5. Extraction confidence: `A direct table/text`, `B reliable figure read`, `C calculated conversion`, `D uncertain`.

Never round intermediate values merely to match a displayed result. Separate reported precision from calculated precision.

## Claim synthesis

Label each statement:

- `Fact`: directly reported or observed in the cited source.
- `Inference`: reasoned synthesis supported by stated premises.
- `Hypothesis`: testable proposed explanation.
- `Unknown`: evidence is missing, conflicting, inaccessible, or too weak.

For each major claim report supporting evidence, conflicting evidence, evidence level, transferability, alternative explanation, and the next observation or experiment that would discriminate among explanations.

