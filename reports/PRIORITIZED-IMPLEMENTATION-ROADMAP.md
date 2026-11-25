---
id: DD-RPT-ROAD-001
title: Prioritized implementation roadmap
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [roadmap, prioritization]
---

# Prioritized implementation roadmap

Ordering principle: fix what blocks every customer conversation before what improves
any one answer; prefer cheap, verifiable facts over expensive programs; build evidence
generation into work that has to happen anyway. Durations are sequencing guidance, not
estimates. Cost bands are order-of-magnitude judgments unless a document cited gives a
source.

Inputs: adversarial reviews DD-VAL-ADV-001 and DD-VAL-ADV-002 (no reviewer would pass
Echelon or Unbound today), organizational policy gaps DD-GAP-POL-001, system capability
gaps DD-GAP-SYS-001, Unbound gaps DD-GAP-UNB-001, security by construction DD-SBC-001,
external assurance DD-EXT-001, cost avoidance DD-COST-001/002, open questions
`research/open-questions.jsonl`.

## Phase 0: make the truth knowable (weeks 0 to 2, mostly owner time, low cost)

| # | Action | Unblocks | Ref |
|---|---|---|---|
| 0.1 | Complete owner fact verification checklist (15 items: formation, IP assignment, MFA, branch protection, package publishing credentials, devices, backups, DNS, AI provider terms, insurance, bank controls, incidents, headcount, disclosure channel) | Converts about 70 `unknown` answer units into facts or known gaps | `research/OWNER-FACT-VERIFICATION-CHECKLIST.md`, BL-020 |
| 0.2 | Finish entity formation and IP assignment to the LLC | Contracting, IP, escrow, OFAC ownership answers | OQ-DD-ENT-001 |
| 0.3 | Decide the commercial license for Echelon components used by Unbound and the rerun grant for customers, auditors and escrow agents | Procurement, escrow, auditor evidence verification | OQ-DD-LIC-001, CNV-GOV-009 |
| 0.4 | Publish a vulnerability disclosure policy and security.txt | VUL answers; cheap credibility | DD-GAP-POL-001 P30 |
| 0.5 | Turn on and evidence the corporate baseline: phishing-resistant MFA on admin accounts, branch protection with required review, signed commits or trusted publishing for packages | Insurance application, AUN, CHG, SCS | DD-IND-INS-001 |
| 0.6 | Begin human review of answer units (start with the top 40 deciding questions in the Unbound profile) | Nothing is customer-releasable until approved | Operating contract, review gate |

## Phase 1: legal positions and the minimal truthful policy set (weeks 2 to 8)

| # | Action | Ref |
|---|---|---|
| 1.1 | Counsel opinions: GLBA and FTC Safeguards status (Echelon and sponsors); bank service provider status; Nacha TPSP versus Third-Party Sender; crypto-shredding as deletion; state charitable platform registration (California, Hawaii technical-vendor exclusion); automated decision laws | OQ-DD-POL-001..003, OQ-DD-PAY-001, OQ-DD-PRV-001 |
| 1.2 | Draft and adopt P0 policies with in-force versus target clauses: information security, secure construction (corrected Standard), access, change, vulnerability, incident response, vendor, subprocessor, AI use, exceptions, disclosure, claims | REC-ORGPOL-001..005 |
| 1.3 | Correct the Secure Construction Standard: ownership table (Tutela as security authority; no Aegis or Vigila security roles), add AI-authored code rule, runtime support rule, PostgreSQL trusted-code rules; mark SEC-DB-001 dependency on a runtime data access layer | REC-ORGADMIN-*, REC-SBC-*, proposed construction rules |
| 1.4 | Privacy foundation: privacy notice, DPA template, record of processing, applicable-law register | BL-019 |
| 1.5 | Insurance: cyber and tech E&O quotes answered only from verified facts | DD-IND-INS-001 |
| 1.6 | Name second-person roles or adopt documented compensating controls for two-person controls; contract fractional security or operations capacity if needed | DD-VAL-ADV-001 finding 3 |

## Phase 2: build evidence into engineering (months 2 to 6)

| # | Action | Owner (recommended) | Ref |
|---|---|---|---|
| 2.1 | CI security baseline in every Echelon repository: secret scanning (history), dependency scanning (OSV), SBOM (Syft), license scan, pinned actions, build provenance; findings in SARIF | Praxis runs gates; Tutela owns rules | DD-SCN-001, D11 |
| 2.2 | F# rule-level analyzers for SEC-* rules on FSharp.Analyzers.SDK plus compiled-assembly checks for banned APIs and compiler settings (FS0025 as error, checked arithmetic where required, nullness) | Tutela | DD-SBC-001, REC-SBC-* |
| 2.3 | Decide and build the runtime typed data access layer or amend SEC-DB-001 | Owner decision then Strata or new library | OQ-DD-ARC-001 |
| 2.4 | Upgrade Strata and Ordo off .NET 8 (end of support 2026-11-10) | Repository owners | SRC-DOTNET-SUPPORT-POLICY |
| 2.5 | Evidence records with DSSE signing from Praxis verifier; Tutela trust root; revocation and supersession | Praxis, Tutela | DD-ARC-003 |
| 2.6 | Assign runtime security monitoring ownership; buy managed detection if no system will own it | Owner decision | OQ-DD-ARC-002 |
| 2.7 | Fix pass on knowledge base from adversarial reviews | This repository | BL-015..BL-019, BL-021, BL-022 |

## Phase 3: Unbound readiness to be assessed (aligned with Unbound build, months 4 to 12)

| # | Action | Ref |
|---|---|---|
| 3.1 | Implement P0 Unbound proposed requirements (`product-profiles/unbound/proposed-requirements.jsonl`) and resolve verified baseline contradictions | DD-GAP-UNB-001 |
| 3.2 | Hosting decision, tenant isolation profile decision, key management design | OQ-DD-HOST-001, OQ-DD-TEN-001, ADR-006 |
| 3.3 | Independent penetration test with architecture-informed scope (expect the first test to cost more, not less) | DD-COST-001, BL-018 |
| 3.4 | Engage CPA firm: SOC 2 Type I and SOC 1 Type 1 timing relative to first hosted sponsor's fiscal year end; decide criteria version (2027 exposure draft) | OQ-DD-SOC-001, DD-VAL-ADV-001 finding 5 |
| 3.5 | Design-partner sponsor with parallel run through a fiscal year end | DD-VAL-ADV-001 |
| 3.6 | Trust center phase 1 (public, generated, honest status) then phase 2 (NDA tier) when first independent artifact exists | DD-TC-002 |
| 3.7 | AQR phase 1 tooling in this repository: answer a CSV questionnaire with references and gates; build the labeled matching benchmark | DD-ARC-004, OQ-DD-AQR-001 |

## Phase 4: continuous assurance (after go-live)

SOC 2 Type II period; continuous control monitoring per Unbound architecture; monthly
continuous assurance summary; scanner validation report per scanner release; annual
independent pen test; measured cost avoidance against hypotheses H1 to H12; second
diminishing-returns pass on public questionnaires (BL-013).

## What not to do

- Do not buy a compliance automation or trust center platform before Phase 0 and 1 are
  done; it would automate the presentation of unknowns.
- Do not answer any questionnaire or insurance application from target answers.
- Do not market security by construction until at least the L1/L2 claims for SQL and
  command injection and authorization have reproducible, scoped evidence and an
  independent tester has tried to break them.
