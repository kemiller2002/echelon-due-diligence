---
id: DD-ARC-003
title: Evidence architecture specification
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [architecture, evidence, due-diligence, signing, provenance]
related_documents:
  - architecture/ECHELON-SYSTEM-CAPABILITY-ANALYSIS.md
  - gap-analysis/ECHELON-SYSTEM-CAPABILITY-GAPS.md
  - schemas/dd/evidence-record.schema.json
  - recommendations/system-recommendations.jsonl
---

# Evidence architecture specification

## 1. Status and purpose

This is a **proposed design**. Nothing in it is implemented. It defines one standard
evidence record that Echelon systems can emit, so that due diligence answers, the
Secure Construction Standard's assurance deliverables
(`echelon-organization-administration@2763e576:policies/security/secure-construction-standard.md`,
"Assurance deliverables") and Unbound's continuous control monitoring
(`unbound@9b38de47:architecture/CONTINUOUS-CONTROL-MONITORING-AND-EVIDENCE-ASSURANCE.md`)
can rely on the same verifiable unit.

Design rules:

1. Extend existing systems; do not create a new evidence system. Security meaning stays
   with Tutela (`tutela@476dc682:docs/SECURITY-OWNERSHIP.md`); work provenance with
   Praxis; state legality with Ordo; release identity with the Echelon Registry.
2. The record is a superset of Tutela Security Evidence
   (`tutela@476dc682:schemas/security-evidence.schema.json`) so that every record can be
   projected losslessly into the form the Tutela gate already checks.
3. Reuse existing cryptographic conventions: SHA-256 digests and ECDSA P-256 over
   SHA-256 in DSSE v1 envelopes, which Praxis, Dokimos and Strata already use
   (`praxis@12bf9951:src/Praxis.Domain/Work/VerificationReceipt.fs`;
   `dokimos@6ea86246:src/Dokimos.Core/CompletionAttestation.fs`;
   `strata@c6a384ec:src/Strata.Host.Files/Attestation.fs`), plus GitHub/Sigstore build
   provenance attestations already used by several release workflows.
4. Unknown, indeterminate and unverifiable never render as pass. This follows Strata's
   six-state rule, Tutela TUT-0004 and Ordo's `Indeterminate` receipt result.
5. Internal evidence is labeled by independence; it is never presented as independent
   assurance.

## 2. Evidence record model

Machine contract: `schemas/dd/evidence-record.schema.json` (JSON Schema 2020-12,
`schema: echelon.dd.evidence-record/0.1`).

### 2.1 Fields

