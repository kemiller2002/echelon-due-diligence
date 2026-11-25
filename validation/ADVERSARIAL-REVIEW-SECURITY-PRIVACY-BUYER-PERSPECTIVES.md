---
id: DD-VAL-ADV-002
title: Adversarial review from security, privacy, procurement, insurance and skeptical buyer perspectives
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [validation, adversarial-review, due-diligence, penetration-testing, privacy, procurement, insurance]
related_documents:
  - validation/objections-security-buyer.jsonl
  - docs/DUE-DILIGENCE-OPERATING-CONTRACT.md
  - architecture/ECHELON-CURRENT-STATE-BRIEF.md
  - security-by-construction/CWE-ARCHITECTURAL-PREVENTION-MATRIX.md
  - scanner-validation/SCANNER-VALIDATION-RESEARCH-REPORT.md
  - cost-avoidance/PENETRATION-TESTING-COST-REDUCTION-STRATEGY.md
  - architecture/AUTOMATED-QUESTIONNAIRE-RESPONSE-REQUIREMENTS.md
  - trust-center/TRUST-CENTER-REQUIREMENTS.md
---

# Adversarial review: security, privacy, procurement, insurance and skeptical buyer

## 1. Scope and method

Five reviewers, each reading as a skeptical expert in one role, examined the knowledge
base as it stood on 2026-11-25 (517 answer units, 2,363 canonical questions; the TEN
category was added while this review ran and was included). Objections are recorded in
`validation/objections-security-buyer.jsonl` (109 records, valid against
`schemas/dd/objection.schema.json`; every `target` ID and path was checked to exist).
No question, answer or other record was edited.

Sampling was by script over `answers/*.jsonl`, reading target, current, provable,
customer statement and challenge fields:

| Perspective | Answer units read closely | Other material |
|---|---|---|
| Penetration tester (PENTEST) | PEN, VUL, SCN, TEN, API, WLB, AIS, plus AUZ, ISP, NET, MON elimination claims (about 70) | CWE matrix L1 to L4 rows and bypass fields, SBC report Limen and Strata sections, capability analysis, DD-COST-001 |
| Privacy officer (PRIVACY) | PRV, RET, DON, AIG, plus IPR-004, LEG-005, TEN-007, BKP-005, AIS-002, SUP-004/005, DCL and GRT anonymity items (about 50) | AQR data handling, trust center |
| Procurement officer (PROCURE) | FST, ESC, TRM, INS, LEG, IPR, GOV, CUS, AUD, TPR, SUP (about 70) | Capability analysis licensing, cost avoidance report |
| Insurance underwriter (INSURER) | INS, AUN, END, BKP, PAY, IR, HR, FRD-003, ISP-006, FST-004 (about 60) | Insurance underwriting profile |
| Skeptical customer (SKEPTIC) | AIA, AIS, AIG, SDL, SCN, PEN, AUD, VUL, HR-006 (about 60) plus a full-corpus scan of history, cost_basis and acceptance fields | CWE matrix, scanner validation, DD-COST-001, AQR, trust center, `tools/build.fsx` |

Credit where due: the knowledge base is unusually candid. Every CWE row is marked
`proposed-target-state` with demonstrated level `none`; no answer claims a certification,
test, policy or insurance that does not exist; first-party material is labeled; and the
cost strategy claims no percentage saving. Ten objections were rejected on that basis.
The problems below are what remains after that candor.

## 2. Cross-cutting findings

1. **No human has approved anything.** All 517 answer units have one history entry,
   created by `research-agent` on 2026-11-25, and the schema has no reviewer or approval
   field (OBJ-SKEPTIC-001, OBJ-PROCURE-014). The honesty check in `tools/build.fsx`
   compares two metadata fields set by the same agent and never reads statement text
   (OBJ-SKEPTIC-002), yet ANS-AIA-007 cites it to customers as a safeguard.
