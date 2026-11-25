---
id: DD-GAP-POL-001
title: Echelon organizational policy gap analysis
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [gap-analysis, policy, governance]
---

# Echelon organizational policy gap analysis

## Finding

`echelon-organization-administration@2763e576` contains exactly one security policy
document, `policies/security/secure-construction-standard.md` (v0.1, proposed). The
business plan (`business-plan/`, 136 sections, all `status: draft`) describes intended
positions, but 133 sections share a common template ("Decision and purpose", "Current
thesis", "Evidence gate", "Open Evidence / Validation Needs") with generic text, and
none is an operating policy with scope, requirements, roles, exceptions, enforcement and
review. Customers, auditors and insurers will ask for a policy set that does not exist.

This is the single largest organizational gap for due diligence. It is also the
cheapest to close badly (template policies) and the most expensive to close well
(policies that are true). The recommendation below favors short, enforceable,
machine-checkable policies that describe what Echelon actually does, and explicitly
mark target-state clauses until they operate.

## Method

Expected policy set derived from what SOC 2 (`SRC-AICPA-TSC`), ISO/IEC 27001 Annex A
(`SRC-ISO-27001-2022`), NIST CSF 2.0 (`SRC-NIST-CSF-2.0`), the 2023 Interagency TPRM
Guidance (`SRC-INTERAGENCY-TPRM-2023`), the FTC Safeguards Rule
(`SRC-FTC-SAFEGUARDS-RULE`) and common questionnaires (`SRC-SA-SIG`, `SRC-CSA-CAIQ-V4`,
`SRC-EDUCAUSE-HECVAT`) ask a vendor to produce. Inclusion here means customers commonly
request the document; it does not mean a law requires Echelon to have it. The
"Required by" column distinguishes the two.

## Gap table

Legend. Current: **None** (no document), **Partial** (topic touched by the Standard or
Unbound requirements, not an organizational policy), **Plan** (business plan aspiration
only). Enforcement: how the policy can be made self-verifying.

| # | Policy | Commonly requested by | Required by law for Echelon? | Current | Enforcement opportunity | Priority |
|---|---|---|---|---|---|---|
| P01 | Information security policy (umbrella, roles, accountable executive) | SOC 2 CC1/CC2, ISO 5.2, SIG, CAIQ, banks | Not directly; FTC Safeguards Rule may apply if Echelon is a "financial institution" under GLBA (open: OQ-DD-POL-001) | None | Policy-as-code index linking each clause to controls and evidence | P0 |
| P02 | Secure development and construction | SSDF, SOC 2 CC8, ISO A.8.25-8.28, CISA attestation | No (federal attestation only for federal sales) | Partial (Standard v0.1, proposed) | Praxis/Tutela gates; adopt the Standard after the ownership corrections in REC-ORGADMIN-001 | P0 |
| P03 | Access control and identity (including AI agent identities) | SOC 2 CC6, ISO A.5.15-5.18, FFIEC authentication guidance | No | Partial (Unbound SOC2-010, GOV-AUT-*) | Identity provider configuration as code; access review evidence generated | P0 |
| P04 | Change management | SOC 2 CC8.1, ISO A.8.32 | No | Partial (Praxis work protocol in tooling repositories) | Branch protection, required reviews and Praxis completion evidence | P0 |
| P05 | Vulnerability and patch management | SOC 2 CC7.1, ISO A.8.8, PCI 6.3 (if in scope), insurers | No | None | SLA timers computed from scanner findings; exceptions expire automatically | P0 |
| P06 | Incident response and breach notification | SOC 2 CC7.3-7.5, banks (36-hour bank service provider notice), state breach laws, Reg S-P 2024 service provider terms | State breach laws bind data owners; vendor duties usually contractual; bank service provider notice under the 2021 rule applies to bank service providers (open: OQ-DD-POL-002) | None | Runbook with timers; tabletop evidence; contact roster | P0 |
| P07 | Data classification and handling | SOC 2 C1, ISO A.5.12-5.13 | No | Partial (Unbound DCL requirements) | Classification as types in code; handling enforced by type | P1 |
| P08 | Data retention and disposal | SOC 2 C1.2/P4, ISO A.8.10, customers' recordkeeping rules | Customer recordkeeping duties flow down by contract | Partial (Unbound RET requirements; SOC2-032) | Retention schedule as data; deletion jobs emit evidence | P1 |
| P09 | Privacy policy (external) and privacy program (internal) | State privacy laws, GDPR if EU data, customers | Public privacy notice required for consumer-facing collection under several state laws; applicability depends on role (service provider versus business) | None | Data inventory generated from schemas | P0 before any donor data |
| P10 | Encryption and key management | SOC 2 CC6.1/CC6.7, ISO A.8.24 | No | Partial (SEC-CRYPTO-001) | Approved algorithm list enforced by analyzer; KMS configuration as code | P1 |
| P11 | Logging and monitoring | SOC 2 CC7.2, ISO A.8.15-8.16 | No | Partial (Unbound SOC2-012/027) | Missing-heartbeat detection as a control; no runtime monitor exists yet (GAP-SYS) | P1 |
| P12 | Business continuity and disaster recovery | SOC 2 A1, ISO A.5.29-5.30, FFIEC BCM, FINRA 4370 (customers) | No (binds regulated customers) | Plan (13.06) | Scheduled restore tests emitting evidence | P1 |
| P13 | Backup | SOC 2 A1.2, ISO A.8.13, insurers | No | Partial (Unbound BKP) | Restore test automation | P1 |
| P14 | Third-party and vendor risk management | Interagency TPRM (customers), SOC 2 CC9.2, ISO A.5.19-5.22 | No (binds banks; flows down) | Plan (12.02) | Vendor register as data with review dates | P0 |
| P15 | Subprocessor management and public list | DPAs, GDPR Art. 28, customers | Contractual; GDPR if processor for EU data | None | Subprocessor list generated from vendor register | P0 before first customer |
| P16 | Risk management methodology and register | SOC 2 CC3, ISO 6.1, NIST CSF GV.RM | No | Plan (13.02) | Risk register linked to controls and residual risk fields | P1 |
| P17 | Acceptable use (workforce and AI tools) | SOC 2 CC1/CC2, ISO A.5.10 | No | None | Endpoint and tool allowlists | P1 |
| P18 | AI use and AI governance | ISO 42001, NIST AI RMF, customers, Colorado AI Act if high-risk decisions | Possibly for consequential decisions (open: OQ-DD-POL-003) | Plan (10.02-10.04) | EDF responsibility model as executable policy; agent permissions as code | P0 (Echelon builds with AI agents) |
| P19 | Personnel security (screening, onboarding, offboarding, training) | SOC 2 CC1.4, ISO A.6, banks, insurers | Background checks subject to FCRA and state law if performed | None | Joiner-mover-leaver automation evidence | P1 |
| P20 | Security awareness training | SOC 2 CC2.2, insurers, FTC Safeguards | FTC Safeguards requires training if the rule applies | None | Completion evidence | P1 |
| P21 | Code of conduct, ethics, conflicts of interest | SOC 2 CC1.1, banks, DAF sponsors | No | None | Annual attestation evidence | P1 |
| P22 | Anti-bribery and corruption, sanctions compliance (company level) | Banks, global enterprises | OFAC applies to all US persons | None | Screening of Echelon's own counterparties | P1 |
| P23 | Whistleblower and speak-up | Banks, larger enterprises | Some statutory protections apply; policy not mandated for a private LLC | None | Channel and log | P2 |
| P24 | Physical and environmental security | SOC 2 CC6.4, ISO A.7 | No | None (cloud reliance) | Carve-out to cloud provider SOC report; remote-work controls | P2 |
| P25 | Asset management | ISO A.5.9, CIS 1-2 | No | None | Inventory generated from infrastructure as code and SBOM | P1 |
| P26 | Exception management | SOC 2 CC5, Standard enforcement model | No | Partial (Standard requires explicit, time-limited exceptions) | Exceptions as records with expiry and compensating controls | P0 |
| P27 | Accessibility policy and conformance statement | Public sector, universities, ADA exposure | ADA Title II binds public entities (customers); Title III exposure for public accommodations is contested for web | None | Automated plus manual testing evidence; ACR generation | P1 |
| P28 | Records management and legal hold | Regulated customers, litigation readiness | Depends on customer recordkeeping duties | None | Legal hold flag in data model | P2 |
| P29 | Customer communication and complaint handling | Banks, DAF sponsors | Complaint duties bind regulated customers | None | Ticket evidence | P2 |
| P30 | Responsible disclosure (public) | Researchers, customers, CISA Secure by Design | No | None | security.txt and intake process | P0 (cheap, high signal) |
| P31 | Open-source and licensing policy (inbound and outbound) | Customers, escrow, acquirers | No | Partial (Standard prefers MIT; repositories mostly PolyForm Noncommercial) | License scanning gate | P1 |
| P32 | Evidence and assurance claims policy (what may be said publicly) | Supports SOC2-020; prevents misrepresentation | FTC Act section 5 deception exposure for false security claims | Partial (this repository's honesty rules) | `tools/build.fsx` honesty rule; trust center publishing gate | P0 |

## Observations

1. **Truthful minimal policies beat comprehensive template policies.** A template
   policy that states unperformed practices converts a gap into a misrepresentation.
   Each policy should separate "requirements in force" from "target state" exactly as
   answer units do.
2. **Policy-as-code is feasible for roughly half the set** (P02, P03, P04, P05, P07,
   P10, P11, P14, P15, P25, P26, P31, P32): the policy clause is the specification of
   an automated check, and the evidence is the check's output. This is where the
   Echelon approach saves recurring cost (see `cost-avoidance/`).
3. **The FTC Safeguards Rule question (OQ-DD-POL-001) changes several priorities.**
   If Echelon or Unbound's operating entity is a "financial institution" under the FTC
   definition, or if customers contractually impose Safeguards-equivalent duties, a
   qualified individual, written risk assessment, annual board report, penetration
   testing and vulnerability assessment cadence become obligations rather than options.
   This requires counsel review; it is not resolved here.
4. **One person cannot credibly hold all roles.** Several policies require separation of
   duties (change approval, access review, exception approval). With a very small team,
   the honest answer is compensating controls (automated enforcement, external review
   cadence) and disclosure, not invented roles.

## Recommendations

Recorded as `REC-ORGPOL-*` in `recommendations/policy-recommendations.jsonl`. Summary:

- REC-ORGPOL-001 (P0): Create `policies/` structure in echelon-organization-administration
  with a policy index that links each clause to a control ID in this repository and
  marks clause status (in force or target).
- REC-ORGPOL-002 (P0): Draft the P0 set first: P01, P02 (adopt the corrected Standard),
  P03, P04, P05, P06, P14, P15, P18, P26, P30, P32, and P09 before any donor data.
- REC-ORGPOL-003 (P0): Obtain counsel determination on FTC Safeguards Rule and GLBA
  status (OQ-DD-POL-001) before finalizing P01, P06 and P20.
- REC-ORGPOL-004 (P1): Generate the subprocessor list, asset inventory and vendor
  register from data rather than maintain documents.
- REC-ORGPOL-005 (P1): Do not adopt purchased template policy packs without editing every
  clause to match operating reality.

## Open questions

- OQ-DD-POL-001: Is Echelon Foundry, or the Unbound operating entity, a "financial
  institution" under GLBA and the FTC Safeguards Rule given that it provides services to
  DAF sponsors? (Counsel.)
- OQ-DD-POL-002: Would Unbound be a "bank service provider" under the 2021
  Computer-Security Incident Notification rule when serving a bank-affiliated sponsor
  (often a separate 501(c)(3) rather than the bank itself)? (Counsel.)
- OQ-DD-POL-003: Does any Unbound automated decision fall within "consequential
  decisions" under the Colorado AI Act or similar state law? (Counsel.)
