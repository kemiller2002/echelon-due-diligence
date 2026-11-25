---
id: DD-ARC-002
title: Echelon system capability analysis for due diligence evidence
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [architecture, due-diligence, evidence, capability-verification, secure-construction]
related_documents:
  - architecture/ECHELON-CURRENT-STATE-BRIEF.md
  - gap-analysis/ECHELON-SYSTEM-CAPABILITY-GAPS.md
  - architecture/EVIDENCE-ARCHITECTURE-SPECIFICATION.md
  - recommendations/system-recommendations.jsonl
---

# Echelon system capability analysis

## 1. Purpose, method and limits

This record verifies what each Echelon Foundry system actually does, so that due
diligence answers and the evidence architecture rest on observed capability rather
than on the "Proposed system ownership" section of the Echelon Secure Construction
Standard v0.1
(`echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md`,
section "Proposed system ownership (verify against repositories)").

Method. For each repository I read requirements, status and traceability documents,
source code, test inventories, CI workflows, package manifests and Echelon Registry
release records. README text was used only to locate claims, which were then checked
against code or status documents. Every claim is cited as `repo@shortcommit:path`.

Limits.

- All repositories were read from shallow clones at the HEADs below. No code was built
  or executed in this analysis; "implemented" means source and tests exist at that
  commit, not that I ran them. Test pass claims are quoted from the repositories'
  own reports and are first-party.
- "Released" means a release record exists in the Echelon Registry
  (`echelon-registry@f9ea4d0b:releases/`). I did not download released artifacts.
- None of these systems is operated for a production Echelon service. Nothing here is
  operating evidence for Unbound.

### 1.1 Repository baseline

| Repository | HEAD (full) | Cited as | License file |
|---|---|---|---|
| praxis | `12bf9951253fc15e6973c2d3f5b88076f4556245` | `praxis@12bf9951` | PolyForm Noncommercial 1.0.0 (`praxis@12bf9951:LICENSE`) |
| aegis | `711e02603da02cb05731ddfa7f45f2e553273fab` | `aegis@711e0260` | PolyForm Noncommercial 1.0.0 (`aegis@711e0260:LICENSE`) |
| tutela | `476dc68236afa37a5b467590df988c590f1635e1` | `tutela@476dc682` | PolyForm Noncommercial 1.0.0 (`tutela@476dc682:LICENSE`) |
| dokimos | `6ea86246cb13f141201bc5cae5d84ebe9831d02b` | `dokimos@6ea86246` | PolyForm Noncommercial 1.0.0 (`dokimos@6ea86246:LICENSE`) |
| strata | `c6a384ec701904df77cc2756856bbbac5436d79f` | `strata@c6a384ec` | PolyForm Noncommercial 1.0.0 (`strata@c6a384ec:LICENSE`) |
| limen | `743cdb9be8971c0a3a250906a6e2e112170dfae0` | `limen@743cdb9b` | PolyForm Noncommercial 1.0.0 (`limen@743cdb9b:LICENSE`) |
| forma | `c8f40b4c3d3083207dfb5a5ce815bca045020053` | `forma@c8f40b4c` | PolyForm Noncommercial 1.0.0 (`forma@c8f40b4c:LICENSE`) |
| folio | `56a18e1f7aa6513297690a40f180dfe0312853af` | `folio@56a18e1f` | PolyForm Noncommercial 1.0.0 (`folio@56a18e1f:LICENSE`) |
| vigila | `feab75517e791d4ab0db9e42158cd3c7167ce4ee` | `vigila@feab7551` | PolyForm Noncommercial 1.0.0 (`vigila@feab7551:LICENSE`) |
| ordo | `db6d39ed2e7bc185a7fab6821677e7cd00201d8c` | `ordo@db6d39ed` | PolyForm Noncommercial 1.0.0 (`ordo@db6d39ed:LICENSE`) |
| echelon-registry | `f9ea4d0be0fa1b051e0c4f8e8f5d9053a9e5bf6e` | `echelon-registry@f9ea4d0b` | MIT (`echelon-registry@f9ea4d0b:LICENSE`) |
| echelon-knowledge-store | `35d9cee0df94eed89335712fbaade4d491a45bcd` | `echelon-knowledge-store@35d9cee0` | PolyForm Noncommercial 1.0.0 (`echelon-knowledge-store@35d9cee0:LICENSE`) |
| clarity-framework | `200a9ebf029c051eac625bb5185929b20c8d5aed` | `clarity-framework@200a9ebf` | No license file found (`git ls-files`) |
| Echelon-AI-Native-Enterprise-Design-Framework (EDF) | `763ff8c9fcca6c4edbcdea245173988c78f72420` | `Echelon-AI-Native-Enterprise-Design-Framework@763ff8c9` | No license file found |
| unbound | `9b38de47437d2be1e86ded3db856aaf0eefc9fed` | `unbound@9b38de47` | No repository license file found (only vendored font OFL files) |
| echelon-organization-administration | `2763e576fca186b119928a52cfba564d9a8af268` | `echelon-organization-administration@2763e576` | No license file; `package.json` declares `ISC` (`echelon-organization-administration@2763e576:package.json`) |

