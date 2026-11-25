---
id: DD-COST-001
title: Penetration testing cost reduction strategy for the planned independent Unbound test
status: draft
version: 0.2.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, penetration-testing, cost-avoidance, unbound, independence]
related_documents:
  - external-assurance/EXTERNAL-ASSURANCE-REQUIREMENTS-MATRIX.md
  - scanner-validation/SCANNER-VALIDATION-RESEARCH-REPORT.md
  - cost-avoidance/COMPLIANCE-COST-AVOIDANCE-REPORT.md
  - sources/assurance-testing.jsonl
---

# Penetration testing cost reduction strategy

## 1. Context

The proposed Echelon Secure Construction Standard keeps an external penetration test
planned for Unbound and requires Echelon to "provide external testers with threat
models, rules, evidence and residual attack surfaces; agree scope without suppressing
independent discovery" (`SRC-ECH-SCS-0.1`). Unbound's SOC 2 directive SOC2-016 requires
penetration testing programs to record findings, prioritization, fixes, exceptions and
retest evidence (`SRC-ECH-UNB-SOC2-016`). Unbound has no production system today, so
there is no test to reduce yet; this document defines how to buy the first one well.

Cost basis: there is no credible independent public price list for penetration tests.
GSA CALC+ federal ceiling rates for labor categories containing "penetration" had a
median of $157.03 per hour (p25 $125.86, p75 $196.59, n=445) on 2026-11-25
(`SRC-GSA-CALC`). A testing vendor's marketing page quotes $15,000 to $50,000 for
human-led external network plus authenticated web testing (`SRC-VENDOR-SOFTWARESECURED-PENTEST-COST`,
VENDOR MARKETING). Because test fees scale mainly with tester-days, the levers below
target tester-days spent on low-value work. Every saving is a hypothesis until measured.

**The first test is expected to cost more, not less (revised 2026-11-25, BL-018).** The
scope Echelon itself specifies in ANS-PEN-002 is larger than a conventional web
application test: architecture-informed testing with explicit objectives to bypass
claimed structural controls, the Limen browser boundary and WebAssembly guest
tampering, Strata-backed data access and deploy-path RLS removal, intra-tenant and
cross-tenant authorization, payment and grant business logic including race
conditions, AI agent tool authority, server-side document rendering, cloud
configuration and an assumed-breach perspective (compromised workforce, CI or agent
credentials). The first engagement should therefore be budgeted above the
conventional range cited above, and a white-box structural review of the L1 to L4
claims is a separate cost on top of it (a black-box pen test cannot confirm those
claims). The levers below are hypotheses about cost per meaningful finding and about
later test cycles, once a baseline exists; none is a reduction of the first
engagement.

## 2. Non-negotiable constraints

1. **Independence stays intact.** The tester chooses techniques, may test outside the
   suggested focus within the authorized scope, and reports every finding. Echelon does not
   pre-approve or edit findings. If the test must also satisfy PCI DSS 11.4, the tester must
   be organizationally independent and qualified (`SRC-PCI-DSS-V4-SAQ-D`).
2. **Completeness is not traded for price.** Scope reduction removes duplicated or
   unnecessary work, never in-scope assets. All internet-facing and tenant-reachable
   surfaces of the release under test stay in scope.
3. **No suppression by documentation.** Supplying threat models and known-issue lists must
   not be framed as "these are handled, skip them". The rules of engagement should state
   that supplied material is orientation, not exclusion.
4. **Labeling.** Internal testing and automated evidence are first-party. Only the external
   report is described as independent.

## 3. Levers (later-cycle hypotheses)

Each lever's effect is a hypothesis to be measured against the first test as baseline; the expected benefit is a lower cost per meaningful finding or fewer tester-days in later cycles, not a cheaper first test.

