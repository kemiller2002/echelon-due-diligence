---
id: DD-RPT-IDX-001
title: Deliverables index and traceability
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
---

# Deliverables index

Maps the 26 required deliverables to their files and states maturity honestly.
"Generated" files are produced by `dotnet fsi tools/build.fsx` from canonical records
and must not be edited by hand. Traceability runs by identifier: questions (`DDQ-*`)
link to answer units (`ANS-*`), which link to controls (`ECTL-*`), evidence
requirements (`EVR-*`), policies (`SEC-*`) and Unbound requirements; every record cites
sources (`SRC-*`); proposed requirements (`DD-UNB-*`) cite originating questions;
objections (`OBJ-*`) cite the records they challenge; recommendations (`REC-*`) cite
the documents that justify them.

| # | Deliverable | Location | Maturity |
|---|---|---|---|
| 1 | Executive research findings | `reports/EXECUTIVE-RESEARCH-FINDINGS.md` | Draft |
| 2 | Master source register | `sources/*.jsonl`; generated `reports/generated/master-source-register.csv`; notes in `research/sources/` | 405 sources, majority verified at issuer |
| 3 | Canonical question register | `questions/*.jsonl`; generated `canonical-question-register.csv` | 2,380+ questions, 67 categories |
| 4 | Target answer register | `answers/*.jsonl`; generated `target-answer-register.csv` | Draft, unreviewed |
| 5 | Verified current answer register | generated `verified-current-answer-register.csv` | Honest statuses; no answer human-approved yet |
| 6 | Control register | `controls/*.jsonl`; generated `control-register.csv` | Proposed controls |
| 7 | Evidence requirements register | `evidence-requirements/*.jsonl`; generated `evidence-requirements-register.csv`; record schema `schemas/dd/evidence-record.schema.json` | Proposed |
| 8 | Framework crosswalk | generated `framework-crosswalk.csv` (question and control to source locator) | Generated |
| 9 | Regulatory applicability matrix | generated `regulatory-applicability-matrix.csv`; narrative matrices in `research/sources/FINANCIAL-SERVICES-SOURCE-NOTES.md`, `SECURITY-PRIVACY-AI-OPERATIONAL-SOURCE-NOTES.md`, `SUPPLEMENTARY-SOURCE-NOTES.md` | Counsel review pending |
| 10 | External assurance requirements matrix | `external-assurance/EXTERNAL-ASSURANCE-REQUIREMENTS-MATRIX.md`, `external-assurance-matrix.csv` | Draft |
| 11 | Security by construction research report | `security-by-construction/SECURITY-BY-CONSTRUCTION-RESEARCH-REPORT.md`; proposed rules `proposed-construction-rules.jsonl` | Draft |
| 12 | CWE architectural prevention matrix | `security-by-construction/cwe-architectural-prevention-matrix.csv`, `CWE-ARCHITECTURAL-PREVENTION-MATRIX.md` | Targets only; nothing demonstrated |
| 13 | Scanner validation research report | `scanner-validation/SCANNER-VALIDATION-RESEARCH-REPORT.md` | Draft |
| 14 | Penetration testing cost reduction strategy | `cost-avoidance/PENETRATION-TESTING-COST-REDUCTION-STRATEGY.md` | Hypotheses |
| 15 | Compliance cost avoidance report | `cost-avoidance/COMPLIANCE-COST-AVOIDANCE-REPORT.md` | Hypotheses H1 to H12 |
| 16 | Financial services vendor assessment profile | `industry-profiles/financial-services/FINANCIAL-SERVICES-VENDOR-ASSESSMENT-PROFILE.md`; insurance `industry-profiles/enterprise-software/INSURANCE-UNDERWRITING-PROFILE.md`; DAF sponsors `industry-profiles/donor-advised-funds/` | Draft |
| 17 | Unbound-specific due diligence profile | `product-profiles/unbound/UNBOUND-DUE-DILIGENCE-PROFILE.md` | Draft |
| 18 | Unbound requirements gap analysis | `gap-analysis/UNBOUND-REQUIREMENTS-GAP-ANALYSIS.md`; `product-profiles/unbound/proposed-requirements.jsonl`; screening `gap-analysis/generated/unbound-baseline-coverage.csv` | 104 proposed requirements; not adopted by Unbound |
| 19 | Echelon organizational policy gap analysis | `gap-analysis/ORGANIZATIONAL-POLICY-GAP-ANALYSIS.md`; `recommendations/policy-recommendations.jsonl` | Draft |
| 20 | Trust center requirements | `trust-center/TRUST-CENTER-REQUIREMENTS.md`; research `trust-center/TRUST-CENTER-RESEARCH.md` | Draft |
| 21 | Automated questionnaire response requirements | `architecture/AUTOMATED-QUESTIONNAIRE-RESPONSE-REQUIREMENTS.md` | Draft |
| 22 | Evidence architecture specification | `architecture/EVIDENCE-ARCHITECTURE-SPECIFICATION.md`, `schemas/dd/evidence-record.schema.json` | Draft |
| 23 | Echelon system capability gap analysis | `architecture/ECHELON-SYSTEM-CAPABILITY-ANALYSIS.md`, `gap-analysis/ECHELON-SYSTEM-CAPABILITY-GAPS.md`; `recommendations/system-recommendations.jsonl`, `security-by-construction-recommendations.jsonl` | Verified against pinned commits |
| 24 | Open questions and unresolved decisions | `research/open-questions.jsonl`; generated `open-questions-register.csv`; `research/OWNER-FACT-VERIFICATION-CHECKLIST.md` | Living |
| 25 | Prioritized implementation roadmap | `reports/PRIORITIZED-IMPLEMENTATION-ROADMAP.md` | Draft |
| 26 | Commercial opportunity assessment | `reports/COMMERCIAL-OPPORTUNITY-ASSESSMENT.md` | Hypotheses |

Supporting: real-world questionnaire research `questionnaires/REAL-WORLD-QUESTIONNAIRE-RESEARCH.md`;
adversarial reviews `validation/ADVERSARIAL-REVIEW-*.md` and `validation/objections-*.jsonl`;
decisions `decisions/`; progress `research/PROGRESS-LEDGER.md`, backlog
`research/RESEARCH-BACKLOG.md`, batch findings `research/BATCH-1-AGENT-FINDINGS.md`.