## 2. Findings by system

Status vocabulary used below: **released** (Registry release record exists),
**implemented** (source plus tests at HEAD), **experimental** (source exists but is
explicitly outside the product path), **specified** (requirements only),
**not found** (no evidence located).

### 2.1 Praxis

- Verified purpose: repository operating system providing a work protocol with legal
  transitions, canonical research records with lifecycle and supersession, execution
  telemetry, agent identity and provenance, validation and CI
  (`praxis@12bf9951:README.md`, "What it provides").
- Status: released 3.25.0 at `12bf9951` as self-contained native CLI bundles
  (`echelon-registry@f9ea4d0b:releases/praxis/3.25.0.release.json`); also a .NET
  global tool `EchelonFoundry.Praxis` (`praxis@12bf9951:README.md`). Test projects
  `tests/Praxis.Tests` (196 files) and `tests/Site.Tests`.
- Evidence-relevant capabilities:
  - Provenance: actor identity (`kind`, `id`, `provider`, `model`, `runtime`),
    execution identity `EXE-...`, append-only execution-keyed contribution history in
    front matter, content digests `previous.sha256` / `current.sha256` on events
    (`praxis@12bf9951:docs/agent-provenance.md`). Identity is asserted, not
    cryptographically verified: "Signed events, verified execution receipts, and key
    management are deferred" (`praxis@12bf9951:docs/agent-provenance.md`, line 162),
    and remote requester identity is marked `asserted-by-request` (same file,
    line 177).
  - Work evidence: `praxis work complete --evidence TYPE=PATH` binds completion
    evidence to a work item (`praxis@12bf9951:AGENTS.md`).
  - Supersession: validation fails on nonreciprocal supersession and stale
    registries (`praxis@12bf9951:README.md`).
  - Signed verification receipts: a trusted verifier process holds an ECDSA P-256
    key in memory (or imported from a PEM secret in CI) and signs
    `echelon.verification-receipt/1` payloads in DSSE v1 envelopes
    (`praxis@12bf9951:src/Praxis.Infrastructure/Work/TrustedVerifier.fs`;
    `praxis@12bf9951:src/Praxis.Domain/Work/VerificationReceipt.fs`), tested in
    `praxis@12bf9951:tests/Praxis.Tests/AttestedCompletionTests.fs`. The receipt
    payload binds work item, commit, tree id, Ordo contract digest, validation policy
    digest, command, exit code and status.
  - Signed human approvals for construction (ECIR) are verified with a public key
    (`praxis@12bf9951:src/Praxis.Infrastructure/Planning/EcirApprovals.fs`).
  - Security metrics: `praxis tutela ingest` and `praxis tutela metrics` track Tutela
    invariant, exception and evidence age trends without a single score, all rows
    marked Met (`praxis@12bf9951:requirements/TUTELA-SECURITY-METRICS.md`).
  - Release provenance: native release assets carry GitHub build-provenance
    attestations (`praxis@12bf9951:.github/workflows/native-release.yml`,
    `actions/attest-build-provenance`).
- Not found: SBOM generation; dependency, SAST or secret scanning in Praxis CI;
  a generic security merge or release gate that runs Tutela. Praxis's own secret
  heuristic is a local regex set that Tutela flags as divergent
  (`tutela@476dc682:docs/SECURITY-OWNERSHIP.md`).

### 2.2 Aegis

- Verified purpose: "handling and recovering from unexpected operational failure in
  .NET applications" with fault model, capture, redaction, recovery, escalation and
  storage adapters (`aegis@711e0260:README.md`). It explicitly is "not a logging
  framework, a metrics platform, a tracing product, an analytics system or a
  monitoring tool" (`aegis@711e0260:docs/aegis/README.md`, "What Aegis is not").
- Status: released 2.0.2 as NuGet `EchelonFoundry.Aegis.Core`
  (`echelon-registry@f9ea4d0b:releases/aegis/2.0.2.release.json`); 137 of 143
  requirements done, 4 partial, 2 not started
  (`aegis@711e0260:docs/aegis/REQUIREMENTS-STATUS.md`). Tests in
  `tests/Aegis.Core.Tests` and `tests/Aegis.Core.CSharpTests`. No build-provenance
  attestation step found in its workflows.
- Evidence-relevant capabilities: `Aegis.Tutela.tryProjectFault` projects a fault into
  a `tutela/evidence/v1` observation with subject ref, producer, method and
  limitations (`aegis@711e0260:src/Aegis.Core/Tutela.fs`), per
  `aegis@711e0260:requirements/TUTELA-INTEGRATION.md`, which states "Aegis observations
  are security evidence inputs, not security certification." Tutela notes this
  projection lacks a provenance-authority rule and so cannot yet support a Verified
  invariant (`tutela@476dc682:docs/SECURITY-OWNERSHIP.md`).
