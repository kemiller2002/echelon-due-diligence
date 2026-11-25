---
id: DD-GAP-UNB-001
title: Unbound requirements gap analysis against the due diligence question bank
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [gap-analysis, due-diligence, unbound, requirements, donor-advised-funds]
related_documents:
  - product-profiles/unbound/UNBOUND-DUE-DILIGENCE-PROFILE.md
  - product-profiles/unbound/proposed-requirements.jsonl
  - gap-analysis/generated/unbound-baseline-coverage.csv
  - architecture/ECHELON-CURRENT-STATE-BRIEF.md
  - architecture/ECHELON-SYSTEM-CAPABILITY-ANALYSIS.md
  - research/BATCH-1-AGENT-FINDINGS.md
---

# Unbound requirements gap analysis

## 1. Summary

Unbound (`unbound@9b38de47`) is a requirements-only product. Its baseline is unusually
deep on DAF business controls: grant approval under board delegation, sanctions
screening, payment roles, reconciliation, fund accounting, tenant isolation and AI
authority boundaries are each governed by convergence clauses with acceptance criteria.
It is thin or silent on the security program, infrastructure and commercial topics that
procurement and third-party risk teams ask first: encryption, key management, hosting,
vulnerability management, penetration testing, scanning, personnel security, insurance,
escrow, subprocessors, incident notification, AI provider terms and the contract package.

Nothing in this document describes an implemented control. Every Unbound answer remains
`proposed-target-state` at best (DD-ARC-001).

Headline results:

- 2,248 questions in the bank apply to Unbound (`products` includes `unbound` or
  `all-echelon-products`), served by 508 answer units. Counts were taken on 2026-11-25
  while other agents were still adding records; the bank grew from 2,319 questions
  during this work.
- 317 questions (14 percent) cite no Unbound requirement at all; 23 cite only proposed,
  unvalidated, non-normative or missing records; 173 have an answer status of `unknown`
  or `requires-external-validation`.
- 457 questions cite at least one of 59 baseline records that a convergence clause
  amends, without also citing the governing clause. 256 questions cite at least one
  record whose release scope is `Deferred`.
- 16 identifiers cited in question and answer `requirements` fields (`UNB-CTRL-064`,
  `UNB-CTRL-065`, `UNB-CTRL-070`, `UNB-CTRL-071`, `UNB-CTRL-082` and 11 `UNB-SCTRL-*`)
  are control identifiers from `requirements/governance/*.csv`, not baseline
  requirements. They exist, but citing them as requirements is a category error.
- Eight internal contradictions were verified in the baseline (section 5), plus four
  inconsistencies that are not strict contradictions.
- 104 proposed requirements are recorded in
  `product-profiles/unbound/proposed-requirements.jsonl` (29 P0, 48 P1, 23 P2, 4 P3).

## 2. Method

### 2.1 Inputs

| Input | Location | Use |
|---|---|---|
| Unbound baseline | `unbound@9b38de47:requirements/baseline/baseline.jsonl` (1,653 records) | Existence, status, classification, release scope and `converged_by` of each cited ID |
| Convergence clauses | `unbound@9b38de47:requirements/convergence/2026-11-24-master/data/convergence-clauses.jsonl` (82) | `amends` lists, used with `converged_by` to find governed records |
| Precedence rule | `unbound@9b38de47:requirements/AUTHORITATIVE-BASELINE.md` | CNV clauses govern, then adopted refinements, then originals |
| Question bank | `questions/*.jsonl` | Questions in Unbound scope, importance, cited requirements |
| Answer units | `answers/*.jsonl` | Cited requirements, status and `open_questions` |
| Coverage screen | `gap-analysis/generated/unbound-baseline-coverage.csv` | Thin categories (INS, SDL, VUL, SCN, CLD, ESC, SUB) |
| Batch 1 findings | `research/BATCH-1-AGENT-FINDINGS.md` | Claimed contradictions and gaps, each re-verified here |
| Sponsor audit matrix | `daf-landscape/data/technology-audit-control-matrix-2026.csv` (`SRC-ECH-DAF-TECH-AUDIT`, C01 to C24) | Sponsor-perspective control mapping in the profile |

### 2.2 Mining procedure

A script (kept in the session scratchpad, not committed) did the following for each
in-scope question:

1. Took the union of the question's and its answer unit's `requirements`, excluding
   Secure Construction Standard rule IDs (`SEC-*`).
2. Checked each ID against the baseline. Missing IDs were recorded.
3. Marked an ID as governed when a CNV clause lists it in `amends` or the record's
   `converged_by` is non-empty, and as "governed but uncited" when the question did not
   also cite the governing clause.
4. Marked an ID as weak when its status is `proposed` or `unvalidated` or its
   classification is not `normative` (for example `research-hypothesis`), and as
   deferred when its release scope begins with `Deferred`.