2. **The corporate environment that exists is answered as if it did not.** Email, code
   hosting, package registries, domains and laptops exist today, and published npm and
   NuGet packages are live third-party attack surface, but MFA, EDR, backups, VDP and
   payment controls are recorded as `unknown` (OBJ-INSURER-001, OBJ-PENTEST-014).
   These are knowable facts, not research questions.
3. **Strongest claims depend on unbuilt components.** CWE-89 L1 relies on a Strata runtime
   query interface that does not exist; CWE-862 and CWE-639 rely on types not yet
   designed in code; the F# analyzers that would detect bypass do not exist
   (OBJ-PENTEST-007, OBJ-SKEPTIC-008).
4. **Commitments exceed the capacity and funding of a single-member company**: 24x7
   Severity 1 response in 30 minutes, 12-month transition at unchanged service levels,
   escrow with usability verification, SOC 1 and SOC 2, a funded wind-down plan
   (OBJ-PROCURE-004, OBJ-PROCURE-017).
5. **Licensing blocks commercial use.** Every Echelon component Unbound depends on is
   PolyForm Noncommercial 1.0.0; no commercial grant exists (OBJ-PROCURE-005).

## 3. Independent penetration tester

**Top objections**

- Nothing is testable: no code, environment or tenant (OBJ-PENTEST-001, blocking).
- Client-resident F# compiled to WebAssembly is attacker-controlled; the CWE matrix never
  limits L1 to L4 claims to server assemblies (OBJ-PENTEST-003, blocking).
- The source and build chain (single maintainer, gates inside the repositories they
  govern, partial provenance) is the real present attack surface (OBJ-PENTEST-013,
  blocking).
- L1 to L4 claims are verified by white-box code and build review, not by a pen test; a
  clean letter must not be read as confirming them (OBJ-PENTEST-002).
- RLS "owner bypass eliminated by FORCE" ignores superuser, BYPASSRLS and the Strata
  deploy identity, which can disable RLS (OBJ-PENTEST-004); shared-cluster leakage
  channels (pg_stat_statements, search_path, SECURITY DEFINER) are unaddressed
  (OBJ-PENTEST-005).
- CWE-639 at L2 conflates cross-tenant isolation with intra-tenant object authorization
  (OBJ-PENTEST-006); CONC rows at L2 cannot prevent transaction races
  (OBJ-PENTEST-015).
- Strata and Ordo run on .NET 8, out of support since 2026-11-10 (OBJ-PENTEST-008).
- Limen is "a lexical check, not a proof"; counter-evidence in Forma; wasm-unsafe-eval;
  Trusted Types gaps (OBJ-PENTEST-009). Embedded widgets add framing, postMessage and
  launch-token surface (OBJ-PENTEST-010). Folio HTML-to-PDF rendering is an unmodeled
  SSRF and file-read sink (OBJ-PENTEST-016).
- Prompt injection is not "contained by architecture": read-scope exfiltration and
  injection-to-human-approval remain (OBJ-PENTEST-011); repository instruction files are
  an injection path into coding agents (OBJ-PENTEST-012).
- A public honest-status trust center publishes a map of missing defenses
  (OBJ-PENTEST-019).

**Missing questions:** session token theft and OAuth consent phishing; agent instruction
file integrity; HTML-to-PDF renderer isolation; shared-cluster PostgreSQL hygiene;
client-side versus server-side trust boundary for WASM code; race-condition testing of
money flows; protocol-aware testing of the Limen boundary.

**Verdict:** cannot pass today; there is no target. What would change it: a deployed
release candidate; a server-only scope qualifier on all structural claims; RLS and
migration-identity separation with a release gate; a white-box structural review
separate from the pen test; hardened maintainer and CI identities; a VDP covering
published packages.

## 4. Privacy officer

**Top objections**

- No privacy program, notice, record of processing, DPA or named owner (OBJ-PRIVACY-001,
  blocking).
- No applicability register: GLBA status, Echelon's own Safeguards Rule status, which
  state laws cover nonprofit sponsors, and Indiana's own law are unresolved
  (OBJ-PRIVACY-002, OBJ-PRIVACY-003).