- Refuted: rule registry, semantic F# analysis, scanner orchestration and findings
  management. No such code, schema or requirement exists in Aegis; a search for SARIF,
  Semgrep, CodeQL, "rule registry", "static analysis" or "scanner" found only
  `aegis@711e0260:docs/development-telemetry.md` (unrelated).

### 2.3 Tutela

- Verified purpose: "Echelon Foundry's security engineering discipline", modeling
  Asset, Trust Boundary, Threat, Security Invariant, Control, Evidence,
  Finding/Unknown and Release Posture, and never asserting that a system is secure
  (`tutela@476dc682:README.md`). Tutela declares itself the single owner of security
  meaning across the portfolio (`tutela@476dc682:docs/SECURITY-OWNERSHIP.md`), and
  this is corroborated by
  `dokimos@6ea86246:requirements/REQUIREMENTS.md` (R8, "Security-specific analysis
  SHALL route to Tutela") and by
  `echelon-organization-administration@2763e576:application-governance/AEGIS-FORMA-FOLIO-COMPLIANCE.md`
  (line 25).
- Status:
  - Released 0.1.0 (commit `94afcc91`) as npm `@echelon-foundry/tutela`, distribution
    class `repository-lifecycle` (`echelon-registry@f9ea4d0b:releases/tutela/0.1.0.release.json`).
    The published package contains only an installer and schemas
    (`tutela@476dc682:package.json`, `files`), not the F# gate.
  - Implemented in source (not in the released package): F# `Tutela.Core` and
    `Tutela.Cli` with commands `gate`, `scan-secrets` and `trace`
    (`tutela@476dc682:src/Tutela.Cli/Program.fs`), run in its own CI
    (`tutela@476dc682:.github/workflows/tutela-foundation.yml`). A Python reference
    implementation remains as a conformance oracle that the workflow expires on
    2027-01-31 (same workflow; TUT-1804 in
    `tutela@476dc682:requirements/TUTELA-REQUIREMENTS.md`). The organization's own
    report records "CI green, 246 F# + 70 Python" tests as of 2026-10-05
    (`echelon-organization-administration@2763e576:application-governance/QUALITY-REMEDIATION-REPORT-2026-10-05.md`, line 195), a first-party claim.
  - Normative baseline TUT-0001 to TUT-1807
    (`tutela@476dc682:requirements/TUTELA-REQUIREMENTS.md`).
- Evidence-relevant capabilities:
  - Evidence model: `schemas/security-evidence.schema.json` requires id, type (Test,
    Aegis, StaticAnalysis, DependencyScan, SecretScan, ConfigScan, Fuzz, ManualReview,
    AdversarialTest, RuntimeObservation, Other), source, observedAt, subjectRef,
    producer, producerIdentity, artifactDigest (sha256/sha512) and provenance (kind,
    issuer, runRef, workflowRef), with optional validUntil, invalidatedAt,
    invalidationReason, independentOfImplementation, redacted, limitations and
    bundleDigest (`tutela@476dc682:schemas/security-evidence.schema.json`).
  - Evidence producer: `src/tutela_evidence.py` computes an artifact digest and emits
    an evidence record; its stated limitation is "Digest proves byte identity of the
    named artifact, not the truth or completeness of its claims"
    (`tutela@476dc682:src/tutela_evidence.py`). No signature is produced.
  - Gate rule registry: stable rule ids `TUTELA-G001` onward (policy defaults,
    assessment structure, gate weakening, verified-without-evidence, contradictory
    evidence, independent verification, evidence digest and provenance), "never
    reused or renumbered" (`tutela@476dc682:src/Tutela.Core/Rules.fs`;
    `tutela@476dc682:docs/VERIFICATION-CONTRACT.md`).
  - Sensitive-data rule catalog `TUTELA-SD-K*` and `TUTELA-SD-V*`
    (`tutela@476dc682:security/SENSITIVE-DATA-RULES.json`), applied by
    `tutela scan-secrets`, which emits `tutela.secret-scan/1` without matched values
    (`tutela@476dc682:src/Tutela.Core/SensitiveData.fs`).
  - Invariant states Verified, Violated, Unknown, NotApplicable, Stale with freshness
    and expiry (TUT-0603, TUT-0605); release postures PASS, CONDITIONAL, BLOCKED,
    INDETERMINATE bound to immutable commit and artifact identity (TUT-1201 to
    TUT-1206).
  - Exceptions: `SEC-EXC-NNN` with scope, covers, rationale, compensating controls,
    evidence, createdAt, expiresAt, and requester and approver identities bound to
    GitHub numeric subject ids with platform-API binding evidence; the approver must
    be distinct and hold `security-owner` in `security/ROLE-REGISTRY.json`
    (`tutela@476dc682:schemas/exception.schema.json`).
  - Trust-root change control that blocks an agent from weakening a gate and
    certifying the same change (`tutela@476dc682:src/tutela_trust_root.py`;
    SEC-INV-001 in `tutela@476dc682:security/SECURITY-PROFILE.md`).
  - Requirement-to-test traceability (`tutela trace`, `tutela.traceability/1`).
