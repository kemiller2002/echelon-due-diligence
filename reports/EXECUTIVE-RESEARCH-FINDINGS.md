---
id: DD-RPT-EXEC-001
title: Executive research findings
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [executive, findings]
---

# Executive research findings

Research phase, session 1 (2026-11-25), Praxis work item `DD-RESEARCH-2026-001`.
Nothing here is a customer-facing claim. Full traceability is in
`reports/DELIVERABLES-INDEX.md`.

## The answer in one paragraph

Echelon now knows, question by question, what it can and cannot say to a customer, and
the honest answer today is that it can prove almost nothing. Of 522 answer units
covering 2,380 canonical questions, none is verified operational. Most are proposed
target states, many are unknown, and none has been approved by a human for customer
release. That is the correct starting point, not a failure: Unbound is unbuilt and
Echelon is pre-revenue. The research shows the gap to being assessable is dominated by
**organizational facts and decisions that are cheap to close** (entity formation, IP
assignment, licensing, policies, MFA and repository controls, insurance, counsel
opinions), not by engineering. Security by construction is a real potential advantage,
but no bank, auditor or insurer will credit it until it is scoped, reproducible and
independently tested; marketing it early would do more harm than not claiming it.

## What was built

| Asset | Scale | Location |
|---|---|---|
| Canonical question bank | 2,380 materially distinct questions, 67 categories, real-world wording as alternatives | `questions/` |
| Answer units | 522, each separating current practice, intended practice, what is provable and what may be said | `answers/` |
| Controls and evidence requirements | 640 controls, 596 evidence requirements | `controls/`, `evidence-requirements/` |
| Source register | 405 sources, versions and licensing verified at issuers where accessible | `sources/` |
| Validator and registers | F# build tool enforcing schemas, referential integrity, "no aspirational claim as current fact", statement wording lint, human review gate, em dash ban | `tools/build.fsx`, `reports/generated/` |
| Adversarial reviews | 207 objections from 10 perspectives | `validation/` |
| Unbound gap analysis | 104 proposed requirements (29 P0), 8 verified baseline contradictions | `product-profiles/unbound/`, `gap-analysis/` |

## Key findings

1. **Most customer requirements are not law.** Of the canonical questions, about 8
   percent are classified legal-regulatory and about 3 percent supervisory guidance; the
   rest are industry convention, customer preference, contractual convention or
   certification criteria (`reports/generated/REGISTER-SUMMARY.md`). This is where
   alternatives to conventional controls are possible, and also where acceptance depends
   on persuasion rather than compliance.
2. **Obligations already in force for Unbound's design.** OFAC applies directly to
   Echelon. Nacha's fraud monitoring rule (Phase 2, June 2026) applies to all third-party
   service providers, which is Unbound's designed role (CNV-PAY-001). State breach
   notification laws will apply once donor data is held. Most other obligations flow down
   from customers by contract or apply only to certain customer types
   (`reports/generated/regulatory-applicability-matrix.csv`).
3. **The largest legal unknown** is whether Echelon or its sponsors are "financial
   institutions" under GLBA and the FTC Safeguards Rule. The answer changes several
   policies from optional to mandatory (OQ-DD-POL-001).
4. **The Secure Construction Standard assigns work to systems that do not do it.** Aegis
   is a fault-handling library, Vigila a task organizer; Tutela is the actual security
   authority. No Echelon system provides typed runtime database access (SEC-DB-001
   depends on it), runtime security monitoring, F# security analysis or SBOMs
   (`architecture/ECHELON-SYSTEM-CAPABILITY-ANALYSIS.md`).
5. **No mature tool scans F# for security issues**, but the gap is narrow: rule-level
   analyzers on the MIT-licensed FSharp.Analyzers.SDK plus compiled-assembly checks would
   cover the Standard's rules. Scanners carry no general accreditation; approved vendors
   are required only for specific activities such as PCI ASV scans and FedRAMP
   (`scanner-validation/`).
6. **Security by construction is credible in a narrow scope.** Elimination (L1) is
   plausible only for SQL injection, OS command and code injection, unsafe
   deserialization and memory corruption, only within server-side F# assemblies, and
   only with a compiled-reference gate. The architecture's largest advantage is in
   classes scanners rarely find: missing authorization, tenant isolation, idempotency,
   workflow integrity and money arithmetic. It adds little for vulnerable dependencies,
   secrets and configuration. PostgreSQL trusted code, F# compiler defaults and .NET 8
   end of support (Strata, Ordo) are concrete bypasses to close
   (`security-by-construction/`).
7. **Independent assurance cannot be avoided, only made cheaper later.** Every financial
   perspective expects an independent penetration test, SOC 2 and, for sponsors relying
   on Unbound for financial records, SOC 1. The first architecture-informed pen test will
   likely cost more, not less; savings are hypotheses for later cycles
   (`cost-avoidance/`, DD-VAL-ADV-001).
8. **No reviewer would pass Echelon or Unbound today**, across all ten adversarial
   perspectives. The knowledge base was judged candid; the blockers are organizational:
   unverified basics, PolyForm Noncommercial licensing of every component, commitments
   one person cannot meet, and almost no planned independent evidence (565 of 595
   evidence requirements were first-party before the fix pass) (`validation/`).
9. **DAF sponsors publish no vendor security requirements.** Their expectations are
   inferred from affiliated financial institutions (Fidelity, Morgan Stanley, Truist
   publish detailed supplier requirements). An incumbent administrator publicly cites
   only a SOC 2 Type 1, so the market bar may be low, which is both an opportunity and a
   reason not to overinvest before demand is proven
   (`industry-profiles/donor-advised-funds/`).
10. **Unbound's requirements are deep on financial correctness and thin on security
    operations.** Insurance, secure SDLC, vulnerability management, scanning, cloud
    hosting, escrow, subprocessors, encryption and AI security have few or no
    requirements. Eight verified internal contradictions (for example investment pools,
    tenant isolation default, Strata as runtime persistence) would mislead an assessor
    (`gap-analysis/UNBOUND-REQUIREMENTS-GAP-ANALYSIS.md`).
11. **AI-built software is a disclosure obligation, not a footnote.** Echelon builds with
    AI coding agents; customers (Morgan Stanley's supplier standards explicitly) expect
    disclosure. Agent attribution in Praxis is self-declared, not authenticated; branch
    protection and human review of agent code are not yet evidenced.

## What to do next

Follow `reports/PRIORITIZED-IMPLEMENTATION-ROADMAP.md`. In order: complete the owner
fact checklist; finish formation and IP assignment; decide licensing; publish a
vulnerability disclosure policy; obtain counsel opinions; adopt truthful minimal
policies; correct the Standard; then build evidence generation into engineering and
Unbound's P0 requirements.

## Limits of this research

- Agent-produced records have not been human-reviewed; the review gate marks all of them
  unreleasable.
- Customer acceptance of unconventional approaches is unvalidated; no buyer was
  consulted.
- Cost data is weak; savings are hypotheses.
- Several recent regulatory items should be reverified by counsel before use (BL-023).
- Diminishing returns have not yet been demonstrated by a second questionnaire sampling
  pass (BL-013).