- Cryptographic erasure as deletion lacks a legal basis, and retained amounts, dates and
  grantees re-identify donors in small populations (OBJ-PRIVACY-004); erasure collides
  with 17a-4, IRS and hold duties without a precedence rule (OBJ-PRIVACY-005); key
  persistence in replicas, archives and KMS waiting periods is unaddressed
  (OBJ-PRIVACY-006).
- Donor anonymity leaks through fund names that contain donor surnames and through bank
  remittance channels (OBJ-PRIVACY-007); legal process directed at Echelon is not
  handled (OBJ-PRIVACY-008).
- "No training or evaluation" contradicts model risk validation promised to banks
  (OBJ-PRIVACY-009); provider retention and offshore abuse review conflict with US-only
  processing (OBJ-PRIVACY-010); questionnaires may already be reaching model providers
  (OBJ-PRIVACY-011).

**Missing questions:** government and third-party legal process served on the vendor;
state donor privacy statutes; Indiana Consumer Data Protection Act applicability; host
page tracking around embedded widgets; retention of security telemetry; precedence of
retention over erasure.

**Verdict:** cannot pass today. What would change it: a counsel-reviewed DPA and
applicability register; a counsel opinion on cryptographic erasure and a precedence rule
set; a re-identification analysis of retained payloads; a written decision on AI training
and evaluation; verified provider terms; a subprocessor list.

## 5. Procurement officer

**Top objections**

- Contracting entity standing undocumented (OBJ-PROCURE-001), no insurance
  (OBJ-PROCURE-002), no financials or runway (OBJ-PROCURE-003): each blocking.
- Staffing-dependent commitments a single person cannot meet (OBJ-PROCURE-004,
  blocking).
- PolyForm Noncommercial licensing of every dependency (OBJ-PROCURE-005, blocking).
- AI-drafted responses with no named signatory cannot be relied on as representations
  (OBJ-PROCURE-014, blocking).
- Chain of title unrecorded and AI-authored code may be only partly protectable
  (OBJ-PROCURE-006); escrow unusable without the founder's toolchain
  (OBJ-PROCURE-007).
- No SOC report possible for months after launch (OBJ-PROCURE-009); no contract paper or
  counsel (OBJ-PROCURE-010); no hosting decision (OBJ-PROCURE-011); regulatory perimeter
  asserted as fact in GOV-007 while AML-006 says counsel has not confirmed it
  (OBJ-PROCURE-012).
- The cost of the target program is never totaled; all 517 cost bases are unsourced
  judgments (OBJ-PROCURE-017).

**Missing questions:** customer references and production track record (only bank and
trade references are asked); live customer count; pilot and design-partner terms;
refund or exit rights if delivery slips.

**Verdict:** cannot pass today; would be stopped at entity, insurance and financial
gates before security review begins. What would change it: formed entity in good
standing; bound cyber and E&O; a financial transparency package showing runway beyond
contract term; a commercial license grant; counsel-drafted paper with commitments sized
to capacity; a named signatory; an honest pilot offer with exit rights.

## 6. Cyber insurance underwriter

**Top objections**

- The corporate environment is answered `unknown` on every gating control
  (OBJ-INSURER-001, blocking).
- The answer library and AI drafting must never be used to complete applications;
  aspirational answers become warranties and support rescission (OBJ-INSURER-002,
  blocking).
- Founder account takeover is the catastrophic loss and its controls are unrecorded
  (OBJ-INSURER-003, blocking).
- EDR is argued away architecturally (OBJ-INSURER-004); corporate and repository
  backups are unaddressed (OBJ-INSURER-005); no IR plan or tabletop for the company
  (OBJ-INSURER-009).
- Third-party liability for misdirected grants is missed by the "no funds held"
  argument (OBJ-INSURER-006); no dual authorization for Echelon's own payments
  (OBJ-INSURER-007).
- Panel vendor and consent conditions ignored (OBJ-INSURER-008); contractual liability
  beyond policy coverage (OBJ-INSURER-011); AI-related exclusions not considered
  (OBJ-INSURER-012); the profile relies on 2022 supplements and never retrieved a
  technology E&O form (OBJ-INSURER-016).