- Gaps inside Tutela: no evidence signature, no disclosure class beyond a `redacted`
  boolean, no control or questionnaire identifiers, no explicit residual-risk object,
  no SARIF or scanner-output intake, SBOM only as an unimplemented MUST "where
  warranted" (TUT-0905). Tutela itself records that "No portfolio repository runs
  secret scanning, dependency review or CodeQL in CI" beyond Tutela's self-scan
  (`tutela@476dc682:docs/SECURITY-OWNERSHIP.md`, line 47).

### 2.4 Dokimos

- Verified purpose: evidence-based code-quality measurement with immutable
  longitudinal snapshots identified by repository, revision, timestamp, analyzer
  versions, rule-set version, configuration identity and scope
  (`dokimos@6ea86246:requirements/REQUIREMENTS.md`, R0.1 to R0.10).
- Status: released 0.11.1 native CLI (`echelon-registry@f9ea4d0b:releases/dokimos/0.11.1.release.json`),
  provides `quality.snapshot`, `quality.compare`, `quality.evaluate`,
  `quality.history` (`echelon-registry@f9ea4d0b:registry/systems-v2.json`). Test
  projects `Dokimos.Domain.Tests`, `Dokimos.Core.Tests`, `Dokimos.Cli.Tests`. Release
  workflow attests build provenance (`dokimos@6ea86246:.github/workflows/release.yml`).
  Self-observations are stored under `dokimos@6ea86246:observations/` with
  `schemaVersion`, `snapshotId`, `repository`, `revision`, `collectedAt`,
  `collector`.
- Evidence-relevant capabilities:
  - Longitudinal observations, ratchets and baselines
    (`dokimos@6ea86246:src/Dokimos.Core/Ratchet.fs`, `Snapshots.fs`, `History.fs`).
  - Quality rule catalog (`dokimos@6ea86246:src/Dokimos.Core/QualityRules.fs`),
    quality only.
  - Independent completion verification of Praxis claims, failing closed, and in
    attested mode verification of DSSE-signed `echelon.verification-receipt/1`
    receipts against pinned verifier keys
    (`dokimos@6ea86246:docs/completion-verification.md`;
    `dokimos@6ea86246:src/Dokimos.Core/CompletionAttestation.fs`; tests
    `tests/Dokimos.Core.Tests/CompletionAttestationTests.fs`). Dokimos verifies; it
    does not hold the signing key.
  - F# analysis is lexical line counting
    (`dokimos@6ea86246:src/Dokimos.Core/FSharpQuality.fs`). An experimental
    FSharp.Compiler.Service AST scanner for business-rule provenance exists but is
    "not in `Dokimos.sln`, not on the default `dokimos` CLI path and not in any CI gate"
    (`dokimos@6ea86246:experiments/rule-provenance/README.md`).
  - Verification benchmarks measure the verification compiler on two synthetic
    applications (`dokimos@6ea86246:experiments/verification-benchmarks/BENCHMARK-RESULTS.md`);
    they are not scanner benchmarks against NIST SARD or OWASP Benchmark.
- Refuted or not found: adversarial security testing ownership, scanner precision and
  recall benchmarking. R8 routes security analysis to Tutela. The README sentence
  "Security remains owned by Aegis/Tutors" (`dokimos@6ea86246:README.md`, line 13) is
  internally inconsistent with R8; "tutors" is a registered alias of Tutela
  (`echelon-registry@f9ea4d0b:registry/systems-v2.json`), but naming Aegis as a
  security owner contradicts R8.

### 2.5 Strata

- Verified purpose: declarative PostgreSQL schema management: compile `.sql` files to
  an artifact, diff against a live database, judge each change, apply allowed changes
  (`strata@c6a384ec:README.md`). "Status: pilot", PostgreSQL 16 only, not run against a
  large real migration history (`strata@c6a384ec:README.md`, line 14).
- Status: released 0.1.1 at `f650d91e` as native CLI for linux-x64, osx-x64,
  osx-arm64, win-x64 (`echelon-registry@f9ea4d0b:releases/strata/0.1.1.release.json`).
  The Registry lists distribution classes `self-contained-native-cli` and
  `nuget-library` (`echelon-registry@f9ea4d0b:registry/systems-v2.json`) but no NuGet
  release record exists. Tests: `strata@c6a384ec:tests/Strata.Tests/` (schema diff,
  golden, deployment gate, validation, type checking, catalog introspection and more).
  Release workflow attests build provenance
  (`strata@c6a384ec:.github/workflows/release.yml`, line 255).
- Evidence-relevant capabilities:
  - Six-state comparison (`matches`, `differs`, `not-compared`, `not-modelled`,
    `unverifiable`, `absent`) so unchecked items never render as pass
    (`strata@c6a384ec:README.md`).
  - `plan`, `check` (exit 0 allow, 1 block, 2 approval), `drift` (read-only, exit 0,
    1, 2), `validate <file.sql>` with optional `--types` server-side PREPARE in a
    rolled-back transaction, and offline validation against a compiled artifact
    (`strata@c6a384ec:README.md`, "Command reference").
  - `readers`, `writers`, `impact`, `relationships` over a SQL corpus.
  - Artifact integrity digest (SHA-256) and optional ECDSA P-256 signature with
    `deploy --require-signature`; the code documents that signing is a custody
    property Strata cannot enforce
    (`strata@c6a384ec:src/Strata.Host.Files/Attestation.fs`).