| Group | Field | Type | Required | Notes |
|---|---|---|---|---|
| Identity | `schema` | const | yes | `echelon.dd.evidence-record/0.1` |
| | `id` | string `EVD-<PRODUCER>-<YYYYMMDD>-<8 hex>` | yes | Suffix is the first 8 hex of `record_digest`; immutable |
| | `title` | string | yes | |
| | `evidence_kind` | enum (26 values) | yes | Maps to Tutela `type` (section 7.1) |
| Subject | `subject.product_ids` | string[] | yes | Product or Registry system ids |
| | `subject.repository`, `subject.commit` | string, 40 or 64 hex | yes | Source commit hash |
| | `subject.tree_id`, `subject.ref` | string | no | Tree id binds content independent of history |
| | `subject.artifacts[]` | name, digest, media_type, registry_release, build_provenance | no | Build artifact hashes; must match Registry release record when given |
| | `subject.environment.kind` | enum | no | `source-only`, `ci`, `test`, `staging`, `production`, `local`, `unknown` |
| Traceability | `traces.control_ids` | string[] | yes (may be empty) | `ECTL-*` or `UNB-CTRL-*` |
| | `traces.question_ids`, `answer_unit_ids`, `evidence_requirement_ids` | string[] | no | `DDQ-*`, `ANS-*`, `EVR-*` |
| | `traces.policy_refs[]` | `{document: repo@commit:path, rule_id}` | yes (may be empty) | For example SEC-DB-001 |
| | `traces.requirement_ids`, `tutela_ids`, `related_records` | string[] | no | Links to Unbound requirements, Tutela invariants, Praxis records |
| Producer | `producer.system`, `system_version` | enum, string | yes | Echelon system, `external-tool` or `human` |
| | `producer.registry_release`, `capability_id` | string | no | Ties producer to a Registry release and capability |
| | `producer.tool` | name, version, digest | conditional | Required by verification rule V-08 for analysis kinds |
| | `producer.rule_set` | id, version, digest | conditional | Scanner and rule versions |
| | `producer.databases[]` | name, version, retrieved_at | conditional | Vulnerability or advisory database versions |
| | `producer.configuration_digest` | digest | no | |
| Method | `method.description`, `command`, `scope_included`, `scope_excluded`, `coverage` | | description yes | Scope and exclusions per Standard |
| Result | `result.outcome` | `pass`, `fail`, `indeterminate`, `not-applicable`, `informational` | yes | |
| | `result.summary`, `exit_code`, `finding_counts`, `payload` | | summary yes | `payload` is a digest-bound reference to raw output (for example SARIF) |
| Time | `timestamps.observed_at`, `recorded_at` | date-time | yes | |
| | `timestamps.valid_from`, `valid_until` | date-time or null | no | Expiration; null means "until superseded", which verifiers may override by policy |
| Provenance | `provenance.actor` | Praxis actor shape | yes | `kind`, `id`, `provider`, `model`, `runtime` |
| | `provenance.identity_assurance` | `asserted`, `platform-verified`, `key-verified` | yes | Honest label of how identity is known |
| | `provenance.execution_id`, `work_item_id`, `run_ref`, `workflow_ref`, `inputs[]` | | no | Praxis `EXE-*`, CI run |
| Independence | `independence.assurance_independence` | DD enum | yes | `first-party` for all current Echelon tooling |
| | `independence.independent_of_implementation`, `verifier` | bool, string | bool yes | TUT-0006 |
| Review | `reviews[]` | reviewer (bound identity), role, decision, reviewed_at | no | Reviewer identity |
| Risk | `exceptions[]` | `SEC-EXC-*`, expires_at | no | Links to Tutela exceptions |
| | `residual_risks[]` | description, treatment, owner, review_by | no | |
| | `limitations[]` | string[] | yes, min 1 | |
| Disclosure | `disclosure.class` | `public`, `authenticated-prospect`, `nda`, `customer-only`, `auditor-only`, `internal` | yes | Same enum as `schemas/dd/answer-unit.schema.json` |
| | `disclosure.redacted`, `restricted_fields`, `public_summary`, `rationale` | | redacted yes | |
| Retention | `retention.policy_ref`, `retain_until`, `legal_hold` | | no | Retention periods are not yet established by the organization |
| Integrity | `record_digest` | digest | no in draft, yes from `recorded` | See 2.3 |
| | `signatures[]` | signature | no in draft, yes from `verified` | See 2.3 |
| Lifecycle | `lifecycle.state`, `supersedes`, `superseded_by`, `events[]` | | state and events yes | See section 3 |

### 2.2 Disclosure classes

| Class | Audience | Typical content | Rules |
|---|---|---|---|
| `public` | Anyone | Trust center summaries | No exploitable detail, no sensitive data, first-party label required |
| `authenticated-prospect` | Logged-in prospects | Control summaries, report covers | `restricted_fields` removed |
| `nda` | Prospects under NDA | Assessment summaries, architecture descriptions | |
| `customer-only` | Contracted customers | Release assessments, residual risks | |
| `auditor-only` | Engaged auditors and examiners | Raw scanner payloads, exceptions, findings with locations | |
| `internal` | Echelon only | Everything else, including keys metadata and unremediated detail | Default for new records |

A record can only be reclassified by a signed `disclosure-reclassified` lifecycle event.
Folio and any trust-center renderer must drop `restricted_fields` for every audience
below the stated class and must never render a lower class than the record allows.

### 2.3 Canonicalization, digest and signing

1. **Signed content** is the record without `signatures`, `lifecycle` and
   `record_digest`, serialized as RFC 8785 JSON Canonicalization Scheme bytes.
