---
id: DD-IND-FS-001
title: Financial services vendor assessment profile (banks, broker-dealers, RIAs, custodians, wealth managers)
status: draft
version: 0.1.0
created: 2026-11-25
updated: 2026-11-25
tags: [due-diligence, financial-services, industry-profile, third-party-risk]
---

# Financial services vendor assessment profile

## Scope and reading guide

What banks, broker-dealers, registered investment advisers (RIAs), custodians and wealth
managers require of technology vendors, as evidenced by public documents. Requirements
are separated into:

- **Regulatory-driven:** the customer must impose or oversee it because a law,
  regulation or supervisory expectation applies to the customer.
- **Contractually common:** appears in published supplier requirements or contract
  templates of more than one institution, or is standard in that document family.
- **Preference:** appears in a single institution's document, or is framed as
  illustrative or "should".

Confidence levels: **High** (directly documented in a retrieved primary document),
**Medium** (documented in one primary source or inferred from consistent secondary
evidence), **Low** (inferred). Source IDs prefixed `SRC-Q-` were retrieved and verified in
this task (`sources/questionnaires-and-customer-expectations.jsonl`). Other `SRC-` IDs are
pre-allocated seed identifiers from `sources/SEED-IDS.json` that were not verified here.

Relevance to Echelon: Unbound would sell to DAF sponsors, several of which are affiliated
with banks, broker-dealers or wealth managers (DD-IND-DAF-001). Per CNV-PAY-001 Unbound
acts as a third-party service provider. Per DD-ARC-001 Echelon has no SOC report, pen
test, insurance or adopted policy set, so most matching answers are `unknown` or
`proposed-target-state`.

## Who is in the population and what drives them

| Buyer type | Primary drivers of vendor requirements | Source IDs |
|---|---|---|
| National and state banks, bank trust departments (for example Bank of America N.A. as trustee of its Charitable Gift Fund) | Interagency third-party risk management guidance; GLBA safeguards; FFIEC handbooks; computer-security incident notification rule; resolution planning for the largest banks | SRC-INTERAGENCY-TPRM-2023, SRC-INTERAGENCY-GLBA-SAFEGUARDS, SRC-FFIEC-IT-HANDBOOK, SRC-CIRN-RULE-2021, SRC-TPRM-COMMUNITY-BANK-GUIDE-2024, SRC-Q-MS-THIRD-PARTY-REG-REQS |
| Broker-dealers (Morgan Stanley, Edward Jones, Schwab, Fidelity Brokerage) | Regulation S-P amendments (service provider oversight and notice), FINRA supervision of outsourcing, books and records | SRC-Q-SEC-REG-SP-2024-FACT-SHEET, SRC-SEC-REG-SP-2024, SRC-FINRA-RN-21-29, SRC-FINRA-RULE-3110, SRC-SEC-17A-4 |
| SEC-registered investment advisers | Regulation S-P amendments; Compliance Rule; fiduciary duty. The proposed adviser outsourcing rule and adviser cybersecurity rule were withdrawn in June 2025 | SRC-Q-SEC-REG-SP-2024-FACT-SHEET, SRC-SEC-ADVISERS-COMPLIANCE-RULE, SRC-Q-DECHERT-SEC-WITHDRAWALS-2025, SRC-SEC-ADVISER-OUTSOURCING-PROPOSAL |
| New York DFS-licensed entities (banks, trust companies, some insurers) | 23 NYCRR Part 500 and the October 2025 third-party service provider guidance | SRC-NYDFS-PART-500, SRC-Q-NYDFS-IL-20251021-TPSP |
| Firms with EU affiliates | DORA ICT third-party provisions flowed into global supplier terms | SRC-EU-DORA, SRC-Q-MS-THIRD-PARTY-REG-REQS |
| Custodians and their integration programs (Schwab Advisor Services, Fidelity) | Custodian integration agreements; data access via APIs | Public pages on Schwab integration returned HTTP 403 to retrieval; integration security criteria are **unknown** |