- Refuted: typed parameterized runtime database access and restricted data
  interfaces. Strata has no application-facing query library, query definition
  format or runtime access API. Npgsql use is limited to Strata's own host adapters
  (for example `strata@c6a384ec:src/Strata.Host.Postgres/ReferenceData.fs`). The only
  Strata document about application data interaction,
  `strata@c6a384ec:docs/requirements/data-interaction-virtualization.md`
  (STRATA-DIV-001), is about mocks and replay, is "Proposed baseline requirements",
  and states "No code implementation is implied by this document."
- Strata's own current state records that deployment-safety value is "capability
  demonstrated, value unproven" (`strata@c6a384ec:context/CURRENT-STATE.md`).

### 2.6 Limen

- Verified purpose: dependency-free browser kernel and application engine split; only
  JSON-serializable data crosses (`limen@743cdb9b:README.md`). The npm kernel is
  TypeScript; the lifecycle CLI is F#.
- Status: released 0.9.1 npm `@echelon-foundry/limen` and 0.9.0 NuGet `limen-fsharp`
  packages (`echelon-registry@f9ea4d0b:releases/limen/0.9.1.release.json`,
  `releases/limen-fsharp/0.9.0.release.json`). Conformance suites under
  `limen@743cdb9b:conformance/`; publish workflow attests provenance
  (`limen@743cdb9b:.github/workflows/publish.yml`).
- Evidence-relevant capabilities: `limen verify [--strict] [--json]` enforces
  `architecture/boundary-rules.json`: engine code must not acquire browser, JS-interop,
  network, filesystem or process authority, and no `eval`; an unconfigured boundary
  exits 8 rather than passing. Limen states "It is a lexical check, a guard rail, not
  a proof" (`limen@743cdb9b:README.md`, line 470). `wasm-check` validates WASM
  interpreter frame limits. Browser packs run under strict CSP with Trusted Types
  (`limen@743cdb9b:docs/29-binding-security.md`).
- Gaps versus SEC-UI-002: no inventory of third-party scripts, no inspection of
  generated bundles outside the configured engine and kernel directories found.

### 2.7 Forma

- Verified purpose: zero-component-runtime design system of semantic HTML patterns,
  CSS, tokens and accessibility contracts (`forma@c8f40b4c:README.md`).
- Status: `package.json` version 1.1.0, tag `v1.1.0`; latest Registry record 1.0.1
  (`echelon-registry@f9ea4d0b:releases/forma/1.0.1.release.json`). Accessibility
  target WCAG 2.2 AA (`forma@c8f40b4c:requirements/ACCESSIBILITY-AND-INCLUSIVE-DESIGN.md`,
  A11Y-001); axe-core Playwright conformance (`forma@c8f40b4c:package.json`,
  `@axe-core/playwright`); machine-readable contracts under `forma@c8f40b4c:contracts/`.
- Refuted: "safe input and rendering primitives" in the sense of SEC-UI-001. Forma is
  HTML and CSS only (`forma@c8f40b4c:requirements/COMPONENT-CATALOG.md`, line 3) and
  has no input validation, sanitization or contextual encoding code. It can document
  safe output patterns but cannot enforce them.

### 2.8 Folio

- Verified purpose: print component system (light-DOM custom elements, print CSS) for
  paper and PDF (`folio@56a18e1f:README.md`).
- Status: `package.json` 0.4.2; Registry 0.4.1 npm `@echelon-foundry/print-components`
  (`echelon-registry@f9ea4d0b:releases/folio/0.4.1.release.json`). Tests under
  `folio@56a18e1f:tests/`.
- Evidence-relevant capabilities: Tutela Security Evidence Record components
  (`ef-print-security-record`, posture, invariant, evidence, unknown, exception),
  required by `folio@56a18e1f:requirements/TUTELA-SECURITY-EVIDENCE-RECORD.md` and
  fixture-tested by `folio@56a18e1f:tests/run-tutela-security-record-tests.mjs`. The
  requirement says "Export MUST be deterministic from the same assessment artifact."
- Gap: deterministic PDF export is specified (EPC-OUT-002 to EPC-OUT-008 in
  `folio@56a18e1f:docs/requirements/PRINT-COMPONENTS-REQUIREMENTS.md`) and the
  current state says "Keep deterministic Chromium PDF generation outside core"
  (`folio@56a18e1f:context/CURRENT-STATE.md`). PDF generation was found only in test
  and experiment scripts and `tools/forma-icon-print.mjs`, not as a packaged
  reproducible renderer. Reproducible security reports are therefore specified, not
  delivered.

### 2.9 Vigila