2. `record_digest` is SHA-256 over those bytes. The `id` suffix is its first 8 hex.
3. A **signature** is a DSSE v1 envelope with payload type
   `application/vnd.echelon.dd.evidence-record.v0.1+json` over the canonical bytes,
   ECDSA P-256 / SHA-256, IEEE P1363 `r||s`, matching the existing receipt convention.
   `key_id` is `sha256:<hex of SHA-256 over SPKI DER>`, as in Praxis and Dokimos.
   Release-artifact attestations may instead be referenced as `sigstore-bundle`.
4. The signer must be the producing system's verifier key, not the actor that made the
   change being evidenced. A signature proves custody of a key, not the truth of the
   content (the limitation Strata already documents).
5. **Trusted keys** are published in a Tutela-governed trust-root file (proposed
   `security/EVIDENCE-SIGNING-KEYS.json`) changed only through Tutela's trust-root
   transition process (`tutela@476dc682:src/tutela_trust_root.py`). Each key entry
   carries `valid_from`, `valid_until`, `revoked_at` and `revocation_reason`.
6. Lifecycle events are individually signed, so revocation or supersession never alters
   the signed content of the original record.

## 3. Lifecycle

States: `draft`, `recorded`, `verified`, `stale`, `expired`, `superseded`, `revoked`,
`rejected`. The legal transitions should be declared as an Ordo state model so the
legality is checked rather than conventional (REC-ORDO-001).

| From | Event | To | Who may perform | Preconditions |
|---|---|---|---|---|
| (none) | create | `draft` | Producer | Schema valid except integrity fields |
| `draft` | `recorded` | `recorded` | Producer | `record_digest` present and correct; secret scan clean against `TUTELA-SD-*` |
| `recorded` | `verified` | `verified` | Verifier distinct from implementer | All criteria in section 5 pass; at least one trusted signature |
| `recorded` | `rejected` | `rejected` | Verifier | Any blocking criterion fails; reason recorded |
| `verified` | `marked-stale` | `stale` | Tutela gate or producer | Subject changed (TUT-1304), producer version withdrawn, or dependent evidence revoked |
| `verified`, `stale` | `expired` | `expired` | Any verifier, automatic | `valid_until` passed |
| `verified`, `stale`, `expired` | `superseded` | `superseded` | Producer | Successor record `verified` and lists this id in `supersedes`; reciprocal `superseded_by` (Praxis rule) |
| any except `rejected` | `revoked` | `revoked` | Tutela `security-owner` role | Reason code required; signed event; dependent answers re-evaluated |

Terminal states: `superseded`, `revoked`, `rejected`. Records are never deleted;
`revoked` and `superseded` remain readable so history is preserved (TUT-1603,
REG-DIST-161 analogue).

Consumer rules:

- Only `verified` records may support a `customer_statement_kind` of `current-fact` or
  `qualified-current-fact` in an answer unit.
- `stale` and `expired` records support at most `qualified-current-fact` with the age
  stated, and make the Tutela invariant `Stale`.
- A revocation propagates: every answer unit or Tutela assessment citing the record
  becomes `INDETERMINATE` or loses the claim until re-evidenced.
- Exceptions referenced in `exceptions[]` stop satisfying a gate at `expires_at`
  (TUT-1105).

## 4. Producer responsibilities by system