| # | Lever | Mechanism | Effect on tester-days | Independence risk | Control |
|---|---|---|---|---|---|
| P1 | Small attack surface by construction | Strata as the only data path, Limen as the only JavaScript path, no user HTML, few exposed endpoints | Fewer endpoints and sinks to enumerate (hypothesis) | None | Only claims backed by L0 structural evidence (DD-SCN-001 section 8) |
| P2 | Gray-box test with documentation | Architecture, data flow, authorization model, OpenAPI schema, roles matrix, test tenants and accounts supplied before kickoff | Less discovery time; more time on authorization and money movement | Low | Tester may still test black-box paths |
| P3 | Threat model handover | Tutela threats, invariants, trust boundaries and residual risks given to tester | Focus on highest-impact abuse cases | Medium if used to steer away | Rules of engagement say threat model is input, not limit |
| P4 | Pre-test hygiene | Run OSV-Scanner, Trivy, Gitleaks, ZAP baseline, Nuclei, Schemathesis and fix results before the test | Tester does not bill for scanner-class findings (hypothesis) | None | Share scan reports so tester can verify |
| P5 | Known issues register | List accepted risks and open findings with IDs | Avoid re-reporting known items | Medium | Tester may re-rate severity; known issues still appear in report |
| P6 | Stable, production-like environment | Dedicated test environment with seeded data, reset scripts, no blocking WAF rules for tester IPs (unless testing the WAF is in scope) | Less lost time | Low: the test does not measure the deployed defense | Document any differences from production; include one phase with the production WAF configuration enabled and report both |
| P7 | Focus on authorization and financial invariants | Provide policy model and invariants (balanced journals, idempotent disbursements, separation of duties, tenant isolation) | Higher-value findings per day | Low | Tester designs own cases |
| P8 | Shared component reuse across products | Test shared Echelon components once per version; later product tests reference that report | Avoid retesting identical builds (later cycles only) | Low if versions match exactly | Restricted to library-level findings; every product test still includes composition tests of the reused component (for example Limen with a given F# engine and server API) |
| P9 | Fixed-fee retest included | Negotiate retest of findings within a window | Avoid separate retest engagement | None | Retest by same firm |
| P10 | Multi-year engagement with rotation plan | Same firm for continuity, rotate testers or firm periodically | Faster ramp-up (hypothesis) | Medium: familiarity | Rotate individuals; periodic firm change (DORA uses external testers every three tests as one benchmark for rotation, `SRC-TIBER-EU`) |
| P11 | Combine scopes into one test window | Web, API and cloud configuration reviewed together | Shared setup | None | Scope document lists each target |
| P12 | Bug bounty or disclosure program after launch | Continuous external discovery | May lengthen time between full tests only where contracts allow | Medium | Never replaces contractual annual test |

## 4. What not to cut

- Authenticated testing of every role, including cross-tenant attempts.
- Business logic around grants, disbursements, fees and approvals.
- AI agent tool-use paths and their authority limits.
- Administrative and support interfaces.
- Retest of fixed findings.

## 5. Evidence package to give the tester

1. Scope document with asset inventory, release identifier and commit hashes.
2. Architecture and data flow diagrams; trust boundaries.
3. Threat model and security invariants from Tutela, with residual risks.
4. Authorization model and roles matrix; test accounts per role and tenant.
5. API schemas.
6. Latest automated scan outputs (SARIF) and the scanner validation report, including known
   blind spots (for example F# rules not yet built).
7. Known issues register.
8. Rules of engagement that preserve independent discovery.

## 6. Measurement plan

Record for each test: tester-days quoted and used, days spent on discovery versus
exploitation, findings by severity and by class, findings that automated layers should
have caught (feeds scanner improvement), retest outcomes, and total internal hours. Compare
against the first test as the baseline. No percentage saving is claimed in this document,
and the first test is expected to cost more than a conventional web application test
(section 1); savings, if any, are hypotheses for the second and later cycles.

## 7. Risks

- Testers anchoring on supplied threat models (mitigation: P3 control, ask tester to
  report areas explored outside the threat model).
- Over-reliance on architecture claims that are not yet true (mitigation: only cite
  structural controls with build evidence).
- Customer rejection of reused component reports (mitigation: ask customers in advance).
- Cheapest quote bias: price below market often means scanner-led tests (vendor marketing
  itself distinguishes automated from human-led tiers).

## 8. Open questions

- Will PCI, FedRAMP or any customer contract govern the Unbound test? This sets tester
  qualification and independence needs.
- Which qualifications will Echelon ask for (for example CREST company accreditation,
  OSCP or GIAC staff)? None is mandated by PCI.
- What retest window and report format do target customers require?