- Verified purpose: "system of record for personal and business follow-ups, open
  loops, reminders, waiting items, and lightweight tasks", explicitly not a project
  management system (`vigila@feab7551:PROJECT-CHARTER.md`; `vigila@feab7551:README.md`
  "Task organizer").
- Status: F# projects `Vigila.Application`, `Vigila.Semantic`, `Vigila.Transition`,
  `Vigila.Host.GitHub`, `Vigila.Wasm` with tests; Registry lists capabilities
  `followup.create`, `followup.update`, `followup.resolve`, `followup.query`
  (`echelon-registry@f9ea4d0b:registry/systems-v2.json`) but no release record under
  `echelon-registry@f9ea4d0b:releases/`.
- Refuted: runtime monitoring and operational evidence. Nothing in Vigila collects
  runtime signals. A reasonable fit is tracking follow-ups such as expiring exceptions
  and evidence renewal through `followup.create`.

### 2.10 Ordo

- Verified purpose: State-Directed Engineering method (explicit semantic states,
  legal transitions, invariants, evidence, capabilities, obligations, effects)
  (`ordo@db6d39ed:PROJECT-CHARTER.md`); its own charter treats SDE's validity as "an
  open, evidence-gated question".
- Status: released 1.20.0 native CLI (`echelon-registry@f9ea4d0b:releases/ordo/1.20.0.release.json`);
  `Ordo.Core` includes `Capability.fs`, `Authorization.fs`, `Evidence.fs`,
  `NegativeKnowledge.fs`, `Receipt.fs` (typed expected and observed receipts with
  `Indeterminate` distinct from success, `ordo@db6d39ed:src/Ordo.Core/Receipt.fs`).
  Tests `Ordo.Tests`, `Sde.Core.Tests` and others. Native release attests provenance.
- Evidence-relevant: state legality and transition receipts; the Ordo contract digest
  is bound into Praxis verification receipts
  (`praxis@12bf9951:src/Praxis.Domain/Work/VerificationReceipt.fs`). Ordo is the
  natural place to define the legal lifecycle of an evidence record.

### 2.11 Echelon Knowledge Store

- Verified purpose and status: "research phase", "No stable schema, no released
  packages"; finding: "keep Markdown with front matter canonical (as Praxis already
  does), and compile it, deriving links, closures and authority, validating agent
  edits and delivering task-specific packages" (`echelon-knowledge-store@35d9cee0:README.md`).
- Implemented in source: F# compiler with front matter parsing, identifiers, graph,
  validation, freshness of compiled artifacts and context packages
  (`echelon-knowledge-store@35d9cee0:src/Echelon.KnowledgeStore.Core/`,
  `src/Echelon.KnowledgeStore.Compiler/Artifacts.fs`), with tests
  (`tests/Echelon.KnowledgeStore.Tests/`). Its CI is the only portfolio repository
  found running GitHub dependency review
  (`echelon-knowledge-store@35d9cee0:.github/workflows/dependency-review.yml`).

### 2.12 Echelon Registry

- Verified purpose: discovery and interoperability specification; capability
  resolution returns `available`, `unavailable` or `misconfigured`; the registry never
  holds credentials or another system's persistence layout
  (`echelon-registry@f9ea4d0b:README.md`).
- Status: specification plus data. 32 systems in
  `echelon-registry@f9ea4d0b:registry/systems-v2.json`; release records with tag,
  commit and per-artifact SHA-256 under `releases/`.
- Evidence-relevant: release manifests are the best existing source of build artifact
  hashes and commit binding. The v2 manifest schema supports `sbom`, `licenses`,
  `provenance` and `signature` evidence references and a `lifecycleState` of active,
  deprecated, withdrawn or security-revoked
  (`echelon-registry@f9ea4d0b:schemas/release-manifest-v2.schema.json`); the
  supporting spec REG-DIST-160 to REG-DIST-170 is "Status: draft"
  (`echelon-registry@f9ea4d0b:spec/distribution-resilience-requirements.md`). No
  current release record carries SBOM, provenance or signature references; the only
  SPDX file is an example fixture
  (`echelon-registry@f9ea4d0b:examples/release-contract/artifacts/fixture.spdx.json`).
  No `evidence.*` or `security.*` capability is registered.

### 2.13 Other repositories

- Clarity (`clarity-framework@200a9ebf:README.md`): a framework for making beliefs,
  assumptions, evidence, confidence and reassessment explicit; documents only. Its
  "reconsideration criteria" concept maps to evidence expiration and revocation
  triggers, but provides no tooling.
- EDF (`Echelon-AI-Native-Enterprise-Design-Framework@763ff8c9:README.md`): F#
  enterprise modeling framework, "foundation phase (v0, unreleased)", one DAF case
  study. Not an evidence producer for security controls.
- Unbound (`unbound@9b38de47`): requirements only. Its continuous control monitoring
  architecture is "Requirements specification, not implemented or audited" and
  already specifies signed, append-only evidence observations with content digests
  and lineage (`unbound@9b38de47:architecture/CONTINUOUS-CONTROL-MONITORING-AND-EVIDENCE-ASSURANCE.md`,
  lines 2 and 13). It states "Strata is mandatory as an architectural persistence
  dependency, but its actual API capabilities have not been independently verified"
  (same file, line 35). This analysis verifies that Strata is not a runtime
  persistence layer.
