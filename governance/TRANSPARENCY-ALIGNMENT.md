---
id: DD-GOV-TRN-001
title: Due diligence alignment with the organizational transparency policy
status: proposed
version: 0.1.0
classification: public
created: 2026-11-25
updated: 2026-11-25
origin: echelon-registry work item GOV-TRN-001
related:
  - POL-ORG-TRN-001 Organizational Transparency Policy (public projection: echelon-registry portfolio/governance/policies/)
  - STD-ORG-CLS-001 Information Classification Standard
  - STD-ORG-PUB-001 Public Disclosure and Publication Safeguards Standard
  - DD-GOV-001 Due Diligence Research Operating Contract (research branch claude/echelon-due-diligence-research-6vrnsy, unmerged as of 2026-11-25)
---

# Due diligence alignment with the organizational transparency policy

**Status: proposed.** This file adds governance requirements; it does not change the research
operating contract DD-GOV-001 being written on the due diligence research branch, and it introduces no
competing vocabulary. Where DD-GOV-001 already covers a point, this file only maps to it. The
comprehensive due diligence research initiative (INIT-002) continues independently.

## 1. This repository stays public

echelon-due-diligence is **public** and its research is **Public** by default (POL-ORG-TRN-001 §3:
"due diligence questions and approved answers"). Nothing here changes repository visibility.

## 2. What the public knowledge base contains

| Content | Public? | Record (DD-GOV-001) |
|---|---|---|
| Canonical due diligence questions (original wording) | yes | `questions/` (`DDQ-*`) |
| Recommended target answers | yes | answer unit `target_answer` |
| Approved current answers | yes, once approved (§4) | answer unit `customer_statement` |
| Control definitions | yes | `controls/` (`ECTL-*`) |
| Regulatory applicability research | yes | research records with sources |
| Evidence requirements | yes | `evidence-requirements/` (`EVR-*`) |
| Verification methodologies | yes | answer unit `evidence_mechanism`, methodology documents |
| External assurance and cost-avoidance research | yes | research records; cost figures with `cost_basis` |
| Security-by-construction research | yes | links to SEC-* rules |
| Framework mappings | yes, by identifier and locator only (licensed text excluded, DD-GOV-001 rule 5) | question `alternatives`/sources |
| Non-sensitive capability gaps | yes | answer unit `status` and `residual_risks` |
| Research limitations, decision rationale | yes | research records, decisions |
| **Supporting evidence itself** | **no**, unless the evidence is itself Public | referenced by evidence id and class only |

Requirement **DDT-01**: a public question or answer never implies that its supporting evidence is
public. Where evidence is Confidential or Restricted, the answer cites an evidence reference
(id, class, freshness, status) and, where useful, a sanitized summary; the evidence stays in the
restricted evidence store (STD-ORG-CLS-001 §2).

## 3. Five distinctions every answer must make

The transparency policy requires every public capability statement to distinguish what Echelon
intends, has implemented, has verified, has had independently assessed, and may legitimately claim.
DD-GOV-001 already encodes most of this. Mapping (requirement **DDT-02**: use DD-GOV-001's fields; do
not add a parallel field):

| Policy claim status (POL-ORG-TRN-001 §6) | DD-GOV-001 answer unit |
|---|---|
| `intended` | `status`: `proposed-target-state` or `approved-policy-implementation-pending`; `customer_statement_kind`: `planned` |
| `implemented` | `status`: `partially-implemented` or `implemented-not-independently-verified`; `assurance_independence`: `none` or `first-party` |
| `verified-internal` | `status`: `verified-operational` with `assurance_independence`: `first-party` and an evidence reference |
| `assessed-independent` | `status`: `verified-operational` with `assurance_independence`: `independent-third-party` or `regulatory-examination`, plus `external_assurance` naming scope and date |
| `claimable` | **gap**: DD-GOV-001 has no approval state for customer use. Proposed: add `approval` `{ "approvedBy", "approvedOn", "scope", "expires" }` to the answer unit (DDT-03) |
| unknown | `status`: `unknown` |

**DDT-03** (proposed schema change for the research branch owner to decide): an answer's
`customer_statement` may be used outside this repository only when `approval` is present and not
expired. Until then every `customer_statement` is a draft.

**DDT-04** First-party verification is labelled first-party wherever it appears, including generated
reports and any trust center projection; no wording such as "certified", "audited" or "compliant" is
used without `assessed-independent` status for exactly that scope.

## 4. Classification of answer units

DD-GOV-001's `disclosure_classification` describes the **audience tier** (public, authenticated
prospect, NDA, customer-only, auditor-only, internal). STD-ORG-CLS-001 describes the **information
class**. Mapping (DDT-05):

| `disclosure_classification` | STD-ORG-CLS-001 class | May live in this public repository? |
|---|---|---|
| `public` | Public | yes |
| `authenticated-prospect`, `nda`, `customer-only`, `auditor-only` | Confidential (audience-limited) | **no** — record only the answer's existence, status and audience tier here; the text lives in the access-controlled store |
| `internal` | Internal | **no** |

There is no Restricted tier for answers by design: an answer that would need Restricted content is
answered with an opaque reference.

**DDT-06** The build tool should fail when a record in this repository has a non-`public`
`disclosure_classification` and a non-empty `customer_statement` (aligns with STD-ORG-PUB-001
PUB-SG-10).

## 5. Restriction requires a justification

Answers withheld from the public tier must record a legitimate justification category from
STD-ORG-CLS-001 §7 (for example `security-exploitable`, `contractual`). "The answer is unfavourable"
(for example `unsupported` or `unknown` status) is **not** a justification: unfavourable statuses are
published (POL-ORG-TRN-001 §5.2). DDT-07.

## 6. Freshness

**DDT-08** Approved answers carry `evidence_freshness`; an approved answer whose evidence has expired
reverts to draft for external use. The organizational measurement framework counts "due diligence
answers supported by current evidence" (metric M-12).

## 7. Boundaries with neighbouring repositories

| Concern | Owner |
|---|---|
| Control design, evidence architecture, assurance coordination | echelon-assurance |
| Policies | organization administration (public projections in the registry) |
| Portfolio facts referenced by answers (systems, maturity) | echelon-registry portfolio (cite by id) |
| Trust center presentation | generated projection; requirements in echelon-registry `portfolio/governance/trust-center-requirements.md` |

Overlap note: the echelon-assurance research branch also defines a trust center specification and a
control catalog. This repository answers questions; controls are referenced, not redefined (open
decision OD-GOV-020 in the registry).

## 8. Open questions

- OQ-DD-TRN-1: adopt DDT-03 (`approval`) in `answer-unit.schema.json`?
- OQ-DD-TRN-2: where is the access-controlled store for Confidential answers (shared with assurance's
  evidence store decision, OD-GOV-007)?
