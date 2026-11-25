---
id: DD-VAL-ADV-001
title: Adversarial review of the due diligence knowledge base from five financial-sector perspectives
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, adversarial-review, validation, financial-services, soc2, tprm, daf]
related_documents:
  - validation/objections-financial.jsonl
  - docs/DUE-DILIGENCE-OPERATING-CONTRACT.md
  - architecture/ECHELON-CURRENT-STATE-BRIEF.md
  - schemas/dd/objection.schema.json
  - reports/generated/REGISTER-SUMMARY.md
---

# Adversarial review: five financial-sector perspectives

## 1. Scope and method

This review tests the knowledge base as five skeptical reviewers would. A bank chief
information security officer (BANKCISO); a financial institution vendor risk manager
applying the 2023 Interagency Guidance on Third-Party Relationships (VRM); a CPA
performing a SOC 2 (and SOC 1) examination (SOC2AUD); a financial regulator examining a
bank's critical vendor relationship (REGULATOR); and a DAF sponsor, both a national
sponsor and a bank-affiliated sponsor's board and CFO (DAFSPONSOR).

What was read:

- The operating contract, current-state brief, objection schema and generated register
  summary (517 answer units, 595 evidence requirements, 167 challenge analyses at the time
  of review; the register grew during the review as another agent added the TEN category).
- Answer units dumped by script and read closely: every unit in TPR, ISP, AUD, PEN, SUB,
  INS, FST, IR, BCP, DR, CON, REG, TEN, DAF, PAY, RCN, GRT, INV, AML and FEE (about 190
  units), plus ENC, IAM, SDL, CHG, HR, SCS, MON, AVL, LEG, GOV, RSK, AIG and selected FCT,
  AIA, PRV, CLD, CUS, IPR and SUP units. Each perspective drew on well over 40 units.
- All 167 challenge analyses, summarized by script, with the 40 rated "likely" in core
  security and financial categories read individually.
- Evidence requirements for TPR, AUD, TEN, IAM, PAY, ISP, FST and BCP, plus an
  independence tally across all 595.
- `security-by-construction/` (report summary, assurance model, sections 6 to 12),
  `scanner-validation/` (findings), `external-assurance/` (matrix and CSV), both
  `cost-avoidance/` reports, both `trust-center/` documents,
  `architecture/AUTOMATED-QUESTIONNAIRE-RESPONSE-REQUIREMENTS.md`,
  `architecture/EVIDENCE-ARCHITECTURE-SPECIFICATION.md` and the financial-services and
  DAF industry profiles.
- The canonical question bank, searched by script for questions each perspective always
  asks.

Output: 98 objections in `validation/objections-financial.jsonl` (BANKCISO 20, VRM 21,
SOC2AUD 20, REGULATOR 18, DAFSPONSOR 19). 5 are blocking, 63 major and 30 minor. 88 are
`accepted-open`. 10 are `rejected-with-rationale` because the knowledge base already
handles them; they are kept to show where it holds up. No question, answer or other
record was edited.

## 2. Cross-cutting findings

These findings recur under several perspectives.

1. **The honesty is real.** Statuses are conservative, customer statements do not claim
   unbuilt capability, first-party labeling is consistent, and stale references (FFIEC
   CAT, OCC 2013-29, the withdrawn adviser outsourcing proposal) are already flagged.
   Most rejected objections fall here. The knowledge base will not mislead a reviewer
   about what exists. Its weaknesses are what it does not plan for and the institutional
   judgments it makes without evidence.
2. **The evidence model is almost entirely first-party.** 565 of 595 evidence
   requirements are first-party and 23 are independent. In the security, financial,
   legal and operational categories reviewed, 264 of 284 answer units link no
   independent evidence requirement. That includes every payment, reconciliation, grant,
   fee and sanctions unit. Five of the seven `requires-external-validation` units have no
   non-first-party evidence requirement. (OBJ-BANKCISO-001, OBJ-BANKCISO-007,
   OBJ-REGULATOR-005)
3. **Institutional acceptance ratings are unsourced.** None of the 167 challenge
   analyses cites a source. 134 rate the alternative "stronger" and 84 rate acceptance
   "likely", all as the authors' own judgment. This is the main place where technical
   superiority is presented as if it meant institutional acceptance. (OBJ-VRM-019,
   OBJ-SOC2AUD-007, OBJ-SOC2AUD-016)
4. **Many controls depend on people who do not exist yet.** The target state relies on
   two-person and three-person controls (independent review, break-glass, restores,
   payment release, AQR release separation), but headcount is never stated and the
   company is founder-led. (OBJ-BANKCISO-004, OBJ-SOC2AUD-004, OBJ-DAFSPONSOR-011)
