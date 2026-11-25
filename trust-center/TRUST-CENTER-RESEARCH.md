---
id: DD-TC-001
title: Trust center research and recommended disclosure tiering
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, trust-center, disclosure, assurance]
---

# Trust center research and recommended disclosure tiering

## Purpose

Record what established SaaS, fintech and wealth-technology companies publish in trust
centers, what they gate behind login, request or NDA, which document types appear, and
what platform vendors (Conveyor, Vanta, Drata/SafeBase) document about tiering. Then
recommend a disclosure tier per artifact type for Echelon and Unbound.

All `SRC-Q-` sources are in `sources/questionnaires-and-customer-expectations.jsonl`.
Only public pages were read; no trust center access was requested and no NDA was signed.
Whistic documentation did not surface in searches and is not covered.

## Findings

### Platform tiering models

| Platform | Documented access model | Source IDs |
|---|---|---|
| Conveyor | Four document levels: Anyone (public, suited to SOC 3); Approved visitors with NDA (suited to SOC 2 Type II); Some approved visitors by access group or customer domain (suited to full pen test reports or customer-specific information); Internal Only (default) | SRC-Q-CONVEYOR-DOC-ACCESS |
| Vanta | NDA (clickwrap or DocuSign) enforced only when visitors request access to the trust center or "requestable" documents such as a SOC 2 report, security report or completed questionnaire; public documents bypass the NDA | SRC-Q-VANTA-TC-NDA |
| Drata (now owner of SafeBase) | Request and approval workflow for sensitive documents; governance of who sees what, for how long and under what terms; SafeBase blog URLs redirect to Drata | SRC-Q-DRATA-TRUST-CENTER, SRC-Q-SAFEBASE-GRANULAR-ACCESS-BLOG (unverified) |
| CSA article (by Vanta) | Recommends audit reports, policies, diagrams, prefilled CAIQ or SIG, subprocessor list and pen test summaries; share sensitive documents under NDA; set access expiry; conditional auto-approval; verify NDA before sharing | SRC-Q-CSA-BUILDING-TRUST-CENTER-2024 |

### Company practice

| Company | Public | Gated | Source IDs |
|---|---|---|---|
| GitLab | Handbook policies and standards; product security documentation; self-attestations reviewed annually | SOC 2 Type 2 and pen test executive summary via "Get Access" with company email; documents labeled NDA Required; internal SLAs of 10 business days for questionnaires and 5 for contract reviews | SRC-Q-GITLAB-CUSTOMER-ASSURANCE |
| Stripe | SOC 3 | SOC 1 and SOC 2 downloadable by existing customers with Owner or Administrator dashboard roles, no separate NDA (terms acceptance may apply) | SRC-Q-STRIPE-SOC-REPORTS |
| Plaid | ISO certificate and prefilled standard questionnaires | SOC 2 Type 2, ISO 27001 and 27701 certificates, pen test results, cyber insurance, policies on request | SRC-Q-PLAID-SECURITY-PORTAL-2023 |
| Addepar | Security overview; SOC 3 reports by platform and period | SOC 2 Type II (described as annual; access path not published) | SRC-Q-ADDEPAR-SECURITY-OVERVIEW, SRC-Q-ADDEPAR-SOC3-2024-2025 |
| Envestnet | Trust center sections for privacy, cybersecurity, legal, business continuity, AI, policies; subprocessor table with purpose and location | Not determined | SRC-Q-ENVESTNET-TRUST-SUBPROCESSORS |

### Document types observed

SOC 3 (public), SOC 2 Type II (gated), SOC 1 (gated, finance-relevant), ISO 27001 and
27701 certificates (often public), pen test executive summary or letter (gated), full pen
test report (narrowest tier), prefilled CAIQ or SIG (public or gated), self-attestations,
policies (public summaries or gated full text), architecture and data flow diagrams,
subprocessor lists (public), BC/DR summaries, AI sections, cyber insurance certificate
(gated), status pages (public).

### Constraints that shape tiering

- **SOC 2 is a restricted use report** intended for user entities, prospective user
  entities and others with sufficient knowledge, and is not suitable for public
  distribution (SRC-Q-SENSIBA-SOC2-SHARING-2023). **SOC 3 is a general use report** that
  can be freely distributed (SRC-Q-AICPA-SOC3).
