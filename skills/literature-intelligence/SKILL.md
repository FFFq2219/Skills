---
name: literature-intelligence
description: Build traceable scientific literature intelligence from one or more local PDF folders plus high-quality online sources. Use for literature radar scans, deep reviews of a research question, forward/backward citation tracing, cross-domain idea discovery, local thesis or report mining, prioritizing papers to read, retrieving legally accessible full text, and producing evidence matrices or research-question briefs. Search local PDFs without journal-tier exclusion; apply a strict journal-quality gate to newly discovered online papers; keep facts, inferences, hypotheses, and unsupported claims separate.
---

# Literature Intelligence

Turn scattered literature searching into a repeatable evidence workflow. Treat the local PDF collection as the first-priority knowledge base and the web as a high-quality update layer.

## Select the mode

- `radar`: scan recent work and return a short reading queue.
- `deep-dive`: answer one defined scientific question with full-text evidence.
- `question-discovery`: identify unresolved, consequential, testable questions.
- `citation-trace`: trace backward references and forward citations around seed papers.
- `local-library`: search, organize, or mine one or more local PDF roots.

If the request is ambiguous, infer the lightest mode that satisfies it and state the choice. Ask only when the choice materially changes scope, date range, or outputs.

## Establish the research frame

Capture before searching:

1. Scientific question or target decision.
2. Focal system, scale, process, and acceptable analog systems.
3. Date range and whether foundational work is needed.
4. Project constraints and known seed papers.
5. Requested output: brief, reading queue, evidence matrix, question list, or citation map.

Do not search from one phrase alone. Expand the question into mechanism, process, method, organism/system, and cross-domain analog terms. Read [search-and-output.md](references/search-and-output.md) for the full strategy and required report shapes.

## Use the local library first

Accept multiple PDF roots and recurse through subdirectories. Do not apply the journal-quality gate to local files. Include journal articles, reviews, dissertations, theses, reports, preprints, books, and method documents, while labeling `source_type` separately from evidentiary strength.

For a reusable local index:

1. Initialize a workspace with `scripts/init_workspace.py`.
2. Build or incrementally update the index with `scripts/index_local_pdfs.py`.
3. Search extracted text with concept-expanded terms using `scripts/search_local_index.py`.
4. Open the original PDFs for every passage used in a final claim and verify page, section, figure, or table location.

Never move, rename, or modify pre-existing PDFs. Keep extracted text and indexes in the configured workspace. Treat local paths as private; do not upload local full text to an external service unless the user explicitly requests it.

Use relevant dissertations and theses as literature navigators: extract unusually detailed methods and key references, then seek the original primary papers online. Do not make a thesis the sole support for a major claim when stronger primary evidence is available.

If the user has not supplied PDF roots, ask for them only when local-library coverage is necessary. Otherwise continue with available files and label the local search incomplete.

## Search the web as an update layer

Search broadly enough to avoid vocabulary bias, then apply the online quality gate before presenting papers. Prefer primary research and authoritative bibliographic records. Verify title, authors, year, journal, DOI, publication status, and access route; do not rely on search-result snippets for scientific claims.

Apply [source-and-quality-policy.md](references/source-and-quality-policy.md):

- Newly discovered online papers must normally pass Tier S, A, or B.
- Exclude ordinary findings from low-impact or questionable venues.
- Preserve narrowly defined exceptions for foundational methods, field-defining classics, and necessary contradictory evidence; label the exception and do not let it silently become primary support.
- Never apply this gate retroactively to local PDFs.

For time-sensitive journal quartiles, metrics, publication status, or newest papers, verify current information online. Do not invent impact factors, JCR quartiles, CAS partitions, citations, DOIs, or access status.

## Retrieve full text legally

Check the local index before downloading. Deduplicate in this order: DOI or stable identifier, normalized title, author-year, then file hash.

For a paper selected for deep reading or the evidence chain, try lawful routes: publisher open access, PubMed Central or Europe PMC, arXiv or another recognized preprint server, institutional repository, or author manuscript. Use `scripts/fetch_oa_pdf.py` only after resolving a direct public PDF URL.

Do not bypass paywalls, authentication, CAPTCHAs, DRM, robots restrictions, or access controls. If no lawful PDF is available, retain verified metadata and the landing-page link with `FULLTEXT_UNAVAILABLE`; never imply that an abstract supports a full-text claim.

Download only papers that enter deep reading, the evidence matrix, or the final citation set. Store managed downloads separately from existing PDFs and preserve source URL, DOI, download date, hash, project, topic, and access route.

## Screen, read, and extract evidence

Run three distinct decisions:

1. `relevance`: Does the paper address the question or offer a transferable method?
2. `study_quality`: Are design, measurements, statistics, and reporting fit for the claim?
3. `claim_support`: What exact claim does the evidence support, at what strength and transferability?

Do not infer paper quality from journal prestige alone. Do not infer claim support from paper quality alone.

Extract from full text whenever possible. For numeric or method claims record section, page, figure/table/supplement, original unit, any conversion, and extraction method. Use [evidence-schema.md](references/evidence-schema.md) for required fields and A-D claim-evidence levels.

Maintain status transitions:

`DISCOVERED → SCREENED → FULLTEXT_AVAILABLE → READ → EVIDENCE_EXTRACTED → INCLUDED`

or `EXCLUDED` with a recorded reason.

## Synthesize without overclaiming

For every major conclusion:

- State the claim at the narrowest defensible scope.
- Separate `Fact`, `Inference`, `Hypothesis`, and `Unknown`.
- Cite the exact supporting source near the claim.
- Give evidence level and transferability to the focal system.
- Identify important conflicting evidence and plausible alternative explanations.
- State what evidence would change the conclusion.

For omics work, never promote gene presence or pathway potential into measured process rate. For cross-domain papers, distinguish `inspiration value` from `direct evidence value`.

## Deliver a decision-ready output

Default to a selective output rather than an exhaustive bibliography. In `radar` mode return roughly 3-5 must-read papers, 5-10 worth knowing, and a small cross-domain section when evidence permits. In `deep-dive` mode answer the scientific question first, followed by the evidence matrix, conflicts, gaps, and next actions.

Include:

- Search scope and local-library coverage.
- Inclusion/exclusion rules and any quality-gate exceptions.
- A prioritized reading list with `why it matters`.
- Major contribution, methodological novelty, borrowable idea, relevance, and evidence strength.
- A claim-evidence table and explicit unknowns.
- Effects on the current project or experimental design, when relevant.

Do not conceal an empty or weak evidence base. Report when no qualifying online literature was found.

## Preserve reusable research state

When the user asks for reusable outputs, save the search log, paper registry, evidence matrix, and brief in the project workspace. Prefer `paper_registry.jsonl`, `evidence_matrix.csv`, `search_log.md`, and a dated Markdown brief. Never overwrite project context or prior decisions silently. Append new evidence and mark superseded conclusions rather than deleting their history.

This skill supplies evidence to a future project-management or experiment-design workflow; it does not make the final research decision for the user.