**Missing questions:** insurer panel and consent; AI exclusions and sublimits;
retroactive date and prior acts for already-published software; material change notice
at go-live; email domain authentication (SPF, DKIM, DMARC).

**Verdict:** would not bind today; the application could not be completed truthfully
with "yes" answers on MFA, EDR, backups or IR planning. What would change it: a two-week
corporate hardening sprint (hardware-key MFA on every founder account, named EDR,
immutable repository backups, DMARC reject, a written IR plan and tabletop, bank dual
approval with an outside accountant), each recorded as a dated current fact, and an
application completed by a human from that evidence only.

## 7. Skeptical prospective customer

**Top objections**

- The knowledge base is entirely AI-written and unapproved (OBJ-SKEPTIC-001, blocking);
  the customer-facing description of the build check overstates it (OBJ-SKEPTIC-002).
- AI-generated code controls are the weakest area (AIS-008 `unknown`) while its customer
  statement leads with a present-tense benefit; agents can add warning suppressions to
  gates in the repositories they edit (OBJ-SKEPTIC-009, blocking).
- Candor is not assurance; the volume of target answers reads as progress
  (OBJ-SKEPTIC-020, blocking).
- The CWE matrix: 202 rows labeled "beyond" scanning with nothing demonstrated
  (OBJ-SKEPTIC-003); level assignments contradicted by their own bypass lists for
  CWE-457, CWE-396, CWE-252 and CWE-636 (OBJ-SKEPTIC-004); copy-paste bypass text in
  CWE-1321 (OBJ-SKEPTIC-005); generator not committed (OBJ-SKEPTIC-006); L1 count
  inflated by 11 not-applicable platform rows (OBJ-SKEPTIC-008).
- Provenance is self-reported with `model: unknown` (OBJ-SKEPTIC-010); scanner holdouts
  cannot be independent with one person and AI agents (OBJ-SKEPTIC-011).
- The pen test cost lever conflicts with the larger scope Echelon itself specifies; the
  first test will likely cost more, not less (OBJ-SKEPTIC-012). Acceptance likelihoods
  are agent opinions (OBJ-SKEPTIC-014).
- AQR: unspecified claim-diff mechanism, negated questions and picklists defeat the
  status-to-wording rule (OBJ-SKEPTIC-015); wrong-match failures pass every gate
  (OBJ-SKEPTIC-016); knowledge base text is trusted though agent-written from web sources
  (OBJ-SKEPTIC-017).

**Missing questions:** who reviewed each answer and what they verified; what share of
code is AI-written and what share of that was human-reviewed; how many warning
suppressions or banned-API attempts gates have blocked; how matching errors are measured
after release.

**Verdict:** would not buy today and would discount the security-by-construction story
as marketing until at least one structural claim is demonstrated with build evidence and
confirmed by an independent party. What would change it: human approval on every
released answer; the CWE-89, CWE-862 and CWE-639 mechanisms built with negative and
bypass tests; out-of-repository gates with suppression reporting; an independent
white-box review that tests the structural claims; a reproducible matrix generator.

## 8. Prioritized actions (proposed; nothing here is implemented)

1. Add human approval fields and a release gate to the answer-unit schema.
2. Record verified current facts for the existing corporate environment (accounts, MFA,
   devices, backups, DNS, payments, published packages).
3. Bind insurance only from those facts; prohibit AI or target-answer use in
   applications.
4. Issue a commercial license grant covering all Echelon components.
5. Commit the CWE matrix generator; fix contradictory level assignments and the
   CWE-1321 copy-paste; add a server-only scope qualifier and a dependency-exists field.
6. Publish a VDP and SECURITY.md for published packages; harden maintainer and CI
   identities.
7. Engage counsel for the privacy applicability register, DPA, erasure opinion and
   regulatory perimeter memo.
8. Resize staffing-dependent commitments to current capacity.
9. Build a sourced cost model of the target assurance program.
10. Produce the first independent artifact (design review now, pen test when a release
    candidate exists) before expanding the knowledge base further.