## Regulatory-driven requirements

| Requirement on the vendor | Driver | Confidence | Source IDs |
|---|---|---|---|
| Accept customer due diligence and ongoing monitoring proportional to risk and criticality | Interagency TPRM guidance; Regulation S-P written policies requiring service provider oversight "including through due diligence and monitoring" | High (Reg S-P fact sheet retrieved); seed for TPRM | SRC-Q-SEC-REG-SP-2024-FACT-SHEET, SRC-INTERAGENCY-TPRM-2023 |
| Notify the covered institution of a breach of customer information as soon as possible and not later than 72 hours after becoming aware | Regulation S-P amendments | High | SRC-Q-SEC-REG-SP-2024-FACT-SHEET |
| Support the covered institution's individual notice not later than 30 days after it becomes aware of unauthorized access | Regulation S-P amendments | High | SRC-Q-SEC-REG-SP-2024-FACT-SHEET |
| Contract terms on MFA, encryption, prompt incident notice, data location, subcontractor disclosure and rejection rights, data use limits including AI training, exit and deletion | NYDFS Part 500 and Oct 2025 industry letter (for DFS-regulated customers) | High | SRC-Q-NYDFS-IL-20251021-TPSP |
| Periodic attestations (SOC 2, ISO 27001), pen test summaries, participation in customer IR and BCP testing | NYDFS letter; DORA (EU affiliates) | High | SRC-Q-NYDFS-IL-20251021-TPSP, SRC-Q-MS-THIRD-PARTY-REG-REQS |
| Offboarding with removal of personnel, subcontractor, API and federated access and certified destruction including backups | NYDFS letter | High | SRC-Q-NYDFS-IL-20251021-TPSP |
| Regulator access and audit rights, cooperation with regulator requests, termination on regulator request | DORA and resolution planning as flowed down by a global bank | High (as documented by Morgan Stanley) | SRC-Q-MS-THIRD-PARTY-REG-REQS |
| Continuity of service during the customer's resolution event; assignment to successors or divestees | Bank recovery and resolution planning | High for systemically important banks; Low for others | SRC-Q-MS-THIRD-PARTY-REG-REQS |
| Online accessibility at WCAG 2.2 A and AA | Applicable accessibility laws as interpreted by the institution | High (documented); the legal basis is the institution's interpretation | SRC-Q-MS-THIRD-PARTY-REG-REQS, SRC-Q-FIDELITY-SUPPLIER-POLICIES |

Note: the SEC withdrew the proposed Investment Adviser Outsourcing Rule in June 2025
(SRC-Q-DECHERT-SEC-WITHDRAWALS-2025). RIA vendor diligence is therefore driven by
Regulation S-P, the Compliance Rule and fiduciary expectations, plus examination focus,
rather than by a dedicated outsourcing rule. Do not cite the proposal as a requirement.

## Contractually common requirements

Documented in two or more large-institution supplier documents or standard across a
document family.