5. Classified the question:

| Class | Rule | Count |
|---|---|---|
| covered | At least one cited ID exists, is normative, not weak and not governed-but-uncited; answer status not unknown; no open questions | 990 |
| covered-with-open-questions | As above, but the answer unit lists open questions | 745 |
| answer-unknown | Strong citation exists but the answer status is `unknown` or `requires-external-validation` | 173 |
| only-weak-or-missing | Every cited ID is weak, missing or governed-but-uncited | 23 |
| no-unbound-requirement | No Unbound ID cited | 317 |

### 2.3 Limits of the mining

"Covered" means only that an in-force requirement is cited. It does not mean the
requirement is adequate, testable, or answers the specific concern. Adequacy was judged
manually per scope area by reading the governing clauses (section 4 and the profile's
area table). Several categories score as covered while the governing text is a single
list item (for example encryption in `SOC2-014`). Conversely, the coverage screen's
keyword match placed `UNB-XIN-OTH-004` (print vendor dispositions) under scanning, which
is a false positive.

### 2.4 Mining results by category

Counts are questions in Unbound scope: covered (C), covered with open questions (O), no
Unbound requirement (N), answer unknown (U), only weak or missing (W).

| Cat | Total | C | O | N | U | W | Cat | Total | C | O | N | U | W |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A11Y | 35 | 26 | 0 | 4 | 5 | 0 | IPR | 25 | 13 | 4 | 8 | 0 | 0 |
| ACT | 39 | 32 | 7 | 0 | 0 | 0 | IR | 48 | 16 | 9 | 15 | 5 | 3 |
| AIA | 41 | 30 | 6 | 0 | 5 | 0 | ISP | 18 | 4 | 8 | 0 | 6 | 0 |
| AIG | 43 | 13 | 4 | 1 | 25 | 0 | LEG | 37 | 13 | 4 | 18 | 1 | 1 |
| AIS | 42 | 30 | 0 | 0 | 12 | 0 | MON | 42 | 30 | 4 | 2 | 6 | 0 |
| AML | 36 | 18 | 13 | 0 | 5 | 0 | NET | 33 | 0 | 23 | 5 | 0 | 5 |
| API | 36 | 29 | 7 | 0 | 0 | 0 | PAY | 40 | 12 | 28 | 0 | 0 | 0 |
| APP | 60 | 16 | 5 | 39 | 0 | 0 | PEN | 32 | 3 | 0 | 29 | 0 | 0 |
| ARC | 40 | 17 | 6 | 17 | 0 | 0 | PHY | 7 | 6 | 0 | 1 | 0 | 0 |
| ASM | 25 | 15 | 4 | 0 | 6 | 0 | PRF | 15 | 15 | 0 | 0 | 0 | 0 |
| AUD | 38 | 29 | 8 | 1 | 0 | 0 | PRT | 21 | 3 | 14 | 0 | 4 | 0 |
| AUN | 43 | 24 | 19 | 0 | 0 | 0 | PRV | 56 | 0 | 44 | 0 | 9 | 3 |
| AUZ | 44 | 28 | 12 | 0 | 4 | 0 | RCN | 35 | 4 | 31 | 0 | 0 | 0 |
| AVL | 26 | 23 | 0 | 3 | 0 | 0 | REG | 31 | 22 | 5 | 4 | 0 | 0 |
| BCP | 32 | 22 | 4 | 6 | 0 | 0 | RET | 31 | 8 | 18 | 0 | 5 | 0 |
| BKP | 21 | 21 | 0 | 0 | 0 | 0 | RRP | 40 | 0 | 36 | 0 | 4 | 0 |
| CHG | 30 | 21 | 5 | 4 | 0 | 0 | RSK | 31 | 19 | 12 | 0 | 0 | 0 |
| CHV | 50 | 24 | 26 | 0 | 0 | 0 | SCN | 36 | 14 | 0 | 22 | 0 | 0 |
| CLD | 32 | 8 | 20 | 0 | 4 | 0 | SCS | 45 | 0 | 0 | 45 | 0 | 0 |
| CON | 44 | 15 | 29 | 0 | 0 | 0 | SDL | 45 | 17 | 6 | 22 | 0 | 0 |
| CUS | 30 | 0 | 30 | 0 | 0 | 0 | SUB | 21 | 9 | 0 | 0 | 12 | 0 |
| DAF | 54 | 15 | 35 | 0 | 4 | 0 | SUP | 20 | 13 | 0 | 0 | 3 | 4 |
| DCL | 21 | 4 | 17 | 0 | 0 | 0 | TEN | 44 | 29 | 11 | 0 | 4 | 0 |
| DON | 34 | 20 | 14 | 0 | 0 | 0 | TPR | 36 | 26 | 0 | 0 | 10 | 0 |
| DR | 26 | 19 | 4 | 0 | 0 | 3 | TRM | 28 | 5 | 11 | 7 | 5 | 0 |
| ENC | 48 | 0 | 35 | 10 | 0 | 3 | TXI | 36 | 29 | 7 | 0 | 0 | 0 |
| END | 22 | 0 | 7 | 14 | 1 | 0 | VUL | 39 | 2 | 15 | 22 | 0 | 0 |
| ESC | 16 | 0 | 5 | 4 | 7 | 0 | WLB | 41 | 23 | 13 | 0 | 5 | 0 |
| FCT | 35 | 20 | 15 | 0 | 0 | 0 | GOV | 12 | 3 | 3 | 6 | 0 | 0 |
| FEE | 29 | 15 | 14 | 0 | 0 | 0 | GRT | 49 | 40 | 9 | 0 | 0 | 0 |
| FRD | 36 | 28 | 8 | 0 | 0 | 0 | HR | 17 | 8 | 0 | 3 | 6 | 0 |
| FST | 9 | 0 | 6 | 0 | 2 | 1 | IAM | 48 | 31 | 12 | 0 | 5 | 0 |
| INF | 33 | 6 | 23 | 4 | 0 | 0 | INS | 4 | 0 | 0 | 1 | 3 | 0 |
| INV | 35 | 5 | 30 | 0 | 0 | 0 | | | | | | | |

