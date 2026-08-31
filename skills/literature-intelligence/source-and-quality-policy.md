# Source and quality policy

## Contents

- Source tracks
- Online journal quality gate
- Exceptions
- Study-quality appraisal
- Full-text and access policy
- Deduplication and status

## Source tracks

Use two independent tracks.

| Track | Admission rule | Typical role |
|---|---|---|
| Local PDF | Index all readable PDFs; no journal-tier exclusion | Evidence, methods, theses, reports, seed references, idea generation |
| Newly found online | Apply the journal-quality gate before inclusion | Current high-quality evidence and cross-domain advances |

Never treat `local` as a quality label. Record `source_origin` and `source_type` separately.

Suggested `source_type` values: `peer_reviewed_article`, `review`, `phd_dissertation`, `master_thesis`, `preprint`, `technical_report`, `conference_paper`, `book_chapter`, `other`.

## Online journal quality gate

Classify current online discoveries conservatively:

- `Tier S`: Nature, Science, Cell, their relevant high-selectivity research titles, and equivalently field-defining general journals.
- `Tier A`: JCR Q1, CAS Zone 1 or recognized strong Zone 2 journals, major academies/general journals, and clear field-leading journals.
- `Tier B`: high-quality specialist flagships or journals with strong field recognition and rigorous peer review, even when a single metric does not fully capture that standing.
- `Excluded`: ordinary findings from JCR Q3/Q4, CAS Zone 3/4, weak or questionable venues, predatory outlets, conference abstracts, informal webpages, and unverifiable publications.

Do not fabricate metrics. Journal quartiles and partitions are year- and category-specific; verify the current or publication-year classification when it affects inclusion. If current proprietary metrics are unavailable, label the tier as `PROVISIONAL` and justify it with transparent field-standing evidence.

Passing the venue gate does not guarantee study quality or claim relevance.

## Exceptions

Permit an online paper below the normal gate only when it is one of:

- `FOUNDATIONAL_METHOD`: original method, instrument, calibration, or model source that later high-quality work relies on.
- `FIELD_DEFINING_CLASSIC`: historically central evidence needed to explain the field.
- `UNIQUE_PRIMARY_DATA`: irreplaceable observations required to understand a narrow parameter, used cautiously.
- `CONTRADICTORY_EVIDENCE`: necessary evidence that challenges the emerging conclusion.

Record `quality_gate_exception`, rationale, downstream citations showing importance when applicable, and whether the paper may support a major claim. Ordinary low-impact findings do not qualify merely because they are relevant.

## Study-quality appraisal

Assess independently from venue:

1. Match between question, design, and inference.
2. Experimental unit, controls, replication, randomization/blocking, and independence.
3. Measurement validity, calibration, detection limits, and unit consistency.
4. Statistical model, assumptions, effect sizes, uncertainty, multiplicity, and missing data.
5. Completeness of methods and data availability.
6. Alternative explanations, confounding, and boundary conditions.
7. Directness and transferability to the focal ecosystem or process.

Use `high`, `moderate`, `low`, or `unclear`, with a one-sentence rationale.

## Full-text and access policy

Allowed routes include publisher open access, recognized repositories, author manuscripts, PubMed Central/Europe PMC, arXiv, and comparable lawful public hosts.

Never use credential harvesting, institutional-session copying without user direction, CAPTCHA circumvention, DRM bypass, shadow libraries, or access-control workarounds. When access fails, record:

- landing page and DOI;
- abstract availability;
- attempted lawful routes;
- `FULLTEXT_UNAVAILABLE`;
- claims that remain unverified.

## Deduplication and status

Match DOI/PMID/arXiv ID first, then normalized title, author-year, then PDF hash. Prefer the version of record for citation, while retaining a lawful manuscript or preprint as the accessible full text and recording the relationship.

Use one terminal exclusion reason: `duplicate`, `wrong_question`, `wrong_system`, `no_relevant_measurement`, `method_unsuitable`, `review_only`, `insufficient_evidence`, `low_quality_venue`, `fulltext_unavailable`, or `other`.

