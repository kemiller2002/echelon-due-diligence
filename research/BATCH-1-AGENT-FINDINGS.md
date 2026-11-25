---
id: DD-RES-B1-001
title: Batch 1 research agent findings log
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
---

# Batch 1 findings log

Condensed findings reported by batch 1 research agents, kept so later work (gap
analysis, adversarial review, source register completion) can act on them. Agent reports
are model output; each item below must be checked against the cited repository record
before it is relied upon.

## System capability analysis (DD-ARC-002)

- SEC-DB-001 runtime typed database access: no provider exists (Strata is schema
  compile/diff/deploy only, PG16, 0.1.1).
- No runtime security monitoring exists in any Echelon system.
- Evidence signing partial (Praxis DSSE receipts, Strata artifact signing); Tutela
  evidence digest-only; key management deferred.
- No release carries an SBOM; GitHub build provenance attestations exist in several
  release workflows.
- Nearly all Echelon tools are PolyForm Noncommercial; Standard prefers MIT. Customer,
  auditor and escrow rerun rights are unaddressed.
- Unbound monitoring architecture assumes Strata as persistence layer; unverified.

## RCN, CUS, INV, FEE, RRP question batch

Unseeded sources needed (to add to the register): IRS General Instructions for Certain
Information Returns and 1099-MISC/NEC/K instructions; IRS Form 8283 and 8282
instructions; Form 990 Schedules I, F, L; Form 990-T; IRC 4943; FASB ASC 820; Investment
Company Act 3(c)(10) and 7(e); Advisers Act custody rule 206(4)-2; GIPS; Exchange Act
3(e)(2).

Contradictions in Unbound (verify, then record in the Unbound gap analysis):
1. `CNV-LEG-001` (no sponsor-maintained pools; values from the sponsor's external
   manager per `CNV-FIN-005`) versus `UNB-NAV-001..053` and `UNB-INV-003/004/022`
   (full NAV and unitization engine).
2. `UNB-CUST-007` execution APIs versus `CNV-LEG-001` prohibition on routing orders.
3. `UNB-RCN-*` are requirement-reconciliation clauses, not financial reconciliation; the
   prefix invites misreading by assessors.

Gaps: Form 1099 support; UPMIFA analysis; advance notice of fee increases; vendor
related-party disclosure; Unbound's own published CUEC list (`UNB-XIN-ACC-009` requires
it); reconciliation tolerances, sampling, materiality, retention periods, acknowledgment
templates, state unclaimed property rule table. Open Unbound items: `TVR-ORG-003-Q`,
`TVR-CMP-004-Q`, `CNV-LEG-002` California interpretation, `UNB-NAV-051` reliance on
unverified Strata append-only capability.