Only a few INS, FST and GOV questions appear because most carry the product tag
`echelon-organization`, not `unbound`; they were still used as originating questions
where an Unbound sale depends on them.

## 3. Severity scale

| Severity | Meaning | Proposed priority |
|---|---|---|
| Critical | A sale cannot pass procurement, or a direct legal obligation is unmet, or the baseline gives a materially wrong answer | P0 |
| High | Required before the first production pilot or a customer evidence package | P1 |
| Medium | Expected by sophisticated buyers; can follow first pilot | P2 |
| Low | Quality or clarity improvement | P3 |

## 4. Gap list by area

Each gap names the proposed requirement that would close it. "Existing" lists the
baseline records that partly address the concern.

### 4.1 Security program and infrastructure (thin areas)

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| No encryption-at-rest requirement (algorithm, coverage, backups) | Critical | SOC2-014, UNB-TEN-006 (list items) | DD-UNB-SEC-001 |
| No transport encryption requirement | Critical | UNB-CUST-017 ("secure transport") | DD-UNB-SEC-002 |
| Key management design unresolved (ADR-006) | Critical | UNB-TEN-008 (list item) | DD-UNB-SEC-003 |
| Bank account numbers, TINs and SSNs have no field-level protection requirement | Critical | CNV-ARC-001 (PII vault references) | DD-UNB-SEC-004, DD-UNB-PAY-002 |
| No secrets management or secret scanning requirement | Critical | UNB-API-STD-005 (integrations only) | DD-UNB-SEC-005 |
| Vulnerability management has no scope, targets or exceptions | Critical | SOC2-016 | DD-UNB-SEC-006 |
| No vulnerability disclosure policy or security.txt | Medium | none | DD-UNB-SEC-007 |
| No independent penetration test requirement (29 of 32 PEN questions uncited) | Critical | SOC2-016 | DD-UNB-SEC-008 |
| No security scanning gates; no F# SAST exists | High | SOC2-016, CNV-GOV-009 | DD-UNB-SEC-009 |
| Secure development standard not adopted; review of AI-authored and administrator changes unspecified | Critical | CNV-PLT-010 (control-relevant modules only) | DD-UNB-SEC-010 |
| No SBOM content or deployment signature verification | High | CNV-PLT-010, CNV-GOV-009 | DD-UNB-SEC-011 |
| Threat modeling is a research hypothesis | High | UNB-GAP-029 | DD-UNB-SEC-012 |
| No application security verification standard (39 of 60 APP questions uncited) | High | CNV-PLT-010 | DD-UNB-SEC-013 |
| Security log retention undefined (SOC2-023 forbids inventing one) | High | SOC2-023, CNV-PLT-009 | DD-UNB-SEC-014 |
| No runtime security monitoring; no Echelon system provides it | High | MON-018, SOC2-012 | DD-UNB-SEC-015 |
| Incident response plan absent beyond list items | Critical | SOC2-015, UNB-OPS-001, UNB-GAP-034 | DD-UNB-SEC-016 |
| Deprovisioning targets absent | High | SOC2-010, CNV-PLT-003 | DD-UNB-SEC-017 |
| No personnel security requirement | High | none | DD-UNB-SEC-018 |
| No endpoint security requirement (14 of 22 END questions uncited) | High | none | DD-UNB-SEC-019 |
| No security program charter or qualified individual | Critical | CNV-GOV-003 (assumes a CISO) | DD-UNB-SEC-020 |
| Hosting provider and regions not chosen | Critical | CNV-ARC-001 | DD-UNB-SEC-021 |
| Cloud account structure and root credentials unspecified | High | CNV-PLT-010 | DD-UNB-SEC-022 |
| Network segmentation and egress control unspecified | High | CNV-ARC-002 | DD-UNB-SEC-023 |
| Two-person controls require at least two qualified people | Critical | CNV-PLT-010, CNV-GOV-003, TVR-ORG-003-Q | DD-UNB-SEC-024 |
| Control matrix lacks infrastructure and program controls | High | SOC2-013, SOC2-014, SOC2-016 | DD-UNB-GOV-003 |
| No SOC 2 timing commitment | High | CNV-GOV-001, UNB-RCN-PLT-013 | DD-UNB-AUD-001 |