5. **The assurance timeline is inconsistent and SOC 1 is missing from the cost
   picture.** SOC 2 is planned "after production launch", while a SOC 1 Type 2 is
   required "before the first hosted sponsor's fiscal year end". The external assurance
   matrix and the cost avoidance report have no SOC 1 entry. (OBJ-SOC2AUD-001,
   OBJ-SOC2AUD-002)
6. **There are internal contradictions.**
   - ANS-HR-006, the only `implemented-not-independently-verified` unit, states
     attribution as fact. ANS-ISP-007 says the same records are self-declared and
     unauthenticated.
   - LEG-003 and IR-004 use different triggers for the 24-hour notice.
   - PAY-008's three-person release conflicts with RCN-004's residual-risk acceptance for
     small sponsors.

   (OBJ-BANKCISO-002, OBJ-BANKCISO-012, OBJ-DAFSPONSOR-011)
7. **Bank-facing gaps that end a sale:** no operating history or references question; no
   12 CFR Part 9 coverage for bank-trustee sponsors; no default contacts (CEO and CIO)
   under the incident notification rule; no resolution-planning continuity terms; and no
   handling of the confidentiality of customer questionnaires processed by AI.

## 3. Bank chief information security officer (BANKCISO)

**Top objections**

- OBJ-BANKCISO-001 (blocking): no independent assurance today, and an evidence model
  that rarely names how a money or tenancy control will be independently proven.
- OBJ-BANKCISO-004 (blocking): two-person controls without a second person.
- OBJ-BANKCISO-010 (blocking): incident notification promises without 24x7 detection or
  an IR retainer (IR-002 and MON-004 are unknown).
- OBJ-BANKCISO-003: AI-written code in a payment system. No independent secure code
  review is planned, and the share of agent-authored code is not disclosed.
- OBJ-BANKCISO-005 and -006: the security-by-construction L-scale and "202 beyond
  scanning" counts are self-ratings, and home-built F# analyzers have no track record.
- OBJ-BANKCISO-011: founder endpoint and AI engineering providers that receive source
  code, threat models and pipeline context are not addressed.
- OBJ-BANKCISO-008: out-of-support .NET runtime in Strata and Ordo.
- OBJ-BANKCISO-009: pen test cost levers (P3, P5, P8, P10) read as steering or reduced
  independence.
- OBJ-BANKCISO-012: contradictory notification triggers.
- OBJ-BANKCISO-013: payment file integrity requirements are not written.

**Missing questions:** threat intelligence sharing (FS-ISAC or equivalent); headcount and
named operators of two-person controls; AI engineering provider access to source and
security design; independent secure code review.

**Verdict: would not pass today.** The architecture would interest a bank CISO, but no
control operates and nothing is independently tested. A CISO cannot approve a critical
vendor on that basis.

**What would change the verdict:**

- An independent pen test letter covering tenant isolation, authorization and payment
  paths.
- A SOC 2 Type I at minimum.
- An independent secure code review of control-relevant modules.
- A contracted MDR and IR retainer.
- Named second operators for two-person controls.
- Supported runtimes.
- Endpoint and AI-provider controls with evidence.

## 4. Vendor risk manager under the Interagency Guidance (VRM)

**Top objections**

- OBJ-VRM-001 (blocking): every interagency due diligence factor lacks evidence, and the
  activity is critical.
- OBJ-VRM-002: no operating-history or references question.
- OBJ-VRM-003: reviewed rather than audited financial statements, plus a first-party
  runway attestation.
- OBJ-VRM-004: liability super-cap tied to shared aggregate insurance limits, and an
  admitted-carrier requirement that may be unachievable.
- OBJ-VRM-005, -006 and -007: AQR picklists strip qualifiers; customer questionnaires go
  to model providers without consent; AI-drafted answers and agent-verified regulatory
  citations have had no human or counsel review.
- OBJ-VRM-008: no minimum operating control set before a financial-services submission.
- OBJ-VRM-010 and -012: evidence records that could make a consultant letter or a
  non-attest review look equivalent to a SOC report.
- OBJ-VRM-013: the escrow exit plan is not executable while components are PolyForm
  Noncommercial with no commercial license.
- OBJ-VRM-014: Nacha Rules compliance audit expectation from the ODFI.
- OBJ-VRM-016: amended Regulation S-P terms are an intention, not a commitment, after
  the compliance dates have passed.
- OBJ-VRM-019: unsourced acceptance ratings.

**Missing questions:** operating history, customer count and references; handling of
customer-supplied questionnaires and contracts with AI tools; implementation plan.

