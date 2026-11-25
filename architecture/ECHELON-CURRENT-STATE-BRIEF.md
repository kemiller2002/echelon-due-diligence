---
id: DD-ARC-001
title: Echelon current-state brief for due diligence answering
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
---

# Echelon current-state brief (as observed 2026-11-25)

Purpose: give every research agent the same verified baseline so that answer statuses
are honest. Each fact cites `repository@commit:path`. Anything not listed here is
`unknown` until verified. The capability analysis in
`architecture/ECHELON-SYSTEM-CAPABILITY-ANALYSIS.md` supersedes this brief where they
differ.

## Organization

- Echelon Foundry, LLC is an Indiana LLC under formation/administration
  (`echelon-organization-administration@2763e576:entities/echelon-foundry/`). Ownership,
  headcount, financial statements, insurance and adopted policies are not established in
  public records reviewed here. Treat organizational answers as `unknown` or
  `proposed-target-state`.
- The only security policy located is the **Echelon Secure Construction Standard v0.1**,
  status "Proposed organizational standard; implementation and external acceptance not
  yet verified" (`echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md`).
  Rule IDs: SEC-DB-001, SEC-UI-001, SEC-UI-002, SEC-LANG-001, SEC-LANG-002,
  SEC-EXEC-001, SEC-DATA-001, SEC-CRYPTO-001, SEC-AUTH-001, SEC-SUPPLY-001. Adoption
  status: `approved-policy-implementation-pending` is NOT accurate; use
  `proposed-target-state` because formal adoption is explicitly unestablished.
- The business plan (`business-plan/`) describes intended governance, vendor
  governance, insurance and AI governance; it is a plan, not evidence of operation.

## Unbound (DAF administration platform)

- Requirements only. `unbound@9b38de47`. 1,653 baseline records
  (`requirements/baseline/baseline.jsonl`), 82 convergence clauses (`CNV-*`), a master
  enterprise control matrix of 90 controls `UNB-CTRL-*` all with status `Designed` and
  operating evidence, test execution and auditor review all `No`
  (`requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv`).
- SOC 2 readiness directive `SOC2-001`..`SOC2-036`
  (`requirements/governance/SOC2-CONTROLS-EVIDENCE-AND-ENTERPRISE-DIRECTIVE.md`): a design
  directive, explicitly not a claim of SOC 2 compliance.
- Continuous control monitoring architecture
  (`architecture/CONTINUOUS-CONTROL-MONITORING-AND-EVIDENCE-ASSURANCE.md`): specified, not
  implemented or audited.
- Payment role decision `CNV-PAY-001`: the sponsor originates payments; Unbound acts as a
  third-party service provider (TPSP) in Nacha terms.
- No production system, no customers, no SOC report, no penetration test, no ISO
  certificate exist. All Unbound operational answers are at best `proposed-target-state`.

## Echelon systems (verified purpose differs from the Standard's proposed ownership)

| System | Verified purpose (README/charter) | Implication |
|---|---|---|
| Praxis (`praxis@12bf9951`) | Repository operating system: work protocol, provenance, research records, validation, CI workflow. v3.25.0 | Candidate for governance and change evidence; not a security scanner |
| Aegis (`aegis@711e0260`) | Operational fault handling library for .NET (capture, recovery, redaction, escalation). NuGet packages | NOT a security rule registry or SAST orchestrator, contrary to the Standard's proposal |
| Tutela (`tutela@476dc682`) | Security engineering discipline: assets, trust boundaries, threats, invariants, controls, evidence, release posture | Dokimos requirements name Tutela as the security authority (`dokimos@6ea86246:requirements/REQUIREMENTS.md` line 118) |
| Dokimos (`dokimos@6ea86246`) | Evidence-based code-quality measurement with longitudinal observations | Security analysis routes to Tutela; scanner benchmarking role is unverified |
| Strata (`strata@c6a384ec`) | Declarative PostgreSQL schema management (compile, diff, deploy), pilot status, PG16 only | No verified runtime typed query interface; SEC-DB-001 depends on a capability not found |
| Limen (`limen@743cdb9b`) | Browser kernel/engine boundary library; only serializable data crosses | Supports SEC-UI-002 |
| Forma (`forma@c8f40b4c`) | Zero-runtime CSS design system with accessibility contracts | Supports accessibility; not an input-validation library |
| Folio (`folio@56a18e1f`) | Print/PDF component system | Candidate for report rendering |
| Vigila (`vigila@feab7551`) | Personal and business follow-up/task organizer | NOT runtime monitoring, contrary to the Standard's proposal |
| Ordo (`ordo@db6d39ed`) | State-Directed Engineering method (application state legality) | Candidate for explicit-state verification |
| Echelon Knowledge Store (`echelon-knowledge-store@35d9cee0`) | Research phase; recommends Markdown with front matter canonical plus compiled registries | Shapes this repository's record format |
| Echelon Registry (`echelon-registry@f9ea4d0b`) | Capability discovery specification | Integration model for evidence producers |

## Answering rules derived from this brief

- No answer may claim a certification, audit, pen test, insurance policy, named
  security officer, background check program, incident history, uptime record or
  customer count. Use `unknown` and an open question.
- Architectural intentions from the Standard and Unbound requirements are
  `proposed-target-state`, cite them, and set `customer_statement_kind` to `planned`.
- Where Echelon tooling genuinely exists (for example Praxis provenance, Limen boundary,
  Strata schema diff), the answer may describe it as an existing tool but must say that
  it is not yet operated for a production Echelon service.
