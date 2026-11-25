---
id: DD-GAP-SYS-001
title: Echelon system capability gaps for secure construction and due diligence evidence
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [gap-analysis, due-diligence, evidence, secure-construction]
related_documents:
  - architecture/ECHELON-SYSTEM-CAPABILITY-ANALYSIS.md
  - architecture/EVIDENCE-ARCHITECTURE-SPECIFICATION.md
  - recommendations/system-recommendations.jsonl
---

# Echelon system capability gaps

This register lists every capability the Echelon Secure Construction Standard v0.1
(`echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md`)
and the due diligence evidence mission need, compared with what the repositories
verified in `architecture/ECHELON-SYSTEM-CAPABILITY-ANALYSIS.md` (DD-ARC-002) actually
provide. Citations for each "current provider" are in DD-ARC-002; key paths are
repeated here.

Status values: `implemented` (source and tests at HEAD), `released` (Registry release
record), `partial`, `experimental`, `specified` (requirements only), `absent`.
Priority: P0 blocks honest answers or the Standard's core rules; P1 needed before any
Unbound production release or customer evidence package; P2 improves evidence quality;
P3 optional.

Recommended owners follow two rules: prefer extending an existing system over a new
one, and keep security meaning in Tutela as all three of Tutela, Dokimos and the
organization's application-governance document already require
(`tutela@476dc682:docs/SECURITY-OWNERSHIP.md`;
`dokimos@6ea86246:requirements/REQUIREMENTS.md` R8;
`echelon-organization-administration@2763e576:application-governance/AEGIS-FORMA-FOLIO-COMPLIANCE.md`).

## Gap register