| Requirement | Detail observed | Confidence | Source IDs |
|---|---|---|---|
| Written information security program approved by senior management | Explicit | High | SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS, SRC-Q-MS-THIRD-PARTY-REG-REQS |
| MFA for access to systems holding customer data and for remote and privileged access | Explicit in all bank documents | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS, SRC-Q-NYDFS-IL-20251021-TPSP |
| Encryption in transit and at rest, often with named algorithms | TLS 1.2 or above; AES-128/192/256 with named modes; AES-256 and RSA-4096 for some purposes | High | SRC-Q-MS-SECURITY-STANDARDS-IT-CYBER, SRC-Q-TRUIST-TPISS |
| Formal key management program | Separation of keys from data, KMS or secrets manager, HSM for high-value keys, rotation, inventory, single-purpose keys | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS |
| Customer-dedicated encryption keys | Required for public cloud services (Morgan Stanley); unique keys unless otherwise approved (Truist) | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS |
| Least privilege, unique IDs, no shared accounts, annual access reviews | Quarterly for privileged (Truist) | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS |
| Independent penetration testing at least annually, findings tracked to resolution | Covering web, cloud, mobile apps and internal and external networks | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS |
| Customer right to perform or commission security testing or assessments | Pen test right; annual non-intrusive audit; on-site audit with notice | High | SRC-Q-MS-SECURITY-STANDARDS-IT-CYBER, SRC-Q-TRUIST-TPISS, SRC-Q-MS-THIRD-PARTY-REG-REQS |
| Vulnerability and patch management with defined timeframes and emergency process | Daily signature updates; code, image and secret scanning; SCA for open source | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS |
| Data loss prevention | MFA for privileged, egress scanning, removable media prohibited | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS, SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS |
| Subcontractor oversight and flow-down of equivalent requirements | Written notice or consent before subcontractor accesses data; periodic assessment of material subcontractors | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-TRUIST-TPISS, SRC-Q-BOA-SUPPLIER-EXPECTATIONS, SRC-Q-NYDFS-IL-20251021-TPSP |
| Incident notification per contract with investigation and root cause | 24 hours common in bank documents | High | SRC-Q-MS-DATA-PROCESSING-TERMS, SRC-Q-TRUIST-TPISS, SRC-Q-JPMC-SUPPLIER-CODE |
| BC/DR plans provided to the customer, tested, RPO aligned to the customer | Single points of failure identified | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-SIFMA-COB-ASSESSMENT |
| Annual independent assurance report | SOC 1 or SOC 2 Type II for the most recent 12 months, ISAE 3402, or ISO 27001 with SoA | High | SRC-Q-MS-THIRD-PARTY-REG-REQS, SRC-Q-NYDFS-IL-20251021-TPSP |
| Return or destruction of data on request and at exit with certificates | Explicit | High | SRC-Q-BOA-SUPPLIER-EXPECTATIONS, SRC-Q-MS-MIN-SECURITY-STANDARDS |
| Secure SDLC with segregated environments and no production data in lower environments | Explicit | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS |
| Personnel security training | Includes safe AI usage with reported metrics (Morgan Stanley) | High | SRC-Q-MS-MIN-SECURITY-STANDARDS, SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS |
| Background investigations | Detailed checks including credit (Fidelity) | Medium (one detailed public source; common market practice) | SRC-Q-FIDELITY-SUPPLIER-POLICIES |
| Restriction on customer data entering third-party GenAI tools; disclosure of model use | Explicit in two banks' documents | High | SRC-Q-TRUIST-TPISS, SRC-Q-MS-MIN-SECURITY-STANDARDS |
| Accessibility conformance with evidence | WCAG 2.2 AA; ACR or VPAT; remediation schedule | High | SRC-Q-FIDELITY-SUPPLIER-POLICIES, SRC-Q-MS-THIRD-PARTY-REG-REQS |
| Conduct, ESG and modern slavery commitments | Supplier codes | High | SRC-Q-GS-VENDOR-CODE, SRC-Q-MS-SUPPLIER-CODE, SRC-Q-BOA-SUPPLIER-EXPECTATIONS, SRC-Q-JPMC-SUPPLIER-CODE |
| Published data processing terms | Per-sub-processor prior written consent; 24-hour incident and government access request notice; 48-hour instruction response | High (one institution publishes; DPAs are universal) | SRC-Q-MS-DATA-PROCESSING-TERMS |

## Preference (single-source or illustrative)