- Organization administration: the application-governance inventory already assigns
  security posture to Tutela and operational faults to Aegis
  (`echelon-organization-administration@2763e576:application-governance/AEGIS-FORMA-FOLIO-COMPLIANCE.md`,
  "Shared ownership model"), contradicting the Standard in the same repository. Its
  Tutela row ("no executable implementation yet", line 42, updated 2026-09-25) is stale
  relative to `tutela@476dc682` and to its own 2026-10-05 report.

## 3. Specific questions

| Question | Answer | Evidence |
|---|---|---|
| Does any system provide typed parameterized runtime database access for SEC-DB-001? | **Refuted.** No Echelon system provides an application runtime data access library, typed query definitions or enforcement that application SQL is fixed and parameterized. Strata provides adjacent build-time capabilities: SQL validation against a schema or artifact, type checking via PREPARE, reader and writer analysis, migration gating and drift detection. | `strata@c6a384ec:README.md`; `strata@c6a384ec:src/`; `strata@c6a384ec:docs/requirements/data-interaction-virtualization.md` |
| Does any system provide F# semantic security analysis or a rule registry? | **Refuted for F# semantic security analysis.** Only lexical checks exist (Limen verify, Dokimos FSharpQuality, Tutela secret scan); FSharp.Compiler.Service is used only in experimental Dokimos rule-provenance and in Ordo complexity tooling. **Partially confirmed for a rule registry**, owned by Tutela, not Aegis: Tutela gate rules `TUTELA-G*` and sensitive-data rules `TUTELA-SD-*`. No registry of the Standard's `SEC-*` rules with owner, CWE mapping, negative tests and evidence requirements exists. | `tutela@476dc682:src/Tutela.Core/Rules.fs`; `tutela@476dc682:security/SENSITIVE-DATA-RULES.json`; `dokimos@6ea86246:experiments/rule-provenance/README.md`; `ordo@db6d39ed:tools/Ordo.Complexity/Ordo.Complexity.fsproj` |
| Does any system provide runtime security monitoring? | **Refuted.** Vigila is a follow-up organizer; Aegis produces fault events and disclaims monitoring; Tutela defines a `RuntimeObservation` evidence type and TUT-1301 to TUT-1304 operations requirements, but no collector. The only runtime-adjacent check is Strata's read-only schema `drift`. | `vigila@feab7551:PROJECT-CHARTER.md`; `aegis@711e0260:docs/aegis/README.md`; `tutela@476dc682:schemas/security-evidence.schema.json`; `strata@c6a384ec:README.md` |
| Does any system sign evidence? | **Partially confirmed.** Praxis's trusted verifier signs DSSE verification receipts (ECDSA P-256); Dokimos verifies them; Praxis verifies signed ECIR approvals; Strata signs schema artifacts. Tutela security evidence carries digests only and is not signed. No signing of general evidence records, scanner results or reports. Key custody and management are not established (Praxis defers key management; Strata states custody is outside its control). | `praxis@12bf9951:src/Praxis.Infrastructure/Work/TrustedVerifier.fs`; `dokimos@6ea86246:src/Dokimos.Core/CompletionAttestation.fs`; `strata@c6a384ec:src/Strata.Host.Files/Attestation.fs`; `tutela@476dc682:src/tutela_evidence.py`; `praxis@12bf9951:docs/agent-provenance.md` |
| Does any system produce SBOM or provenance? | **SBOM: refuted** (schema slots and draft requirements only). **Build provenance: confirmed for some releases**: GitHub `actions/attest-build-provenance` in Praxis, Strata, Dokimos, Ordo native releases and Limen and Folio publishes; not found for Aegis, Forma or Tutela. **Change provenance: confirmed** in Praxis (asserted identity). | `echelon-registry@f9ea4d0b:schemas/release-manifest-v2.schema.json`; `.github/workflows/` in each repository; `praxis@12bf9951:docs/agent-provenance.md` |

## 4. Divergences between the Standard and the repositories

