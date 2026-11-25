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

## Scanner validation and external assurance (DD-SCN-001, DD-EXT-001, DD-COST-001/002)

- No mature open-source SAST analyzes F# source (Semgrep, Opengrep, CodeQL, Roslyn,
  Security Code Scan: none support F#). Language-independent tools (OSV-Scanner, Syft,
  Grype, Gitleaks, Trivy, ZAP, Nuclei, Schemathesis, garak, PyRIT) apply unchanged.
- FSharp.Analyzers.SDK (MIT) exposes typed compiler information and emits SARIF; rule
  analyzers for SEC-* are feasible; full F# taint analysis is research-scale.
- Semgrep rules license (since 2024-12-13) restricts use to internal, non-competing,
  non-SaaS; engine remains LGPL-2.1. CodeQL is not free for private repositories.
- No general scanner accreditation exists; NIST SATE V explicitly disclaims tool
  rating. Approved-vendor requirements are activity-specific: PCI ASV (11.3.2), FedRAMP
  3PAO, DORA TLPT. PCI pen testing allows qualified internal resources with
  organizational independence (text verified from SAQ D v4.0; v4.0.1 PDF license-gated).
- SOC 2 does not itself mandate penetration testing (secondary source; AICPA text not
  retrieved; verify).
- Real-world SAST detection is far below benchmark scores (Li et al. 2023: 12.7 percent;
  Lipp et al. 2022: 47 to 80 percent missed).
- Recommended ownership: Tutela owns rule registry, F# analyzers, findings normalization
  and benchmark; Praxis runs gates and provenance; Dokimos measures; Folio renders.
- Public cost data is weak; only GSA CALC+ ceiling labor rates, BLS wages, GAO FedRAMP
  ranges and labeled vendor marketing are available.
- PCI applicability to Unbound is unestablished; if card data never touches Echelon
  systems ASV scans are likely avoidable (card contributions deferred per CNV-PAY-008).

## VUL, PEN, SCN, MON, IR question batch

196 questions, 47 answer units (36 proposed-target-state, 9 unknown, 1 not-applicable,
1 partially-implemented: ANS-MON-008 relies on Praxis agent attribution for repository
changes; review in adversarial pass whether that overstates production logging).

Unseeded sources needed: RFC 9116; NIST SP 800-40 Rev. 4; NIST SP 800-92 (and r1 draft);
NIST SP 800-86; NIST SP 800-216; CISA BOD 20-01; CISA SSVC; CISA #StopRansomware guide;
OFAC 2021 ransomware advisory; OMB M-21-31; CIRCIA; NAIC Insurance Data Security Model
Law; Interagency Guidance on Response Programs (Supplement A to the GLBA safeguards
guidelines).

Gaps: no VDP, SECURITY.md or security.txt in any Echelon repository; no security
scanning in Praxis CI; no owner for SAST or runtime monitoring; no security log
retention period (SOC2-023 forbids inventing one; IR-008 proposes seven years as an
open question); no named security officer, IR retainer, breach counsel, cyber insurance
or 24x7 coverage; incident history of corporate systems unknown. Target SLAs (KEV 7
days, critical 15 days, customer notice within 24 hours of reasonable suspicion) are
research recommendations pending owner decision.