| Requirement | Confidence | Source IDs |
|---|---|---|
| SaaS federation to the bank's enterprise IdP (Azure AD named) | High that Truist requires it; Low that all FS buyers do | SRC-Q-TRUIST-TPISS |
| Federated login or SSO | Medium (illustrative list) | SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS |
| Independent cloud implementation reviews | Medium | SRC-Q-GS-VENDOR-TECH-RISK-EXPECTATIONS |
| Remote access restricted to the United States | High for Truist | SRC-Q-TRUIST-TPISS |
| Remediation of customer-identified material findings within 5 days or agreed plan | High for Truist | SRC-Q-TRUIST-TPISS |
| OSINT and threat hunting against higher-risk suppliers | High for Truist | SRC-Q-TRUIST-TPISS |
| CIS Level 1 hardening for supplier devices; always-on VPN | High for Truist | SRC-Q-TRUIST-TPISS |
| Prevention of concurrent logins; session ID rotation; DNS over HTTPS or TLS | High for Morgan Stanley | SRC-Q-MS-MIN-SECURITY-STANDARDS |
| Country of software development and maintenance on invoices | High for Fidelity | SRC-Q-FIDELITY-SUPPLIER-POLICIES |
| Third-party (not self-assessed) VPAT or ACR | High for Fidelity | SRC-Q-FIDELITY-SUPPLIER-POLICIES |
| Sustainability due diligence exercise for certain suppliers | High for Morgan Stanley | SRC-Q-MS-SUPPLIER-CODE |
| Small-business accommodation with remediation plans | High for Bank of America | SRC-Q-BOA-SUPPLIER-EXPECTATIONS |

## Wealth-technology peer disclosures (what RIAs and wealth managers see from comparable vendors)

| Peer | Public posture | Source IDs |
|---|---|---|
| Addepar | Annual SOC 2 Type II, annual third-party pen tests, board security updates, background checks; public SOC 3 with AWS carved out | SRC-Q-ADDEPAR-SECURITY-OVERVIEW, SRC-Q-ADDEPAR-SOC3-2024-2025 |
| Envestnet | Public trust center sections for privacy, cybersecurity, business continuity, AI, policies and a subprocessor list with purpose and location | SRC-Q-ENVESTNET-TRUST-SUBPROCESSORS |
| Plaid (fintech data access) | Public ISO certificate and prefilled questionnaires; gated SOC 2, pen test results and cyber insurance | SRC-Q-PLAID-SECURITY-PORTAL-2023 |
| Ren (third-party DAF administrator) | Publicly described as holding SOC 2 Type 1 | SRC-Q-GIVINGCOMPASS-REN-2026 |

Inference (Medium confidence): RIAs and wealth managers benchmark a new DAF platform
against these peers. An Unbound launch without at least a SOC 2 Type II and a pen test
summary would be below the peer baseline. This is a market inference, not a documented
requirement.

## Custodians

- Schwab Advisor Services publishes that third-party integrations exist and that RIAs are
  solely responsible for evaluating vendors (seen in search results), but the pages
  returned HTTP 403 on retrieval and no integration security criteria were found.
  Status: **unknown**.
- Fidelity: integration program criteria not found publicly. Status: **unknown**.
- Recommendation: treat custodian integration security criteria as an open question;
  they are typically disclosed under integration agreements.

## Implications for Echelon answers

- Regulatory-driven items must be answered by every Unbound proposal to a bank,
  broker-dealer or RIA sponsor. Most are `proposed-target-state` today.
- The contractually common items define the minimum control set for an FS-ready Unbound
  and should map to Unbound control matrix entries (`UNB-CTRL-*`) and to Secure
  Construction Standard rules (for example SEC-CRYPTO-001, SEC-AUTH-001, SEC-SUPPLY-001)
  in later answer units. Mapping is not done in this document.
- Preference items should be captured as alternatives in the question bank, not as
  baseline requirements.

## Open questions

- Content of Bank of America's Service Provider Security Requirements Document (not
  public).
- Whether DAF programs affiliated with these institutions use the parent institution's
  supplier requirements for DAF technology vendors (see DD-IND-DAF-001).
- Custodian integration security requirements for Schwab, Fidelity and Pershing.