### 4.2 Legal, commercial and vendor

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| Regulatory perimeter (money transmission, adviser, broker-dealer, Nacha TPS versus TPSP, bank service provider) rests on an owner interpretation | Critical | CNV-LEG-001, CNV-PAY-001, UNB-XIN-REG-002 | DD-UNB-LEG-001 |
| No contract package (MSA, security addendum, DPA, SLA, exit schedule) | High | CNV-GOV-001, CNV-ENT-002 | DD-UNB-LEG-002 |
| No insurance requirement (zero baseline matches) | High | none | DD-UNB-LEG-003 |
| Contracting entity and IP title not established | Critical | none | DD-UNB-LEG-004 |
| Platform-generated records not defined as customer data | High | CNV-ENT-002 | DD-UNB-LEG-005 |
| No incident notification timing | Critical | UNB-GAP-034 | DD-UNB-LEG-006 |
| Echelon's own sanctions screening and ownership disclosure | High | none | DD-UNB-LEG-007 |
| UCC 4A security procedure and loss allocation | High | CNV-PAY-001 | DD-UNB-LEG-008 |
| Vendor related-party disclosure | Medium | CNV-GRT-009 | DD-UNB-LEG-009 |
| Subprocessor register deferred | High | UNB-XIN-SAS-011 (Deferred) | DD-UNB-VEND-001 |
| No critical provider selected (bank, custodian, screening, identity proofing, hosting) | Critical | SOC2-013, CNV-GOV-002 | DD-UNB-VEND-002 |
| PolyForm Noncommercial components; customer and successor rights | Critical | CNV-GOV-009 | DD-UNB-VEND-003 |
| Customer and examiner access terms | Medium | CNV-GOV-001 | DD-UNB-AUD-002 |

### 4.3 Privacy

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| Which privacy notice governs a white-labeled session | High | UNB-RCN-WF-009, REQ-X-030 | DD-UNB-PRV-001 |
| Processor role and DPA | High | UNB-TEN-008 | DD-UNB-PRV-002 |
| GLBA and Safeguards Rule applicability; no contractual safeguards commitment | High | SOC2-014 | DD-UNB-PRV-003 |
| Rights requests against append-only records not designed; counsel review pending | High | UNB-DATA-007, UNB-IMM-008, UNB-DATA-001 | DD-UNB-PRV-004 |
| No prohibition on sale, sharing or third-party tracking tags | High | UNB-XIN-CRM-003 | DD-UNB-PRV-005 |
| No data location default | High | UNB-TEN-008 | DD-UNB-PRV-006 |
| No privacy impact assessment gate | Medium | SOC2-014 | DD-UNB-PRV-007 |
| No privacy officer | Medium | none | DD-UNB-PRV-008 |

### 4.4 AI

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| No AI provider inventory or data terms | Critical | UNB-XIN-SAS-009 (metering) | DD-UNB-AIA-001 |
| No no-training commitment | Critical | none | DD-UNB-AIA-002 |
| Engineering agents' permissions and production isolation | Critical | CNV-AIO-001 (product only) | DD-UNB-AIA-003 |
| No AI adversarial testing gate | High | CNV-AIO-002, UNB-AIO-003, AIN-012 (proposed), UNB-GAP-033 (hypothesis) | DD-UNB-AIA-004 |
| Model change and deprecation control | Medium | CNV-AIO-001 | DD-UNB-AIA-005 |
| Automated decision law applicability | Medium | CNV-GRT-012 | DD-UNB-AIA-006 |

The product AI authority boundary itself (CNV-AIO-001, CNV-AIO-002, CNV-GRT-001) is
strong and specific; the gaps are around it, not in it.