| System | Emits `evidence_kind` | Current basis (verified) | Required change | Priority |
|---|---|---|---|---|
| Tutela | `secret-scan`, `exception-record`, `policy-approval`, `manual-review`, interpretation of all security kinds | `scan-secrets`, `gate`, exception schema, security evidence schema | Adopt this record as a superset of its evidence schema; add signature, disclosure, trace and residual-risk fields; ingest SARIF payloads; host the SEC-* rule registry and evidence key trust root | P0/P1 |
| Praxis | `work-completion`, and signing service for others | Provenance, `EXE-*`, trusted verifier DSSE signing, `work complete --evidence` | Generalize the trusted verifier to sign evidence records; accept `--evidence` paths that are evidence records; supersession validation for `EVD-*` | P1 |
| Dokimos | `quality-observation`, `semantic-analysis` (future), benchmark results | Immutable snapshots with revision, analyzer and rule versions; DSSE receipt verification | Export snapshots as records; add FCS security analyzer adapter that applies Tutela rules; host scanner benchmark harness | P1/P2 |
| Strata | `schema-validation`, `schema-diff`, `schema-drift` | `validate`, `check`, `plan`, `drift` with exit codes; artifact digest and signature | Emit `--evidence` output in this format; carry artifact digest as `subject.artifacts`; record `unverifiable` counts | P1 |
| Limen | `boundary-verification` | `verify --strict --json` with stable exit codes | Emit record including rule file digest; add third-party script and bundle inventory | P2 |
| Forma | `accessibility-conformance` | axe and Playwright conformance | Emit record per release; state component-level limitation | P3 |
| Ordo | `state-legality` | Receipts with Match, Mismatch, Indeterminate | Emit records for transition legality checks; define evidence lifecycle model | P2 |
| Aegis | `fault-observation` | `Aegis.Tutela.tryProjectFault` | Map projection to this record; obtain Tutela provenance-authority rule | P3 |
| Echelon Registry | `release-manifest`, `build-provenance`, `sbom` references | Release records with commit and SHA-256 | Populate `sbom`, `provenance`, `signature` references; register `evidence.*` capabilities | P1 |
| Releasing repositories | `sbom`, `build-provenance` | GitHub attestations in some workflows | Generate SBOM; attest every artifact | P1 |
| Folio | Renders records; emits nothing | Security Evidence Record components | Deterministic export; disclosure-class filtering; render record digest and signature status | P2 |
| Vigila | Nothing | `followup.*` capabilities | Create follow-ups for `valid_until`, exception expiry and residual risk `review_by` | P3 |
| echelon-due-diligence | Links records to `ANS-*`, `DDQ-*`, `EVR-*` | DD schemas and build tool | Validate records, build `registries/evidence-records.json`, enforce consumer rules in section 3 | P1 |
| External tools and assessors | `external-attestation`, `dependency-scan`, `static-analysis` | None | Wrapped by Tutela intake with `producer.system: external-tool` and independence labeled accurately | P1 |

No system is assigned runtime security monitoring. That capability does not exist in
Echelon and its owner is an open decision (DD-ARC-002 OQ-ARC-002-02). Runtime data,
once collected, enters as `runtime-observation` records through Tutela intake.

## 5. Verification criteria

A verifier (Tutela gate, DD build tool or an external auditor using openly licensed
primitives) checks, in order. Any failure of V-01 to V-07 makes the record
`rejected`; V-08 to V-15 failures make it ineligible to support a current-fact claim.

| ID | Criterion |
|---|---|
| V-01 | Record validates against `schemas/dd/evidence-record.schema.json`. |
| V-02 | Recomputed `record_digest` over RFC 8785 canonical bytes equals the stored digest, and the `id` suffix matches. |
| V-03 | At least one signature verifies with a key in the trust root that was valid and unrevoked at `signed_at`. |
| V-04 | `subject.commit` exists in `subject.repository`; `tree_id`, when present, matches. |
| V-05 | Each `subject.artifacts[].digest` matches the Registry release record or the attested artifact. |
| V-06 | `payload` and `inputs` digests match the referenced content. |
| V-07 | Tutela sensitive-data scan finds no `TUTELA-SD-*` match in the record or payload below `auditor-only`. |
| V-08 | Analysis kinds (`static-analysis`, `semantic-analysis`, `dependency-scan`, `secret-scan`, `config-scan`, `sbom`) carry `producer.tool` and `producer.rule_set`; `dependency-scan` carries `producer.databases`. |
| V-09 | `timestamps.observed_at` is not later than `recorded_at`; `valid_until` is in the future at evaluation time. |
| V-10 | `lifecycle.state` is `verified`, and no `revoked` or `superseded` event exists. |
| V-11 | `independence.independent_of_implementation` is true only if the signer and actor differ from the change author; `assurance_independence` other than `first-party` requires a `reviews[]` entry from the named party or an `external-attestation` payload. |
| V-12 | Every `reviews[].reviewer` has `binding_verified: true` and a role in the Tutela role registry. |
| V-13 | Every id in `traces` resolves to an existing record; every `policy_refs[].rule_id` exists in the cited document. |
| V-14 | Every referenced `SEC-EXC-*` is approved and unexpired at evaluation time. |
| V-15 | The audience requesting the record is permitted by `disclosure.class`. |