**Verdict: would not pass today.** The file cannot be completed defensibly. An honest
AQR response would answer "not yet" to most items, and a bank TPRM scoring tool would
rate residual risk high.

**What would change the verdict:**

- The minimum operating control set in OBJ-VRM-008 reaching implemented status.
- CPA-reviewed financials, with agreed-upon procedures on runway.
- Bound insurance.
- A selected and assessed subprocessor set.
- A commercial license plus verified escrow.
- AQR safeguards for qualifiers and confidentiality.
- Human and counsel sign-off on released answers.

## 5. SOC 2 auditor (SOC2AUD)

**Top objections**

- OBJ-SOC2AUD-001 (blocking): the SOC 2 and SOC 1 timing is inconsistent and infeasible.
- OBJ-SOC2AUD-002 and -003: SOC 1 is missing from the cost and assurance matrices, and
  Processing Integrity is in the SOC 2 scope without serving user auditors.
- OBJ-SOC2AUD-004: the CC1.2 governance independence gap.
- OBJ-SOC2AUD-005: AI-performed controls cannot be baselined like automated controls.
- OBJ-SOC2AUD-006: signed evidence proves integrity, not completeness. The Praxis,
  Tutela and Strata pipelines become in-scope systems, and first-year hours may rise.
- OBJ-SOC2AUD-007: self-declared Praxis provenance is not change-authorization evidence.
- OBJ-SOC2AUD-008: V-11 equates "different identity" with independence.
- OBJ-SOC2AUD-009: "auditor acceptance" of a gate design misreads the auditor's role and
  risks independence.
- OBJ-SOC2AUD-010: readiness or advisory work by the same firm would raise independence
  questions.
- OBJ-SOC2AUD-011: SOC 1 restricted use is incompatible with NDA-tier auto-approval in
  the trust center.
- OBJ-SOC2AUD-013: CUEC burden on small sponsors.
- OBJ-SOC2AUD-017: the proposed Standard assigns controls to systems that do not perform
  them.
- OBJ-SOC2AUD-018: first-period reports with no occurrences to test.

**Missing questions:** the bank asks about SOC 1 and CUECs (DDQ-AUD-0008, DDQ-FCT-0021),
but nothing covers the first report's type, as-of date and period relative to each
sponsor's fiscal year end, or which CPA firm and peer review applies.

**Verdict: not examinable today.** No controls are placed in operation, so even a Type I
cannot be issued. Several design choices would create exceptions or independence
concerns in a first examination.

**What would change the verdict:**

- Adopted and corrected policies.
- A governance body with real oversight.
- Named control performers, with no AI-only key controls.
- An agreed reliance approach for custom evidence pipelines.
- A CPA firm independent of readiness work.
- A sequenced plan: SOC 2 Type I and SOC 1 Type 1 at go-live, then Type 2 periods sized
  to transaction volume and sponsor fiscal years.

## 6. Financial regulator examining a bank's critical vendor (REGULATOR)

**Top objections**

- OBJ-REGULATOR-001 (blocking): the examiner judges the bank's diligence file, and that
  file would draw criticism. This is the real reason banks will not engage.
- OBJ-REGULATOR-002: no coverage of OCC fiduciary activities under 12 CFR Part 9 (or
  state trust analogues) for bank-trusteed charitable funds.
- OBJ-REGULATOR-003: the default-contact (CEO and CIO) fallback under the 2021 incident
  notification rule is missing, and IR-005 is unknown.
- OBJ-REGULATOR-004: GOV-007 states a regulatory-perimeter conclusion that counsel has
  not confirmed.
- OBJ-REGULATOR-005: requires-external-validation units with no validation evidence
  requirement.
- OBJ-REGULATOR-006: Echelon's own OFAC strict-liability exposure in the payment chain.
- OBJ-REGULATOR-007: resolution-planning continuity terms for large banks.
- OBJ-REGULATOR-013: unfair or deceptive practices in donor-facing experiences.
- OBJ-REGULATOR-014: examination readiness with one principal.
- OBJ-REGULATOR-015: no independent verification of AI agent controls.
- OBJ-REGULATOR-017: correlated key-person risk across institutions.

**Stale or uncertain references:** the knowledge base already marks the FFIEC CAT
withdrawn, OCC 2013-29 rescinded and the adviser outsourcing proposal withdrawn
(rejected objections confirm this). Some recent items were verified only by agent
retrieval. These need professional reverification before any customer use: the 2026
interagency TPRM replacement proposal, the October 2025 NYDFS third-party letter, the
Nacha 2026 rules edition and the FFIEC Outsourcing booklet status (OBJ-REGULATOR-011).
This reviewer could not independently confirm them.