### 4.5 Tenancy, white labeling, embedded components and APIs

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| Conflicting isolation default and stale dependency language | Critical | CNV-ARC-001, CNV-TEN-001, CNV-ARC-003, RR-UNB-PLAT-008-r1 | DD-UNB-TEN-001 |
| No continuous production canaries or independent isolation testing | High | CNV-ARC-001, UNB-RCN-WF-009 | DD-UNB-TEN-002 |
| Custom domains and certificates | Medium | REQ-X-030 | DD-UNB-WLB-001 |
| Embedded components specified only as one-line rows; ADR-M-03 open | High | INT-015, AIN-029, MON-022 | DD-UNB-WLB-002 |
| Brand attribution rule unclear | Low | UNB-EXP-002, REQ-X-030 | DD-UNB-WLB-003 |
| No API authentication method named | High | UNB-API-STD-005 | DD-UNB-API-001 |
| No sandbox or public changelog | Medium | CNV-EXP-001 | DD-UNB-API-002 |
| Rate limits deferred | Medium | RR-UNB-API-STD-003-r1 (unvalidated, Deferred) | DD-UNB-API-003 |

### 4.6 Money movement, fraud and sanctions

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| Payment file encryption, signing and bank channel | Critical | CNV-PAY-001, CNV-ARC-003 | DD-UNB-PAY-001 |
| Nacha account number protection (direct TPSP obligation) | Critical | CNV-PAY-001 | DD-UNB-PAY-002 |
| Nacha risk-based fraud monitoring program (in force since June 2026) | Critical | CNV-PAY-001 | DD-UNB-PAY-003 |
| Emergency payments during an Unbound outage | High | TVR-PAY-004-Q (open), CNV-PLT-007 | DD-UNB-PAY-004 |
| Check stock and signature custody | Medium | CNV-PAY-002, UNB-XIN-OTH-004 | DD-UNB-PAY-005 |
| ACH end-to-end idempotency binding | High | TVR-PAY-002-Q (open), CNV-PAY-004 | DD-UNB-PAY-006 |
| Reference sanctions matcher unfit; no provider | Critical | CNV-GRT-006 | DD-UNB-AML-001 |
| Adverse media | Low | CNV-GRT-003 | DD-UNB-AML-002 |

Grant approval, recipient eligibility and reverification, payee change verification,
dispatch fencing and unknown payment outcomes are strongly specified (CNV-GRT-001,
CNV-GRT-003, CNV-GRT-006, REQ-X-005, CNV-PLT-011, CNV-ARC-003, CNV-PAY-004) and are not
listed as gaps.

### 4.7 Finance, accounting and investments

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| Scheduled and recurring contributions absent (and absent from the question bank) | Medium | CNV-FIN-003, CNV-PAY-005 | DD-UNB-FIN-001 |
| Reconciliation sampling method and break reporting | High | CNV-FIN-004 | DD-UNB-FIN-002 |
| No advance notice of fee increases | Medium | CNV-FIN-002 | DD-UNB-FIN-003 |
| Form 1099 applicability | Medium | UNB-ACC-021 | DD-UNB-FIN-004 |
| Ledger integrity mechanism undecided | High | UNB-DATA-012, CNV-PLT-010 | DD-UNB-FIN-005 |
| CUEC list deferred though needed before reliance | High | UNB-XIN-ACC-009 (Deferred), CNV-GOV-001 | DD-UNB-FIN-006 |
| Sponsor-pool NAV text contradicts the no-pools clause | Critical | CNV-LEG-001, CNV-FIN-005 | DD-UNB-FIN-007 |
| Trade execution API text contradicts the perimeter | Critical | CNV-LEG-001, UNB-CUST-007 | DD-UNB-FIN-008 |
| Custodian activation gate | High | UNB-CUST-009, UNB-CUST-017, CNV-FIN-013 | DD-UNB-FIN-009 |
| Non-cash substantiation only as hypotheses | Medium | UNB-GAP-011, UNB-GAP-012, CNV-GRT-013 | DD-UNB-FIN-010 |
| No independent fee recomputation | Medium | CNV-FIN-002 | DD-UNB-FIN-011 |
| Retention period stated two ways | Medium | CNV-PLT-004, REQ-X-037 to REQ-X-045 | DD-UNB-FIN-012 |

### 4.8 Grants, charities and donors

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| Expenditure responsibility grants not explicitly blocked while the workflow is deferred | High | CNV-GRT-002, CNV-GRT-008 (deferred) | DD-UNB-GRT-001 |
| State charity standing beyond California | Low | CNV-GRT-015 | DD-UNB-CHV-001 |
| Death verification sources and executor access | Medium | CNV-ENT-001, AUTH-I5, UNB-GAP-015 | DD-UNB-DON-001 |