## 6. Evidence need allocation

For each evidence need in the due diligence mission: which existing system can provide
it, what is missing, and the recommended owning repository.

| Need | Existing provider (verified) | Missing | Recommended owner |
|---|---|---|---|
| Control IDs | echelon-due-diligence `ECTL-*`; Unbound `UNB-CTRL-*` (`unbound@9b38de47:requirements/governance/MASTER-ENTERPRISE-CONTROL-MATRIX.csv`) | No producer attaches them | echelon-due-diligence (mapping); producers pass through |
| Question IDs | echelon-due-diligence `DDQ-*` | Not on any evidence | echelon-due-diligence |
| Policy refs | Standard SEC-* IDs exist as prose | No machine-readable rule registry | Tutela (SEC-* rule registry) |
| Product IDs | Registry system ids (`echelon-registry@f9ea4d0b:registry/systems-v2.json`) | Unbound not registered | Echelon Registry |
| Source commit hashes | Tutela `subjectRef`; Praxis receipts; Dokimos snapshots; Registry release `commit` | Uniform field | Each producer, via this record |
| Build artifact hashes | Registry release `artifacts[].sha256`; Strata artifact digest; Tutela `artifactDigest` | Not linked to evidence | Echelon Registry |
| Test results | Repository CI; Tutela `Test` evidence type; Dokimos verification | No uniform test evidence export | Dokimos (test evidence), Tutela (security interpretation) |
| Scanner and rule versions | Dokimos snapshots carry analyzer and rule-set versions (R0.1); Tutela rule ids | No security scanners run; no database versions | Tutela (intake contract) |
| Timestamps | Tutela `observedAt`; Praxis events; Dokimos `collectedAt` | Recorded-at separation | All producers |
| Expiration | Tutela `validUntil`, Stale | Policy-driven freshness by control | Tutela |
| Provenance | Praxis actor and execution; GitHub build attestations; Tutela provenance object | Identity is asserted; SBOM absent | Praxis (change), releasing repositories plus Registry (build) |
| Reviewer identity | Tutela `boundIdentity` and role registry | Applied only to exceptions | Tutela |
| Digital signatures | Praxis trusted verifier; Strata signing; Dokimos verification | Evidence records unsigned; no key management | Praxis (signing), Tutela (trust root and verification) |
| Disclosure restrictions | DD `disclosure_classification`; Tutela `redacted` | No class on evidence | Tutela (field), Folio (rendering) |
| Revocation | Tutela `invalidatedAt`; Registry `security-revoked` (draft) | Signed revocation, propagation | Tutela |
| Supersession | Praxis supersedes validation | Not applied to evidence | Praxis |
| Exceptions | Tutela `SEC-EXC-*`, F# gate | Mapping to SEC-* rules | Tutela |
| Residual risks | Tutela unknowns and findings | Explicit residual-risk object | Tutela |

## 7. Compatibility

### 7.1 Tutela