| ID | Capability | Needed for | Current provider | Status | Gap | Recommended owner | Priority |
|---|---|---|---|---|---|---|---|
| GAP-SYS-001 | Correct system ownership in the Standard | All SEC-* rules; every answer that names an owner | Standard "Proposed system ownership" | specified, incorrect | Aegis, Vigila, Forma and Strata roles do not match repositories; Tutela and Ordo are absent (DD-ARC-002 section 4, D1 to D13) | echelon-organization-administration | P0 |
| GAP-SYS-002 | Typed parameterized runtime database access with fixed approved query definitions | SEC-DB-001 | None. Strata is build-time schema tooling (`strata@c6a384ec:README.md`) | absent | No library, query definition format or runtime enforcement exists anywhere; SEC-DB-001 is unsatisfiable today | Strata (extend with an application data access package that consumes the compiled artifact), subject to an explicit decision; otherwise amend SEC-DB-001 | P0 |
| GAP-SYS-003 | Build-time validation of application SQL against the schema | SEC-DB-001 (approved query definitions) | Strata `validate`, `validate --types`, `check` | released (pilot, PG16) | Not wired to application repositories; not emitted as signed evidence; plpgsql bodies are `unverifiable` | Strata | P1 |
| GAP-SYS-004 | Detection of dynamic SQL and data-access bypass in F# code | SEC-DB-001 "semantic checks for bypasses" | None | absent | No analyzer for string-built SQL or direct driver use outside an approved interface | Rule definitions: Tutela. Analyzer adapter: Dokimos (FCS experiment exists at `dokimos@6ea86246:experiments/rule-provenance/`) | P1 |
| GAP-SYS-005 | Machine-readable registry of SEC-* rules (owner, version, scope, CWE, enforcement, negative tests, evidence requirements, residual risks, failure behavior) | Standard "Enforcement model"; all SEC-* rules | Tutela gate rules `TUTELA-G*` and `TUTELA-SD-*` only (`tutela@476dc682:src/Tutela.Core/Rules.fs`) | partial | SEC-* rules have no machine-readable definition anywhere | Tutela | P0 |
| GAP-SYS-006 | F# semantic security analysis (unsafe interop, reflection, dynamic loading, process launch, incomplete matches) | SEC-LANG-001, SEC-LANG-002, SEC-EXEC-001 | Compiler warnings as errors are possible but not verified across repos; lexical checks in Limen and Dokimos | absent | No FCS-based security analyzer; Dokimos AST work is experimental and about business-rule provenance | Rules: Tutela. Analyzer: Dokimos analyzer adapter | P1 |
| GAP-SYS-007 | SAST, SCA and secret scanning orchestration and result intake (SARIF) | SEC-SUPPLY-001, SEC-CRYPTO-001, scanner validation section | Tutela `scan-secrets` on Tutela only; EKS dependency review only (`echelon-knowledge-store@35d9cee0:.github/workflows/dependency-review.yml`) | partial | Tutela records that no portfolio repository runs secret scanning, dependency review or CodeQL (`tutela@476dc682:docs/SECURITY-OWNERSHIP.md` line 47); no SARIF intake into Tutela evidence | Tutela (intake, interpretation); Praxis or Conditor-installed CI templates (execution) | P0 |
| GAP-SYS-008 | Scanner benchmarking (precision, recall by weakness class; SARD, OWASP Benchmark, F# fixtures, holdouts) | Standard "Scanner validation"; assurance deliverable 1 | None; Dokimos verification benchmarks are a different subject | absent | No harness, fixtures or results | Dokimos (measurement owner) with Tutela-defined weakness classes | P2 |
| GAP-SYS-009 | SBOM generation per release | SEC-SUPPLY-001; TUT-0905 | Registry schema slot and draft REG-DIST-164 only | specified | No release carries an SBOM | Each releasing repository's release workflow; Registry validates references (REG-DIST-170) | P1 |
| GAP-SYS-010 | Build provenance attestation for every released artifact | SEC-SUPPLY-001; build artifact hashes | GitHub attestations in Praxis, Strata, Dokimos, Ordo, Limen, Folio | partial | Not found for Aegis, Forma, Tutela; attestation references not recorded in Registry release records | Releasing repositories; Registry records refs | P1 |
| GAP-SYS-011 | Release artifact hash and commit binding | Build artifact hashes, source commit hashes | Registry release records (`echelon-registry@f9ea4d0b:releases/`) | released | No Unbound releases exist; release records are not linked to evidence records | Echelon Registry | P2 |
| GAP-SYS-012 | Digital signature of evidence records | Standard "Sign evidence"; digital signatures | Praxis trusted verifier (DSSE receipts), Strata artifact signing | partial | Tutela evidence unsigned; no general evidence signing; no key custody, rotation or revocation | Praxis (extend trusted verifier to sign evidence records); Tutela (require and verify signatures in gate) | P1 |
| GAP-SYS-013 | Signing key management (custody, rotation, revocation list, trust root publication) | Digital signatures, revocation | None (`praxis@12bf9951:docs/agent-provenance.md` defers key management) | absent | No key registry or published verifier keys | Tutela trust root (`security/` policies) for key authorization; operational custody is an organizational decision | P1 |
| GAP-SYS-014 | Reviewer identity bound to a verified platform identity | Reviewer identity | Tutela exception `boundIdentity` (GitHub numeric subject id) | partial | Only exceptions and trust-root changes use bound identity; Praxis actor identity is asserted | Tutela | P1 |
| GAP-SYS-015 | Evidence expiration and staleness | Expiration | Tutela `validUntil`, Stale state (TUT-0605, TUT-1304) | implemented (schema and gate) | No link to control-level freshness requirements in the DD model | Tutela | P2 |
| GAP-SYS-016 | Evidence revocation | Revocation | Tutela `invalidatedAt`, `invalidationReason`; Registry `security-revoked` release state (draft) | partial | No signed revocation event; no revocation propagation to dependent answers | Tutela (evidence), Registry (releases) | P2 |
| GAP-SYS-017 | Record supersession | Supersession | Praxis supersedes and superseded_by validation | implemented | Not applied to security evidence records | Praxis | P2 |
| GAP-SYS-018 | Exceptions with approver, expiry and compensating controls | Exceptions; Standard enforcement model | Tutela `SEC-EXC-*` and gate (`tutela@476dc682:schemas/exception.schema.json`) | implemented (source, CI) | Not released in package; not mapped to SEC-* rule IDs | Tutela | P1 |
| GAP-SYS-019 | Residual risk records | Residual risks; Standard per-rule residual risks | Tutela unknowns and findings | partial | No explicit residual risk object with acceptance, owner and review date | Tutela | P2 |
| GAP-SYS-020 | Disclosure classification and redaction for evidence | Disclosure restrictions; "Public reports must omit exploitable details" | Tutela `redacted` boolean; Folio "redacted by default" requirement | partial | No disclosure classes on any evidence record | Tutela (field), Folio (rendering by class) | P1 |
| GAP-SYS-021 | Traceability from evidence to control IDs, question IDs, policy refs and product IDs | Control IDs, question IDs, policy refs, product IDs | This repository's DD schemas only | partial | No Echelon system carries these links on evidence | echelon-due-diligence (record model); Tutela (invariant to SEC-* mapping) | P1 |
| GAP-SYS-022 | Runtime security monitoring and operational evidence | Standard purpose "monitor runtime behavior"; Tutela TUT-1301 to TUT-1304 | None. Aegis emits fault events; Strata `drift` checks schema only | absent | No collector, detection or alerting capability | Unbound operations architecture with Aegis as event producer and Tutela `RuntimeObservation` intake; not Vigila. Ownership requires a decision | P1 |
| GAP-SYS-023 | Follow-up tracking for expiring exceptions, stale evidence and remediation | Expiration, exceptions | Vigila `followup.*` capabilities (registered, unreleased) | specified for this use | No integration | Vigila | P3 |
| GAP-SYS-024 | Reproducible security and evidence report rendering | Assurance deliverables 1 to 4 | Folio Security Evidence Record components | partial | Deterministic export specified but not packaged (`folio@56a18e1f:context/CURRENT-STATE.md`) | Folio | P2 |
| GAP-SYS-025 | Safe input handling and contextual output encoding | SEC-UI-001, SEC-DATA-001 | None. Forma is HTML and CSS only | absent | No validation types, encoding library or unsafe sink prohibition check | Ordo and application domain (validated types); Limen (sink restriction, Trusted Types); Forma (documented safe patterns only) | P1 |
| GAP-SYS-026 | Browser boundary verification and third-party script inventory | SEC-UI-002 | Limen `verify --strict --json` (lexical) | released (partial) | No third-party script or generated bundle inventory; lexical only | Limen | P2 |
| GAP-SYS-027 | Accessibility conformance evidence | Accessibility questionnaire items | Forma axe and Playwright conformance, WCAG 2.2 AA target | implemented (component level) | Component conformance is not application conformance (A11Y-001) | Forma | P3 |
| GAP-SYS-028 | State and transition legality evidence | SEC-AUTH-001, Unbound workflow invariants | Ordo | released | Not emitted as evidence records | Ordo | P2 |
| GAP-SYS-029 | Work and change provenance | Provenance | Praxis | released | Identity asserted, unsigned | Praxis | P2 |
| GAP-SYS-030 | Longitudinal quality observations | Test and quality evidence trends | Dokimos | released | No security observations by design | Dokimos | P3 |
| GAP-SYS-031 | Independent completion verification | Independence of verification | Dokimos `completion verify` with Praxis receipts | implemented | Covers work completion, not security controls | Dokimos | P2 |
| GAP-SYS-032 | Capability discovery for evidence producers | Integration model | Registry | released (spec) | No `evidence.*` capability identifiers | Echelon Registry | P2 |
| GAP-SYS-033 | Compiled evidence registries from canonical records | Knowledge Store approach | Praxis `registry build`; EKS compiler (research) | partial | No evidence-record compilation or freshness check | echelon-due-diligence build tool now; Echelon Knowledge Store later | P2 |
| GAP-SYS-034 | License terms permitting customer, auditor and escrow use of evidence tooling | Escrow, audit reproduction | PolyForm Noncommercial 1.0.0 on all verified tools except Registry | absent | No commercial or audit grant published; EDF, Clarity, Unbound unlicensed | echelon-organization-administration | P1 |
| GAP-SYS-035 | Security release gate running across application repositories, fail closed | Standard "Block merges and releases" | Tutela gate in Tutela CI only | partial | No portfolio-wide gate | Tutela (gate), Praxis or Conditor (installation into CI) | P1 |
| GAP-SYS-036 | Accurate Unbound persistence assumption | Unbound CCM evidence storage | `unbound@9b38de47:architecture/CONTINUOUS-CONTROL-MONITORING-AND-EVIDENCE-ASSURANCE.md` line 35 | specified, incorrect | Assumes Strata provides persistence and evidence storage features it does not have | unbound | P1 |

## Summary of the five questions

| Question | Result |
|---|---|
| Typed parameterized runtime DB access (SEC-DB-001) | Refuted (GAP-SYS-002) |
| F# semantic security analysis or rule registry | Analysis refuted (GAP-SYS-006); rule registry partial in Tutela, not Aegis (GAP-SYS-005) |
| Runtime security monitoring | Refuted (GAP-SYS-022) |
| Evidence signing | Partial: receipts and schema artifacts only (GAP-SYS-012, GAP-SYS-013) |
| SBOM or provenance | SBOM refuted (GAP-SYS-009); build provenance partial (GAP-SYS-010); change provenance present, unsigned (GAP-SYS-029) |

## Consequences for due diligence answers

- Any answer about parameterized queries, SAST, SCA, secret scanning, SBOM, runtime
  monitoring or signed evidence must be `proposed-target-state` or `unknown`.
- Answers may describe Strata migration gating and drift detection, Limen boundary
  verification, Tutela exception governance and Praxis provenance as existing tools,
  stating that none is operated for a production Echelon service.
- No answer may name Aegis as the security rule owner or Vigila as the monitoring
  owner.