### 4.9 Operations, continuity, accessibility and exit

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| Support model, severity matrix and status page | High | UNB-GAP-028 (hypothesis), ADM-033 | DD-UNB-OPS-001 |
| Consent-based support access | Medium | CNV-ARC-002 | DD-UNB-OPS-002 |
| No single manual intervention register | High | CNV-GOV-006, CNV-PLT-007, UNB-XIN-IAM-005 | DD-UNB-OPS-003 |
| Key-person dependency | Critical | none | DD-UNB-BCP-001 |
| Business continuity program | High | UNB-OPS-001, SOC2-015 | DD-UNB-BCP-002 |
| Recovery objectives unapproved and stated two ways | High | CNV-ARC-001, UNB-RES-003, RR-UNB-RES-003-r2 | DD-UNB-BCP-003 |
| Rebuild after account compromise | High | UNB-GAP-034 | DD-UNB-BCP-004 |
| No accessibility conformance report | High | CNV-EXP-001, UNB-UX-006 | DD-UNB-A11Y-001 |
| Accessible PDF renderer not chosen | High | CNV-EXP-001, UNB-PLAT-003 | DD-UNB-A11Y-002 |
| Accessibility law applicability | Medium | UNB-GAP-031 (hypothesis) | DD-UNB-A11Y-003 |
| Accessible authentication with unselected proofing vendor | Medium | CNV-PLT-011 | DD-UNB-A11Y-004 |
| Inbound migration specification | High | CNV-EXP-002, UNB-RCN-WF-009 | DD-UNB-EXIT-001 |
| Export schema and independent reconstruction | High | CNV-ENT-002, RR-UNB-TEN-016-r1 (unvalidated, Deferred) | DD-UNB-EXIT-002 |
| Termination assistance and in-flight items | High | CNV-ENT-002 | DD-UNB-EXIT-003 |
| Customer escrow, wind-down plan and reserve | High | CNV-GOV-009 (dependency escrow only) | DD-UNB-EXIT-004 |
| Customer-held scheduled exports | Medium | CNV-ENT-002 | DD-UNB-EXIT-005 |
| Exit drill | Medium | CNV-ENT-002 | DD-UNB-EXIT-006 |

### 4.10 Baseline hygiene

| Gap | Severity | Existing | Proposed |
|---|---|---|---|
| Contradicted text not flagged unless listed in `amends` | Critical | CNV-GOV-007, CNV-GOV-011 | DD-UNB-GOV-001 |
| Strata runtime assumptions persist | High | CNV-ARC-004 | DD-UNB-GOV-002 |
| `UNB-RCN-*` prefix misread as financial reconciliation | Low | CNV-FIN-004 | DD-UNB-GOV-004 |

## 5. Verified internal contradictions in the baseline

Each item was checked against `unbound@9b38de47`. Quotes are exact and no longer than
one sentence.

1. **Sponsor investment pools.** `CNV-LEG-001`: "No sponsor-maintained investment pools
   SHALL be offered (OD-M-07)". `UNB-INV-003` (original, not amended): "Support pooled
   investment vehicles with fund-level units/shares, valuation dates, unit prices,
   subscriptions, redemptions, rounding, cash buffers and participant-level holdings."
   `UNB-INV-004`, `UNB-INV-022` and the 53 `UNB-NAV-*` records are likewise unamended
   (only `UNB-NAV-008` is amended, by `CNV-FIN-005`). Confirms batch 1 item. Proposed:
   DD-UNB-FIN-007.
2. **Trade execution.** `UNB-CUST-007` (original, not amended): "Execution APIs require
   separately validated contractual permissions and human authority." `CNV-LEG-001`
   forbids Unbound to "route orders for others' accounts". Confirms batch 1 item.
   Proposed: DD-UNB-FIN-008.
3. **Complex-asset intermediary model.** `UNB-RCN-WF-005` (adopted-provisional, not
   amended): "Each intermediary agreement MUST record its counsel-approved structure
   (donee model for release 1, RCD-034), which determines the donee of record and the
   acknowledgment, Form 8283/8282 and §4943 duties." `CNV-GRT-013`: "Complex-asset
   gifts expected to credit a DAF SHALL use the agent model". Confirms batch 1 item.
   Proposed: DD-UNB-GOV-001.
4. **Tenant isolation default.** `CNV-ARC-001` places the ledger in one cluster "with a
   schema and database role per sponsor tenant". `RR-UNB-PLAT-008-r1`
   (adopted-provisional, not amended): "The platform MUST support Profile B (dedicated
   database per tenant on shared managed infrastructure) as the default." `CNV-TEN-001`
   and `CNV-ARC-003` both still say "This clause depends on acceptance of the
   database-per-sponsor architecture decision", although each also describes the
   shared-cluster case. Confirms and extends batch 1 item. Proposed: DD-UNB-TEN-001.
5. **Document rendering.** `UNB-PLAT-003` (original, not amended) requires all
   enterprise documents to "use **Folio** where technically supported". `CNV-EXP-001`:
   "(Folio provides markup only; the PDF pipeline is Unbound-owned until an upstream
   renderer exists)". Confirms batch 1 item. Proposed: DD-UNB-A11Y-002.