| Tutela field | Evidence record field |
|---|---|
| `id` | `id` |
| `type` | `evidence_kind` mapped: `test-result` to Test, `fault-observation` to Aegis, `static-analysis` and `semantic-analysis` to StaticAnalysis, `dependency-scan` and `sbom` to DependencyScan, `secret-scan` to SecretScan, `config-scan` to ConfigScan, `fuzz` to Fuzz, `manual-review` to ManualReview, `adversarial-test` to AdversarialTest, `runtime-observation` to RuntimeObservation, all others to Other |
| `source` | `producer.system` plus `producer.tool.name` |
| `subjectRef` | `subject.repository` + `@` + `subject.commit` |
| `observedAt`, `validUntil` | `timestamps.observed_at`, `timestamps.valid_until` |
| `invalidatedAt`, `invalidationReason` | latest `revoked` or `marked-stale` event |
| `producer`, `producerIdentity` | `producer.system`, `provenance.actor` |
| `artifactDigest` | first `subject.artifacts[].digest`, else `result.payload.digest` |
| `provenance.kind/issuer/runRef/workflowRef` | `provenance.identity_assurance`, signer provider, `provenance.run_ref`, `provenance.workflow_ref` |
| `independentOfImplementation` | `independence.independent_of_implementation` |
| `method`, `result`, `redacted`, `limitations` | `method.description`, `result.summary`, `disclosure.redacted`, `limitations` |

The projection is lossy only in the direction record to Tutela. Tutela should adopt
the richer fields (REC-TUTELA-002) rather than this repository maintaining a parallel
model.

### 7.2 Knowledge Store approach and storage

The Echelon Knowledge Store recommends Markdown with front matter as canonical plus
compiled registries (`echelon-knowledge-store@35d9cee0:README.md`); this repository
already uses JSON Lines for high-volume records (`docs/DUE-DILIGENCE-OPERATING-CONTRACT.md`,
"Record formats"). Evidence follows both:

- **Machine-produced records** (scans, diffs, quality snapshots, receipts) are canonical
  as one JSON object per line in `evidence/<producer>/<YYYY-MM>.jsonl`, or one JSON
  file per record when the producer writes atomically. Raw payloads are stored outside
  the record and referenced by digest.
- **Human-authored records** (manual reviews, exceptions, external attestations) are
  canonical as Markdown files whose YAML front matter is a valid evidence record and
  whose body is explanatory prose excluded from the signed content.
- **Compiled registry** `registries/evidence-records.json` is generated by the build
  tool, never edited, with per-record state, digest, signature verification result and
  reverse links from controls, answers and questions. Freshness of the compiled
  registry against sources is checked the way the Knowledge Store compiler does
  (`echelon-knowledge-store@35d9cee0:src/Echelon.KnowledgeStore.Compiler/Artifacts.fs`).

### 7.3 Praxis

- `provenance.actor` reuses the Praxis actor object and `provenance.execution_id` the
  `EXE-*` identifier (`praxis@12bf9951:docs/agent-provenance.md`).
- Praxis `EV-*` records are research evidence (`schemas/evidence.schema.json`,
  `evidence_type` primary, secondary, derived, test-result). They are not replaced;
  an evidence record links to them through `traces.related_records`.
- Human-authored evidence Markdown files carry Praxis front matter `provenance`
  contributions in addition to the evidence fields, and are attributed with
  `praxis provenance record`.
- `praxis work complete --evidence TYPE=PATH` may cite evidence record paths, binding
  a work item to signed evidence.
- Supersession uses the Praxis reciprocity rule (`supersedes` and `superseded_by`).
- Praxis verification receipts (`echelon.verification-receipt/1`) are embedded as
  `work-completion` records whose `signatures[]` carry the existing DSSE envelope.

## 8. Licensing constraint on verification

All proposed producers except the Registry are PolyForm Noncommercial 1.0.0
(DD-ARC-002 section 5). Verification criteria V-01 to V-15 deliberately depend only on
open standards (JSON Schema, RFC 8785, SHA-256, DSSE, ECDSA, Git) so an auditor can
verify records without a license to Echelon tooling. Reproducing a producer's
observation still requires a license (REC-ORGADMIN-002).

## 9. Open questions

- OQ-ARC-003-01: Key custody for producer signing keys (hardware, CI secret, managed
  KMS) and rotation period.
- OQ-ARC-003-02: Retention periods per disclosure class; the Standard leaves them
  unestablished.
- OQ-ARC-003-03: Whether RFC 8785 canonicalization is acceptable to Tutela's F# gate
  or whether a byte-exact payload (as in Praxis receipts) is preferred.
- OQ-ARC-003-04: Owner of runtime monitoring and therefore of `runtime-observation`
  producers.