**Missing questions:** bank-trustee fiduciary oversight; resolution continuity; donor-facing
UDAP and deceptive claims; examination readiness and regulatory liaison.

**Verdict: would not pass today.** A bank relying on Echelon for a critical activity
would be exposed to supervisory criticism. Echelon's own BSCA acknowledgment and its
approach to GLBA, model risk and OFAC recordkeeping are sound in design (rejected
objections), but nothing operates.

**What would change the verdict:**

- Everything under BANKCISO and VRM.
- Counsel opinions on regulatory perimeter, OFAC exposure and bank-trustee fiduciary
  requirements.
- Corrected incident notification contacts.
- Resolution-resilient terms.
- A named regulatory liaison and successor operator.

## 7. DAF sponsor: national sponsor and bank-affiliated sponsor's board and CFO (DAFSPONSOR)

**Top objections**

- OBJ-DAFSPONSOR-001 (blocking): a board cannot document a prudent selection of a
  pre-production, single-principal administrator.
- OBJ-DAFSPONSOR-002: no conversion or parallel-run coverage.
- OBJ-DAFSPONSOR-003: no pricing or total cost to the sponsor.
- OBJ-DAFSPONSOR-004: allocation of excise tax under sections 4966, 4967 and 4958 when
  a platform defect lets a prohibited distribution through.
- OBJ-DAFSPONSOR-005: who pays for incremental audit work before a SOC 1 exists.
- OBJ-DAFSPONSOR-006: Pub. L. 119-21 section 170(p) excludes DAF gifts from the new
  non-itemizer deduction. It is recorded in the sources, but no question or answer uses
  it in donor-facing content.
- OBJ-DAFSPONSOR-007: first year-end readiness.
- OBJ-DAFSPONSOR-008: the build-instead-of-buy agenda competes with core delivery.
- OBJ-DAFSPONSOR-009: the wind-down, escrow and license protections do not exist yet.
- OBJ-DAFSPONSOR-010: achievable insurance limits are tiny relative to sponsor assets.
- OBJ-DAFSPONSOR-011 and -012: three-person release and the sponsor-as-Originator model
  shift staffing and banking cost to sponsors.
- OBJ-DAFSPONSOR-014: an incumbent's SOC 2 Type 1 treated as the baseline to beat.

**Cost avoidance claims that would not survive this reader:** H10 and H11 (own
compliance monitoring and own F# analyzers) carry high delivery opportunity cost for a
one-principal vendor. H4 (fewer auditor hours) may reverse in early years
(OBJ-SOC2AUD-006). H5 (one SOC 2 for all products) increases blast radius. SOC 1 is
missing from the cost picture altogether.

**Missing questions:** conversion from the incumbent administrator; Echelon pricing and
total cost; excise tax and correction-cost allocation; implementation plan and sponsor
effort; donor-facing deductibility after the 2025 tax law changes.

**Verdict: would not pass today** for either sponsor type as a production system of
record. A bank-affiliated sponsor is in practice decided by the parent's TPRM (see
VRM). A national sponsor would at most consider a design-partner arrangement with the
incumbent kept as system of record.

**What would change the verdict:**

- A design-partner phase with a completed parallel run through a year-end.
- A SOC 1 Type 1, then Type 2, aligned to the sponsor's fiscal year.
- Disclosed pricing.
- An excise-tax error indemnity outside the general cap.
- A funded wind-down with a commercial license and verified escrow.
- A named successor operator.
- Release-control tiers that match sponsor staffing.

## 8. Recommended next steps for the knowledge base (proposals only)

1. Add the missing canonical questions listed above (operating history and references,
   conversion, pricing, excise tax allocation, implementation plan, threat intelligence
   sharing, AI handling of customer documents, bank-trustee fiduciary oversight,
   resolution continuity, donor-facing deceptive claims, 170(p) deductibility language).
2. Add a build rule that `requires-external-validation` answers must link a
   non-first-party evidence requirement. Add independent evidence requirements to money
   movement, tenant isolation and privileged access answers.
3. Add a `basis` field to challenge analyses and reset unsourced acceptance ratings to
   "author judgment, unvalidated".
4. Write one assurance roadmap answer (SOC 2, SOC 1, pen test, code review) and point
   AUD-001, AUD-002, FCT-004 and RCN-005 to it. Add SOC 1 to the external assurance
   matrix and the cost report.
5. Resolve the HR-006 versus ISP-007, LEG-003 versus IR-004 and PAY-008 versus RCN-004
   contradictions, and add them as AQR contradiction fixtures.
6. Define a minimum operating control set and a staffing statement that gate
   financial-services submissions.
