---
id: DDD-002
title: Canonical question deduplication and overlap log
status: accepted
version: 1.0.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, question-bank, deduplication]
---

# DDD-002: Canonical question deduplication and overlap log

## Context

DD-GOV-001 requires that a new question differ from existing questions in concern, tested
control, required evidence or population, and that rewordings live in `alternatives`.
`tools/build.fsx` flags question pairs whose token Jaccard similarity is 0.8 or more as
`NEAR-DUP`. A refinement pass on 2026-11-25 reviewed the build warning, the known ASM
versus SCS SBOM overlap, and every other question pair with similarity of 0.6 or more.

## Rules applied

1. Nothing is retired silently. A redundant question is either kept and pointed to the
   same answer unit as its twin, with an `answer_scope_note` naming the twin, or merged by
   moving its text into the surviving question's `alternatives`.
2. Merging retires the identifier. A retired identifier is listed below and must not be
   reused.
3. Every affected record carries a `history` entry with `decision_ref` `DDD-002`.
4. Lexical similarity alone is not duplication. Pairs that share wording but differ in
   concern are recorded as reviewed and kept.

## Decisions

| # | Questions | Finding | Decision |
|---|---|---|---|
| D1 | DDQ-FCT-0015, DDQ-FEE-0015 | Build `NEAR-DUP` (Jaccard 0.86). Both ask how fee waivers are approved, time-limited and reported. ANS-FEE-003 explicitly covers waivers; ANS-FCT-003 covers fee schedule and computation change control. | Merged. DDQ-FCT-0015 text added to DDQ-FEE-0015 `alternatives`; its source references and industries were folded into DDQ-FEE-0015. **DDQ-FCT-0015 is retired and must not be reused.** ANS-FCT-003 keeps four questions (DDQ-FCT-0012 to 0014 and 0016). |
| D2 | DDQ-ASM-0005, DDQ-SCS-0011 | Both ask for a per-release SBOM in SPDX or CycloneDX and how it is kept current and obtained. They were answered twice (ANS-ASM-002 and ANS-SCS-003). | Kept both. DDQ-ASM-0005 repointed to ANS-SCS-003 with controls and evidence requirements aligned and an `answer_scope_note` naming DDQ-SCS-0011. DDQ-ASM-0005 wording added to DDQ-SCS-0011 `alternatives`. ANS-ASM-002 remains the answer for the broader component inventory (internal frameworks, AI components, unapproved software, end-of-life; DDQ-ASM-0006 to 0009). |
| D3 | DDQ-LEG-0011, DDQ-IR-0021 | Same duty: bank service provider notice under the 2021 Computer-Security Incident Notification rule (four-hour material disruption). Answered by both ANS-LEG-003 and ANS-IR-005. | Kept both. DDQ-LEG-0011 repointed to ANS-IR-005 with controls and evidence requirements aligned; scope note names DDQ-IR-0021. ANS-LEG-003 still answers general notification obligations (DDQ-LEG-0010, 0012 to 0014). |
| D4 | DDQ-ACT-0034, DDQ-RRP-0002 | Both ask how Form 990 Schedule D figures reconcile to audited statements and to fund statements (Jaccard 0.60). | Kept both. DDQ-ACT-0034 repointed from ANS-ACT-008 to ANS-RRP-001 (Schedule D data package) with controls and evidence requirements aligned; scope note names DDQ-RRP-0002. |
| D5 | DDQ-CHG-0027, DDQ-INF-0023, DDQ-ASM-0019 | Overlap in "detect changes outside the approved process" (CHG-0027 versus INF-0023, Jaccard 0.67) and configuration drift (INF-0023 versus ASM-0019). | Kept distinct: CHG-0027 tests unauthorized change to deployed code, infrastructure definitions and data paths; INF-0023 tests configuration setting drift; ASM-0019 tests drift from secure baselines. Scope note added to DDQ-CHG-0027 naming the other two. |
| D6 | DDQ-AIG-0011, DDQ-INV-0025 | Jaccard 0.78 on shared exception-process wording. Concerns differ (AI policy exceptions versus investment policy exceptions); different populations and evidence. | No change. Lexical false positive. |

## Reviewed and kept (no change)

- DDQ-INF-0014 (SBOM of the deployed service including base image and runtime,
  ANS-INF-004): distinct population (runtime environment of a hosted service) from the
  release SBOM in ANS-SCS-003.
- DDQ-IPR-0013 (SBOM with license information, ANS-IPR-003): distinct concern (license
  compliance) even though its alternative also asks for an SBOM.
- DDQ-ESC-0013 (reproducible builds with SBOMs for escrow, ANS-ESC-004): distinct concern
  (correspondence of escrowed source to running software).
- DDQ-AIS-0025 (AI bill of materials, ANS-AIS-005) and DDQ-ASM-0008 (AI model and agent
  inventory, ANS-ASM-002): related but distinct; one tests the SBOM format, the other the
  inventory of AI used in product and engineering.

## Consequences

- The build reports no `NEAR-DUP` warning after this pass.
- Questions added from DD-QNR-001 on the same date were checked against existing
  question text and alternatives by script before creation; covered topics were added as
  `alternatives` with `SRC-Q-*` references instead of new questions.
- Future near-duplicates should be resolved the same way and appended to this log.