6. **Recovery objective basis.** `UNB-RES-003` (original, not amended): "Every
   capability SHALL have defined RTO/RPO". `CNV-ARC-001`: "Recovery objectives SHALL be
   one versioned table keyed by data class and isolation profile". `CNV-ARC-001` amends
   `RR-UNB-RES-003-r1` but not the original. Confirms batch 1 item (the governing text
   is CNV-ARC-001, not RR-UNB-RES-003-r2, which is only proposed). Proposed:
   DD-UNB-BCP-003.
7. **Strata as runtime persistence.** `ACC-MDL-011` (original, not amended): "Use Strata
   in the approved persistence architecture; validate actual capabilities before mapping
   event store, journals, projections and integrity enforcement to Strata."
   `CNV-ARC-004`: "Authoritative append-only history SHALL be an Unbound-owned ledger
   component on managed PostgreSQL." The same unamended assumption appears in
   `UNB-ACC-026`, `UNB-CHAR-040`, `UNB-CUST-013`, `UNB-INV-042`, `UNB-NAV-044`,
   `UNB-NAV-051`, `SOC2-025` and `GOV-AUTH-022`, and in
   `unbound@9b38de47:architecture/CONTINUOUS-CONTROL-MONITORING-AND-EVIDENCE-ASSURANCE.md`
   line 35: "Strata is mandatory as an architectural persistence dependency, but its
   actual API capabilities have not been independently verified." Confirms batch 1
   item. Proposed: DD-UNB-GOV-002.
8. **CUEC list timing.** `UNB-XIN-ACC-009` requires the operator to "publish to each
   sponsor a list of complementary user-entity controls derived from that sponsor's
   configuration" but its release scope is `Deferred`, while `CNV-GOV-001` requires
   evidence engineering "with complementary user entity controls mapped" before live
   reliance. New finding. Proposed: DD-UNB-FIN-006.

### 5.1 Inconsistencies that are not strict contradictions