- **Buyers want reports before signing** (SRC-Q-ARIZONA-3P-SEC-PRIV-Q) and some accept a
  SOC 2 in lieu of a long questionnaire (SRC-Q-WI-DOA-10816), so the prospect tier must
  reach SOC 2 under NDA, not only customers.
- **Public records exposure:** a state buyer may be compelled to disclose submissions and
  asks for redacted and unredacted copies (SRC-Q-WI-DOA-10816). Anything given to a
  public-sector prospect should be assumed potentially disclosable.
- **Regulators and customer auditors** have their own access rights (SRC-Q-MS-THIRD-PARTY-REG-REQS,
  SRC-Q-TRUIST-TPISS), which argues for an auditor-only tier for raw evidence.
- **Honesty constraint (DD-GOV-001, DD-ARC-001):** Echelon has no SOC report, pen test,
  certification or insurance. A trust center must not imply otherwise. Several tiers will
  be empty or show "planned" until artifacts exist.

## Recommended disclosure tiering

Tiers:

1. **Public:** anyone, no login.
2. **Authenticated prospect:** verified business email, no NDA; access logged and expiring.
3. **NDA:** prospect or partner with signed NDA (clickwrap acceptable), approval required, access expiry (for example 90 days to 12 months).
4. **Existing customer:** contracted customers, through the product or customer portal, under contract confidentiality.
5. **Auditor only:** the customer's auditors, examiners and regulators exercising contractual audit rights, under supervised access.
6. **Internal:** Echelon only.