| # | Standard says | Repositories show | Severity |
|---|---|---|---|
| D1 | Aegis owns "rule registry, semantic F# analysis, scanner orchestration and findings" | Aegis is an operational fault library that disclaims monitoring; none of the four functions exists there. Tutela owns rules and findings by its own charter, Dokimos R8 and the org's own application-governance document. | High |
| D2 | Tutela is absent from the ownership list | Tutela is the declared and corroborated security authority with evidence, invariant, exception and posture models and an F# gate. | High |
| D3 | Strata owns "typed parameterized database access and restricted data interfaces"; SEC-DB-001 requires "all application database access through Strata" | Strata is a pilot schema compile, diff and deploy CLI for PostgreSQL 16 with SQL validation; no runtime access interface exists or is specified. SEC-DB-001 as written cannot be satisfied by any existing system. | High |
| D4 | Vigila owns "runtime monitoring and operational evidence" | Vigila is a follow-up and task organizer. No Echelon system does runtime security monitoring. | High |
| D5 | Dokimos owns "independent verification, adversarial tests and scanner benchmarks" | Dokimos owns code-quality evidence and independent completion verification; security analysis routes to Tutela (R8); no scanner benchmark exists; adversarial security tests are a Tutela concern (TUT-1004, TUT-1006). Partially aligned for "independent verification" only. | Medium |
| D6 | Forma owns "safe input and rendering primitives" | Forma is HTML and CSS only with accessibility contracts; no input handling. Validation belongs to the application domain under Ordo; DOM sink restriction is closer to Limen (Trusted Types tests). | Medium |
| D7 | Praxis owns "mandatory CI/release gates and provenance" | Praxis provides work-protocol completion gates, provenance and its own validation CI. It does not run Tutela, scanners or security release gates for other repositories; Tutela's gate runs only in Tutela's CI. Partially aligned. | Medium |
| D8 | Folio owns "reproducible security reports" | Folio has Tutela Security Evidence Record components with fixture tests; deterministic export is specified but kept outside core and not packaged. Aligned in intent, not delivered. | Low |
| D9 | Limen owns "controlled browser execution and interop" | Aligned; verification is lexical by Limen's own statement; third-party script and generated-bundle inventory not found. | Low |
| D10 | "Sign evidence and retain it under controlled access" | Only verification receipts and Strata artifacts are signed; no retention or access control system exists for evidence. | Medium |
| D11 | SEC-SUPPLY-001 requires "provenance, SBOM, vulnerability and license checks" | Some build provenance exists; no SBOM, no vulnerability scanning except EKS dependency review; Tutela reports no portfolio-wide secret, dependency or CodeQL scanning. | High |
| D12 | "prefer MIT for original public tooling" | All verified tools except the Registry are PolyForm Noncommercial 1.0.0; EDF, Clarity and Unbound have no license file. | Medium (customer escrow and audit) |
| D13 | Standard is silent on Ordo and the Registry | Ordo owns state and transition legality (TUT-1401) and Registry release records are the source of artifact hashes; both are needed for SEC-AUTH-001 and SEC-SUPPLY-001 evidence. | Low |

Related divergence outside the Standard: Unbound's monitoring architecture assumes
Strata is the persistence layer (`unbound@9b38de47:architecture/CONTINUOUS-CONTROL-MONITORING-AND-EVIDENCE-ASSURANCE.md`,
line 35), which repeats D3.

## 5. Licensing implications

PolyForm Noncommercial 1.0.0 permits noncommercial use only; commercial use "requires a
separate license from Echelon Foundry" and "Commercial licensing information is
forthcoming" (`tutela@476dc682:README.md`, "License"; same text in
`dokimos@6ea86246:README.md`). For due diligence this means:

- A customer, auditor or escrow agent who wants to rerun Echelon evidence tooling (for
  example Strata `drift`, Tutela `gate`, Dokimos `completion verify`) to reproduce
  evidence for a commercial engagement has no published license grant to do so.
  Evidence verification by third parties must either use only openly licensed
  primitives (DSSE, ECDSA, SHA-256, JSON Schema, GitHub attestations) or receive a
  written license.
- Source escrow of Unbound would include dependencies under PolyForm Noncommercial
  whose release-condition use by a customer is not addressed by the license text.
- The Registry (MIT) is the only verified repository whose specification and schemas
  can be redistributed without restriction.
- EDF, Clarity and Unbound carry no license file; their terms are `unknown`.

## 6. Corrections to the current-state brief

`architecture/ECHELON-CURRENT-STATE-BRIEF.md` (DD-ARC-001) is consistent with these
findings, with these refinements, which this record supersedes:

1. Dokimos "scanner benchmarking role is unverified" is now **refuted**: the only
   benchmarks are verification-compiler benchmarks.
2. Strata "no verified runtime typed query interface" is now **refuted outright**, and
   Strata's adjacent capabilities (`validate --types`, `check`, `drift`, artifact
   signing) are verified.
3. Signing exists in Praxis (receipts), Dokimos (receipt verification) and Strata
   (artifact signing); the brief did not record this.
4. Tutela's F# gate exists in source and CI but is not in the 0.1.0 release package.
5. Build-provenance attestations exist for several releases; SBOM does not.

## 7. Open questions

- OQ-ARC-002-01: Will Echelon build an application data access layer to satisfy
  SEC-DB-001, and if so in which repository? No decision record found.
- OQ-ARC-002-02: Who owns production runtime monitoring for Unbound? No Echelon
  system does it.
- OQ-ARC-002-03: Where will evidence signing keys be held, by whom, and how are they
  rotated and revoked? Not established in any repository.
- OQ-ARC-002-04: What commercial or audit license will apply to PolyForm
  Noncommercial tooling used to produce or verify customer-facing evidence?
- OQ-ARC-002-05: Is the Tutela F# CLI intended to ship in a release, given that the
  0.1.0 package contains only schemas and an installer?