- **Retention floor.** `REQ-X-037` to `REQ-X-041`, `REQ-X-045`, `REQ-X-048` and
  `RR-REQ-X-036-r1` state a seven-year financial floor (for example `REQ-X-045`: "no
  bypass of financial seven-year floor"); `CNV-PLT-004` applies "the 10-year floor to
  all transaction-level financial and grant records" in release 1 and amends only
  `REQ-X-036`. A ten-year period satisfies a seven-year minimum, so this is not a logical
  contradiction, but an assessor quoting the older text gives the wrong period.
  Proposed: DD-UNB-FIN-012.
- **ACH debit rails.** `CNV-FIN-003` says "With no donor ACH debit origination in
  release 1", while `UNB-RCN-WF-001` requires an unknown-resolution protocol for each ACH
  debit collection rail. The latter is conditional on the rail existing; low risk.
- **Brand identity.** `UNB-EXP-002`: "Public identity SHALL be independently branded as
  Unbound, with transparent attribution to EF as its construction platform." Sponsor
  Brand Kits (`REQ-X-030`) and the Echelon default theme (`CNV-EXP-001`) leave the
  white-label attribution rule unstated. Proposed: DD-UNB-WLB-003.
- **Deferred scope cited as current design.** `UNB-XIN-SAS-011` (subprocessor register,
  Deferred) is cited by 39 in-scope questions and `RR-UNB-TEN-016-r1` (exit package,
  unvalidated, Deferred, amended by `CNV-ENT-002`) by 33. Answers built on them overstate
  release-1 scope. Proposed: DD-UNB-VEND-001, DD-UNB-EXIT-002.

### 5.2 Batch 1 items not confirmed as contradictions

- **Payment execution.** Batch 1 reported `CNV-LEG-001` ("SHALL NOT be able to execute a
  payment") as contradicting `UNB-XIN-REG-001`, `UNB-XIN-EVA-011` and `CNV-ARC-003`.
  `CNV-LEG-001` itself defines execution so that relaying a sponsor-authorized
  instruction under the sponsor's delegation is not execution by Unbound. The baseline is
  internally consistent; the open issue is whether banks and regulators accept that
  definition, which is a legal question (DD-UNB-LEG-001).
- **Superseded accounting text.** `UNB-XIN-ACC-002` (by `CNV-FIN-007`) and `UNB-ACC-004`
  and `UNB-ACC-012` (by `CNV-FIN-012`, with `RR-UNB-ACC-012-r1` adopted) are correctly
  marked through `converged_by`; they mislead only when cited without the clause (section
  6).
- **`UNB-RCN-*` prefix.** A naming hazard, not a contradiction (DD-UNB-GOV-004).

## 6. Superseded text that misleads assessors

The question bank and answer units are owned by other work streams and were not
modified. The following citations should be corrected by their owners.

| Amended record (cited without its clause) | Governing clause | In-scope questions affected |
|---|---|---|
| UNB-TEN-008 | CNV-TEN-001 | 40 |
| RR-UNB-TEN-016-r1 | CNV-ENT-002 | 33 |
| UNB-XIN-SAS-007 | CNV-ENT-002 | 29 |
| UNB-TEN-006 | CNV-TEN-001 | 28 |
| UNB-TEN-007 | CNV-TEN-001 | 25 |
| UNB-XIN-IAM-005 | CNV-PLT-007 | 24 |
| UNB-XIN-IAM-003 | CNV-PLT-003 | 18 |
| UNB-XIN-CLM-004 | CNV-GRT-012 | 17 |
| UNB-XIN-NPG-004 | CNV-GRT-014 | 16 |
| RR-REQ-X-032-r1 | CNV-PLT-005 | 14 |
| UNB-TEN-003 | CNV-TEN-001 | 13 |
| UNB-RCN-FIN-001 | CNV-PAY-006 (deferred) | 13 |
| REQ-X-020 | CNV-ARC-001 | 13 |
| UNB-XIN-SAS-001 | CNV-GOV-006, CNV-LEG-002 | 12 |
| UNB-TEC-STRATA-004 | CNV-ARC-004 | 12 |
| UNB-XIN-EVA-005 | CNV-PAY-005, CNV-PAY-007 | 12 |
| REQ-X-005 | CNV-PAY-001 | 10 |
| UNB-XIN-OTH-003 | CNV-PAY-001 | 10 |
| UNB-INV-031 | CNV-LEG-001 | 10 |

In total 59 distinct amended records are cited without their governing clause across 457
questions. The unamended contradictions in section 5 mislead even when cited correctly,
because nothing in the baseline flags them; DD-UNB-GOV-001 proposes a register that
does.

## 7. Dependencies on unverified Echelon capabilities

| Unbound dependency | Unbound records | Verified state (DD-ARC-002) | Effect on answers | Proposed |
|---|---|---|---|---|
| Strata runtime persistence, append-only guarantees, ordering and integrity | UNB-NAV-051, ACC-MDL-011, UNB-ACC-026, SOC2-025, monitoring architecture line 35 | Strata is schema compile, diff and deploy for PostgreSQL 16 only; no runtime typed query interface | Ledger immutability and SEC-DB-001 answers must cite an Unbound-owned component that does not yet exist | DD-UNB-GOV-002, DD-UNB-FIN-005 |
| Strata version support gating database upgrades | CNV-ARC-004 | PostgreSQL 16 only | Risk of stranding on an unsupported major version | DD-UNB-GOV-002 |
| Runtime security monitoring | MON-* (control monitoring), SOC2-012 | No Echelon system provides it (Vigila is a task organizer; Aegis is fault handling) | Detection and response answers are unknown | DD-UNB-SEC-015 |
| Evidence and build signing, ledger anchoring | CNV-PLT-010, UNB-DATA-012, CNV-AIO-001 (signed build) | Partial: Praxis DSSE receipts and Strata artifact signing; Tutela evidence is digest only; key management deferred; Praxis identity is asserted | Signed provenance and tamper-evidence answers cannot be verified | DD-UNB-SEC-011, DD-UNB-FIN-005 |
| SAST and rule registry | SOC2-016 | No F# SAST exists; Tutela is the security authority; Aegis is not a scanner | Static analysis answers must describe compensating analyzers | DD-UNB-SEC-009 |
| Limen embeddable roots | ADR-M-03, INT-015 | Limen lacks element or shadow-root roots | Embedded component answers remain interim | DD-UNB-WLB-002 |
| Folio accessible PDF | UNB-PLAT-003, UNB-ACC-025 | Folio provides markup; no tagged PDF or PDF/UA | Accessible document answers are unknown | DD-UNB-A11Y-002 |
| Commercial license for components | CNV-GOV-009 | Nearly all components PolyForm Noncommercial 1.0.0 | Licensing and escrow answers blocked | DD-UNB-VEND-003, DD-UNB-EXIT-004 |

## 8. Open items for other work streams

- Question bank: add a question on scheduled and recurring contributions (none exists;
  DD-UNB-FIN-001 originates from the nearest questions).
- Source register: IRS information return and Form 8283/8282 instructions are cited as
  needed but absent (DD-UNB-FIN-004 and DD-UNB-FIN-010 carry notes).
- Answer owners: replace `UNB-CTRL-*` and `UNB-SCTRL-*` identifiers in `requirements`
  fields with baseline requirement IDs or move them to a controls field, and add
  governing clauses to the citations in section 6.
- Recommendations to the Unbound repository belong in `recommendations/`; this document
  does not modify Unbound.