| Artifact | Tier | Rationale | Echelon status (DD-ARC-001) | Supporting sources |
|---|---|---|---|---|
| Security overview, program description, honest status statement | Public | Reduces questionnaire volume; must state what does not yet exist | Can be written now as `planned` | SRC-Q-ADDEPAR-SECURITY-OVERVIEW, SRC-Q-CSA-BUILDING-TRUST-CENTER-2024 |
| Subprocessor list with purpose and location | Public | Market norm; FS DPAs require notice and consent for changes | Not established | SRC-Q-ENVESTNET-TRUST-SUBPROCESSORS, SRC-Q-MS-DATA-PROCESSING-TERMS |
| Privacy notice, DPA template, accessibility statement | Public | Already public by nature; buyers read them before engaging | Not established | SRC-Q-CSA-BUILDING-TRUST-CENTER-2024, SRC-Q-YALE-ACCESSIBLE-PURCHASING |
| AI use disclosure (which features use models, data use and training commitments) | Public | FS buyers require disclosure of model use; NYDFS names AI training as a contract topic | Not established | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-NYDFS-IL-20251021-TPSP, SRC-Q-ENVESTNET-TRUST-SUBPROCESSORS |
| SOC 3 | Public | General use report | Does not exist | SRC-Q-AICPA-SOC3 |
| ISO certificates | Public | Certificates are routinely published | Do not exist | SRC-Q-PLAID-SECURITY-PORTAL-2023 |
| Status page and incident history | Public | Availability transparency | No production service | none (market practice) |
| Vulnerability disclosure policy | Public | Enables external reporting | Not established | seed SRC-ISO-29147-30111 |
| Policy summaries (titles, scope, review dates) | Authenticated prospect | Shows existence without exposing operational detail | Only the proposed Secure Construction Standard v0.1 exists | SRC-Q-GITLAB-CUSTOMER-ASSURANCE |
| Prefilled standard questionnaire (CAIQ, HECVAT-style, SIG Lite) | Authenticated prospect | Plaid publishes publicly; gating by email gives lead tracking and audit trail without NDA friction | Can be drafted with `proposed-target-state` answers | SRC-Q-PLAID-SECURITY-PORTAL-2023, SRC-Q-CSA-BUILDING-TRUST-CENTER-2024 |
| VPAT or ACR | Authenticated prospect | Universities and FS buyers request it pre-purchase | Does not exist | SRC-Q-YALE-ACCESSIBLE-PURCHASING, SRC-Q-FIDELITY-SUPPLIER-POLICIES |
| SOC 2 Type II report and bridge letter | NDA | Restricted use; buyers need it before signing | Does not exist | SRC-Q-SENSIBA-SOC2-SHARING-2023, SRC-Q-CONVEYOR-DOC-ACCESS, SRC-Q-VANTA-TC-NDA, SRC-Q-ARIZONA-3P-SEC-PRIV-Q |
| SOC 1 Type II (if ever obtained for financial processing) | NDA | Restricted use; relevant to sponsor financial statement auditors | Does not exist | SRC-Q-MS-THIRD-PARTY-REG-REQS |
| Pen test executive summary or attestation letter | NDA | Common gated artifact | Does not exist | SRC-Q-GITLAB-CUSTOMER-ASSURANCE, SRC-Q-PLAID-SECURITY-PORTAL-2023 |
| Full policies (infosec, IR, BC/DR, access control) | NDA | Operational detail useful to attackers; buyers request full text | Not adopted | SRC-Q-CSA-BUILDING-TRUST-CENTER-2024, SRC-Q-MS-MIN-SECURITY-STANDARDS |
| High-level architecture and data flow diagrams | NDA | Requested by universities and FS buyers | Design-stage only (Unbound requirements) | SRC-Q-UTS-MIN-SECURITY-REQS |
| BC/DR plan summary and test summary | NDA | FS buyers require plans be provided | Not established | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-SIFMA-COB-ASSESSMENT |
| Cyber insurance certificate | NDA | Plaid gates it; reveals limits that could inform attackers | No policy | SRC-Q-PLAID-SECURITY-PORTAL-2023 |
| Completed customer-specific questionnaires | Existing customer (or NDA for the requester only) | Specific to one customer; must not be reused across customers without review | n/a | SRC-Q-VANTA-TC-NDA |
| Full pen test report with findings | Existing customer, domain-restricted access group | Narrowest external tier recommended by Conveyor | Does not exist | SRC-Q-CONVEYOR-DOC-ACCESS |
| Detailed network diagrams, key management design, tenant isolation design | Existing customer, on request | Needed for bank requirements on dedicated keys and segmentation | Design-stage | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS |
| Customer-specific incident reports and RCAs | Existing customer (affected customer only) | Contractual notice obligations | n/a | SRC-Q-MS-DATA-PROCESSING-TERMS |
| Certificates of destruction | Existing customer (requesting customer) | Exit obligations | n/a | SRC-Q-NYDFS-IL-20251021-TPSP |
| Control evidence (logs, tickets, access reviews, sample populations) | Auditor only | Raw evidence for customer auditors and regulators exercising audit rights | n/a | SRC-Q-MS-THIRD-PARTY-REG-REQS, SRC-Q-TRUIST-TPISS |
| Risk register, exceptions, vulnerability backlog, red team detail, secrets inventory | Internal | Would materially aid attackers; disclose summaries only | n/a | DD-GOV-001 |

### Operating rules for the tiers (proposed)

- Every gated grant is logged, expires and is periodically reviewed
  (SRC-Q-CSA-BUILDING-TRUST-CENTER-2024, SRC-Q-DRATA-TRUST-CENTER).
- Public-sector requesters receive redaction-ready versions by default (SRC-Q-WI-DOA-10816).
- Artifacts state their assurance independence (`first-party` self-attestation versus
  `independent-third-party` report) to comply with DD-GOV-001 rule 4. Avoid the
  incumbent pattern of calling a SOC 2 attestation a "certification"
  (SRC-Q-GIVINGCOMPASS-REN-2026).
- Until independent artifacts exist, the trust center shows planned artifacts with target
  dates only if those dates are approved; otherwise it states "not yet available".

## Objections preserved

- Public prefilled questionnaires (Plaid's practice) reduce friction but expose detail. An
  authenticated-prospect tier is recommended as a compromise; a stricter reviewer could
  argue for NDA gating.
- A trust center for a pre-revenue vendor with no artifacts may signal weakness. The
  alternative (no trust center) increases manual questionnaire load. This trade-off is
  for an owner decision, not resolved here.

## Open questions

- Which trust center platform, if any, Echelon will adopt; not in scope of this research.
- Whether Whistic or other platforms publish tiering guidance (not found in this pass).
